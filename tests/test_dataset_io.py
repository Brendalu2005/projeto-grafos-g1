# [IA] ChatGPT (Codex) – testes do carregador de CSV;
import pytest

from src.graphs.io import carregar_dataset


def test_carregar_dataset_preserva_direcao_destinos_lacos_e_nomes(tmp_path):
    caminho = tmp_path / "tratado.csv"
    caminho.write_text(
        "SOURCE,TARGET,VOTE,RESULT,PESO\n"
        "André,B,-1,1,-1\n"
        "B,B,0,1,0\n"
        "B,C,1,-1,1\n",
        encoding="utf-8-sig",
    )

    assert carregar_dataset(caminho) == {
        "André": [("B", -1)],
        "B": [("B", 0), ("C", 1)],
        "C": [],
    }


def test_carregar_dataset_preserva_pesos_ajustados_sem_reincrementar(tmp_path):
    caminho = tmp_path / "tratado.csv"
    caminho.write_text(
        "SOURCE,TARGET,VOTE,RESULT,PESO\n"
        "A,B,-1,1,-1\n"
        "A,B,-1,1,0\n"
        "A,B,-1,-1,-1\n"
        "A,B,-1,1,1\n",
        encoding="utf-8",
    )

    assert carregar_dataset(caminho) == {
        "A": [("B", -1), ("B", 0), ("B", -1), ("B", 1)],
        "B": [],
    }


@pytest.mark.parametrize(
    "conteudo, mensagem",
    [
        ("SOURCE,TARGET,VOTE,RESULT\nA,B,-1,1\n", "faltam as colunas PESO"),
        ("SOURCE,TARGET,VOTE,RESULT,PESO\n,B,-1,1,-1\n", "SOURCE e TARGET"),
        ("SOURCE,TARGET,VOTE,RESULT,PESO\nA,B,-1,1,abc\n", "PESO deve ser um inteiro"),
        ("SOURCE,TARGET,VOTE,RESULT,PESO\nA,B,-1,1,\n", "PESO deve ser um inteiro"),
    ],
)
def test_carregar_dataset_rejeita_entrada_invalida(tmp_path, conteudo, mensagem):
    caminho = tmp_path / "invalido.csv"
    caminho.write_text(conteudo, encoding="utf-8")

    with pytest.raises(ValueError, match=mensagem):
        carregar_dataset(caminho)
