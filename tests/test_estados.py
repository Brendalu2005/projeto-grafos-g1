# [IA] Claude – sugestão dos casos de teste;
from src.graphs.estados import construir_g_est, rotulo
from src.graphs.graph import arcos
from src.graphs.io import ler_mapa


def test_coletar_chave_muda_de_camada(tmp_path):
    caminho = tmp_path / "chave.txt"
    caminho.write_text("######\n#SaAG#\n######\n")
    grafo = construir_g_est(ler_mapa(caminho))

    pares = []
    for origem, destino, _ in arcos(grafo):
        pares.append((rotulo(origem), rotulo(destino)))

    assert ("(1,1)|-|{}", "(1,2)|a|{}") in pares
    assert ("(1,2)|a|{}", "(1,3)|a|{}") in pares


def test_mapa_minimo_com_contagem_feita_a_mao(tmp_path):
    caminho = tmp_path / "minimo.txt"
    caminho.write_text("######\n#SaAG#\n######\n")
    grafo = construir_g_est(ler_mapa(caminho))

    assert len(grafo) == 6
    assert len(arcos(grafo)) == 7


def test_esteira_apontando_para_parede_gera_estado_sem_saida(tmp_path):
    caminho = tmp_path / "esteira.txt"
    caminho.write_text("#####\n#S^G#\n#####\n")
    grafo = construir_g_est(ler_mapa(caminho))

    esteira = (1, 2, frozenset(), frozenset())

    assert esteira in grafo
    assert grafo[esteira] == []
