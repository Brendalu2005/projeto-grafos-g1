# [IA] ChatGPT (Codex) – verifica normalização por RESULT e rastreabilidade dos extremos.
import pandas as pd
import pytest

from src.verificar_parte2 import verificar_outliers
from src.viz import atributos_por_result_dataset


def test_result_preserva_grupos_distintos_do_mesmo_target(tmp_path):
    csv = tmp_path / "exemplo.csv"
    pd.DataFrame({"SOURCE": ["A", "B", "C", "D"], "TARGET": ["T"] * 4,
                  "VOTE": [-1, 0, 1, 1], "RESULT": [-1, -1, 1, 1],
                  "PESO": [-1, 0, 1, 2]}).to_csv(csv, index=False)
    figura = tmp_path / "result.png"
    resumo = atributos_por_result_dataset(csv, figura)
    assert figura.exists()
    assert resumo["targets_com_result_distinto"] == 1
    assert resumo["registros_por_result"] == {"-1": 2, "1": 2}
    for distribuicao in resumo["distribuicoes"].values():
        for grupo in distribuicao.values():
            assert sum(c["registros"] for c in grupo.values()) == 2
            assert sum(c["percentual"] for c in grupo.values()) == pytest.approx(100)
    voto = resumo["distribuicoes"]["VOTE"]
    assert voto["-1"]["-1"]["percentual"] == 50
    assert voto["1"]["1"]["percentual"] == 100


def test_outliers_confere_incremento_e_rejeita_peso_incorreto(tmp_path):
    bruto = tmp_path / "bruto.csv"
    tratado = tmp_path / "tratado.csv"
    dados = pd.DataFrame({"SOURCE": ["A"] * 7 + [None], "TARGET": ["B"] * 8,
                          "VOTE": [1] * 8, "RESULT": [1] * 8})
    dados.to_csv(bruto)
    mantidos = dados.dropna(subset=["SOURCE"]).copy()
    mantidos["PESO"] = range(1, 8)
    mantidos.to_csv(tratado, index=False)
    antes = tratado.read_bytes()
    resultado = verificar_outliers(tratado, bruto)
    assert resultado["registros_sem_source_excluidos"] == 1
    assert resultado["novas_remocoes_ou_alteracoes"] == 0
    assert resultado["pesos_altos"]["maximo"] == 7
    assert len(resultado["pesos_altos"]["ocorrencias"]) == 4
    assert resultado["graus"]["entrada"]["cinco_maiores_conferidos_no_bruto"][0]["grau"] == 7
    assert tratado.read_bytes() == antes
    mantidos.loc[0, "PESO"] = 100
    mantidos.to_csv(tratado, index=False)
    with pytest.raises(ValueError, match="pesos diferem"):
        verificar_outliers(tratado, bruto)
