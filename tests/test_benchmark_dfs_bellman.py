# [IA] ChatGPT (Codex) – teste da execução e exportação do benchmark, usando os algoritmos existentes.
import json
from copy import deepcopy

import pytest

import src.benchmark_dfs_bellman as executor


def test_executor_exporta_16_configuracoes_sem_modificar_grafos(tmp_path, monkeypatch):
    grafo = {"A": [("B", -1)], "B": [("C", 2)], "C": []}
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
    assert grafo == original

    antes = saida.read_bytes()
    with pytest.raises(ValueError, match="saída já existe"):
        executor.executar_benchmark(csv, saida)
    assert saida.read_bytes() == antes

    completo = executor.executar_benchmark(csv, tmp_path / "tres_fontes.json", fontes_bellman_completo=3)
    assert completo["completo"] is True
    assert len(completo["medicoes"]) == 18
    assert completo["fontes_bellman_por_percentual"]["100"] == ["A", "B", "C"]
