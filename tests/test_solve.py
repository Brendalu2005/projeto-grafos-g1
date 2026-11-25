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


def test_bfs_exporta_ordem_de_visita():
    resultado = resolver("data/mapas/m02_uma_chave.txt", "BFS")

    visitas = resultado["ordem_visita"].split(" -> ")
    assert visitas[0] == "(1,1)|-|{}"
    assert visitas[-1] == "ALVO"
    assert len(visitas) == len(set(visitas))


def test_mapa_do_grupo_tem_rota_otima_pela_esteira_e_bonus():
    resultado = resolver("data/mapas_grupo/grupo_rotas.txt", "BELLMAN_FORD")

    assert resultado["status"] == "OK"
    assert resultado["custo"] == 9
    assert "(3,3)|a|{}" in resultado["caminho"]
    assert "(3,4)|a|{0}" in resultado["caminho"]
    assert "(3,13)|abc|{0}" in resultado["caminho"]


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
