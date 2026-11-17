import math
import csv
from pathlib import Path

from src.graphs.algorithms import bellman_ford, bfs, dfs, dijkstra, reconstruir_caminho
from src.graphs.estados import ALVO, construir_g_est, estado_inicial, rotulo
from src.graphs.io import exportar_parte1, ler_mapa

COLUNAS_SOLUCOES = ['mapa', 'algoritmo', 'passos', 'custo', 'status', 'caminho']
COLUNAS_DFS = ['mapa', 'arvore', 'retorno', 'avanco', 'cruzamento']

# Roda algoritmo no mapa e devolve linha em solucoes.csv
def resolver(caminho_mapa, algoritmo, fonte_consumivel = False):

    mapa = ler_mapa(caminho_mapa)

    grafo = construir_g_est(mapa, fonte_consumivel)

    origem = estado_inicial(mapa)

    linha = {"mapa": mapa.nome, "algoritmo": algoritmo, "passos": "", "custo": "", "status": "", "caminho": ""}

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
            return linha

    if dist[ALVO] == math.inf:
        linha['status'] = 'SEM_SOLUCAO'
        return linha

    caminho_reconstruido = reconstruir_caminho(dist, pred, ALVO)

    # Subtraindo 1 (pelos movimentos entre estados) e removendo o alvo
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

# Roda DFS e devolve linha em dfs_classificacao.csv
def contar_classificacao(caminho_mapa):

    mapa = ler_mapa(caminho_mapa)
    
    grafo = construir_g_est(mapa)
    
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
            escritor = csv.DictWriter(arquivo, fieldnames = (colunas))
            escritor.writeheader()
            escritor.writerows(linhas)

# Percorre todos os mapas, chama as duas funções.
def resolver_todos(pastas, pasta_saida):

    pasta_saida = Path(pasta_saida)
    pasta_saida.mkdir(parents = True, exist_ok = True)

    linhas_solucoes = []
    linhas_classificacao = []

    algoritmos = ['BFS', 'DIJKSTRA', 'BELLMAN_FORD']

    for pasta in pastas:
        for caminho in sorted(Path(pasta).glob("*.txt")):
            linhas_classificacao.append(contar_classificacao(caminho))
            for algoritmo in algoritmos:
                linhas_solucoes.append(resolver(caminho, algoritmo))

    escrever_csv(linhas_solucoes, COLUNAS_SOLUCOES, pasta_saida / 'solucoes.csv')
    escrever_csv(linhas_classificacao, COLUNAS_DFS, pasta_saida / 'dfs_classificacao.csv')
    
    exportar_parte1(pastas, pasta_saida)