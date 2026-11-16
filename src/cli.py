import argparse

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
    return parser


def main():

    parser = criar_parser()
    args = parser.parse_args()

    if args.todos:
        resolver_todos(['data/mapas', 'data/mapas_grupo'], args.out)
        print(f"CSVs gravados em {args.out}")
        return
    
    if args.mapa is None or args.alg is None:
        parser.error("É preciso passar --mapa e --alg ou --todos.")

    if args.alg == 'DFS':
        print(contar_classificacao(args.mapa))

    else:
        print(resolver(args.mapa, args.alg, args.fonte_consumivel))

if __name__ == "__main__":
    main()