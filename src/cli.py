import argparse
import json
from pathlib import Path

from src.solve import resolver, resolver_todos, contar_classificacao

# [IA] Claude – sintaxe do argparse
def criar_parser():
    parser = argparse.ArgumentParser(
        prog="python -m src.cli",
        description="Labirinto com chaves (Parte 1) e dataset maior (Parte 2).",
    )
    parser.add_argument("--mapa", help="arquivo .txt de um mapa")
    parser.add_argument(
        "--alg",
        choices=["BFS", "DFS", "DIJKSTRA", "BELLMAN_FORD"],
        help="algoritmo a rodar no grafo de estados",
    )
    parser.add_argument("--out", default="./out/parte1/", help="pasta das saídas")
    parser.add_argument(
        "--fonte-consumivel",
        action="store_true",
        help="cada fonte * só vale -2 na primeira vez (correção do m06)",
    )
    parser.add_argument(
        "--todos", 
        action="store_true", help="roda todos os mapas e gera os CSVs da Parte 1"
    )
    # [IA] ChatGPT – OFERECE ALIAS EXPLICITO
    parser.add_argument("--armadilhas", action="store_true", help="gera as saídas em lote, incluindo estados-armadilha")
    return parser


def main():

    parser = criar_parser()
    args = parser.parse_args()

    # [IA] ChatGPT – GRAVA RESULTADOS NO JSON
    try:
        if args.todos:
            destino = Path(args.out) / ("fonte_consumivel" if args.fonte_consumivel else "")
            resolver_todos(['data/mapas', 'data/mapas_grupo'], destino, args.fonte_consumivel)
            print(f"Saídas gravadas em {destino}")
            return

        if args.armadilhas:
            destino = Path(args.out) / ("fonte_consumivel" if args.fonte_consumivel else "")
            resolver_todos(['data/mapas', 'data/mapas_grupo'], destino, args.fonte_consumivel)
            print(f"Saídas e armadilhas gravadas em {destino}")
            return
    
        if args.mapa is None or args.alg is None:
            parser.error("É preciso passar --mapa e --alg ou --todos.")

        if args.alg == 'DFS':
            resultado = contar_classificacao(args.mapa, args.fonte_consumivel)

        else:
            resultado = resolver(args.mapa, args.alg, args.fonte_consumivel)

        mapa_nome = Path(args.mapa).stem
        sufixo = "_fonte_consumivel" if args.fonte_consumivel else ""
        destino = Path(args.out)
        destino.mkdir(parents=True, exist_ok=True)
        arquivo = destino / f"solucao_{mapa_nome}_{args.alg}{sufixo}.json"
        arquivo.write_text(json.dumps(resultado, ensure_ascii=False, indent=2), encoding="utf-8")
        print(json.dumps(resultado, ensure_ascii=False, indent=2))
        print(f"Resultado gravado em {arquivo}")
    except (OSError, ValueError, KeyError) as error:
        parser.error(str(error))

if __name__ == "__main__":
    main()
