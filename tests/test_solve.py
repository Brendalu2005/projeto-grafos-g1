from src.solve import resolver

def test_resolver_preserva_ciclo_negativo_do_m06():
    resultado = resolver("data/mapas/m06_fonte.txt", "BELLMAN_FORD")
    assert resultado["status"] == "CICLO_NEGATIVO"
    assert len(resultado["ciclo"]) >= 3
    assert resultado["ciclo"][0] == resultado["ciclo"][-1]


def test_fonte_consumivel_remove_ciclo_negativo_do_m06():
    resultado = resolver("data/mapas/m06_fonte.txt", "BELLMAN_FORD", fonte_consumivel=True)
    assert resultado["status"] == "OK"
    assert resultado["ciclo"] == []
