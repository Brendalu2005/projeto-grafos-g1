# [IA] Claude – sugestão dos casos de teste;
from src.graphs.estados import construir_g_est, rotulo
from src.graphs.graph import arcos
from src.graphs.io import ler_mapa
from src.graphs.estados import (ALVO, estado_inicial, movimentos)
from src.solve import estados_armadilha_local


def test_coletar_chave_muda_de_camada(tmp_path):
    caminho = tmp_path / "chave.txt"
    caminho.write_text("######\n#SaAG#\n######\n")
    grafo = construir_g_est(ler_mapa(caminho))

    pares = []
    for origem, destino, _ in arcos(grafo):
        pares.append((rotulo(origem), rotulo(destino)))

    assert ("(1,1)|-|{}", "(1,2)|a|{}") in pares
    assert ("(1,2)|a|{}", "(1,3)|a|{}") in pares


# [IA] ChatGPT (Codex) – amplia a cobertura das transições previstas no enunciado.
def test_mapa_minimo_tem_estados_e_arcos_calculados_a_mao(tmp_path):
    caminho = tmp_path / "minimo.txt"
    caminho.write_text("#####\n#S.G#\n#####\n")
    grafo = construir_g_est(ler_mapa(caminho))
    assert len([v for v in grafo if v != ALVO]) == 3
    assert sum(len(vizinhos) for estado, vizinhos in grafo.items() if estado != ALVO) == 4
    assert grafo[ALVO] == []


def test_vizinhos_sao_gerados_na_ordem_n_l_s_o(tmp_path):
    caminho = tmp_path / "ordem.txt"
    caminho.write_text("#####\n#..G#\n#.S.#\n#...#\n#####\n")
    mapa = ler_mapa(caminho)
    vizinhos = movimentos(mapa, estado_inicial(mapa))
    assert [(v[0], v[1]) for v, _ in vizinhos] == [(1, 2), (2, 3), (3, 2), (2, 1)]


def test_bonus_e_fonte_consumivel_so_dao_peso_negativo_na_primeira_entrada(tmp_path):
    caminho = tmp_path / "itens.txt"
    caminho.write_text("#######\n#S+*G.#\n#######\n")
    mapa = ler_mapa(caminho)
    inicial = estado_inicial(mapa)
    pos_bonus, peso_bonus = movimentos(mapa, inicial)[0]
    assert peso_bonus == -4 and pos_bonus[3] == frozenset({0})
    pos_fonte, peso_fonte = movimentos(mapa, pos_bonus, fonte_consumivel=True)[0]
    assert peso_fonte == -2 and len(pos_fonte[3]) == 2
    pos_volta, _ = next((v, p) for v, p in movimentos(mapa, pos_fonte, fonte_consumivel=True) if v[0:2] == (1, 2))
    _, peso_reentrada_fonte = next((v, p) for v, p in movimentos(mapa, pos_volta, fonte_consumivel=True) if v[0:2] == (1, 3))
    assert peso_reentrada_fonte == 1


def test_esteira_restringe_a_saida_e_g_nao_tem_saida(tmp_path):
    caminho = tmp_path / "esteira.txt"
    caminho.write_text("#######\n#S>G..#\n#######\n")
    grafo = construir_g_est(ler_mapa(caminho))
    estado_esteira = next(v for v in grafo if v != ALVO and v[:2] == (1, 2))
    assert [v[:2] for v, _ in grafo[estado_esteira]] == [(1, 3)]
    estado_saida = next(v for v in grafo if v != ALVO and v[:2] == (1, 3))
    assert grafo[estado_saida] == [(ALVO, 0)]


def test_armadilhas_consideram_estados_sem_caminho_ao_alvo(tmp_path):
    caminho = tmp_path / "armadilha.txt"
    caminho.write_text("########\n#S.G####\n#v######\n#>>>>>##\n########\n")
    mapa = ler_mapa(caminho)
    grafo = construir_g_est(mapa)
    armadilhas = estados_armadilha_local(grafo, estado_inicial(mapa))
    assert len(armadilhas) == 6
