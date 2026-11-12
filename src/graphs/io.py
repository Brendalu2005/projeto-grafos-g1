import csv
import json
from pathlib import Path

from src.graphs.estados import (ALVO, camadas_do_mapa, construir_g_est, construir_g_pos, graus, metricas_do_mapa, nome_do_movimento, rotulo, sem_alvo)
from src.graphs.graph import arcos

SIMBOLOS_VALIDOS = "#.SG,~abcdABCD><^v+*"


class Mapa:
    def __init__(self, nome, grade):
        self.nome = nome
        self.grade = grade
        self.linhas = len(grade)
        self.colunas = len(grade[0])
        self.inicio = None
        self.bonus = {}
        self.fontes = {}

        for linha in range(self.linhas):
            for coluna in range(self.colunas):
                if grade[linha][coluna] == "S":
                    self.inicio = (linha, coluna)
                if grade[linha][coluna] == "+":
                    self.bonus[(linha, coluna)] = len(self.bonus)

        for linha in range(self.linhas):
            for coluna in range(self.colunas):
                if grade[linha][coluna] == "*":
                    self.fontes[(linha, coluna)] = len(self.bonus) + len(self.fontes)

    def casa(self, linha, coluna):
        return self.grade[linha][coluna]

    def dentro(self, linha, coluna):
        return 0 <= linha < self.linhas and 0 <= coluna < self.colunas


def ler_mapa(caminho):
    grade = []
    with open(caminho, encoding="utf-8") as arquivo:
        for linha in arquivo:
            linha = linha.rstrip("\n")
            if linha == "" or linha.startswith(";"):
                continue
            grade.append(linha)

    nome = Path(caminho).stem
    validar_grade(nome, grade)
    return Mapa(nome, grade)


def validar_grade(nome, grade):
    casas = "".join(grade)
    if casas.count("S") != 1:
        raise ValueError(f"Mapa {nome}: precisa ter exatamente um S, mas tem {casas.count('S')}.")
    if casas.count("G") == 0:
        raise ValueError(f"Mapa {nome}: precisa ter pelo menos um G, mas não tem nenhum.")

    largura = len(grade[0])
    for numero, linha in enumerate(grade):
        if len(linha) != largura:
            raise ValueError(f"Mapa {nome}: grade não retangular (a linha {numero} tem {len(linha)} colunas, a primeira tem {largura}).")
        for simbolo in linha:
            if simbolo not in SIMBOLOS_VALIDOS:
                raise ValueError(f"Mapa {nome}: símbolo desconhecido '{simbolo}' na linha {numero}.")


def exportar_arestas(grafo, mapa, caminho):
    with open(caminho, "w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow(["origem", "destino", "movimento", "casa_destino", "peso"])
        for origem, destino, peso in arcos(grafo):
            if destino == ALVO:
                escritor.writerow([rotulo(origem), ALVO, "", "", peso])
            else:
                movimento = nome_do_movimento(origem, destino)
                casa = mapa.casa(destino[0], destino[1])
                escritor.writerow([rotulo(origem), rotulo(destino), movimento, casa, peso])


def exportar_graus(g_est, caminho):
    vertices, lista = sem_alvo(g_est)
    entrada, saida = graus(vertices, lista)
    with open(caminho, "w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow(["estado", "grau_entrada", "grau_saida"])
        for v in vertices:
            escritor.writerow([rotulo(v), entrada[v], saida[v]])


def escrever_json(dados, caminho):
    with open(caminho, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=2)


def exportar_parte1(pastas_mapas, pasta_saida):
    pasta_saida = Path(pasta_saida)
    metricas = []
    camadas = {}

    for pasta in pastas_mapas:
        for caminho_mapa in sorted(Path(pasta).glob("*.txt")):
            mapa = ler_mapa(caminho_mapa)
            g_pos = construir_g_pos(mapa)
            g_est = construir_g_est(mapa)

            exportar_arestas(g_est, mapa, pasta_saida / f"arestas_{mapa.nome}.csv")
            exportar_graus(g_est, pasta_saida / f"graus_{mapa.nome}.csv")
            metricas.append(metricas_do_mapa(mapa, g_pos, g_est))
            camadas[mapa.nome] = camadas_do_mapa(mapa, g_est)

    escrever_json(metricas, pasta_saida / "metricas_global.json")
    escrever_json(camadas, pasta_saida / "camadas.json")
