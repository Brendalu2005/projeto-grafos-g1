import argparse
import json
from pathlib import Path

from src.solve import (resolver, resolver_todos, contar_classificacao, CASOS_BELLMAN,
                       resolver_dataset, executar_experimentos_dataset, salvar_resultado_dataset)

# [IA] Claude – sintaxe do argparse
def criar_parser():
    parser = argparse.ArgumentParser(
        prog="python -m src.cli",
        description="Labirinto com chaves (Parte 1) e dataset maior (Parte 2).",
    )
    # [IA] ChatGPT (Codex) – seleção explícita entre mapa e dataset.
    entrada = parser.add_mutually_exclusive_group()
    entrada.add_argument("--mapa", help="arquivo .txt de um mapa")
    entrada.add_argument("--dataset", help="CSV tratado da Parte 2, com a coluna PESO")
    parser.add_argument(
        "--alg",
        choices=["BFS", "DFS", "DIJKSTRA", "BELLMAN_FORD"],
        help="algoritmo a executar",
    )
    parser.add_argument("--out", help="pasta das saídas (padrão: out/parte1 ou out/parte2)")
    # [IA] ChatGPT (Codex) – parâmetros de chamada das funções existentes da Parte 2.
    parser.add_argument("--source", help="usuário de origem no dataset")
    parser.add_argument("--target", help="usuário de destino para Dijkstra no dataset")
    parser.add_argument("--deslocamento", type=int, help="somar este inteiro aos pesos de Dijkstra; padrão 0")
    parser.add_argument("--caso", choices=list(CASOS_BELLMAN), help="recorte de Bellman-Ford definido no notebook")
    parser.add_argument("--experimentos", action="store_true", help="reproduz os experimentos registrados da Parte 2")
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

    # [IA] ChatGPT (Codex) – validação das combinações e encaminhamento da Parte 2.
    if args.dataset:
        if args.todos or args.armadilhas or args.fonte_consumivel:
            parser.error("--todos, --armadilhas e --fonte-consumivel são exclusivos dos mapas.")
        if args.experimentos:
            if any(valor is not None for valor in (args.alg, args.source, args.target, args.caso, args.deslocamento)):
                parser.error("--experimentos já define algoritmos, fontes, pares, recortes e transformação.")
        elif args.alg is None:
            parser.error("Com --dataset, informe --alg ou --experimentos.")
        elif args.alg == "BELLMAN_FORD":
            if args.caso is None:
                parser.error("Com BELLMAN_FORD, informe --caso para executar um dos recortes registrados.")
        elif args.source is None:
            parser.error("Informe --source para executar BFS, DFS ou DIJKSTRA no dataset.")
        args.out = args.out or "./out/parte2/"
        try:
            if args.experimentos:
                arquivos = executar_experimentos_dataset(args.dataset, args.out)
                for arquivo in arquivos:
                    print(f"Resultado gravado em {arquivo}")
            else:
                resultado = resolver_dataset(args.dataset, args.alg, args.source, args.target,
                                             args.caso, args.deslocamento or 0)
                sufixo = f"_{args.caso}" if args.caso else ""
                arquivo = Path(args.out) / f"solucao_dataset_{args.alg}{sufixo}.json"
                salvar_resultado_dataset(resultado, arquivo)
                print(f"Resultado gravado em {arquivo}")
        except (OSError, ValueError, KeyError) as error:
            parser.error(str(error))
        return
    if args.experimentos or any(valor is not None for valor in (args.source, args.target, args.caso, args.deslocamento)):
        parser.error("--source, --target, --caso, --deslocamento e --experimentos exigem --dataset.")
    args.out = args.out or "./out/parte1/"

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
