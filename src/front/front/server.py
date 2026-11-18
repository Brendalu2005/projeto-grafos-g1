"""Servidor local do front, conectado ao resolvedor oficial do projeto.

Execute na raiz do repositório: python -m src.front.server
"""

# [IA[  ChatGPT (Codex) - ponte HTTP entre src.solve e a interface originalmente gerada pelo Vercel v0.
import json
import argparse
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

from src.solve import resolver


ROOT = Path(__file__).resolve().parents[2]
MAP_DIRS = (ROOT / "data" / "mapas", ROOT / "data" / "mapas_grupo")
ALGORITHMS = {"BFS", "DIJKSTRA", "BELLMAN_FORD"}


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
        if url.path != "/api/resultado":
            return super().do_GET()

        params = parse_qs(url.query)
        name = params.get("mapa", [""])[0]
        algorithm = params.get("alg", [""])[0]
        path = find_map(name)
        if path is None:
            return self.send_json(404, {"erro": "Mapa não encontrado."})
        if algorithm == "DFS":
            return self.send_json(200, {"mapa": name, "algoritmo": algorithm,
                                        "status": "PENDENTE", "caminho": "", "custo": ""})
        if algorithm not in ALGORITHMS:
            return self.send_json(400, {"erro": "Algoritmo desconhecido."})

        try:
            result = resolver(str(path), algorithm)
        except (OSError, ValueError, KeyError) as error:
            return self.send_json(422, {"erro": str(error)})
        return self.send_json(200, result)

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
