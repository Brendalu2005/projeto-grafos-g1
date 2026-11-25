import argparse
import hashlib
import json
import math
import platform
import random
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean, median, stdev
from time import perf_counter

from src.graphs.graph import adicionar_arco
from src.graphs.algorithms import bfs, dijkstra
from src.graphs.io import carregar_dataset


# [IA] ChatGPT (Codex) – recortes aninhados conforme as definições aprovadas pela equipe.
def criar_recortes(grafo, semente=42):
    """Retorna os recortes de 10%, 50% e 100%, sem modificar o grafo.

    Cada ocorrência é (id, origem, destino, peso). O id é sua posição na
    enumeração das listas de adjacência, não o índice da linha do CSV.
    Pesos devem estar previamente calculados. Vértices isolados não entram.
    """
    ocorrencias = []
    for origem, vizinhos in grafo.items():
        for destino, peso in vizinhos:
            identificador = len(ocorrencias)
            ocorrencias.append((identificador, origem, destino, peso))

    # Uma instância local evita alterar o gerador aleatório de outras tarefas.
    sorteio = random.Random(semente)
    sorteio.shuffle(ocorrencias)

    recortes = []
    for percentual in (10, 50, 100):
        if percentual == 100:
            quantidade = len(ocorrencias)
        else:
            quantidade = int(len(ocorrencias) * (percentual / 100))

        selecionadas = ocorrencias[:quantidade]
        grafo_recorte = {}
        for identificador, origem, destino, peso in selecionadas:
            adicionar_arco(grafo_recorte, origem, destino, peso)

        recortes.append({
            "percentual": percentual,
            "semente": semente,
            "vertices": len(grafo_recorte),
            "arcos": quantidade,
            "ocorrencias": selecionadas,
            "grafo": grafo_recorte,
        })

    return recortes


# [IA] ChatGPT (Codex) – seleção determinística das fontes conforme regra aprovada pela equipe.
def selecionar_fontes(recortes):
    """Escolhe três fontes no recorte de 10% e confere sua presença nos demais.

    Considera grau de saída >= 3, ordena por grau decrescente e nome
    crescente e usa as posições 0, n // 4 e n // 2. Retorna os nomes.
    """
    grafo_menor = None
    for recorte in recortes:
        if recorte["percentual"] == 10:
            grafo_menor = recorte["grafo"]
            break

    if grafo_menor is None:
        raise ValueError("É necessário fornecer o recorte de 10%.")

    candidatos = []
    for usuario, vizinhos in grafo_menor.items():
        grau_saida = len(vizinhos)
        if grau_saida >= 3:
            candidatos.append((usuario, grau_saida))

    candidatos.sort(key=lambda candidato: (-candidato[1], candidato[0]))
    quantidade = len(candidatos)
    if quantidade < 3:
        raise ValueError("Há menos de três candidatos com grau de saída >= 3. Revise a regra.")

    posicoes = [0, quantidade // 4, quantidade // 2]
    if len(set(posicoes)) != 3:
        raise ValueError("As posições da regra repetem fontes. Revise a regra.")

    fontes = []
    for posicao in posicoes:
        fontes.append(candidatos[posicao][0])

    for recorte in recortes:
        for fonte in fontes:
            if fonte not in recorte["grafo"]:
                raise ValueError(f"Fonte {fonte} ausente no recorte de {recorte['percentual']}%.")

    return fontes


# [IA] ChatGPT (Codex) – medição com aquecimento e estatísticas conforme aprovado pela equipe.
def medir_algoritmo(algoritmo, grafo, fonte, repeticoes=5, registrar_ciclo_negativo=False):
    """Mede chamadas algoritmo(grafo, fonte), sem preparar ou exportar dados.

    Faz um aquecimento sem cronômetro e pelo menos cinco repetições medidas.
    registrar_ciclo_negativo usa o retorno do aquecimento de Bellman-Ford.
    O algoritmo deve preservar o grafo. Erros são propagados, sem gerar
    estatísticas parciais. O desvio padrão é amostral; tempos são em segundos.
    """
    if not isinstance(repeticoes, int) or repeticoes < 5:
        raise ValueError("Use um número inteiro de pelo menos 5 repetições.")
    if fonte not in grafo:
        raise ValueError("A fonte deve estar presente no grafo.")

    resultado = algoritmo(grafo, fonte)
    # [IA] ChatGPT (Codex) – registra o retorno de Bellman-Ford fora do cronômetro.
    dados_ciclo = {}
    if registrar_ciclo_negativo:
        ciclo = resultado[2]
        dados_ciclo = {
            "status": "CICLO_NEGATIVO" if ciclo is not None else "OK",
            "tem_ciclo_negativo": ciclo is not None,
            "ciclo_negativo": ciclo,
        }
    del resultado

    tempos = []
    for _ in range(repeticoes):
        inicio = perf_counter()
        resultado = algoritmo(grafo, fonte)
        fim = perf_counter()
        tempos.append(fim - inicio)
        # Libera o retorno fora do intervalo medido, antes da próxima chamada.
        del resultado

    return {
        "aquecimentos": 1,
        "repeticoes": repeticoes,
        "unidade_tempo": "segundos",
        "tempos": tempos,
        "media": mean(tempos),
        "minimo": min(tempos),
        "mediana": median(tempos),
        "desvio_padrao_amostral": stdev(tempos),
        **dados_ciclo,
    }


# [IA] ChatGPT (Codex) – metadados compartilhados pelos dois executores de benchmark.
def ambiente_atual():
    processador = platform.processor() or None
    if platform.system() == "Windows":
        import winreg
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                r"HARDWARE\DESCRIPTION\System\CentralProcessor\0") as chave:
                processador = winreg.QueryValueEx(chave, "ProcessorNameString")[0].strip()
        except OSError:
            pass
    try:
        import psutil
        memoria = psutil.virtual_memory().total
    except ImportError:
        memoria = None
    return {
        "python": platform.python_version(), "sistema": platform.system(),
        "versao_sistema": platform.version(), "processador": processador,
        "memoria_total_bytes": memoria,
    }


# [IA] ChatGPT (Codex) – executor de BFS/Dijkstra com o procedimento aprovado.
def executar_benchmark(caminho_csv, caminho_saida):
    """Mede 18 configurações e confere o alcance fora do cronômetro."""
    caminho_csv = Path(caminho_csv)
    caminho_saida = Path(caminho_saida)
    if caminho_saida.exists():
        raise ValueError("A saída já existe. Use outro caminho em --out.")

    grafo = carregar_dataset(caminho_csv)
    recortes = criar_recortes(grafo, semente=42)
    fontes = selecionar_fontes(recortes)
    relatorio = {
        "arquivo_entrada": caminho_csv.name if caminho_csv.is_absolute() else caminho_csv.as_posix(),
        "sha256_entrada": hashlib.sha256(caminho_csv.read_bytes()).hexdigest(),
        "ambiente": ambiente_atual(),
        "inicio_utc": datetime.now(timezone.utc).isoformat(),
        "semente": 42,
        "regra_recorte": "prefixos de 10%, 50% e 100% das ocorrências embaralhadas uma vez; PESO preservado",
        "regra_fontes": "no recorte de 10%, grau de saída >= 3; ordem por grau decrescente e nome crescente; posições 0, n // 4, n // 2",
        "fontes": fontes,
        "alcance_inclui_fonte": False,
        "intervalo_medido": "somente a chamada do algoritmo; busca completa por fonte",
        "configuracoes_esperadas": 18,
        "completo": False,
        "medicoes": [],
    }
    caminho_saida.parent.mkdir(parents=True, exist_ok=True)
    for recorte in recortes:
        grafo_base = recorte["grafo"]
        grafo_transformado = {}
        for origem, vizinhos in grafo_base.items():
            grafo_transformado[origem] = [(destino, peso + 1) for destino, peso in vizinhos]

        for fonte in fontes:
            # Conferência por conjuntos, sem incluir a fonte e sem medir tempo.
            distancias_bfs, _ = bfs(grafo_base, fonte)
            distancias_dijkstra, _ = dijkstra(grafo_transformado, fonte)
            alcance_bfs = {no for no, distancia in distancias_bfs.items()
                           if no != fonte and math.isfinite(distancia)}
            alcance_dijkstra = {no for no, distancia in distancias_dijkstra.items()
                                if no != fonte and math.isfinite(distancia)}
            if alcance_bfs != alcance_dijkstra:
                raise ValueError(f"Alcances diferentes: {recorte['percentual']}% | {fonte}.")

            tarefas = [("BFS", bfs, grafo_base, "PESO", 0),
                       ("DIJKSTRA", dijkstra, grafo_transformado, "PESO + 1", 1)]
            for nome, algoritmo, entrada, versao, deslocamento in tarefas:
                medicao = medir_algoritmo(algoritmo, entrada, fonte, repeticoes=5)
                medicao.update({
                    "algoritmo": nome, "tarefa": "busca_completa_por_fonte",
                    "fonte": fonte, "percentual": recorte["percentual"],
                    "vertices": recorte["vertices"], "arcos": recorte["arcos"],
                    "grau_saida_fonte": len(grafo_base[fonte]),
                    "outros_usuarios_alcancados": len(alcance_bfs),
                    "versao_pesos": versao, "deslocamento": deslocamento, "semente": 42,
                })
                relatorio["medicoes"].append(medicao)
                relatorio["completo"] = len(relatorio["medicoes"]) == 18
                if relatorio["completo"]:
                    relatorio["fim_utc"] = datetime.now(timezone.utc).isoformat()
                caminho_saida.write_text(
                    json.dumps(relatorio, ensure_ascii=False, indent=2, allow_nan=False), encoding="utf-8"
                )
                print(f"{nome} | {recorte['percentual']}% | {fonte} | média: {medicao['media']:.6f} s", flush=True)
    return relatorio


# [IA] ChatGPT (Codex) – comando para reproduzir as medições na máquina de André.
def main():
    parser = argparse.ArgumentParser(description="Benchmark de BFS e Dijkstra na Parte 2.")
    parser.add_argument("--dataset", default="data/dataset_parte2/processed/wikiRfA_tratado.csv")
    parser.add_argument("--out", default="out/parte2/benchmark_bfs_dijkstra_mesmo_ambiente.json")
    argumentos = parser.parse_args()
    executar_benchmark(argumentos.dataset, argumentos.out)


if __name__ == "__main__":
    main()
