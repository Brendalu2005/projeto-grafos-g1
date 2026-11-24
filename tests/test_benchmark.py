# [IA] ChatGPT (Codex) – testes das regras de recorte aprovadas pela equipe.
from collections import Counter
from copy import deepcopy
import csv
import hashlib
import json
import math
import sys

import pytest

from src.benchmark import criar_recortes, selecionar_fontes, medir_algoritmo


@pytest.fixture
def grafo():
    return {
        "A": [("A", -1), ("B", 0), ("B", 0), ("B", 2)]
             + [("C", peso) for peso in range(12)],
        "B": [("A", -1), ("A", 0), ("B", 1), ("C", 2)],
        "C": [],
        "isolado": [],
    }


def test_tamanhos_e_aninhamento_das_ocorrencias(grafo):
    pequeno, medio, completo = criar_recortes(grafo)

    assert [r["percentual"] for r in (pequeno, medio, completo)] == [10, 50, 100]
    assert [r["arcos"] for r in (pequeno, medio, completo)] == [2, 10, 20]
    assert pequeno["ocorrencias"] == medio["ocorrencias"][:2]
    assert medio["ocorrencias"] == completo["ocorrencias"][:10]
    ids = [ocorrencia[0] for ocorrencia in completo["ocorrencias"]]
    assert sorted(ids) == list(range(20))


def test_semente_reproduzivel_e_preservacao_da_entrada(grafo):
    original = deepcopy(grafo)

    primeira = criar_recortes(grafo, semente=42)
    segunda = criar_recortes(grafo, semente=42)
    outra = criar_recortes(grafo, semente=7)

    assert primeira == segunda
    assert primeira[-1]["ocorrencias"] != outra[-1]["ocorrencias"]
    assert all(r["semente"] == 42 for r in primeira)
    assert grafo == original


def test_preserva_pesos_lacos_paralelos_e_vertices_efetivos(grafo):
    originais = []
    for origem, vizinhos in grafo.items():
        for destino, peso in vizinhos:
            originais.append((origem, destino, peso))

    recortes = criar_recortes(grafo)
    for recorte in recortes:
        extremos = set()
        selecionados = []
        for identificador, origem, destino, peso in recorte["ocorrencias"]:
            assert (origem, destino, peso) == originais[identificador]
            extremos.update((origem, destino))
            selecionados.append((origem, destino, peso))

        carregados = []
        for origem, vizinhos in recorte["grafo"].items():
            for destino, peso in vizinhos:
                carregados.append((origem, destino, peso))

        assert Counter(carregados) == Counter(selecionados)
        assert set(recorte["grafo"]) == extremos
        assert recorte["vertices"] == len(extremos)
        assert len(carregados) == recorte["arcos"]
        assert "isolado" not in recorte["grafo"]

    completo = recortes[-1]
    assert Counter(o[1:] for o in completo["ocorrencias"]) == Counter(originais)
    assert originais.count(("A", "B", 0)) == 2


def test_arredondamento_e_grafo_vazio():
    vazio = criar_recortes({})
    assert all(r["arcos"] == 0 and r["vertices"] == 0 for r in vazio)
    assert all(r["grafo"] == {} and r["ocorrencias"] == [] for r in vazio)

    recortes = criar_recortes({"A": [("B", -1)], "B": []})
    assert [r["arcos"] for r in recortes] == [0, 0, 1]
    assert [r["vertices"] for r in recortes] == [0, 0, 2]


# [IA] ChatGPT (Codex) – testes de escolha, desempate e falhas da seleção de fontes.
def test_fontes_por_grau_nome_e_posicoes():
    grafo = {
        "B": [("alvo", 0)] * 8,
        "A": [("alvo", 0)] * 8,
        "D": [("alvo", 0)] * 6,
        "C": [("alvo", 0)] * 6,
        "E": [("alvo", 0)] * 5,
        "F": [("alvo", 0)] * 4,
        "G": [("alvo", 0)] * 3,
        "H": [("alvo", 0)] * 3,
        "baixo": [("alvo", 0)] * 2,
        "alvo": [],
    }
    # Oito candidatos: posições 0, 2 e 4 na ordem A, B, C, D, E, F, G, H.
    recortes = [{"percentual": p, "grafo": deepcopy(grafo)} for p in (10, 50, 100)]
    original = deepcopy(recortes)

    assert selecionar_fontes(recortes) == ["A", "C", "E"]
    assert selecionar_fontes(recortes) == selecionar_fontes(recortes)
    assert recortes == original


def test_fontes_exigem_recorte_de_dez_por_cento():
    with pytest.raises(ValueError, match="recorte de 10%"):
        selecionar_fontes([])


@pytest.mark.parametrize("quantidade", [0, 2, 3])
def test_fontes_rejeitam_candidatos_insuficientes_ou_posicoes_repetidas(quantidade):
    grafo = {str(i): [(str(i), 0)] * 3 for i in range(quantidade)}
    with pytest.raises(ValueError, match="Revise a regra"):
        selecionar_fontes([{"percentual": 10, "grafo": grafo}])


def test_fontes_precisam_existir_nos_outros_recortes():
    grafo = {nome: [(nome, 0)] * 3 for nome in ["A", "B", "C", "D"]}
    recortes = [
        {"percentual": 10, "grafo": grafo},
        {"percentual": 50, "grafo": {"A": [], "B": []}},
        {"percentual": 100, "grafo": grafo},
    ]
    with pytest.raises(ValueError, match="ausente no recorte de 50%"):
        selecionar_fontes(recortes)


# [IA] ChatGPT (Codex) – relógio simulado para verificar aquecimento, tempos e estatísticas.
def test_medicao_exclui_aquecimento_e_calcula_estatisticas(monkeypatch):
    grafo = {"A": []}
    chamadas = []
    instantes = iter([0, 1, 10, 12, 20, 23, 30, 34, 40, 45])

    def relogio():
        # O aquecimento deve ter ocorrido antes de qualquer leitura do relógio.
        assert len(chamadas) >= 1
        return next(instantes)

    def algoritmo_exemplo(entrada, fonte):
        assert entrada is grafo
        assert fonte == "A"
        chamadas.append(fonte)
        return {"A": 0}

    monkeypatch.setattr("src.benchmark.perf_counter", relogio)
    resultado = medir_algoritmo(algoritmo_exemplo, grafo, "A")

    assert len(chamadas) == 6  # Um aquecimento e cinco medições.
    assert resultado == {
        "aquecimentos": 1,
        "repeticoes": 5,
        "unidade_tempo": "segundos",
        "tempos": [1, 2, 3, 4, 5],
        "media": 3,
        "minimo": 1,
        "mediana": 3,
        "desvio_padrao_amostral": pytest.approx(2.5 ** 0.5),
    }


def test_medicao_aceita_mais_de_cinco_repeticoes(monkeypatch):
    chamadas = []
    instantes = iter(range(12))

    def algoritmo_exemplo(grafo, fonte):
        chamadas.append(fonte)

    monkeypatch.setattr("src.benchmark.perf_counter", lambda: next(instantes))
    resultado = medir_algoritmo(algoritmo_exemplo, {"A": []}, "A", repeticoes=6)

    assert len(chamadas) == 7
    assert resultado["repeticoes"] == 6
    assert resultado["tempos"] == [1] * 6
    assert resultado["desvio_padrao_amostral"] == 0


@pytest.mark.parametrize("repeticoes", [0, 4, 5.5])
def test_medicao_rejeita_repeticoes_invalidas(repeticoes):
    def nao_executar(grafo, fonte):
        pytest.fail("O algoritmo não deve executar com repetições inválidas.")

    with pytest.raises(ValueError, match="pelo menos 5"):
        medir_algoritmo(nao_executar, {"A": []}, "A", repeticoes)


def test_medicao_rejeita_fonte_ausente():
    def nao_executar(grafo, fonte):
        pytest.fail("O algoritmo não deve executar com fonte ausente.")

    with pytest.raises(ValueError, match="fonte"):
        medir_algoritmo(nao_executar, {"A": []}, "B")


# [IA] ChatGPT (Codex) – integração do comando, preservação dos dados e falhas de alcance.
@pytest.fixture
def csv_benchmark(tmp_path):
    caminho = tmp_path / "tratado.csv"
    with caminho.open("w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow(["SOURCE", "TARGET", "VOTE", "RESULT", "PESO"])
        for fonte in ["A", "B", "C", "D"]:
            for peso in [-1, 0, 1, 2] * 25:
                escritor.writerow([fonte, "T", -1, 1, peso])
    return caminho


def test_comando_benchmark_exporta_18_configuracoes(csv_benchmark, tmp_path, monkeypatch):
    import src.benchmark as executor

    saida = tmp_path / "resultado.json"
    original = csv_benchmark.read_bytes()
    dijkstra_original = executor.dijkstra
    pesos_recebidos = []

    def conferir_pesos(grafo, fonte):
        pesos_recebidos.extend(peso for vizinhos in grafo.values() for _, peso in vizinhos)
        return dijkstra_original(grafo, fonte)

    monkeypatch.setattr(executor, "dijkstra", conferir_pesos)
    monkeypatch.setattr(sys, "argv", ["benchmark", "--dataset", str(csv_benchmark), "--out", str(saida)])
    executor.main()

    relatorio = json.loads(saida.read_text(encoding="utf-8"))
    assert relatorio["completo"] is True
    assert relatorio["configuracoes_esperadas"] == len(relatorio["medicoes"]) == 18
    assert len({(m["algoritmo"], m["percentual"], m["fonte"]) for m in relatorio["medicoes"]}) == 18
    assert {m["algoritmo"] for m in relatorio["medicoes"]} == {"BFS", "DIJKSTRA"}
    assert {m["percentual"] for m in relatorio["medicoes"]} == {10, 50, 100}
    assert len(relatorio["fontes"]) == 3
    assert relatorio["sha256_entrada"] == hashlib.sha256(original).hexdigest()
    assert relatorio["arquivo_entrada"] == csv_benchmark.name
    assert csv_benchmark.read_bytes() == original
    assert set(pesos_recebidos) == {0, 1, 2, 3}
    for medicao in relatorio["medicoes"]:
        assert len(medicao["tempos"]) == medicao["repeticoes"] == 5
        assert medicao["aquecimentos"] == 1
        assert medicao["outros_usuarios_alcancados"] == 1
        assert medicao["arcos"] == {10: 40, 50: 200, 100: 400}[medicao["percentual"]]
        assert math.isclose(medicao["media"], sum(medicao["tempos"]) / 5)


def test_executor_preserva_saida_existente(csv_benchmark, tmp_path):
    from src.benchmark import executar_benchmark

    saida = tmp_path / "anterior.json"
    saida.write_text("resultado anterior", encoding="utf-8")
    with pytest.raises(ValueError, match="saída já existe"):
        executar_benchmark(csv_benchmark, saida)
    assert saida.read_text(encoding="utf-8") == "resultado anterior"


def test_executor_rejeita_conjuntos_diferentes_com_mesma_contagem(csv_benchmark, tmp_path, monkeypatch):
    import src.benchmark as executor

    monkeypatch.setattr(executor, "dijkstra", lambda grafo, fonte: ({fonte: 0, "outro": 1}, {}))
    saida = tmp_path / "divergente.json"
    with pytest.raises(ValueError, match="Alcances diferentes"):
        executor.executar_benchmark(csv_benchmark, saida)
    assert not saida.exists()
