# [IA] ChatGPT (Codex) – teste da execução e exportação do benchmark, usando os algoritmos existentes.
import json
from copy import deepcopy

import pytest

import src.benchmark_dfs_bellman as executor


@pytest.mark.parametrize("com_ciclo", [False, True])
def test_executor_exporta_16_configuracoes_sem_modificar_grafos(tmp_path, monkeypatch, com_ciclo):
    grafo = {"A": [("B", -1)], "B": [("C", 2)], "C": []}
    if com_ciclo:
        grafo["B"].append(("A", 0))
    original = deepcopy(grafo)
    recortes = [{"percentual": p, "grafo": grafo, "vertices": 3, "arcos": 2}
                for p in (10, 50, 100)]
    monkeypatch.setattr(executor, "carregar_dataset", lambda caminho: grafo)
    monkeypatch.setattr(executor, "criar_recortes", lambda grafo, semente: recortes)
    monkeypatch.setattr(executor, "selecionar_fontes", lambda recortes: ["A", "B", "C"])
    csv = tmp_path / "exemplo.csv"
    csv.write_text("entrada do teste", encoding="utf-8")
    saida = tmp_path / "resultado.json"

    relatorio = executor.executar_benchmark(csv, saida)
    salvo = json.loads(saida.read_text(encoding="utf-8"))
    assert salvo == relatorio
    assert relatorio["completo"] is True
    assert len(relatorio["medicoes"]) == 16
    assert len({(m["algoritmo"], m["percentual"], m["fonte"]) for m in relatorio["medicoes"]}) == 16
    assert relatorio["fontes_bellman_por_percentual"]["100"] == ["A"]
    for medicao in relatorio["medicoes"]:
        assert medicao["repeticoes"] == 5
        assert medicao["aquecimentos"] == 1
        assert len(medicao["tempos"]) == 5
        assert medicao["media"] >= 0
        assert medicao["versao_pesos"] == "PESO"
        if medicao["algoritmo"] == "BELLMAN_FORD":
            esperado = com_ciclo and medicao["fonte"] in ("A", "B")
            assert medicao["tem_ciclo_negativo"] is esperado
            assert medicao["status"] == ("CICLO_NEGATIVO" if esperado else "OK")
            if esperado:
                ciclo = medicao["ciclo_negativo"]
                assert ciclo[0] == ciclo[-1]
                assert set(ciclo) == {"A", "B"}
            else:
                assert medicao["ciclo_negativo"] is None
        else:
            assert "tem_ciclo_negativo" not in medicao
    assert grafo == original

    antes = saida.read_bytes()
    with pytest.raises(ValueError, match="saída já existe"):
        executor.executar_benchmark(csv, saida)
    assert saida.read_bytes() == antes

    completo = executor.executar_benchmark(csv, tmp_path / "tres_fontes.json", fontes_bellman_completo=3)
    assert completo["completo"] is True
    assert len(completo["medicoes"]) == 18
    assert completo["fontes_bellman_por_percentual"]["100"] == ["A", "B", "C"]


# [IA] ChatGPT (Codex) – confere complemento, preservação da base e recusa de entrada incompatível.
def test_complemento_mede_somente_fontes_pendentes(tmp_path, monkeypatch):
    grafo = {"A": [("B", -1)], "B": [("C", 2)], "C": []}
    recortes = [{"percentual": p, "grafo": grafo, "vertices": 3, "arcos": 2}
                for p in (10, 50, 100)]
    monkeypatch.setattr(executor, "carregar_dataset", lambda caminho: grafo)
    monkeypatch.setattr(executor, "criar_recortes", lambda grafo, semente: recortes)
    monkeypatch.setattr(executor, "selecionar_fontes", lambda recortes: ["A", "B", "C"])
    csv = tmp_path / "exemplo.csv"
    csv.write_text("entrada do teste", encoding="utf-8")
    base = tmp_path / "base.json"
    anterior = executor.executar_benchmark(csv, base)
    bytes_base = base.read_bytes()
    chamadas = []
    medir = executor.medir_algoritmo

    def registrar(algoritmo, entrada, fonte, repeticoes, **opcoes):
        chamadas.append((algoritmo, fonte))
        return medir(algoritmo, entrada, fonte, repeticoes, **opcoes)

    monkeypatch.setattr(executor, "medir_algoritmo", registrar)
    saida = tmp_path / "completo.json"
    completo = executor.executar_benchmark(csv, saida, complementar_de=base)
    assert chamadas == [(executor.bellman_ford, "B"), (executor.bellman_ford, "C")]
    assert completo["medicoes"][:16] == anterior["medicoes"]
    assert completo["completo"] is True
    assert len(completo["medicoes"]) == 18
    assert base.read_bytes() == bytes_base
    assert json.loads(saida.read_text(encoding="utf-8")) == completo

    csv.write_text("entrada diferente", encoding="utf-8")
    with pytest.raises(ValueError, match="sha256_entrada"):
        executor.executar_benchmark(csv, tmp_path / "invalido.json", complementar_de=base)
    assert not (tmp_path / "invalido.json").exists()
