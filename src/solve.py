import math
import csv
import shutil
from pathlib import Path

from src.graphs.algorithms import bellman_ford, bfs, dfs, dijkstra, reconstruir_caminho
from src.graphs.estados import ALVO, construir_g_est, estado_inicial, rotulo
from src.graphs.io import (exportar_parte1, exportar_arestas, exportar_graus,
                           ler_mapa, escrever_json)
from src.graphs.estados import (camadas_do_mapa, construir_g_pos,
                                graus, metricas_do_mapa, sem_alvo)

COLUNAS_SOLUCOES = ['mapa', 'algoritmo', 'passos', 'custo', 'status', 'caminho']
COLUNAS_DFS = ['mapa', 'arvore', 'retorno', 'avanco', 'cruzamento']

def resolver(caminho_mapa, algoritmo, fonte_consumivel = False):

    mapa = ler_mapa(caminho_mapa)

    grafo = construir_g_est(mapa, fonte_consumivel)

    origem = estado_inicial(mapa)

    linha = {"mapa": mapa.nome, "algoritmo": algoritmo, "passos": "", "custo": "", "status": "", "caminho": "", "ciclo": []}

    if (algoritmo == 'DIJKSTRA'):
        try:
            dist, pred = dijkstra(grafo, origem)
        except ValueError:
            linha['status'] = 'RECUSA'
            return linha

    elif (algoritmo == 'BFS'):
        dist, pred = bfs(grafo, origem)

    elif (algoritmo == 'BELLMAN_FORD'):
        dist, pred, ciclo = bellman_ford(grafo, origem)
        if ciclo is not None:
            linha['status'] = 'CICLO_NEGATIVO'
            linha['ciclo'] = [rotulo(estado) if estado != ALVO else ALVO for estado in ciclo]
            return linha

    if dist[ALVO] == math.inf:
        linha['status'] = 'SEM_SOLUCAO'
        return linha

    caminho_reconstruido = reconstruir_caminho(dist, pred, ALVO)

    
    linha['passos'] = len(caminho_reconstruido) - 2

    if (algoritmo == 'BELLMAN_FORD' or algoritmo == 'DIJKSTRA'): 
        linha['custo'] = dist[ALVO]
    else:
        custo = 0

        for i in range(len(caminho_reconstruido) - 1):
            
            estado_atual = caminho_reconstruido[i]
            proximo_estado = caminho_reconstruido[i + 1]

            # [IA] Claude – estrutura do laço pelos pares do caminho
            for destino, peso in grafo[estado_atual]:
                if (destino == proximo_estado):
                    custo += peso
                    break
            
        linha['custo'] = custo

    lista_caminho = []

    # [IA] Claude – sintaxe do join para montar o caminho
    for estado in caminho_reconstruido[:-1]:
        lista_caminho.append(rotulo(estado))
    linha['caminho'] = ' -> '.join(lista_caminho)

    linha['status'] = 'OK'

    return linha

def contar_classificacao(caminho_mapa, fonte_consumivel=False):

    mapa = ler_mapa(caminho_mapa)
    
    grafo = construir_g_est(mapa, fonte_consumivel)
    
    origem = estado_inicial(mapa)

    _, _, _, classif, _ = dfs(grafo, origem)

    linha = {'mapa': mapa.nome,
             'arvore': 0,
             'retorno': 0,
             'avanco': 0,
             'cruzamento': 0}

    for tipo in classif.values():
        linha[tipo] += 1

    return linha

# [IA] Claude – sintaxe de pathlib e csv
def escrever_csv(linhas, colunas, caminho):
    with open(caminho, 'w', newline = '', encoding = 'utf-8') as arquivo:
            escritor = csv.DictWriter(arquivo, fieldnames=colunas, extrasaction="ignore", lineterminator="\n")
            escritor.writeheader()
            escritor.writerows(linhas)


# [IA] ChatGPT (Codex) – IMPLEMENTA AS FUNÇÕES DE EXPORTAÇÃO
def exportar_armadilhas(pastas, pasta_saida):
    pasta_saida = Path(pasta_saida)
    pasta_saida.mkdir(parents=True, exist_ok=True)
    resumos = []
    for pasta in pastas:
        for caminho in sorted(Path(pasta).glob("*.txt")):
            mapa = ler_mapa(caminho)
            grafo = construir_g_est(mapa)
            armadilhas = estados_armadilha_local(grafo, estado_inicial(mapa))
            vertices, arcos_sem_alvo = sem_alvo(grafo)
            _, graus_saida = graus(vertices, arcos_sem_alvo)
            proporcao = len(armadilhas) / len(vertices) if vertices else 0
            arquivo = pasta_saida / f"armadilhas_{mapa.nome}.csv"
            with open(arquivo, "w", newline="", encoding="utf-8") as stream:
                campos = ["mapa", "estado", "grau_saida", "total_estados", "total_armadilhas", "proporcao_armadilhas"]
                escritor = csv.DictWriter(stream, fieldnames=campos, lineterminator="\n")
                escritor.writeheader()
                for estado in sorted(armadilhas, key=rotulo):
                    escritor.writerow({"mapa": mapa.nome, "estado": rotulo(estado),
                                       "grau_saida": graus_saida.get(estado, 0),
                                       "total_estados": len(vertices), "total_armadilhas": len(armadilhas),
                                       "proporcao_armadilhas": proporcao})
            if mapa.nome.startswith("m04_"):
                shutil.copyfile(arquivo, pasta_saida / "armadilhas_m04.csv")
            elif mapa.nome.startswith("m07_"):
                shutil.copyfile(arquivo, pasta_saida / "armadilhas_m07.csv")
            resumos.append({"mapa": mapa.nome, "total_estados": len(vertices),
                            "total_armadilhas": len(armadilhas), "proporcao_armadilhas": proporcao})
    escrever_json(resumos, pasta_saida / "resumo_armadilhas.json")
    return resumos


def estados_armadilha_local(grafo, origem):
    alcancados = set()
    fila = [origem]
    while fila:
        atual = fila.pop(0)
        if atual in alcancados:
            continue
        alcancados.add(atual)
        fila.extend(destino for destino, _ in grafo.get(atual, []) if destino not in alcancados)
    reverso = {vertice: [] for vertice in grafo}
    for atual, vizinhos in grafo.items():
        for destino, _ in vizinhos:
            reverso.setdefault(destino, []).append(atual)
    conseguem_sair = set()
    fila = [ALVO]
    while fila:
        atual = fila.pop(0)
        if atual in conseguem_sair:
            continue
        conseguem_sair.add(atual)
        fila.extend(v for v in reverso.get(atual, []) if v not in conseguem_sair)
    return alcancados - conseguem_sair


# [IA] ChatGPT (Codex) – GERA TABELA DE COMPARAÇÃO
def exportar_comparacao(pastas, pasta_saida, fonte_consumivel=False):
    modelos = ("portas_como_chao", "portas_como_parede", "grafo_de_estados")
    linhas = []
    for caminho in sorted(Path("data/mapas").glob("m0[234]*.txt")):
        mapa = ler_mapa(caminho)
        candidatos = ((construir_g_pos(mapa, "chao"), mapa.inicio),
                      (construir_g_pos(mapa, "parede"), mapa.inicio),
                      (construir_g_est(mapa, fonte_consumivel), estado_inicial(mapa)))
        for nome, (grafo, origem) in zip(modelos, candidatos):
            distancias, _ = bfs(grafo, origem)
            passos = distancias.get(ALVO, math.inf)
            linhas.append({"mapa": mapa.nome, "modelagem": nome,
                           "passos": "" if passos == math.inf else int(passos),
                           "status": "SEM_SOLUCAO" if passos == math.inf else "OK",
                           "fonte_consumivel": fonte_consumivel})
    escrever_csv(linhas, ["mapa", "modelagem", "passos", "status", "fonte_consumivel"], Path(pasta_saida) / "comparacao_modelagem.csv")
    return linhas


def normalizar_csvs(pasta_saida):
    for caminho in Path(pasta_saida).rglob("*.csv"):
        conteudo = caminho.read_bytes()
        if b"\r\n" in conteudo:
            caminho.write_bytes(conteudo.replace(b"\r\n", b"\n"))


def exportar_metricas_variante(pastas, pasta_saida, fonte_consumivel):
    pasta_saida = Path(pasta_saida)
    metricas, camadas = [], {}
    for pasta in pastas:
        for caminho in sorted(Path(pasta).glob("*.txt")):
            mapa = ler_mapa(caminho)
            g_pos = construir_g_pos(mapa)
            g_est = construir_g_est(mapa, fonte_consumivel)
            exportar_arestas(g_est, mapa, pasta_saida / f"arestas_{mapa.nome}.csv")
            exportar_graus(g_est, pasta_saida / f"graus_{mapa.nome}.csv")
            metricas.append(metricas_do_mapa(mapa, g_pos, g_est, fonte_consumivel))
            camadas[mapa.nome] = camadas_do_mapa(mapa, g_est)
    escrever_json(metricas, pasta_saida / "metricas_global.json")
    escrever_json(camadas, pasta_saida / "camadas.json")

def resolver_todos(pastas, pasta_saida, fonte_consumivel=False):

    pasta_saida = Path(pasta_saida)
    pasta_saida.mkdir(parents = True, exist_ok = True)

    linhas_solucoes = []
    linhas_classificacao = []

    algoritmos = ['BFS', 'DIJKSTRA', 'BELLMAN_FORD']

    for pasta in pastas:
        for caminho in sorted(Path(pasta).glob("*.txt")):
            linhas_classificacao.append(contar_classificacao(caminho, fonte_consumivel))
            for algoritmo in algoritmos:
                linhas_solucoes.append(resolver(caminho, algoritmo, fonte_consumivel))

    escrever_csv(linhas_solucoes, COLUNAS_SOLUCOES, pasta_saida / 'solucoes.csv')
    escrever_csv(linhas_classificacao, COLUNAS_DFS, pasta_saida / 'dfs_classificacao.csv')
    
    if fonte_consumivel:
        exportar_metricas_variante(pastas, pasta_saida, True)
    else:
        exportar_parte1(pastas, pasta_saida)
    exportar_armadilhas(pastas, pasta_saida)
    exportar_comparacao(pastas, pasta_saida, fonte_consumivel)
    escrever_json({"fonte_consumivel": fonte_consumivel,
                   "mapas": [Path(p).name for p in pastas]}, pasta_saida / "configuracao_parte1.json")
    normalizar_csvs(pasta_saida)
    for nome, caminho, algoritmo in (
        ("percurso_m03.json", Path("data/mapas/m03_tres_chaves.txt"), "BELLMAN_FORD"),
        ("ciclo_negativo_m06.json", Path("data/mapas/m06_fonte.txt"), "BELLMAN_FORD"),
    ):
        resultado = resolver(caminho, algoritmo, fonte_consumivel)
        if nome == "percurso_m03.json":
            escrever_json(resultado, pasta_saida / nome)
        elif resultado["status"] == "CICLO_NEGATIVO":
            escrever_json({"mapa": resultado["mapa"], "algoritmo": algoritmo,
                           "status": resultado["status"], "ciclo": resultado["ciclo"]}, pasta_saida / nome)
