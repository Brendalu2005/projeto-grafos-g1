import math
import csv
import shutil
import hashlib
import json
from pathlib import Path

from src.graphs.algorithms import bellman_ford, bfs, dfs, dijkstra, reconstruir_caminho
from src.graphs.estados import ALVO, construir_g_est, estado_inicial, rotulo
from src.graphs.io import (exportar_parte1, exportar_arestas, exportar_graus,
                           ler_mapa, escrever_json, carregar_dataset)
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
            # [IA] ChatGPT (Codex) – soma os pesos dos arcos do ciclo já retornado pelo algoritmo.
            linha['custo_ciclo'] = sum(
                next(peso for destino, peso in grafo[u] if destino == v)
                for u, v in zip(ciclo, ciclo[1:])
            )
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
def exportar_armadilhas(pastas, pasta_saida, fonte_consumivel=False):
    pasta_saida = Path(pasta_saida)
    pasta_saida.mkdir(parents=True, exist_ok=True)
    resumos = []
    for pasta in pastas:
        for caminho in sorted(Path(pasta).glob("*.txt")):
            mapa = ler_mapa(caminho)
            grafo = construir_g_est(mapa, fonte_consumivel)
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
            # [IA] ChatGPT (Codex) – depuração: o arco virtual até ALVO não é movimento na grade.
            passos = distancias.get(ALVO, math.inf) - 1
            linhas.append({"mapa": mapa.nome, "abordagem": nome, "modelagem": nome,
                           "passos": "" if passos == math.inf else int(passos),
                           # Validação e observação devem ser preenchidas pelo grupo.
                           "caminho_valido": "", "observacao": "",
                           "status": "SEM_SOLUCAO" if passos == math.inf else "OK",
                           "fonte_consumivel": fonte_consumivel})
    escrever_csv(linhas, ["mapa", "abordagem", "passos", "caminho_valido", "observacao",
                         "modelagem", "status", "fonte_consumivel"], Path(pasta_saida) / "comparacao_modelagem.csv")
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
    exportar_armadilhas(pastas, pasta_saida, fonte_consumivel)
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
                           "status": resultado["status"], "ciclo": resultado["ciclo"],
                           "custo_ciclo": resultado["custo_ciclo"]}, pasta_saida / nome)


# [IA] ChatGPT (Codex) – integração da Parte 2, escolhas copiadas do notebook.
FONTES_DATASET = ["Siva1979", "'sed", "!---slappdash---!"]
PARES_DATASET = [
    ("Siva1979", "(aeropagitica)"),
    ("Siva1979", "Dieter Simon"),
    ("'sed", "9cds"),
    ("'sed", "Caltrop"),
    ("!---slappdash---!", "Caltrop"),
]
CASOS_BELLMAN = {
    "negativo_sem_ciclo": {
        "usuarios": ["Malleus Fatuorum", "BDD"],
        "fonte": "Malleus Fatuorum",
    },
    "ciclo_negativo": {
        "usuarios": ["Rcsprinter123", "Jasper Deng"],
        "fonte": "Rcsprinter123",
    },
}


# [IA] ChatGPT (Codex) – organização dos retornos dos algoritmos existentes, sem reimplementá-los.
def resultado_busca_dataset(grafo, fonte, algoritmo):
    if fonte not in grafo:
        raise ValueError(f"Fonte não encontrada no grafo: {fonte}")
    if algoritmo == "BFS":
        distancias, predecessores = bfs(grafo, fonte)
        finitas = [d for d in distancias.values() if d != math.inf]
        return {
            "fonte": fonte,
            "grau_saida_fonte": len(grafo[fonte]),
            "outros_usuarios_alcancados": len(finitas) - 1,
            "maior_distancia_finita": max(finitas),
            "distancias": {v: None if d == math.inf else d for v, d in distancias.items()},
            "predecessores": predecessores,
        }
    if algoritmo != "DFS":
        raise ValueError("A busca deve ser BFS ou DFS.")
    descoberta, termino, predecessores, classificacao, tem_ciclo = dfs(grafo, fonte)
    contagens = {tipo: 0 for tipo in ("arvore", "retorno", "avanco", "cruzamento")}
    for tipo in classificacao.values():
        contagens[tipo] += 1
    return {
        "fonte": fonte,
        "vertices_alcancados_incluindo_fonte": len(descoberta),
        "outros_usuarios_alcancados": len(descoberta) - 1,
        "ordem_descoberta": list(descoberta),
        "tempos_descoberta": descoberta,
        "tempos_termino": termino,
        "predecessores": predecessores,
        "arcos_classificados": len(classificacao),
        "classificacao_arcos": contagens,
        "tem_ciclo": tem_ciclo,
    }


# [IA] ChatGPT (Codex) – aplica a transformação já definida por Brenda em uma cópia.
def transformar_pesos_dataset(grafo, deslocamento):
    if deslocamento < 0:
        raise ValueError("O deslocamento deve ser não negativo.")
    return {
        origem: [(destino, peso + deslocamento) for destino, peso in vizinhos]
        for origem, vizinhos in grafo.items()
    }


# [IA] ChatGPT (Codex) – exportação de um par a partir dos retornos do Dijkstra existente.
def resultado_par_dataset(distancias, predecessores, origem, destino):
    if destino not in distancias:
        raise ValueError(f"Destino não encontrado no grafo: {destino}")
    alcancavel = distancias[destino] != math.inf
    caminho = reconstruir_caminho(distancias, predecessores, destino) if alcancavel else []
    return {
        "origem": origem,
        "destino": destino,
        "status": "OK" if alcancavel else "SEM_CAMINHO",
        "caminho": caminho,
        "quantidade_arcos": len(caminho) - 1 if alcancavel else None,
        "custo_transformado": distancias[destino] if alcancavel else None,
    }


# [IA] ChatGPT (Codex) – reproduz os recortes e chamadas de Bellman-Ford já conferidos no notebook.
def resultado_bellman_dataset(caminho_csv, caso):
    if caso not in CASOS_BELLMAN:
        raise ValueError(f"Caso de Bellman-Ford desconhecido: {caso}")
    selecao = CASOS_BELLMAN[caso]
    usuarios = selecao["usuarios"]
    fonte = selecao["fonte"]
    completo = carregar_dataset(caminho_csv)
    if any(usuario not in completo for usuario in usuarios):
        raise ValueError(f"O CSV não contém todos os usuários do caso {caso}.")
    grafo = {usuario: [] for usuario in usuarios}
    arcos = []
    with open(caminho_csv, newline="", encoding="utf-8-sig") as arquivo:
        for indice, linha in enumerate(csv.DictReader(arquivo)):
            origem, destino = linha["SOURCE"], linha["TARGET"]
            if origem not in grafo or destino not in grafo:
                continue
            peso = int(linha["PESO"])
            arcos.append({
                "indice_registro_csv_base_zero": indice,
                "linha_csv_com_cabecalho": indice + 2,
                "origem": origem, "destino": destino,
                "indice_adjacencia": len(grafo[origem]),
                "VOTE": int(linha["VOTE"]), "RESULT": int(linha["RESULT"]), "PESO": peso,
            })
            grafo[origem].append((destino, peso))
    if not any(arco["PESO"] < 0 for arco in arcos):
        raise ValueError(f"O recorte {caso} não contém peso negativo neste CSV.")
    distancias, predecessores, ciclo = bellman_ford(grafo, fonte)
    if (ciclo is not None) != (caso == "ciclo_negativo"):
        raise ValueError(f"O recorte {caso} não reproduziu o comportamento registrado no notebook.")
    if ciclo is None and any(d == math.inf for d in distancias.values()):
        raise ValueError(f"O recorte {caso} contém usuário inalcançável pela fonte registrada.")
    resultado = {
        "id": caso, "fonte": fonte, "usuarios": usuarios,
        "vertices": len(grafo), "arcos": arcos, "tem_ciclo_negativo": ciclo is not None,
    }
    if ciclo is None:
        resultado.update({
            "status": "OK",
            "distancias": {v: None if d == math.inf else d for v, d in distancias.items()},
            "predecessores": predecessores,
            "caminhos": {
                v: [] if distancias[v] == math.inf else reconstruir_caminho(distancias, predecessores, v)
                for v in grafo
            },
        })
        return resultado
    arcos_ciclo = []
    for origem, destino in zip(ciclo, ciclo[1:]):
        candidatos = [a for a in arcos if a["origem"] == origem and a["destino"] == destino]
        if len(candidatos) != 1:
            raise ValueError("Ciclo com arcos paralelos: é necessário identificar a ocorrência utilizada.")
        arcos_ciclo.append(candidatos[0])
    resultado.update({
        "status": "CICLO_NEGATIVO", "ciclo": ciclo, "arcos_ciclo": arcos_ciclo,
        "custo_ciclo": sum(a["PESO"] for a in arcos_ciclo), "distancias": None,
        "observacao_distancias": "Valores provisórios da execução com ciclo negativo não são apresentados como custos mínimos finitos.",
    })
    return resultado


# [IA] ChatGPT (Codex) – execução individual da Parte 2 e validação de parâmetros.
def resolver_dataset(caminho_csv, algoritmo, fonte=None, destino=None, caso=None, deslocamento=0):
    if algoritmo not in ("BFS", "DFS", "DIJKSTRA", "BELLMAN_FORD"):
        raise ValueError(f"Algoritmo desconhecido: {algoritmo}")
    if algoritmo == "BELLMAN_FORD":
        if fonte is not None or destino is not None or deslocamento != 0:
            raise ValueError("Os casos de Bellman-Ford já definem a fonte e usam PESO sem deslocamento.")
        resultado = resultado_bellman_dataset(caminho_csv, caso)
        return {"algoritmo": algoritmo, "arquivo_entrada": Path(caminho_csv).as_posix(),
                "coluna_peso": "PESO", "resultado": resultado}
    if caso is not None:
        raise ValueError("--caso é exclusivo de BELLMAN_FORD.")
    grafo = carregar_dataset(caminho_csv)
    if fonte not in grafo:
        raise ValueError(f"Fonte não encontrada no grafo: {fonte}")
    relatorio = {"algoritmo": algoritmo, "arquivo_entrada": Path(caminho_csv).as_posix(),
                 "coluna_peso_carregada": "PESO", "vertices": len(grafo)}
    if algoritmo in ("BFS", "DFS"):
        if destino is not None or deslocamento != 0:
            raise ValueError("BFS e DFS recebem apenas a fonte e não aplicam deslocamento.")
        relatorio["pesos_considerados_na_busca"] = False
        if algoritmo == "BFS":
            relatorio["unidade_distancia"] = "arcos"
        else:
            relatorio["cobrir_todos"] = False
            relatorio["ordem_vizinhos"] = "ordem dos arcos no CSV tratado, preservada pelo carregador"
            relatorio["identidade_arco"] = "(origem, destino, indice_na_adjacencia), com indice iniciando em zero"
        relatorio["resultado"] = resultado_busca_dataset(grafo, fonte, algoritmo)
    else:
        if destino not in grafo:
            raise ValueError(f"Destino não encontrado no grafo: {destino}")
        transformado = transformar_pesos_dataset(grafo, deslocamento)
        distancias, predecessores = dijkstra(transformado, fonte)
        relatorio["transformacao"] = "novo_peso = PESO + deslocamento"
        relatorio["deslocamento"] = deslocamento
        relatorio["resultado"] = resultado_par_dataset(distancias, predecessores, fonte, destino)
    return relatorio


# [IA] ChatGPT (Codex) – JSON estrito: distâncias inalcançáveis são convertidas antes da gravação.
def salvar_resultado_dataset(resultado, caminho):
    caminho = Path(caminho)
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_text(json.dumps(resultado, ensure_ascii=False, indent=2, allow_nan=False), encoding="utf-8")


# [IA] ChatGPT (Codex) – reprodução dos experimentos existentes; não executa benchmark.
def executar_experimentos_dataset(caminho_csv, pasta_saida):
    grafo = carregar_dataset(caminho_csv)
    entrada = Path(caminho_csv).as_posix()
    saida = Path(pasta_saida)
    arquivos = []
    for algoritmo, nome in (("BFS", "bfs_fontes.json"), ("DFS", "dfs_fontes.json")):
        relatorio = {
            "algoritmo": algoritmo, "arquivo_entrada": entrada,
            "coluna_peso_carregada": "PESO", "pesos_considerados_na_busca": False,
            "vertices": len(grafo),
            "resultados": [resultado_busca_dataset(grafo, fonte, algoritmo) for fonte in FONTES_DATASET],
        }
        if algoritmo == "BFS":
            relatorio["unidade_distancia"] = "arcos"
        else:
            relatorio.update({
                "cobrir_todos": False,
                "ordem_vizinhos": "ordem dos arcos no CSV tratado, preservada pelo carregador",
                "identidade_arco": "(origem, destino, indice_na_adjacencia), com indice iniciando em zero",
            })
        salvar_resultado_dataset(relatorio, saida / nome)
        arquivos.append(saida / nome)
    transformado = transformar_pesos_dataset(grafo, 1)
    buscas = {}
    pares = []
    for fonte, destino in PARES_DATASET:
        if fonte not in buscas:
            buscas[fonte] = dijkstra(transformado, fonte)
        distancias, predecessores = buscas[fonte]
        pares.append(resultado_par_dataset(distancias, predecessores, fonte, destino))
    relatorio = {
        "algoritmo": "DIJKSTRA", "arquivo_entrada": entrada, "coluna_peso_base": "PESO",
        "transformacao": "novo_peso = PESO + deslocamento", "deslocamento": 1,
        "vertices": len(grafo), "buscas_por_origem": len(buscas), "resultados": pares,
    }
    salvar_resultado_dataset(relatorio, saida / "dijkstra_pares.json")
    arquivos.append(saida / "dijkstra_pares.json")
    relatorio = {
        "algoritmo": "BELLMAN_FORD", "arquivo_entrada": entrada,
        "sha256_entrada": hashlib.sha256(Path(caminho_csv).read_bytes()).hexdigest(),
        "coluna_peso": "PESO",
        "regra_recorte": "subgrafo induzido pelos usuários informados; todas as ocorrências entre eles são preservadas",
        "selecao": "exemplos mínimos sugeridos por Codex para conferência e justificativa autoral de André",
        "benchmark": False,
        "resultados": [resultado_bellman_dataset(caminho_csv, caso) for caso in CASOS_BELLMAN],
    }
    salvar_resultado_dataset(relatorio, saida / "bellman_ford_casos.json")
    arquivos.append(saida / "bellman_ford_casos.json")
    return arquivos
