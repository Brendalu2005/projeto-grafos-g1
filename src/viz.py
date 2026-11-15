import csv

import matplotlib.pyplot as plt
from matplotlib.patches import Patch

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
