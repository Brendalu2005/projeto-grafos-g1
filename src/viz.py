import csv
import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
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
        arquivo_percurso = pasta_saida / f"percurso_{nome}.png"
        percurso_colorido(caminho, resultado, arquivo_percurso)
        # [IA] ChatGPT (Codex) – nome exigido no enunciado, preservando o arquivo usado pelo front.
        (pasta_saida / f"percurso_{nome.split('_')[0]}.png").write_bytes(arquivo_percurso.read_bytes())
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
    # [IA] ChatGPT (Codex) – paleta solicitada, com preenchimentos sólidos.
    for deslocamento, nome, campo, cor in (
        (-0.19, "Entrada", "graus_entrada", "#0081CF"),
        (0.19, "Saída", "graus_saida", "#8C1F4E"),
    ):
        graus = list(metricas[campo].values())
        contagem = [sum(g >= minimo and (maximo is None or g <= maximo) for g in graus)
                    for minimo, maximo in limites]
        assert len(graus) == total and sum(contagem) == total
        contagens[nome] = contagem
        percentuais = [100 * quantidade / total for quantidade in contagem]
        barras = eixo.bar([i + deslocamento for i in range(len(rotulos))], percentuais,
                          width=0.36, color=cor, label=nome,
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
    # [IA] ChatGPT (Codex) – três cores solicitadas, sem hachuras.
    for deslocamento, (nome, serie), cor in zip(
        (-0.26, 0, 0.26), series.items(), ("#3E4756", "#0081CF", "#8C1F4E"),
    ):
        contagem = serie.value_counts().reindex(valores, fill_value=0)
        contagens[nome] = {str(v): int(contagem[v]) for v in valores}
        presentes = [v for v in valores if contagem[v] > 0]
        eixo.bar([valores.index(v) + deslocamento for v in presentes],
                 [contagem[v] for v in presentes], width=0.24, color=cor, label=nome,
                 edgecolor="#263238", linewidth=0.7)
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
        ("DFS", "#0081CF", "DFS", "o", "-"),
        ("BELLMAN_FORD", "#8C1F4E", "Bellman-Ford", "s", "--"),
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


# [IA] ChatGPT (Codex) – inclui a análise de RESULT na geração das figuras da Parte 2. !andre!
def gerar_figuras_parte2(pasta_saida="out/parte2"):
    pasta_saida = Path(pasta_saida)
    pasta_saida.mkdir(parents=True, exist_ok=True)
    # [IA] ChatGPT (Codex) – entradas independentes da pasta de execução do notebook.
    raiz_projeto = Path(__file__).resolve().parents[1]
    pasta_dados = raiz_projeto / "out" / "parte2"
    csv_tratado = raiz_projeto / "data/dataset_parte2/processed/wikiRfA_tratado.csv"
    csv_bruto = raiz_projeto / "data/dataset_parte2/raw/wikiRfA.csv"
    metricas = json.loads((pasta_dados / "metricas_dataset.json").read_text(encoding="utf-8"))
    benchmark = json.loads((pasta_dados / "benchmark_dfs_bellman.json").read_text(encoding="utf-8"))
    with plt.rc_context({"font.family": "DejaVu Sans", "font.size": 10,
                         "axes.spines.top": False, "axes.spines.right": False,
                         "axes.titleweight": "bold", "figure.facecolor": "white"}):
        dados = {
            "graus": distribuicao_graus_dataset(metricas, pasta_saida / "andre_01_distribuicao_graus.png"),
            "pesos": distribuicao_pesos_dataset(csv_tratado,
                                               pasta_saida / "andre_02_distribuicao_pesos.png"),
            "tempos": tempos_dfs_bellman_dataset(benchmark, pasta_saida / "andre_03_tempos_dfs_bellman.png"),
            "result": atributos_por_result_dataset(csv_tratado,
                                                   pasta_saida / "andre_04_atributos_result.png"),
        }
        faltantes_por_faixa(csv_bruto,
                           pasta_saida / "brenda_01_faltantes_por_faixa.png")
        tempo_bfs_dijkstra(pasta_dados / "benchmark_bfs_dijkstra_mesmo_ambiente.json",
                           pasta_saida / "brenda_02_tempos_bfs_dijkstra.png")
        efeito_transformacao(pasta_dados / "estudo_transformacao.json",
                             pasta_saida / "brenda_03_efeito_transformacao.png")
    (pasta_saida / "dados_visualizacoes_andre.json").write_text(
        json.dumps(dados, ensure_ascii=False, indent=2, allow_nan=False), encoding="utf-8", newline="\n"
    )
    return dados


# [IA] ChatGPT (Codex) – desenho da comparação por fonte escolhida pelo grupo; sem interpretação dos resultados.
def tempo_bfs_dijkstra(caminho_json, caminho_png):
    """Desenha três painéis com médias e intervalos mínimo–máximo em segundos."""
    with open(caminho_json, encoding="utf-8") as arquivo:
        relatorio = json.load(arquivo)

    fontes = relatorio["fontes"]
    if len(fontes) != 3:
        raise ValueError("A figura espera três fontes.")

    figura, eixos = plt.subplots(1, 3, figsize=(15, 6), sharex=True, sharey=True)
    percentuais = [10, 50, 100]
    estilos = [("BFS", "#0081CF", "o", "-"), ("DIJKSTRA", "#8C1F4E", "s", "--")]

    for eixo, fonte in zip(eixos, fontes):
        for algoritmo, cor, marcador, linha in estilos:
            medias = []
            erros_inferiores = []
            erros_superiores = []
            for percentual in percentuais:
                registros = []
                for medicao in relatorio["medicoes"]:
                    if (medicao["algoritmo"] == algoritmo
                            and medicao["fonte"] == fonte
                            and medicao["percentual"] == percentual):
                        registros.append(medicao)
                if len(registros) != 1:
                    raise ValueError(f"Configuração ausente ou duplicada: {algoritmo}, {fonte}, {percentual}%.")
                medicao = registros[0]
                media = medicao["media"]
                medias.append(media)
                erros_inferiores.append(media - min(medicao["tempos"]))
                erros_superiores.append(max(medicao["tempos"]) - media)

            eixo.errorbar(percentuais, medias,
                          yerr=[erros_inferiores, erros_superiores],
                          color=cor, marker=marcador, linestyle=linha, label=algoritmo,
                          linewidth=2.2, capsize=5, markersize=7)

        # [IA] ChatGPT (Codex) – rótulos simplificados conforme solicitação de Brenda.
        eixo.set_xticks(percentuais, [f"{percentual}%" for percentual in percentuais])
        eixo.set_title(fonte, fontsize=12, fontweight="bold")
        eixo.set_xlabel("Recorte por quantidade de arcos", labelpad=10)
        eixo.grid(axis="y", alpha=0.18)
        eixo.set_axisbelow(True)
        eixo.spines[["top", "right"]].set_visible(False)

    maior_tempo = max(max(medicao["tempos"]) for medicao in relatorio["medicoes"])
    eixos[0].set_ylim(0, maior_tempo * 1.15)
    eixos[0].set_ylabel("Tempo médio por execução (segundos)")
    eixos[0].yaxis.set_major_formatter(FuncFormatter(lambda valor, posicao: f"{valor:.2f}".replace(".", ",")))
    eixos[-1].legend(title="Algoritmo", frameon=False)
    figura.suptitle("Tempo de BFS e Dijkstra por tamanho do grafo e fonte", x=0.07, ha="left",
                   fontsize=15, fontweight="bold")
    ambiente = relatorio["ambiente"]
    figura.text(0.07, 0.07,
                f"Fonte: {Path(caminho_json).name} • 5 repetições + 1 aquecimento • Barras: mínimo e máximo.",
                fontsize=9, color="#52606d")
    figura.text(0.07, 0.03,
                f"Mesmo ambiente: Python {ambiente['python']} · {ambiente['processador']} · BFS: PESO; Dijkstra: PESO + 1. Escala vertical comum e linear.",
                fontsize=9, color="#52606d")
    figura.tight_layout(rect=(0, 0.13, 1, 0.94))
    caminho_png = Path(caminho_png)
    caminho_png.parent.mkdir(parents=True, exist_ok=True)
    figura.savefig(caminho_png, dpi=180, bbox_inches="tight")
    plt.close(figura)


# [IA] ChatGPT (Codex) – barras 100% empilhadas conforme alteração solicitada por Brenda.
def faltantes_por_faixa(caminho_csv, caminho_png):
    """Mostra a composição dos votos com e sem SOURCE em cada faixa."""
    dados = pd.read_csv(caminho_csv, index_col=0)
    candidatos = dados.groupby("TARGET").size().rename("votos").to_frame()
    candidatos["sem_source"] = dados["SOURCE"].isna().groupby(dados["TARGET"]).sum()
    rotulos = ["1–4", "5–19", "20–99", "100–499", "500 ou mais"]
    candidatos["faixa"] = pd.cut(
        candidatos["votos"], bins=[0, 4, 19, 99, 499, float("inf")], labels=rotulos
    )
    resumo = candidatos.groupby("faixa", observed=False).agg(
        candidatos=("votos", "size"),
        votos=("votos", "sum"),
        sem_source=("sem_source", "sum"),
    )
    # Faixas vazias ficam sem percentual, em vez de serem apresentadas como 0%.
    denominador = resumo["votos"].replace(0, float("nan"))
    resumo["percentual_sem_source"] = 100 * resumo["sem_source"] / denominador

    figura, eixo = plt.subplots(figsize=(12, 7))
    percentuais = resumo["percentual_sem_source"]
    com_source = 100 - percentuais
    eixo.bar(range(5), com_source, color="#0081CF", width=0.65,
             label="Com SOURCE", edgecolor="#263238", linewidth=0.7)
    eixo.bar(range(5), percentuais, bottom=com_source, color="#8C1F4E", width=0.65,
             label="Sem SOURCE", edgecolor="#263238", linewidth=0.7)
    eixo.set_ylim(0, 100)

    etiquetas = []
    for posicao, (faixa, grupo) in enumerate(resumo.iterrows()):
        quantidade_votos = f"{int(grupo['votos']):,}".replace(",", ".")
        etiquetas.append(f"{faixa}\n{quantidade_votos} votos")
        percentual = grupo["percentual_sem_source"]
        if pd.isna(percentual):
            texto = "Sem dados"
            altura = 0
        else:
            quantidade_sem_source = f"{int(grupo['sem_source']):,}".replace(",", ".")
            percentual_formatado = f"{percentual:.2f}%".replace(".", ",")
            texto = f"{quantidade_sem_source} sem SOURCE\n{percentual_formatado}"
            altura = 100
        eixo.annotate(texto, (posicao, altura), xytext=(0, 7),
                      textcoords="offset points", ha="center", fontsize=11, color="#263238")

    eixo.set_xticks(range(5), etiquetas)
    eixo.set_xlabel("Faixa do total de votos recebidos por candidato (antes do tratamento)", labelpad=14)
    eixo.set_ylabel("Proporção do total de votos da faixa (%)")
    eixo.yaxis.set_major_formatter(FuncFormatter(lambda valor, posicao: f"{valor:.1f}%".replace(".", ",")))
    eixo.set_title("Votos sem origem identificada por faixa de votos recebidos", fontsize=15,
                   fontweight="bold", loc="left", pad=60)
    figura.legend(*eixo.get_legend_handles_labels(), loc="upper left",
                   bbox_to_anchor=(0.09, 0.89), ncol=2, frameon=False)
    eixo.grid(axis="y", alpha=0.18)
    eixo.set_axisbelow(True)
    eixo.spines[["top", "right"]].set_visible(False)
    figura.text(0.09, 0.07,
                "Fonte: wikiRfA.csv original • Todos os candidatos com TARGET identificado; nenhum limite mínimo adicional.",
                fontsize=9, color="#52606d")
    figura.text(0.09, 0.03,
                "Cada barra representa 100% dos votos da faixa. Com SOURCE + sem SOURCE = total; os rótulos destacam os votos sem SOURCE.",
                fontsize=9, color="#52606d")
    figura.subplots_adjust(left=0.09, right=0.98, bottom=0.24, top=0.78)
    caminho_png = Path(caminho_png)
    caminho_png.parent.mkdir(parents=True, exist_ok=True)
    figura.savefig(caminho_png, dpi=180, bbox_inches="tight")
    plt.close(figura)
    return resumo


# [IA] ChatGPT (Codex) – barras de custos do estudo de caso, conforme forma aprovada.
def efeito_transformacao(caminho_json, caminho_png):
    """Compara os custos salvos dos dois caminhos em PESO e PESO + 1."""
    with open(caminho_json, encoding="utf-8") as arquivo:
        estudo = json.load(arquivo)
    alternativas = estudo["alternativas"]
    if estudo["tem_ciclo_negativo"] or len(alternativas) != 2:
        raise ValueError("A figura espera dois caminhos de um caso sem ciclo negativo.")

    # [IA] ChatGPT (Codex) – identifica os algoritmos e exibe os pesos por arco conforme solicitado.
    figura, (eixo, eixo_tabela) = plt.subplots(
        1, 2, figsize=(15, 8), gridspec_kw={"width_ratios": [1.8, 1.2]}
    )
    estilos = [("custo_peso", "Antes: PESO", "#0081CF", -0.18),
               ("custo_transformado", "Depois: PESO + 1", "#8C1F4E", 0.18)]
    for campo, nome, cor, deslocamento in estilos:
        custos = [alternativa[campo] for alternativa in alternativas]
        posicoes = [posicao + deslocamento for posicao in range(2)]
        barras = eixo.bar(posicoes, custos, width=0.36, label=nome, color=cor,
                          edgecolor="#263238", linewidth=0.7)
        eixo.bar_label(barras, labels=[str(custo) for custo in custos], padding=6, fontsize=12)

    rotulos = []
    for alternativa in alternativas:
        caminho = alternativa["caminho"]
        quantidade = len(caminho) - 1
        arcos = "1 arco" if quantidade == 1 else f"{quantidade} arcos"
        algoritmos = []
        if caminho == estudo["caminho_bellman_ford"]:
            algoritmos.append("Bellman-Ford (PESO)")
        if caminho == estudo["caminho_dijkstra"]:
            algoritmos.append("Dijkstra (PESO + 1)")
        rotulos.append(f"Retornado por {' e '.join(algoritmos)}\n{' → '.join(caminho)}\n({arcos})")
    maior_custo = max(alternativa[campo] for alternativa in alternativas
                      for campo in ("custo_peso", "custo_transformado"))
    eixo.set_xticks(range(2), rotulos, fontsize=9)
    eixo.set_ylim(0, max(1, maior_custo) * 1.4)
    eixo.set_yticks(range(int(maior_custo) + 1))
    eixo.set_ylabel("Custo do caminho (soma dos pesos)")
    eixo.set_title("Custo de cada caminho nas duas versões", fontsize=12, loc="left", pad=20)
    eixo.grid(axis="y", alpha=0.18)
    eixo.set_axisbelow(True)
    eixo.legend(title="Versão dos pesos", frameon=False)

    eixo_tabela.axis("off")
    eixo_tabela.set_title("Pesos dos arcos do subgrafo", fontsize=12, loc="left", pad=20)
    linhas_tabela = [[arco["origem"], arco["destino"], arco["PESO"], arco["PESO"] + 1]
                     for arco in estudo["arcos"]]
    tabela = eixo_tabela.table(
        cellText=linhas_tabela, colLabels=["Origem", "Destino", "PESO", "PESO + 1"],
        colWidths=[0.31, 0.29, 0.18, 0.22], loc="center", cellLoc="center",
    )
    tabela.auto_set_font_size(False)
    tabela.set_fontsize(10)
    tabela.scale(1, 2)
    for (linha, coluna), celula in tabela.get_celld().items():
        celula.set_edgecolor("#d8dce2")
        if linha == 0:
            celula.set_facecolor("#3E4756")
            celula.set_text_props(color="white", weight="bold")
    eixo_tabela.text(0, 0.22, "Cada linha representa um arco dirigido.\nO acréscimo de +1 é aplicado a cada arco,\nantes da execução do Dijkstra.",
                     transform=eixo_tabela.transAxes, fontsize=10, color="#3E4756", va="top")
    figura.suptitle("Bellman-Ford e Dijkstra: efeito de somar 1 a cada arco",
                    x=0.07, ha="left", fontsize=16, fontweight="bold", y=0.97)
    figura.text(0.07, 0.14,
                "Bellman-Ford usa PESO e retorna o caminho por 9cds: custo −1 + 1 = 0. Dijkstra usa PESO + 1 e retorna o direto: custo 2.",
                fontsize=10, color="#263238")
    figura.text(0.07, 0.10,
                "Após somar 1 por arco, os dois caminhos empatam em 2. O direto foi retornado no desempate; em PESO, ele custa 1.",
                fontsize=10, color="#263238")
    figura.text(0.07, 0.055,
                "Fonte: estudo_transformacao.json • Subgrafo de três usuários, sem ciclo negativo; exemplo selecionado.",
                fontsize=9, color="#52606d")
    figura.text(0.07, 0.025,
                "Este caso ilustra uma mudança no caminho retornado e não estima a frequência de mudanças na rede.",
                fontsize=9, color="#52606d")
    figura.subplots_adjust(left=0.07, right=0.98, bottom=0.31, top=0.85, wspace=0.24)
    caminho_png = Path(caminho_png)
    caminho_png.parent.mkdir(parents=True, exist_ok=True)
    figura.savefig(caminho_png, dpi=180, bbox_inches="tight")
    plt.close(figura)


# [IA] ChatGPT (Codex) – compara distribuições por RESULT usando registros, sem agregar eleições por usuário. !andre!
def atributos_por_result_dataset(caminho_csv, caminho_png):
    dados = pd.read_csv(caminho_csv)
    if dados.empty or not dados["RESULT"].isin([-1, 1]).all():
        raise ValueError("RESULT deve conter somente -1 e 1, com registros nos dois grupos.")
    totais = dados["RESULT"].value_counts().reindex([-1, 1], fill_value=0)
    if (totais == 0).any():
        raise ValueError("São necessários registros dos dois resultados.")
    grau_entrada = dados["TARGET"].value_counts()
    dados["Votos recebidos por TARGET"] = pd.cut(
        dados["TARGET"].map(grau_entrada), bins=[0, 4, 19, 99, 499, float("inf")],
        labels=["1–4", "5–19", "20–99", "100–499", "500+"],
    )
    dados["PESO agrupado"] = dados["PESO"].map(lambda p: str(p) if p < 2 else "2 ou mais")
    paineis = [("VOTE", [-1, 0, 1], ["Contrário\n−1", "Neutro\n0", "Favorável\n1"]),
              ("PESO agrupado", ["-1", "0", "1", "2 ou mais"], ["−1", "0", "1", "2 ou mais"]),
              ("Votos recebidos por TARGET", ["1–4", "5–19", "20–99", "100–499", "500+"],
               ["1–4", "5–19", "20–99", "100–499", "500+"])]
    resumo = {"unidade": "registro de voto", "total_registros": len(dados),
              "registros_por_result": {str(r): int(totais[r]) for r in (-1, 1)},
              "targets_com_result_distinto": int((dados.groupby("TARGET")["RESULT"].nunique() > 1).sum()),
              "distribuicoes": {}}
    figura, eixos = plt.subplots(1, 3, figsize=(15, 6.5), sharey=True)
    for eixo, (campo, categorias, rotulos) in zip(eixos, paineis):
        resumo["distribuicoes"][campo] = {}
        for resultado, cor, deslocamento, nome in (
            (-1, "#0081CF", -0.19, "RESULT −1 · rejeição"),
            (1, "#8C1F4E", 0.19, "RESULT 1 · aprovação"),
        ):
            contagem = dados.loc[dados["RESULT"] == resultado, campo].value_counts().reindex(categorias, fill_value=0)
            percentuais = [100 * int(n) / int(totais[resultado]) for n in contagem]
            resumo["distribuicoes"][campo][str(resultado)] = {
                str(c): {"registros": int(n), "percentual": p}
                for c, n, p in zip(categorias, contagem, percentuais)}
            barras = eixo.bar([i + deslocamento for i in range(len(categorias))], percentuais,
                              width=0.36, color=cor, edgecolor="#263238",
                              linewidth=0.7, label=nome)
            eixo.bar_label(barras, labels=[f"{p:.1f}%".replace(".", ",") for p in percentuais],
                           padding=4, fontsize=8)
        eixo.set_xticks(range(len(categorias)), rotulos)
        eixo.set_title(campo.replace(" agrupado", ""), fontsize=12, fontweight="bold")
        eixo.set_ylim(0, 105)
        eixo.grid(axis="y", alpha=0.18)
        eixo.set_axisbelow(True)
        eixo.spines[["top", "right"]].set_visible(False)
    eixos[0].set_ylabel("Registros dentro de cada grupo de RESULT (%)")
    handles, labels = eixos[0].get_legend_handles_labels()
    figura.legend(handles, labels, loc="upper center", bbox_to_anchor=(0.5, 0.89), ncol=2, frameon=False)
    figura.suptitle("Votos, pesos e volume recebido por resultado da candidatura", fontsize=15, fontweight="bold", y=0.98)
    figura.text(0.07, 0.11,
                f"Fonte: CSV tratado • {int(totais[-1]):,} registros de rejeição e {int(totais[1]):,} de aprovação. Percentuais normalizados por grupo.".replace(",", "."),
                fontsize=9, color="#263238")
    figura.text(0.07, 0.065, "Volume recebido: todas as ocorrências por TARGET, incluindo paralelos. A distribuição é ponderada pelos registros de votos.", fontsize=9, color="#263238")
    figura.text(0.07, 0.02, "Um TARGET pode aparecer com resultados diferentes; os dados tratados não identificam eleições individuais. Associação não implica causalidade.", fontsize=9, color="#263238")
    figura.subplots_adjust(left=0.07, right=0.98, top=0.78, bottom=0.24, wspace=0.14)
    caminho_png = Path(caminho_png)
    caminho_png.parent.mkdir(parents=True, exist_ok=True)
    figura.savefig(caminho_png, dpi=180, bbox_inches="tight")
    plt.close(figura)
    return resumo


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gera as figuras do projeto.")
    # [IA] ChatGPT (Codex) – mantém a ajuda consistente com a inclusão da figura de RESULT. !andre!
    parser.add_argument("--parte2", action="store_true", help="gera as visualizações implementadas da Parte 2")
    parser.add_argument("--out", help="pasta das imagens")
    argumentos = parser.parse_args()
    if argumentos.parte2:
        gerar_figuras_parte2(argumentos.out or "out/parte2")
    else:
        gerar_figuras_parte1(argumentos.out or "out/parte1")
