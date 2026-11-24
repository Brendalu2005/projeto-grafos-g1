from src.solve import resolver
import pytest

def test_resolver_preserva_ciclo_negativo_do_m06():
    resultado = resolver("data/mapas/m06_fonte.txt", "BELLMAN_FORD")
    assert resultado["status"] == "CICLO_NEGATIVO"
    assert len(resultado["ciclo"]) >= 3
    assert resultado["ciclo"][0] == resultado["ciclo"][-1]


def test_fonte_consumivel_remove_ciclo_negativo_do_m06():
    resultado = resolver("data/mapas/m06_fonte.txt", "BELLMAN_FORD", fonte_consumivel=True)
    assert resultado["status"] == "OK"
    assert resultado["ciclo"] == []


# [IA] Claude - assegura que a exportação de armadilhas use o grafo da variante.
def test_exportador_armadilhas_encaminha_regra_consumivel(tmp_path, monkeypatch):
    import src.solve as solve_module

    pasta_mapas = tmp_path / "mapas"
    pasta_mapas.mkdir()
    (pasta_mapas / "teste.txt").write_text("#######\n#S*G..#\n#######\n")
    original = solve_module.construir_g_est
    argumentos = []

    def construtor(mapa, fonte_consumivel=False):
        argumentos.append(fonte_consumivel)
        return original(mapa, fonte_consumivel)

    monkeypatch.setattr(solve_module, "construir_g_est", construtor)
    resumos = solve_module.exportar_armadilhas([pasta_mapas], tmp_path / "out", True)

    assert argumentos == [True]
    assert resumos[0]["mapa"] == "teste"
    assert (tmp_path / "out" / "armadilhas_teste.csv").is_file()


# [IA] ChatGPT (Codex) – regressão da medição da interface, com relógio simulado.
@pytest.mark.parametrize("recusa", [False, True])
def test_interface_exclui_aquecimento_e_mede_cinco_execucoes_lentas(monkeypatch, recusa):
    from src.front import server

    eventos = []
    instantes = iter([0, 2, 10, 13, 20, 24, 30, 35, 40, 46])
    retorno = ({"A": 0}, {"A": None})

    def algoritmo(grafo, origem):
        eventos.append("algoritmo")
        if recusa:
            raise ValueError("Peso negativo")
        return retorno

    def relogio():
        eventos.append("relogio")
        return next(instantes)

    monkeypatch.setattr(server.time, "perf_counter", relogio)
    saida, tempos = server.medir(algoritmo, {"A": []}, "A")

    assert eventos == ["algoritmo"] + ["relogio", "algoritmo", "relogio"] * 5
    assert tempos == [2000, 3000, 4000, 5000, 6000]
    assert saida == (None if recusa else retorno)
