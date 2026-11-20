# [IA] Claude – sugestão de estrutura de código
import pytest

from src.graphs.io import ler_mapa


def test_mapa_com_dois_s_gera_erro_claro(tmp_path):
    caminho = tmp_path / "dois_s.txt"
    caminho.write_text("#####\n#SSG#\n#####\n", encoding="utf-8")

    with pytest.raises(ValueError, match="exatamente um S"):
        ler_mapa(caminho)


# [IA] ChatGPT (Codex) – cobre mensagens de validação de grade e símbolos.
def test_mapa_sem_grade_gera_erro_claro(tmp_path):
    caminho = tmp_path / "vazio.txt"
    caminho.write_text("; comentário\n\n", encoding="utf-8")
    with pytest.raises(ValueError, match="exatamente um S"):
        ler_mapa(caminho)


def test_mapa_nao_retangular_gera_erro_claro(tmp_path):
    caminho = tmp_path / "torto.txt"
    caminho.write_text("#####\n#S.G#\n####\n", encoding="utf-8")
    with pytest.raises(ValueError, match="não retangular"):
        ler_mapa(caminho)


def test_mapa_sem_g_gera_erro_claro(tmp_path):
    caminho = tmp_path / "sem_g.txt"
    caminho.write_text("#####\n#S..#\n#####\n", encoding="utf-8")
    with pytest.raises(ValueError, match="pelo menos um G"):
        ler_mapa(caminho)


def test_mapa_com_simbolo_desconhecido_gera_erro_claro(tmp_path):
    caminho = tmp_path / "simbolo.txt"
    caminho.write_text("#####\n#S?G#\n#####\n", encoding="utf-8")
    with pytest.raises(ValueError, match="símbolo desconhecido"):
        ler_mapa(caminho)


def test_porta_sem_chave_correspondente_gera_erro_claro(tmp_path):
    caminho = tmp_path / "porta.txt"
    caminho.write_text("######\n#S.AG#\n######\n", encoding="utf-8")
    with pytest.raises(ValueError, match="porta A sem a chave a"):
        ler_mapa(caminho)
