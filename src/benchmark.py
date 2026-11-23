import random
from statistics import mean, median, stdev
from time import perf_counter

from src.graphs.graph import adicionar_arco


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
def medir_algoritmo(algoritmo, grafo, fonte, repeticoes=5):
    """Mede chamadas algoritmo(grafo, fonte), sem preparar ou exportar dados.

    Faz um aquecimento sem cronômetro e pelo menos cinco repetições medidas.
    O algoritmo deve preservar o grafo. Erros são propagados, sem gerar
    estatísticas parciais. O desvio padrão é amostral; tempos são em segundos.
    """
    if not isinstance(repeticoes, int) or repeticoes < 5:
        raise ValueError("Use um número inteiro de pelo menos 5 repetições.")
    if fonte not in grafo:
        raise ValueError("A fonte deve estar presente no grafo.")

    resultado = algoritmo(grafo, fonte)
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
    }
