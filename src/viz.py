import csv

import matplotlib.pyplot as plt
from matplotlib.patches import Patch

from src.graphs.algorithms import bfs
from src.graphs.io import ler_mapa


def casa_do_rotulo(rotulo):
    posicao = rotulo.split("|")[0]
    linha, coluna = posicao.strip("()").split(",")
    return int(linha), int(coluna)


def heatmap_multiplicidade(caminho_mapa, caminho_graus, caminho_png):
    mapa = ler_mapa(caminho_mapa)

    multiplicidade = {}
    with open(caminho_graus, encoding="utf-8") as arquivo:
        for registro in csv.DictReader(arquivo):
            casa = casa_do_rotulo(registro["estado"])
            multiplicidade[casa] = multiplicidade.get(casa, 0) + 1

    maximo = max(multiplicidade.values())
    casas_maximo = list(multiplicidade.values()).count(maximo)

    grade = []
    for linha in range(mapa.linhas):
        grade.append([])
        for coluna in range(mapa.colunas):
            if mapa.casa(linha, coluna) == "#":
                grade[linha].append(float("nan"))
            else:
                grade[linha].append(multiplicidade.get((linha, coluna), 0))

    cores = plt.get_cmap("viridis", maximo + 1).copy()
    cores.set_bad("#3a3a3a")

    figura, eixo = plt.subplots(figsize=(16, 8))
    imagem = eixo.imshow(grade, cmap=cores, vmin=-0.5, vmax=maximo + 0.5)
    barra = figura.colorbar(imagem, ax=eixo, ticks=range(maximo + 1), shrink=0.8)
    barra.set_label("estados do G_est nesta casa")
    eixo.legend(handles=[Patch(color="#3a3a3a", label="parede")], loc="upper center", bbox_to_anchor=(0.5, -0.08))
    eixo.set_title(f"Multiplicidade das casas do {mapa.nome}: máximo {maximo}, atingido por {casas_maximo} casas")
    eixo.set_xlabel("coluna")
    eixo.set_ylabel("linha")

    figura.savefig(caminho_png, dpi=150, bbox_inches="tight")
    plt.close(figura)


def arvore_bfs(caminho_arestas, caminho_png):
    grafo = {}
    inicio = None
    with open(caminho_arestas, encoding="utf-8") as arquivo:
        for linha in csv.DictReader(arquivo):
            origem = linha["origem"]
            destino = linha["destino"]
            if inicio is None:
                inicio = origem
            if origem not in grafo:
                grafo[origem] = []
            if destino not in grafo:
                grafo[destino] = []
            grafo[origem].append((destino, int(linha["peso"])))

    distancia, pai = bfs(grafo, inicio)

    niveis = {}
    for estado in grafo:
        nivel = distancia[estado]
        if nivel not in niveis:
            niveis[nivel] = []
        niveis[nivel].append(estado)

    posicao = {}
    for nivel in niveis:
        quantos = len(niveis[nivel])
        for i in range(quantos):
            estado = niveis[nivel][i]
            posicao[estado] = (i - (quantos - 1) / 2, nivel)

    figura, eixo = plt.subplots(figsize=(8, 14))

    for estado in grafo:
        if pai[estado] is not None:
            x1, y1 = posicao[pai[estado]]
            x2, y2 = posicao[estado]
            eixo.plot([x1, x2], [y1, y2], color="gray", zorder=1)

    for estado in grafo:
        x, y = posicao[estado]
        if estado == "ALVO":
            cor = "black"
        elif "|-|" in estado:
            cor = "green"
        else:
            cor = "orange"
        eixo.scatter(x, y, color=cor, zorder=2)
        eixo.text(x + 0.06, y, estado, fontsize=7, va="center")

    eixo.scatter([], [], color="green", label="estado sem chave")
    eixo.scatter([], [], color="orange", label="estado com a chave a")
    eixo.scatter([], [], color="black", label="ALVO")
    eixo.plot([], [], color="gray", label="aresta da árvore (pai → filho)")
    eixo.legend(loc="lower left")

    eixo.set_title("Árvore BFS de estados do m02")
    eixo.set_ylabel("nível (distância BFS a partir do início)")
    eixo.set_yticks(range(len(niveis)))
    eixo.set_xticks([])
    eixo.set_xlim(-1.5, 2)
    eixo.invert_yaxis()
    eixo.grid(axis="y", alpha=0.3)

    figura.savefig(caminho_png, dpi=150, bbox_inches="tight")
    plt.close(figura)
