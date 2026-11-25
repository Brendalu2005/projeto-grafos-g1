"""Exporta verificações reproduzíveis de outliers e um rastreio esperado do DFS."""

# [IA] ChatGPT (Codex) – conferências técnicas e evidências, sem modificar os dados ou os algoritmos. !andre!
import argparse
import hashlib
import json
from pathlib import Path

import pandas as pd

from src.graphs.algorithms import dfs
from src.graphs.io import carregar_dataset


def verificar_outliers(caminho_csv, caminho_bruto):
    caminho_csv, caminho_bruto = Path(caminho_csv), Path(caminho_bruto)
    dados = pd.read_csv(caminho_csv)
    bruto = pd.read_csv(caminho_bruto, index_col=0)
    colunas = ["SOURCE", "TARGET", "VOTE", "RESULT"]
    mantidos = bruto.dropna(subset=["SOURCE"])
    iguais = dados[colunas].equals(mantidos[colunas].reset_index(drop=True))
    peso_esperado = dados["VOTE"] + dados.groupby(colunas, sort=False).cumcount()
    if not iguais or not dados["PESO"].equals(peso_esperado):
        raise ValueError("Dados tratados ou pesos diferem da regra registrada.")
    vertices = pd.Index(pd.unique(dados[["SOURCE", "TARGET"]].to_numpy().ravel()))
    resultado = {
        "sha256_tratado": hashlib.sha256(caminho_csv.read_bytes()).hexdigest(),
        "sha256_bruto": hashlib.sha256(caminho_bruto.read_bytes()).hexdigest(),
        "registros_brutos": len(bruto), "registros_tratados": len(dados),
        "registros_sem_source_excluidos": len(bruto) - len(mantidos),
        "ordem_e_colunas_originais_preservadas": iguais,
        "regra_peso_confere_em_todas_as_linhas": True,
        "novas_remocoes_ou_alteracoes": 0,
        "criterio_graus": "fora de [Q1 - 1,5 IQR; Q3 + 1,5 IQR]; quantis lineares; inclui graus zero",
        "graus": {},
    }
    for direcao, coluna in (("entrada", "TARGET"), ("saida", "SOURCE")):
        graus = dados[coluna].value_counts().reindex(vertices, fill_value=0)
        q1, q3 = graus.quantile([0.25, 0.75])
        inferior, superior = q1 - 1.5 * (q3 - q1), q3 + 1.5 * (q3 - q1)
        sinalizados = graus[(graus < inferior) | (graus > superior)]
        maiores = []
        for usuario, grau in graus.sort_values(ascending=False, kind="stable").head(5).items():
            registros = dados.loc[dados[coluna] == usuario]
            registros_brutos = mantidos.loc[mantidos[coluna] == usuario]
            evidencia = {"usuario": usuario, "grau": int(grau), "ocorrencias_no_bruto_mantido": len(registros_brutos),
                         "pares_distintos": int(registros[["SOURCE", "TARGET"]].drop_duplicates().shape[0]),
                         "lacos": int((registros["SOURCE"] == registros["TARGET"]).sum()),
                         "repeticoes_exatas_apos_primeira": int(registros.duplicated(colunas).sum()),
                         "primeiros_indices_brutos": [int(i) for i in registros_brutos.index[:5]]}
            if evidencia["grau"] != evidencia["ocorrencias_no_bruto_mantido"]:
                raise ValueError("Grau extremo não coincide com o CSV bruto.")
            maiores.append(evidencia)
        resultado["graus"][direcao] = {"q1": float(q1), "q3": float(q3), "limite_inferior": float(inferior),
            "limite_superior": float(superior), "quantidade_sinalizada": len(sinalizados),
            "usuarios_sinalizados": {str(u): int(g) for u, g in sinalizados.items()},
            "cinco_maiores_conferidos_no_bruto": maiores,
            "tratamento_aplicado": "nenhum; preservados conforme o CSV tratado existente"}
    extremos = dados.loc[dados["PESO"] >= 4]
    resultado["pesos_altos"] = {
        "criterio_investigacao": "PESO >= 4; cauda rara da distribuição, sem presumir erro",
        "minimo": int(dados["PESO"].min()), "maximo": int(dados["PESO"].max()),
        "ocorrencias": [{"indice_tratado": int(i), "indice_bruto": int(mantidos.index[i]), **r}
                        for i, r in extremos.to_dict(orient="index").items()],
        "regra_incremento_confere": True,
        "tratamento_aplicado": "nenhum; valores explicados pelo incremento dentro dos grupos repetidos",
    }
    resultado["result"] = {"dominio_valido": bool(dados["RESULT"].isin([-1, 1]).all()),
        "targets_com_result_distinto": int((dados.groupby("TARGET")["RESULT"].nunique() > 1).sum()),
        "tratamento_aplicado": "nenhum; não atribuir resultado único por TARGET"}
    return resultado


def conferir_dfs(caminho_csv):
    grafo = {
        "A": [("B", 1), ("B", 2), ("D", 1), ("F", 1)],
        "B": [("C", 1)], "C": [("A", 1), ("D", 1)],
        "D": [], "F": [("D", 1)], "E": [("D", 1)],
    }
    esperados = (
        {"A": 1, "B": 2, "C": 3, "D": 4, "F": 8},
        {"D": 5, "C": 6, "B": 7, "F": 9, "A": 10},
        {"A": None, "B": "A", "C": "B", "D": "C", "F": "A"},
        {("A", "B", 0): "arvore", ("B", "C", 0): "arvore", ("C", "A", 0): "retorno",
         ("C", "D", 1): "arvore", ("A", "B", 1): "avanco", ("A", "D", 2): "avanco",
         ("A", "F", 3): "arvore", ("F", "D", 0): "cruzamento"}, True,
    )
    obtidos = dfs(grafo, "A")
    if obtidos != esperados:
        raise ValueError("DFS difere do rastreio esperado do exemplo de quatro tipos de arco.")
    completo = carregar_dataset(caminho_csv)
    usuarios = ["Rcsprinter123", "Jasper Deng"]
    recorte = {u: [(v, p) for v, p in completo[u] if v in usuarios] for u in usuarios}
    esperado_real = ({"Rcsprinter123": 1, "Jasper Deng": 2},
                     {"Jasper Deng": 3, "Rcsprinter123": 4},
                     {"Rcsprinter123": None, "Jasper Deng": "Rcsprinter123"},
                     {("Rcsprinter123", "Jasper Deng", 0): "arvore",
                      ("Jasper Deng", "Rcsprinter123", 0): "retorno"}, True)
    if dfs(recorte, usuarios[0]) != esperado_real:
        raise ValueError("DFS difere do rastreio esperado no recorte do dataset.")
    casos = []
    for nome, entrada, fonte, retorno in (("quatro_tipos_e_paralelos", grafo, "A", esperados),
                                        ("ciclo_dataset", recorte, usuarios[0], esperado_real)):
        d, f, p, classificacao, ciclo = retorno
        casos.append({"caso": nome, "grafo": entrada, "fonte": fonte, "descoberta": d,
                      "termino": f, "predecessores": p, "tem_ciclo": ciclo,
                      "arcos": [{"origem": u, "destino": v, "indice_adjacencia": i, "tipo": tipo}
                                for (u, v, i), tipo in classificacao.items()], "confere": True})
    return {"metodo": "comparação automática com valores esperados explicitados independentemente da execução",
            "conferencia_manual_do_integrante": False, "casos": casos}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", default="data/dataset_parte2/processed/wikiRfA_tratado.csv")
    parser.add_argument("--bruto", default="data/dataset_parte2/raw/wikiRfA.csv")
    parser.add_argument("--out", default="out/parte2")
    args = parser.parse_args()
    pasta = Path(args.out)
    pasta.mkdir(parents=True, exist_ok=True)
    resultados = {"verificacao_outliers.json": verificar_outliers(args.dataset, args.bruto),
                  "conferencia_tecnica_dfs.json": conferir_dfs(args.dataset)}
    for nome, resultado in resultados.items():
        (pasta / nome).write_text(json.dumps(resultado, ensure_ascii=False, indent=2, allow_nan=False), encoding="utf-8")
        print(pasta / nome)


if __name__ == "__main__":
    main()
