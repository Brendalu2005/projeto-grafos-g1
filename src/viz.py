import csv

import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.colors import ListedColormap

from src.graphs.algorithms import bfs
from src.graphs.estados import ALVO, construir_g_est, estado_inicial
from src.graphs.io import ler_mapa
from src.solve import resolver


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


# [IA] ChatGPT (Codex) – AJUSTE DE ESTRUTURA E ERROS (PARTE VISUAL TAMBEM)
def percurso_colorido(caminho_mapa, resultado, caminho_png):
    mapa = ler_mapa(caminho_mapa)
    labels = str(resultado["caminho"]).split(" -> ")
    estados = []
    for label in labels:
        if label == "" or label == ALVO:
            continue
        pos, keys, _ = label.split("|")
        linha, coluna = map(int, pos.strip("()").split(","))
        camada = 0 if keys == "-" else len(keys)
        estados.append((linha, coluna, camada))
    figura, eixo = plt.subplots(figsize=(max(9, mapa.colunas * .28), max(5, mapa.linhas * .28)))
    eixo.set_facecolor("#252a2e")
    grade = [[0 if mapa.casa(r, c) == "#" else 1 for c in range(mapa.colunas)] for r in range(mapa.linhas)]
    eixo.imshow(grade, cmap=ListedColormap(["#30363b", "#f3f0e8"]), vmin=0, vmax=1)
    cores = ["#2878b5", "#ed9b40", "#51a66b", "#a564bd"]
    for camada in range(4):
        pontos = [(c, r) for r, c, k in estados if k == camada]
        if pontos:
            xs, ys = zip(*pontos)
            eixo.plot(xs, ys, color=cores[camada], linewidth=3, marker="o", markersize=4,
                      label=f"camada com {camada} chave(s)", zorder=3)
    for r, linha in enumerate(mapa.grade):
        for c, simbolo in enumerate(linha):
            if simbolo in "SGabcdABCD><^v+*":
                eixo.text(c, r, simbolo, ha="center", va="center", fontsize=8,
                          color="#111111", fontweight="bold", zorder=4)
    eixo.set_title(f"Percurso de menor custo: {mapa.nome} (cores por camada de chaves)")
    eixo.set_xlabel("coluna")
    eixo.set_ylabel("linha")
    eixo.set_xticks(range(mapa.colunas))
    eixo.set_yticks(range(mapa.linhas))
    eixo.grid(alpha=.12)
    eixo.legend(loc="upper center", bbox_to_anchor=(.5, -0.08), ncol=4)
    figura.tight_layout()
    figura.savefig(caminho_png, dpi=170, bbox_inches="tight")
    plt.close(figura)


# [IA] ChatGPT (Codex) – DESENHO DO GRAFO DE ESTADOS (CORREÇÃO E AJUSTES)
def grafo_estados_camadas(caminho_mapa, caminho_png):
    mapa = ler_mapa(caminho_mapa)
    grafo = construir_g_est(mapa)
    vertices = [v for v in grafo if v != ALVO]
    por_camada = {}
    for v in vertices:
        por_camada.setdefault("".join(sorted(v[2])) or "-", []).append(v)
    camadas = sorted(por_camada, key=lambda item: (item != "-", item))
    posicao = {}
    for x, nome in enumerate(camadas):
        grupo = sorted(por_camada[nome], key=lambda estado: (estado[0], estado[1], sorted(estado[3])))
        for indice, estado in enumerate(grupo):
            posicao[estado] = (x * 3.0, -indice * 1.1)
    posicao[ALVO] = (len(camadas) * 3.0, 0)
    figura, eixo = plt.subplots(figsize=(max(10, len(camadas) * 4), max(7, len(vertices) * .22)))
    for origem, vizinhos in grafo.items():
        for destino, _ in vizinhos:
            x1, y1 = posicao[origem]
            x2, y2 = posicao[destino]
            eixo.annotate("", xy=(x2, y2), xytext=(x1, y1),
                          arrowprops={"arrowstyle": "->", "color": "#aab0b6", "lw": .55,
                                      "alpha": .45, "connectionstyle": "arc3,rad=0.08"}, zorder=1)
    palette = {"-": "#70a9d2", "a": "#efad52", "ab": "#77b979", "abc": "#b37cc5"}
    for nome in camadas:
        grupo = por_camada[nome]
        eixo.scatter([posicao[v][0] for v in grupo], [posicao[v][1] for v in grupo],
                     s=210, color=palette.get(nome, "#8e9ca8"), label=f"chaves {nome}", zorder=2)
        for v in grupo:
            eixo.text(*posicao[v], f"({v[0]},{v[1]})", ha="center", va="center", fontsize=6, zorder=3)
    eixo.scatter(*posicao[ALVO], s=250, marker="s", color="#d66c5c", label="ALVO", zorder=2)
    eixo.text(*posicao[ALVO], ALVO, ha="center", va="center", fontsize=7, color="white", zorder=3)
    for x, nome in enumerate(camadas):
        eixo.text(x * 3, 1.0, f"Camada {nome}", ha="center", va="bottom", fontweight="bold")
    eixo.set_title("Grafo de estados do m02 organizado por conjunto de chaves")
    eixo.legend(loc="upper center", bbox_to_anchor=(.5, -0.02), ncol=max(1, len(camadas) + 1))
    eixo.axis("off")
    figura.tight_layout()
    figura.savefig(caminho_png, dpi=180, bbox_inches="tight")
    plt.close(figura)

def gerar_figuras_parte1(pasta_saida="out/parte1"):
    from pathlib import Path
    pasta_saida = Path(pasta_saida)
    pasta_saida.mkdir(parents=True, exist_ok=True)
    for nome in ("m03_tres_chaves", "m08_grande"):
        caminho = Path("data/mapas") / f"{nome}.txt"
        resultado = resolver(caminho, "BELLMAN_FORD")
        if resultado["status"] != "OK":
            raise ValueError(f"Não foi possível gerar percurso para {nome}: {resultado['status']}")
        percurso_colorido(caminho, resultado, pasta_saida / f"percurso_{nome}.png")
    grafo_estados_camadas("data/mapas/m02_uma_chave.txt", pasta_saida / "grafo_estados_camadas_m02.png")


if __name__ == "__main__":
    gerar_figuras_parte1()
