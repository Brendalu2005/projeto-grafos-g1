"""Integração da visualização com ocorrências reais e algoritmos existentes."""

# [IA] ChatGPT (Codex) – verificações da ponte HTTP/visualização.
import csv
import json
from http.client import HTTPConnection
from http.server import ThreadingHTTPServer
from threading import Thread

import pytest

from src.front import dataset
from src.front.server import Handler


@pytest.fixture
def csv_rede(tmp_path, monkeypatch):
    caminho = tmp_path / "rede.csv"
    arcos = [(u, v, -1) for u, v in dataset.PARES_DATASET]
    arcos += [("Malleus Fatuorum", "BDD", -1),
              ("Rcsprinter123", "Jasper Deng", -1),
              ("Jasper Deng", "Rcsprinter123", -1)]
    with caminho.open("w", encoding="utf-8", newline="") as arquivo:
        gravador = csv.writer(arquivo)
        gravador.writerow(["SOURCE", "TARGET", "VOTE", "RESULT", "PESO"])
        gravador.writerows((u, v, p, 1, p) for u, v, p in arcos)
    monkeypatch.setattr(dataset, "CSV", caminho)
    return caminho


def test_recorte_preserva_ocorrencias_lacos_pesos_e_semente():
    grafo = {"a": [("a", -1), ("b", 3), ("b", 3)] + [("c", i) for i in range(30)],
             "b": [("a", -1)], "c": []}
    completo = dataset.recortar(grafo)
    assert len(completo["arcos"]) == 34
    assert ("a", "a", -1, 0) in completo["arcos"]
    assert ("a", "b", 3, 1) in completo["arcos"]
    assert ("a", "b", 3, 2) in completo["arcos"]
    recorte = dataset.recortar(grafo, limite_arcos=20)
    assert recorte == dataset.recortar(grafo, limite_arcos=20)
    assert len(recorte["arcos"]) == 20
    assert len({(u, indice) for u, v, p, indice in recorte["arcos"]}) == 20
    for u, v, peso, indice in recorte["arcos"]:
        assert grafo[u][indice] == (v, peso)
    assert {n["id"] for n in completo["nos"]} == set(grafo)


@pytest.mark.parametrize("algoritmo", ["BFS", "DFS"])
def test_buscas_executam_tres_fontes_sem_restringir_grafo(csv_rede, algoritmo):
    resposta = dataset.executar(algoritmo)
    assert len(resposta["casos"]) == 3
    for caso, fonte in zip(resposta["casos"], dataset.FONTES_DATASET):
        assert caso["fonte"] == fonte
        assert caso["resumo"]["outros_usuarios_alcancados"] >= 1
        if algoritmo == "BFS":
            resultado = caso["resultado_bfs"]
            grafo = dataset.grafo_completo()
            assert resultado == dataset.resultado_busca_dataset(grafo, fonte, "BFS")
            assert resultado["grau_saida_fonte"] == len(grafo[fonte])
            assert set(resultado["distancias"]) == set(grafo)
            assert resultado["distancias"][fonte] == 0
            assert resultado["predecessores"][fonte] is None
            assert resultado["distancias"]["Rcsprinter123"] is None
            assert resultado["predecessores"]["Rcsprinter123"] is None
            alcancados = [d for d in resultado["distancias"].values() if d is not None]
            assert resultado["outros_usuarios_alcancados"] == len(alcancados) - 1
            assert resultado["maior_distancia_finita"] == max(alcancados)
        else:
            assert "resultado_bfs" not in caso
    json.dumps(resposta, allow_nan=False)


def test_dijkstra_executa_cinco_pares_e_preserva_peso_original(csv_rede):
    resposta = dataset.executar("DIJKSTRA")
    assert len(resposta["casos"]) == 5
    for caso, (u, v) in zip(resposta["casos"], dataset.PARES_DATASET):
        assert caso["resumo"]["caminho"] == [u, v]
        assert caso["arcos"] == [[u, v, -1]]
        assert caso["resumo"]["custo_transformado"] == 0
    assert all(p == -1 for arcos in dataset.grafo_completo().values() for _, p in arcos)


def test_conexoes_completas_preservam_direcao_paralelos_e_laco(monkeypatch):
    grafo = {"a": [("a", -1), ("b", 1), ("b", 1)],
             "b": [("a", 2), ("c", 4)], "c": [], "fora do recorte": [("a", -1)]}
    monkeypatch.setattr(dataset, "grafo_completo", lambda: grafo)
    resposta = dataset.conexoes("a")
    assert resposta["entradas"] == 3
    assert resposta["saidas"] == 3
    assert resposta["lacos"] == 1
    assert len(resposta["arcos"]) == 5
    assert resposta["vizinhos"] == ["a", "b", "fora do recorte"]
    assert len({(u, indice) for u, v, p, indice in resposta["arcos"]}) == 5
    assert all(grafo[u][indice] == (v, p) for u, v, p, indice in resposta["arcos"])
    assert dataset.conexoes("c")["vizinhos"] == ["b"]
    with pytest.raises(ValueError, match="não encontrado"):
        dataset.conexoes("inexistente")


def test_bellman_executa_os_dois_cenarios_sem_distancia_finita_no_ciclo(csv_rede):
    casos = dataset.executar("BELLMAN_FORD")["casos"]
    assert len(casos) == 2
    assert casos[0]["resumo"]["tem_ciclo_negativo"] is False
    assert casos[0]["resumo"]["distancias_em_PESO"]["BDD"] == -1
    assert casos[1]["resumo"]["tem_ciclo_negativo"] is True
    assert casos[1]["resumo"]["custo_ciclo"] == -2
    assert "distancias_em_PESO" not in casos[1]["resumo"]
    json.dumps(casos, allow_nan=False)


def test_api_rede_grafo_execucao_e_erro(csv_rede):
    servidor = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = Thread(target=servidor.serve_forever, daemon=True)
    thread.start()
    conexao = HTTPConnection("127.0.0.1", servidor.server_port)
    try:
        for rota, status in [("/api/dataset/grafo", 200),
                             ("/api/dataset/conexoes?usuario=Siva1979", 200),
                             ("/api/dataset/conexoes?usuario=inexistente", 422),
                             ("/api/dataset/executar?alg=BFS", 200),
                             ("/api/dataset/executar?alg=INVALIDO", 422)]:
            conexao.request("GET", rota)
            resposta = conexao.getresponse()
            valor = json.loads(resposta.read())
            assert resposta.status == status
            if rota.endswith("grafo"):
                assert valor["arcos_total"] == 8
            elif "conexoes" in rota and status == 200:
                assert valor["usuario"] == "Siva1979"
                assert valor["saidas"] == 2
                assert len(valor["arcos"]) == 2
            elif status == 200:
                assert len(valor["casos"]) == 3
            else:
                assert "erro" in valor
    finally:
        conexao.close()
        servidor.shutdown()
        servidor.server_close()
        thread.join()
