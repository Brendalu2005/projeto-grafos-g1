from src.solve import resolver
import pytest

def test_resolver_preserva_ciclo_negativo_do_m06():
    resultado = resolver("data/mapas/m06_fonte.txt", "BELLMAN_FORD")
    assert resultado["status"] == "CICLO_NEGATIVO"
    assert len(resultado["ciclo"]) >= 3
    assert resultado["ciclo"][0] == resultado["ciclo"][-1]
    assert resultado["custo_ciclo"] == -1


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


# [IA] ChatGPT (Codex) – valida homepage, acesso anterior e imagens das duas partes pelo servidor.
def test_homepage_preserva_acesso_ao_labirinto_e_figuras_parte2():
    from http.client import HTTPConnection
    from http.server import ThreadingHTTPServer
    from threading import Thread
    from html.parser import HTMLParser
    from urllib.parse import urljoin
    from src.front.server import Handler

    servidor = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = Thread(target=servidor.serve_forever, daemon=True)
    thread.start()
    conexao = HTTPConnection(*servidor.server_address, timeout=10)
    try:
        for rota in ("/", "/index.html", "/out/parte1/labirinto_interativo.html"):
            conexao.request("GET", rota)
            resposta = conexao.getresponse()
            pagina = resposta.read().decode("utf-8")
            assert resposta.status == 200
            assert 'data-page="inicio"' in pagina
            assert 'id="nav-parte1"' in pagina
            assert 'id="nav-parte2"' in pagina
            assert 'id="layer-filter"' in pagina
            assert 'id="trap-toggle"' in pagina
            class Recursos(HTMLParser):
                def __init__(self):
                    super().__init__()
                    self.urls = []

                def handle_starttag(self, tag, attrs):
                    atributos = dict(attrs)
                    if tag == "script" and "src" in atributos:
                        self.urls.append(atributos["src"])
                    if tag == "link" and atributos.get("rel") == "stylesheet":
                        self.urls.append(atributos["href"])

            recursos = Recursos()
            recursos.feed(pagina)
            assert len(recursos.urls) == 4
            for recurso in recursos.urls:
                conexao.request("GET", urljoin(rota, recurso))
                resposta = conexao.getresponse()
                resposta.read()
                assert resposta.status == 200
        for nome in ("andre_01_distribuicao_graus", "andre_02_distribuicao_pesos",
                     "andre_03_tempos_dfs_bellman", "andre_04_atributos_result",
                     "brenda_01_faltantes_por_faixa", "brenda_02_tempos_bfs_dijkstra",
                     "brenda_03_efeito_transformacao"):
            conexao.request("GET", f"/out/parte2/{nome}.png")
            resposta = conexao.getresponse()
            assert resposta.status == 200
            assert resposta.read().startswith(b"\x89PNG\r\n\x1a\n")
    finally:
        conexao.close()
        servidor.shutdown()
        servidor.server_close()
        thread.join(timeout=5)


# [IA] ChatGPT (Codex) – regressão do movimento virtual e do formato de exportação, em exemplo mínimo.
def test_comparacao_nao_conta_arco_virtual_como_movimento(tmp_path, monkeypatch):
    import csv
    from types import SimpleNamespace
    import src.solve as solve

    grafo = {"S": [("G", 1)], "G": [("ALVO", 0)], "ALVO": []}
    monkeypatch.setattr(solve, "ler_mapa", lambda caminho: SimpleNamespace(nome="minimo", inicio="S"))
    monkeypatch.setattr(solve, "construir_g_pos", lambda *args: grafo)
    monkeypatch.setattr(solve, "construir_g_est", lambda *args: grafo)
    monkeypatch.setattr(solve, "estado_inicial", lambda mapa: "S")
    linhas = solve.exportar_comparacao([], tmp_path)
    assert linhas and all(linha["passos"] == 1 for linha in linhas)
    with (tmp_path / "comparacao_modelagem.csv").open(encoding="utf-8") as arquivo:
        leitor = csv.DictReader(arquivo)
        assert {"mapa", "abordagem", "passos", "caminho_valido", "observacao"} <= set(leitor.fieldnames)


# [IA] ChatGPT (Codex) – confere os nomes exigidos sem resolver os mapas do grupo.
def test_gerador_preserva_nomes_das_figuras_e_cria_nomes_exigidos(tmp_path, monkeypatch):
    import src.viz as viz

    monkeypatch.setattr(viz, "resolver", lambda *args: {"status": "OK"})
    monkeypatch.setattr(viz, "percurso_colorido", lambda mapa, resultado, destino: destino.write_bytes(b"figura de teste"))
    monkeypatch.setattr(viz, "grafo_estados_camadas", lambda *args: None)
    viz.gerar_figuras_parte1(tmp_path)
    for mapa, nome in (("m03", "m03_tres_chaves"), ("m08", "m08_grande")):
        assert (tmp_path / f"percurso_{mapa}.png").read_bytes() == (tmp_path / f"percurso_{nome}.png").read_bytes()
