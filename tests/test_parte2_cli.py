# [IA] ChatGPT (Codex) – testes de integração da CLI e das chamadas da Parte 2.
import csv
import json
import sys

import pytest

from src.cli import main
from src.solve import executar_experimentos_dataset, resolver_dataset


@pytest.fixture
def dataset(tmp_path):
    caminho = tmp_path / "tratado.csv"
    with caminho.open("w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow(["SOURCE", "TARGET", "VOTE", "RESULT", "PESO"])
        escritor.writerows([
            ("A", "B", -1, 1, -1),
            ("A", "B", 1, 1, 1),
            ("A", "A", 0, 1, 0),
            ("D", "D", 0, 1, 0),
            ("Siva1979", "(aeropagitica)", 1, 1, 1),
            ("(aeropagitica)", "Dieter Simon", 1, 1, 1),
            ("'sed", "9cds", 0, 1, 0),
            ("9cds", "Caltrop", 1, 1, 1),
            ("!---slappdash---!", "Caltrop", 1, 1, 1),
            ("Malleus Fatuorum", "BDD", -1, 1, -1),
            ("Rcsprinter123", "Jasper Deng", -1, -1, -1),
            ("Jasper Deng", "Rcsprinter123", -1, -1, -1),
        ])
    return caminho


def test_cli_dfs_exporta_paralelos_sem_alterar_csv(dataset, tmp_path, monkeypatch):
    antes = dataset.read_bytes()
    saida = tmp_path / "saida"
    monkeypatch.setattr(sys, "argv", ["cli", "--dataset", str(dataset), "--alg", "DFS",
                                      "--source", "A", "--out", str(saida)])
    main()
    resultado = json.loads((saida / "solucao_dataset_DFS.json").read_text(encoding="utf-8"))
    assert resultado["resultado"]["ordem_descoberta"] == ["A", "B"]
    assert resultado["resultado"]["classificacao_arcos"] == {
        "arvore": 1, "retorno": 1, "avanco": 1, "cruzamento": 0,
    }
    assert dataset.read_bytes() == antes


def test_bfs_exporta_inalcancaveis_como_null(dataset):
    resultado = resolver_dataset(dataset, "BFS", "A")["resultado"]
    assert resultado["distancias"]["B"] == 1
    assert resultado["distancias"]["D"] is None
    assert resultado["predecessores"]["D"] is None


def test_dijkstra_recusa_sem_transformacao_e_aceita_deslocamento(dataset):
    with pytest.raises(ValueError, match="negativos"):
        resolver_dataset(dataset, "DIJKSTRA", "A", "B")
    relatorio = resolver_dataset(dataset, "DIJKSTRA", "A", "B", deslocamento=1)
    assert relatorio["deslocamento"] == 1
    assert relatorio["resultado"]["caminho"] == ["A", "B"]
    assert relatorio["resultado"]["custo_transformado"] == 0
    inalcançavel = resolver_dataset(dataset, "DIJKSTRA", "A", "D", deslocamento=1)
    assert inalcançavel["resultado"]["status"] == "SEM_CAMINHO"
    assert inalcançavel["resultado"]["custo_transformado"] is None


def test_bellman_exporta_recortes_e_custo_do_ciclo(dataset):
    sem_ciclo = resolver_dataset(dataset, "BELLMAN_FORD", caso="negativo_sem_ciclo")["resultado"]
    assert sem_ciclo["vertices"] == 2
    assert sem_ciclo["distancias"]["BDD"] == -1
    com_ciclo = resolver_dataset(dataset, "BELLMAN_FORD", caso="ciclo_negativo")["resultado"]
    assert com_ciclo["status"] == "CICLO_NEGATIVO"
    assert com_ciclo["ciclo"][0] == com_ciclo["ciclo"][-1]
    assert com_ciclo["custo_ciclo"] == -2
    assert len(com_ciclo["arcos_ciclo"]) == 2
    assert com_ciclo["distancias"] is None


def test_experimentos_reproduzem_todos_os_casos(dataset, tmp_path):
    arquivos = executar_experimentos_dataset(dataset, tmp_path / "experimentos")
    relatorios = {p.name: json.loads(p.read_text(encoding="utf-8")) for p in arquivos}
    assert set(relatorios) == {"bfs_fontes.json", "dfs_fontes.json",
                              "dijkstra_pares.json", "bellman_ford_casos.json"}
    assert len(relatorios["bfs_fontes.json"]["resultados"]) == 3
    assert len(relatorios["dfs_fontes.json"]["resultados"]) == 3
    assert len(relatorios["dijkstra_pares.json"]["resultados"]) == 5
    assert relatorios["dijkstra_pares.json"]["buscas_por_origem"] == 3
    assert [r["status"] for r in relatorios["bellman_ford_casos.json"]["resultados"]] == ["OK", "CICLO_NEGATIVO"]


@pytest.mark.parametrize("opcoes, mensagem", [
    (["--mapa", "mapa.txt"], "not allowed"),
    (["--todos"], "exclusivos dos mapas"),
    (["--alg", "DFS"], "--source"),
    (["--alg", "BELLMAN_FORD"], "--caso"),
    (["--alg", "DFS", "--source", "Z"], "Fonte não encontrada"),
    (["--alg", "BFS", "--source", "A", "--target", "B"], "apenas a fonte"),
    (["--alg", "DIJKSTRA", "--source", "A"], "Destino não encontrado"),
    (["--experimentos", "--source", "A"], "já define"),
])
def test_cli_rejeita_combinacoes_invalidas(dataset, opcoes, mensagem, monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["cli", "--dataset", str(dataset), *opcoes])
    with pytest.raises(SystemExit) as erro:
        main()
    assert erro.value.code == 2
    assert mensagem in capsys.readouterr().err


def test_cli_mapa_continua_funcionando(tmp_path, monkeypatch):
    mapa = tmp_path / "mini.txt"
    mapa.write_text("####\n#SG#\n####\n", encoding="utf-8")
    saida = tmp_path / "mapas"
    monkeypatch.setattr(sys, "argv", ["cli", "--mapa", str(mapa), "--alg", "BFS", "--out", str(saida)])
    main()
    resultado = json.loads((saida / "solucao_mini_BFS.json").read_text(encoding="utf-8"))
    assert resultado["status"] == "OK"
    assert resultado["passos"] == 1
