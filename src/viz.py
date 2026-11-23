import csv
import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.colors import ListedColormap
from matplotlib.ticker import FuncFormatter

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
        camada = "" if keys == "-" else keys
        estados.append((linha, coluna, camada))
    figura, eixo = plt.subplots(figsize=(max(9, mapa.colunas * .28), max(5, mapa.linhas * .28)))
    eixo.set_facecolor("#252a2e")
    grade = [[0 if mapa.casa(r, c) == "#" else 1 for c in range(mapa.colunas)] for r in range(mapa.linhas)]
    eixo.imshow(grade, cmap=ListedColormap(["#30363b", "#f3f0e8"]), vmin=0, vmax=1)
    camadas_percurso = list(dict.fromkeys(k for _, _, k in estados))
    paleta = plt.get_cmap("tab20", max(1, len(camadas_percurso)))
    for indice, camada in enumerate(camadas_percurso):
        pontos = [(c, r) for r, c, k in estados if k == camada]
        if pontos:
            xs, ys = zip(*pontos)
            nome_camada = camada or "-"
            eixo.plot(xs, ys, color=paleta(indice), linewidth=3, marker="o", markersize=4,
                      label=f"chaves {nome_camada}", zorder=3)
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
    eixo.legend(loc="upper center", bbox_to_anchor=(.5, -0.08), ncol=min(5, max(1, len(camadas_percurso))))
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
        eixo.text(x * 3, 1.6, f"Camada {nome}", ha="center", va="bottom", fontweight="bold")
    eixo.set_title("Grafo de estados do m02 organizado por conjunto de chaves", pad=24)
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


# [IA] ChatGPT (Codex) – seleção e implementação das visualizações da Parte 2,
# após André informar autorização da professora. Textos analíticos gerados por IA
# ficam identificados como rascunhos para revisão, sem atribuição autoral ao aluno.
def distribuicao_graus_dataset(metricas, caminho_png):
    limites = [(0, 0), (1, 4), (5, 19), (20, 99), (100, 499), (500, None)]
    rotulos = ["0", "1–4", "5–19", "20–99", "100–499", "500 ou mais"]
    total = metricas["vertices"]
    contagens = {}
    figura, eixo = plt.subplots(figsize=(11.5, 6.6))
    # [IA] ChatGPT (Codex) – padrões distinguem as séries sem depender só da cor.
    for deslocamento, nome, campo, cor, padrao in (
        (-0.19, "Entrada", "graus_entrada", "#0072B2", "///"),
        (0.19, "Saída", "graus_saida", "#D55E00", ".."),
    ):
        graus = list(metricas[campo].values())
        contagem = [sum(g >= minimo and (maximo is None or g <= maximo) for g in graus)
                    for minimo, maximo in limites]
        assert len(graus) == total and sum(contagem) == total
        contagens[nome] = contagem
        percentuais = [100 * quantidade / total for quantidade in contagem]
        barras = eixo.bar([i + deslocamento for i in range(len(rotulos))], percentuais,
                          width=0.36, color=cor, label=nome, hatch=padrao,
                          edgecolor="#263238", linewidth=0.7)
        eixo.bar_label(barras, labels=[(f"{p:.2f}%" if p < 1 else f"{p:.1f}%").replace(".", ",") for p in percentuais],
                       padding=4, fontsize=9)
    eixo.set_title("Como se distribuem os graus dos usuários do Wiki-RfA?", loc="left", pad=22)
    eixo.set_xlabel("Grau — intervalos de quantidade de votos")
    eixo.set_ylabel("Usuários em cada intervalo (%)")
    eixo.set_xticks(range(len(rotulos)), rotulos)
    eixo.set_ylim(0, max(100 * max(v) / total for v in contagens.values()) * 1.22)
    eixo.legend(title="Direção do grau", frameon=False)
    eixo.grid(axis="y", alpha=0.18)
    eixo.set_axisbelow(True)
    total_formatado = f"{total:,}".replace(",", ".")
    figura.text(0.09, 0.03, f"Fonte: metricas_dataset.json • {total_formatado} usuários • Laços e arcos paralelos incluídos nos graus.", fontsize=9, color="#52606d")
    figura.subplots_adjust(left=0.09, right=0.98, bottom=0.17, top=0.86)
    figura.savefig(caminho_png, dpi=180)
    plt.close(figura)
    return {"intervalos": rotulos, "vertices": total, "contagens": contagens}


# [IA] ChatGPT (Codex) – gráfico das três versões, preservando os votos e pesos existentes.
def distribuicao_pesos_dataset(caminho_csv, caminho_png):
    import pandas as pd

    dados = pd.read_csv(caminho_csv, usecols=["VOTE", "PESO"])
    series = {"VOTE original": dados["VOTE"], "PESO ajustado": dados["PESO"],
              "PESO + 1 (Dijkstra)": dados["PESO"] + 1}
    valores = list(range(int(min(s.min() for s in series.values())),
                         int(max(s.max() for s in series.values())) + 1))
    contagens = {}
    figura, eixo = plt.subplots(figsize=(11.5, 6.6))
    # [IA] ChatGPT (Codex) – padrões redundantes às cores para distinguir as três versões.
    for deslocamento, (nome, serie), cor, padrao in zip(
        (-0.26, 0, 0.26), series.items(), ("#595959", "#0072B2", "#D55E00"),
        ("///", "xx", ".."),
    ):
        contagem = serie.value_counts().reindex(valores, fill_value=0)
        contagens[nome] = {str(v): int(contagem[v]) for v in valores}
        presentes = [v for v in valores if contagem[v] > 0]
        eixo.bar([valores.index(v) + deslocamento for v in presentes],
                 [contagem[v] for v in presentes], width=0.24, color=cor, label=nome,
                 hatch=padrao, edgecolor="#263238", linewidth=0.7)
    eixo.set_yscale("log")
    eixo.set_ylim(0.7, len(dados) * 5)
    eixo.yaxis.set_major_formatter(FuncFormatter(lambda valor, posicao: f"{int(valor):,}".replace(",", ".")))
    eixo.set_xticks(range(len(valores)), valores)
    eixo.set_xlabel("Valor inteiro na versão do peso")
    eixo.set_ylabel("Registros (escala logarítmica)")
    eixo.set_title("Do voto ao custo: três distribuições de valores", loc="left", pad=22)
    eixo.legend(frameon=False, loc="upper right")
    eixo.grid(axis="y", which="major", alpha=0.18)
    eixo.set_axisbelow(True)
    total_formatado = f"{len(dados):,}".replace(",", ".")
    figura.text(0.09, 0.05, f"Fonte: CSV tratado • {total_formatado} registros em cada versão • Valores sem ocorrências não têm barra.", fontsize=9, color="#52606d")
    figura.text(0.09, 0.025, "O eixo logarítmico permite observar também os valores raros; não mede diretamente diferenças absolutas de altura.", fontsize=8.5, color="#52606d")
    figura.subplots_adjust(left=0.09, right=0.98, bottom=0.19, top=0.86)
    figura.savefig(caminho_png, dpi=180)
    plt.close(figura)
    return {"registros": len(dados), "contagens": contagens,
            "valores_modificados_no_incremento": int(dados["VOTE"].ne(dados["PESO"]).sum())}


# [IA] ChatGPT (Codex) – comparação do benchmark no mesmo ambiente e na mesma fonte.
def tempos_dfs_bellman_dataset(relatorio, caminho_png):
    if not relatorio.get("completo"):
        raise ValueError("O benchmark precisa estar completo para gerar a comparação.")
    fonte = "Siva1979"
    selecionadas = {}
    for nome in ("DFS", "BELLMAN_FORD"):
        selecionadas[nome] = sorted(
            [m for m in relatorio["medicoes"] if m["algoritmo"] == nome and m["fonte"] == fonte],
            key=lambda m: m["percentual"],
        )
        if [m["percentual"] for m in selecionadas[nome]] != [10, 50, 100]:
            raise ValueError(f"Faltam configurações de {nome} para a fonte {fonte}.")
    for dfs_medicao, bellman_medicao in zip(selecionadas["DFS"], selecionadas["BELLMAN_FORD"]):
        assert (dfs_medicao["vertices"], dfs_medicao["arcos"]) == (bellman_medicao["vertices"], bellman_medicao["arcos"])
    razao = selecionadas["BELLMAN_FORD"][-1]["media"] / selecionadas["DFS"][-1]["media"]
    figura, eixo = plt.subplots(figsize=(11.5, 6.6))
    # [IA] ChatGPT (Codex) – linhas, marcadores e rótulos redundantes à cor.
    for nome, cor, rotulo, marcador, estilo in (
        ("DFS", "#0072B2", "DFS", "o", "-"),
        ("BELLMAN_FORD", "#D55E00", "Bellman-Ford", "s", "--"),
    ):
        medicoes = selecionadas[nome]
        medias = [m["media"] for m in medicoes]
        inferiores = [m["media"] - min(m["tempos"]) for m in medicoes]
        superiores = [max(m["tempos"]) - m["media"] for m in medicoes]
        eixo.errorbar([10, 50, 100], medias, yerr=[inferiores, superiores], color=cor,
                      marker=marcador, linestyle=estilo, linewidth=2.2,
                      capsize=5, markersize=7, label=rotulo)
        for percentual, media in zip((10, 50, 100), medias):
            texto = f"{media:.3f} s" if media < 1 else f"{media:.1f} s"
            texto = texto.replace(".", ",")
            if percentual == 100:
                texto = f"{rotulo} · {texto}"
            eixo.annotate(texto, (percentual, media),
                          xytext=(-5, 13) if percentual == 100 else (0, 13),
                          textcoords="offset points", ha="right" if percentual == 100 else "center",
                          color="#263238", fontsize=10)
    eixo.set_yscale("log")
    eixo.set_ylim(0.004, 3000)
    eixo.set_yticks([0.01, 0.1, 1, 10, 100, 1000], ["0,01", "0,1", "1", "10", "100", "1.000"])
    eixo.set_xlim(0, 110)
    eixo.set_xticks([10, 50, 100], ["10%\n19.661 arcos", "50%\n98.307 arcos", "100%\n196.614 arcos"])
    eixo.set_xlabel("Tamanho do recorte — percentual dos arcos, não dos vértices")
    eixo.set_ylabel("Tempo médio por execução (segundos, escala logarítmica)")
    eixo.set_title(f"Neste ambiente, Bellman-Ford levou cerca de {razao / 1000:.0f} mil vezes\no tempo do DFS no grafo completo", loc="left", pad=22)
    eixo.legend(frameon=False, loc="center right")
    eixo.grid(axis="y", which="major", alpha=0.18)
    eixo.set_axisbelow(True)
    figura.text(0.09, 0.05, "Fonte: benchmark_dfs_bellman.json • Siva1979 • 5 repetições + 1 aquecimento • Barras: mínimo e máximo.", fontsize=9, color="#52606d")
    figura.text(0.09, 0.025, "Mesmo ambiente; tarefas diferentes. A razão se refere a esta execução, sem garantia geral de desempenho.", fontsize=8.5, color="#52606d")
    figura.subplots_adjust(left=0.09, right=0.98, bottom=0.22, top=0.80)
    figura.savefig(caminho_png, dpi=180)
    plt.close(figura)
    return {"fonte": fonte, "razao_tempos_100_porcento": razao, "medicoes": selecionadas,
            "ambiente": relatorio["ambiente"]}


# [IA] ChatGPT (Codex) – geração reproduzível das três figuras e dos dados para conferência.
def gerar_figuras_parte2(pasta_saida="out/parte2"):
    pasta_saida = Path(pasta_saida)
    pasta_saida.mkdir(parents=True, exist_ok=True)
    pasta_dados = Path("out/parte2")
    metricas = json.loads((pasta_dados / "metricas_dataset.json").read_text(encoding="utf-8"))
    benchmark = json.loads((pasta_dados / "benchmark_dfs_bellman.json").read_text(encoding="utf-8"))
    with plt.rc_context({"font.family": "DejaVu Sans", "font.size": 10,
                         "axes.spines.top": False, "axes.spines.right": False,
                         "axes.titleweight": "bold", "figure.facecolor": "white"}):
        dados = {
            "graus": distribuicao_graus_dataset(metricas, pasta_saida / "andre_01_distribuicao_graus.png"),
            "pesos": distribuicao_pesos_dataset("data/dataset_parte2/processed/wikiRfA_tratado.csv",
                                               pasta_saida / "andre_02_distribuicao_pesos.png"),
            "tempos": tempos_dfs_bellman_dataset(benchmark, pasta_saida / "andre_03_tempos_dfs_bellman.png"),
        }
    (pasta_saida / "dados_visualizacoes_andre.json").write_text(
        json.dumps(dados, ensure_ascii=False, indent=2, allow_nan=False), encoding="utf-8"
    )
    return dados


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gera as figuras do projeto.")
    parser.add_argument("--parte2", action="store_true", help="gera as três visualizações de André da Parte 2")
    parser.add_argument("--out", help="pasta das imagens")
    argumentos = parser.parse_args()
    if argumentos.parte2:
        gerar_figuras_parte2(argumentos.out or "out/parte2")
    else:
        gerar_figuras_parte1(argumentos.out or "out/parte1")
