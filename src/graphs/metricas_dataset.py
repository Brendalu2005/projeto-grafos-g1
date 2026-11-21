from collections import Counter


# [IA] ChatGPT (Codex) – implementação das convenções de métricas aprovadas por Brenda.
def calcular_metricas_dataset(grafo):
    """Recebe {usuario: [(destino, peso), ...]} e devolve as métricas.

    Todo destino deve também ser uma chave, como garante carregar_dataset.
    Arcos paralelos contam individualmente nos graus; laços contam uma vez
    em cada direção. A densidade usa pares distintos sem laço.

    percentual_peso_negativo descreve os pesos recebidos, em porcentagem.
    Não calcula percentual_vote_negativo: o voto original não está disponível
    quando o grafo foi carregado com pesos ajustados.

    Sem vértices, mínimos e máximos são None e médias são zero. Sem arcos,
    o percentual de pesos negativos é None. Densidade é zero para |V| < 2.
    """
    vertices = len(grafo)
    graus_entrada = dict.fromkeys(grafo, 0)
    graus_saida = {}
    vizinhos_entrada = dict.fromkeys(grafo, 0)
    vizinhos_saida = {}
    quantidade_arcos = 0
    lacos = 0
    pares_distintos = 0
    pares_sem_laco = 0
    pesos_negativos = 0

    for origem, arcos in grafo.items():
        graus_saida[origem] = len(arcos)
        quantidade_arcos += len(arcos)
        destinos_distintos = set()

        for destino, peso in arcos:
            graus_entrada[destino] += 1
            destinos_distintos.add(destino)
            if origem == destino:
                lacos += 1
            if peso < 0:
                pesos_negativos += 1

        vizinhos_saida[origem] = len(destinos_distintos)
        pares_distintos += len(destinos_distintos)
        for destino in destinos_distintos:
            vizinhos_entrada[destino] += 1
            if destino != origem:
                pares_sem_laco += 1

    if vertices > 1:
        densidade = pares_sem_laco / (vertices * (vertices - 1))
    else:
        densidade = 0

    if quantidade_arcos > 0:
        percentual_negativo = 100 * pesos_negativos / quantidade_arcos
    else:
        percentual_negativo = None

    def resumir(graus):
        if vertices == 0:
            return {"minimo": None, "maximo": None, "media": 0}

        return {
            "minimo": min(graus.values()),
            "maximo": max(graus.values()),
            "media": sum(graus.values()) / vertices,
        }

    return {
        "vertices": vertices,
        "arcos": quantidade_arcos,
        "lacos": lacos,
        "pares_distintos": pares_distintos,
        "pares_distintos_sem_laco": pares_sem_laco,
        "densidade_pares_sem_laco": densidade,
        "graus_entrada": graus_entrada,
        "graus_saida": graus_saida,
        "resumo_entrada": resumir(graus_entrada),
        "resumo_saida": resumir(graus_saida),
        "distribuicao_entrada": dict(Counter(graus_entrada.values())),
        "distribuicao_saida": dict(Counter(graus_saida.values())),
        "vizinhos_distintos_entrada": vizinhos_entrada,
        "vizinhos_distintos_saida": vizinhos_saida,
        "percentual_peso_negativo": percentual_negativo,
    }
