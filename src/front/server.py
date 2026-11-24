"""Servidor local do front, conectado ao resolvedor oficial do projeto.

Execute na raiz do repositório: python -m src.front.server
"""

# [IA[  ChatGPT (Codex) - ponte HTTP entre src.solve e a interface originalmente gerada pelo Vercel v0.
import json
import argparse
import math
import time
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

from src.graphs.algorithms import bellman_ford, bfs, dfs, dijkstra
from src.graphs.estados import ALVO, construir_g_est, estado_inicial, rotulo
from src.graphs.io import ler_mapa
from src.solve import resolver


ROOT = Path(__file__).resolve().parents[2]
MAP_DIRS = (ROOT / "data" / "mapas", ROOT / "data" / "mapas_grupo")
ALGORITHMS = {"BFS", "DIJKSTRA", "BELLMAN_FORD"}
FUNCOES = {"BFS": bfs, "DFS": dfs, "DIJKSTRA": dijkstra, "BELLMAN_FORD": bellman_ford}
COMPARACOES = {}


def medir(funcao, grafo, origem):
    tempos = []
    saida = None
    inicio = time.perf_counter()
    try:
        saida = funcao(grafo, origem)
    except ValueError:
        return None, [(time.perf_counter() - inicio) * 1000]
    aquecimento = (time.perf_counter() - inicio) * 1000
    if aquecimento > 100:
        tempos.append(aquecimento)
    while len(tempos) < 5 and sum(tempos) < 1000:
        inicio = time.perf_counter()
        try:
            saida = funcao(grafo, origem)
        except ValueError:
            tempos.append((time.perf_counter() - inicio) * 1000)
            return None, tempos
        tempos.append((time.perf_counter() - inicio) * 1000)
    return saida, tempos


def explorar_dfs(grafo, origem):
    descoberta, _, _, classes, _ = dfs(grafo, origem)
    contagem = {tipo: 0 for tipo in ("arvore", "retorno", "avanco", "cruzamento")}
    for tipo in classes.values():
        contagem[tipo] += 1
    ordem = sorted((estado for estado in descoberta if estado != ALVO), key=descoberta.__getitem__)
    return [rotulo(estado) for estado in ordem], contagem


def comparar(caminho, nome, fonte_consumivel):
    chave = (nome, fonte_consumivel)
    if chave in COMPARACOES:
        return COMPARACOES[chave]
    mapa = ler_mapa(str(caminho))
    grafo = construir_g_est(mapa, fonte_consumivel)
    origem = estado_inicial(mapa)
    linhas = []
    for algoritmo, funcao in FUNCOES.items():
        saida, tempos = medir(funcao, grafo, origem)
        if algoritmo == "DFS":
            exploracao, contagem = explorar_dfs(grafo, origem)
            linha = {"mapa": nome, "algoritmo": "DFS", "status": "EXPLORACAO",
                     "exploracao": exploracao, "classificacao_arcos": contagem}
            alcancados = len(exploracao)
        else:
            linha = resolver(str(caminho), algoritmo, fonte_consumivel)
            alcancados = None
            if saida is not None:
                alcancados = sum(1 for estado, valor in saida[0].items() if estado != ALVO and valor != math.inf)
        linha["tempo_ms"] = sum(tempos) / len(tempos)
        linha["execucoes"] = len(tempos)
        linha["estados_alcancados"] = alcancados
        linhas.append(linha)
    resposta = {"mapa": nome, "fonte_consumivel": fonte_consumivel, "algoritmos": linhas}
    COMPARACOES[chave] = resposta
    return resposta


def find_map(name):
    if not name or Path(name).name != name or not name.replace("_", "").replace("-", "").isalnum():
        return None
    for folder in MAP_DIRS:
        candidate = folder / f"{name}.txt"
        if candidate.is_file():
            return candidate
    return None


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_GET(self):
        url = urlsplit(self.path)
        if url.path == "/api/comparar":
            params = parse_qs(url.query)
            name = params.get("mapa", [""])[0]
            fonte_consumivel = params.get("fonte-consumivel", ["false"])[0].lower() in {"1", "true", "yes"}
            path = find_map(name)
            if path is None:
                return self.send_json(404, {"erro": "Mapa não encontrado."})
            try:
                return self.send_json(200, comparar(path, name, fonte_consumivel))
            except (OSError, ValueError, KeyError) as error:
                return self.send_json(422, {"erro": str(error)})
        if url.path != "/api/resultado":
            return super().do_GET()

        params = parse_qs(url.query)
        name = params.get("mapa", [""])[0]
        algorithm = params.get("alg", [""])[0]
        # [IA] ChatGPT (Codex) - recebe a variante de regra da interface.
        fonte_consumivel = params.get("fonte-consumivel", ["false"])[0].lower() in {"1", "true", "yes"}
        path = find_map(name)
        if path is None:
            return self.send_json(404, {"erro": "Mapa não encontrado."})
        if algorithm == "DFS":
            # [IA[  ChatGPT (Codex) - expõe a ordem de descoberta e a classificação calculadas pela DFS oficial.
            try:
                mapa = ler_mapa(str(path))
                graph = construir_g_est(mapa, fonte_consumivel)
                discovered, _, _, classes, _ = dfs(graph, estado_inicial(mapa))
                counts = {key: 0 for key in ("arvore", "retorno", "avanco", "cruzamento")}
                for kind in classes.values():
                    counts[kind] += 1
                order = sorted((state for state in discovered if state != ALVO), key=discovered.__getitem__)
            except (OSError, ValueError, KeyError) as error:
                return self.send_json(422, {"erro": str(error)})
            return self.send_json(200, {
                "mapa": name,
                "algoritmo": algorithm,
                "status": "EXPLORACAO",
                "exploracao": [rotulo(state) for state in order],
                "classificacao_arcos": counts,
            })
        if algorithm not in ALGORITHMS:
            return self.send_json(400, {"erro": "Algoritmo desconhecido."})

        try:
            result = resolver(str(path), algorithm, fonte_consumivel)
        except (OSError, ValueError, KeyError) as error:
            return self.send_json(422, {"erro": str(error)})
        return self.send_json(200, result)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def send_json(self, status, value):
        body = json.dumps(value, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8766)
    args = parser.parse_args()
    server = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    print(f"Front: http://127.0.0.1:{args.port}/out/parte1/labirinto_interativo.html", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
