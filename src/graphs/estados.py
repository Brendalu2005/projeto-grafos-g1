from src.graphs.graph import adicionar_arco, adicionar_vertice, arcos

ALVO = "ALVO"

DIRECOES = [("N", -1, 0), ("L", 0, 1), ("S", 1, 0), ("O", 0, -1)]
ESTEIRAS = {"^": "N", ">": "L", "v": "S", "<": "O"}
CUSTO = {",": 3, "~": 5, "*": -2}


def estado_inicial(mapa):
    linha, coluna = mapa.inicio
    return (linha, coluna, frozenset(), frozenset())


def rotulo(estado):
    if estado == ALVO:
        return ALVO
    linha, coluna, chaves, bonus = estado

    texto_chaves = "".join(sorted(chaves))
    if texto_chaves == "":
        texto_chaves = "-"

    numeros = []
    for numero in sorted(bonus):
        numeros.append(str(numero))
    texto_bonus = "{" + ",".join(numeros) + "}"

    return f"({linha},{coluna})|{texto_chaves}|{texto_bonus}"


def nome_do_movimento(origem, destino):
    for movimento, dl, dc in DIRECOES:
        if origem[0] + dl == destino[0] and origem[1] + dc == destino[1]:
            return movimento


def movimentos(mapa, estado, fonte_consumivel=False):
    linha, coluna, chaves, bonus = estado
    casa_atual = mapa.casa(linha, coluna)
    resultado = []

    for movimento, dl, dc in DIRECOES:
        if casa_atual in ESTEIRAS and ESTEIRAS[casa_atual] != movimento:
            continue

        nova_linha, nova_coluna = linha + dl, coluna + dc
        if not mapa.dentro(nova_linha, nova_coluna):
            continue
        destino = mapa.casa(nova_linha, nova_coluna)
        if destino == "#":
            continue
        if destino in "ABCD" and destino.lower() not in chaves:
            continue

        peso = CUSTO.get(destino, 1)
        novas_chaves = chaves
        novos_bonus = bonus
        if destino in "abcd":
            novas_chaves = chaves | {destino}
        if destino == "+":
            numero = mapa.bonus[(nova_linha, nova_coluna)]
            if numero not in bonus:
                peso = -4
                novos_bonus = bonus | {numero}
        if destino == "*" and fonte_consumivel:
            numero = mapa.fontes[(nova_linha, nova_coluna)]
            if numero in bonus:
                peso = 1
            else:
                novos_bonus = bonus | {numero}

        proximo = (nova_linha, nova_coluna, novas_chaves, novos_bonus)
        resultado.append((proximo, peso))

    return resultado


def construir_g_est(mapa, fonte_consumivel=False):
    inicial = estado_inicial(mapa)
    grafo = {ALVO: [], inicial: []}
    visitados = {inicial}
    fila = [inicial]

    while len(fila) > 0:
        atual = fila.pop(0)

        if mapa.casa(atual[0], atual[1]) == "G":
            adicionar_arco(grafo, atual, ALVO, 0)
            continue

        for proximo, peso in movimentos(mapa, atual, fonte_consumivel):
            adicionar_arco(grafo, atual, proximo, peso)
            if proximo not in visitados:
                visitados.add(proximo)
                fila.append(proximo)

    return grafo


def construir_g_pos(mapa, porta="chao"):
    grafo = {ALVO: []}

    for linha in range(mapa.linhas):
        for coluna in range(mapa.colunas):
            casa = mapa.casa(linha, coluna)
            if casa == "#" or (porta == "parede" and casa in "ABCD"):
                continue
            adicionar_vertice(grafo, (linha, coluna))

            if casa == "G":
                adicionar_arco(grafo, (linha, coluna), ALVO, 0)
                continue

            for movimento, dl, dc in DIRECOES:
                if casa in ESTEIRAS and ESTEIRAS[casa] != movimento:
                    continue
                nova_linha, nova_coluna = linha + dl, coluna + dc
                if not mapa.dentro(nova_linha, nova_coluna):
                    continue
                destino = mapa.casa(nova_linha, nova_coluna)
                if destino == "#" or (porta == "parede" and destino in "ABCD"):
                    continue

                peso = CUSTO.get(destino, 1)
                if destino == "+":
                    peso = -4
                adicionar_arco(grafo, (linha, coluna), (nova_linha, nova_coluna), peso)

    return grafo


def sem_alvo(grafo):
    vertices = []
    for v in grafo:
        if v != ALVO:
            vertices.append(v)
    lista = []
    for origem, destino, peso in arcos(grafo):
        if destino != ALVO:
            lista.append((origem, destino))
    return vertices, lista


def densidade(ordem, tamanho):
    if ordem < 2:
        return 0
    return tamanho / (ordem * (ordem - 1))


def resumo(grafo):
    vertices, lista = sem_alvo(grafo)
    return {"ordem": len(vertices), "tamanho": len(lista),
            "densidade": densidade(len(vertices), len(lista))}


def graus(vertices, lista):
    entrada = {}
    saida = {}
    for v in vertices:
        entrada[v] = 0
        saida[v] = 0
    for origem, destino in lista:
        saida[origem] += 1
        entrada[destino] += 1
    return entrada, saida


def ordem_de_leitura(estado):
    linha, coluna, chaves, bonus = estado
    return (linha, coluna, "".join(sorted(chaves)), sorted(bonus))


def maior_grau(grau, vertices):
    ordenados = sorted(vertices, key=ordem_de_leitura)
    melhor = ordenados[0]
    for v in ordenados:
        if grau[v] > grau[melhor]:
            melhor = v
    return {"estado": rotulo(melhor), "grau": grau[melhor]}


def camada(estado):
    texto = "".join(sorted(estado[2]))
    if texto == "":
        return "-"
    return texto


def metricas_do_mapa(mapa, g_pos, g_est):
    vertices, lista = sem_alvo(g_est)
    entrada, saida = graus(vertices, lista)

    casas_livres = 0
    chaves = set()
    for linha in mapa.grade:
        for simbolo in linha:
            if simbolo != "#":
                casas_livres += 1
            if simbolo in "abcd":
                chaves.add(simbolo)
    teto = casas_livres * 2 ** len(chaves) * 2 ** len(mapa.bonus)

    becos = []
    for v in vertices:
        if saida[v] == 0 and mapa.casa(v[0], v[1]) != "G":
            becos.append(rotulo(v))

    multiplicidade = {}
    for v in vertices:
        casa = (v[0], v[1])
        multiplicidade[casa] = multiplicidade.get(casa, 0) + 1
    maximo = max(multiplicidade.values())
    casas_maximo = []
    for casa in sorted(multiplicidade):
        if multiplicidade[casa] == maximo:
            casas_maximo.append(f"({casa[0]},{casa[1]})")

    return {
        "mapa": mapa.nome,
        "G_pos": resumo(g_pos),
        "G_est": resumo(g_est),
        "teto_teorico": teto,
        "taxa_ocupacao": len(vertices) / teto,
        "maior_grau_saida": maior_grau(saida, vertices),
        "maior_grau_entrada": maior_grau(entrada, vertices),
        "becos": becos,
        "multiplicidade_maxima": maximo,
        "casas_com_multiplicidade_maxima": casas_maximo,
    }


def camadas_do_mapa(mapa, g_est):
    vertices, lista = sem_alvo(g_est)

    por_camada = {}
    for v in vertices:
        if camada(v) not in por_camada:
            por_camada[camada(v)] = [0, 0]
        por_camada[camada(v)][0] += 1

    entre_camadas = 0
    casas = set()
    for origem, destino in lista:
        if camada(origem) == camada(destino):
            por_camada[camada(origem)][1] += 1
        else:
            entre_camadas += 1
            casas.add((destino[0], destino[1], mapa.casa(destino[0], destino[1])))

    casas_texto = []
    for linha, coluna, simbolo in sorted(casas):
        casas_texto.append(f"({linha},{coluna}) {simbolo}")

    camadas = []
    for nome in sorted(por_camada):
        ordem, tamanho = por_camada[nome]
        camadas.append({"chaves": nome, "ordem": ordem, "tamanho": tamanho,
                        "densidade": densidade(ordem, tamanho)})

    return {"camadas": camadas, "arcos_entre_camadas": entre_camadas,
            "casas_que_mudam_de_camada": casas_texto}
