# [IA] Claude – sugestão de estrutura de código
import pytest

from src.graphs.io import ler_mapa


def test_mapa_com_dois_s_gera_erro_claro(tmp_path):
    caminho = tmp_path / "dois_s.txt"
    caminho.write_text("#####\n#SSG#\n#####\n")

    with pytest.raises(ValueError, match="exatamente um S"):
        ler_mapa(caminho)
