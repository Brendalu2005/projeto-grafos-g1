# Labirinto com chaves: grafo de estados e comparação de algoritmos

Projeto final de Teoria dos Grafos e Análise e Visualização de Dados (CESAR School, 2026.2).

Na Parte 1, cada mapa de `data/mapas/` vira um grafo de estados. Cada nó guarda a posição, as chaves que o jogador tem e os bônus que já consumiu, e sobre esse grafo rodamos BFS, DFS, Dijkstra e Bellman-Ford. Na Parte 2, os mesmos algoritmos rodam sobre um dataset real, e comparamos corretude e desempenho.

Os quatro algoritmos são implementação nossa. O `networkx` só aparece em `tests/`, como oráculo para conferir os resultados.

## Equipe

| Integrante | GitHub |
|---|---|
| Rafael Padilha | r7fael |
| André | avelinoandre |
| Clarissa | clarissalopes6 |
| Brenda | Brendalu2005 |
| Vinícius Spósito | nogsposito |

## Instalação

Precisa de Python 3.11 ou mais novo.

```bash
git clone https://github.com/Brendalu2005/projeto-grafos-g1.git
cd projeto-grafos-g1
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Linux e macOS
pip install -r requirements.txt
```,

## Como executar

Na raiz do repositório, a execução individual imprime e grava um JSON em `--out`:

```bash
# Parte 1: resolução individual
python -m src.cli --mapa ./data/mapas/m03_tres_chaves.txt --alg BFS --out ./out/parte1/
python -m src.cli --mapa ./data/mapas/m03_tres_chaves.txt --alg DIJKSTRA --out ./out/parte1/
python -m src.cli --mapa ./data/mapas/m05_bonus.txt --alg BELLMAN_FORD --out ./out/parte1/
python -m src.cli --mapa ./data/mapas/m06_fonte.txt --alg BELLMAN_FORD --fonte-consumivel --out ./out/parte1/

# Parte 1: exportações para os oito mapas e data/mapas_grupo/*.txt
python -m src.cli --todos --out ./out/parte1/

# Recalcular todas as exportações com fontes consumíveis; os arquivos ficam
# separados em ./out/parte1/fonte_consumivel/ para não misturar regras.
python -m src.cli --todos --fonte-consumivel --out ./out/parte1/

# --armadilhas é um alias da execução em lote (que também gera as armadilhas).
python -m src.cli --armadilhas --out ./out/parte1/

# Gerar as figuras estáticas da Parte 1
python -m src.viz

# Abrir a interface interativa em http://127.0.0.1:8766/out/parte1/labirinto_interativo.html
python -m src.front.server
```

As exportações em lote incluem arestas, graus, métricas globais, camadas, soluções, classificação DFS, comparação das três modelagens, estados-armadilha, percurso do m03 e ciclo negativo do m06. A interface serve os resultados calculados pelo projeto; execute o servidor a partir da raiz para que mapas e CSVs sejam encontrados. O controle “Regra da fonte” permite comparar o cenário original com a fonte consumível.

Os comandos de execução do dataset da Parte 2 ainda não estão implementados na CLI.

## Testes

```bash
pytest
```

## Estrutura

```
projeto-grafos-g1/
├── README.md
├── requirements.txt
├── pytest.ini
├── docs/                  declaração de IA, registro de uso e relatório
├── data/
│   ├── mapas/             mapas fornecidos (m01 a m08)
│   ├── mapas_grupo/       os 2 mapas criados pelo grupo
│   └── dataset_parte2/    dataset da Parte 2
├── out/
│   ├── parte1/            CSVs, JSONs, figuras e labirinto interativo
│   └── parte2/            relatório de desempenho e gráficos
├── src/
│   ├── cli.py             entrada pela linha de comando
│   ├── solve.py           orquestra as duas partes
│   ├── viz.py             visualizações
│   └── graphs/
│       ├── io.py          leitura e validação dos mapas e do dataset
│       ├── estados.py     grafo de posições e grafo de estados
│       ├── graph.py       lista de adjacência dirigida
│       └── algorithms.py  BFS, DFS, Dijkstra e Bellman-Ford
└── tests/                 testes com pytest
```

## Interface dos algoritmos

`graph.py` representa o grafo dirigido por uma lista de adjacência: cada chave é um vértice e cada valor é uma lista de pares `(destino, peso)`. No grafo de estados, um vértice é `(linha, coluna, chaves, bônus_consumidos)`; a saída é ligada ao vértice virtual `ALVO`.

| Algoritmo | Entrada | Retorno principal |
|---|---|---|
| `bfs(grafo, origem)` | Grafo e vértice de origem | Distâncias em arestas (passos) e predecessores |
| `dfs(grafo, origem, cobrir_todos=False)` | Grafo dirigido e origem | Tempos de descoberta/finalização, predecessores, classificação de arcos e indicador de ciclo |
| `dijkstra(grafo, origem)` | Grafo e origem | Distâncias de menor custo e predecessores; lança `ValueError` se encontrar peso negativo |
| `bellman_ford(grafo, origem)` | Grafo e origem | Distâncias, predecessores e ciclo negativo (ou `None`) |

`resolver()` converte esses retornos em status, custo, passos, caminho e sequência do ciclo, quando houver. A opção `--fonte-consumivel` altera a construção do grafo para que cada fonte `*` tenha peso `-2` na primeira entrada e `1` nas seguintes.

## Dataset da Parte 2

Wiki-RfA: votos de usuários da Wikipédia nas eleições para administrador, de 2003 a maio de 2013. Fonte: [Kaggle](https://www.kaggle.com/datasets/boneacrabonjac/wiki-rfa), versão reduzida do [SNAP](https://snap.stanford.edu/data/wiki-RfA.html). Descrição e pergunta de pesquisa a preencher.

## Uso de IA

Seguimos as regras de IA do enunciado. Todo trecho de código feito com apoio de IA leva a marca `# [IA] <ferramenta> – <finalidade>`, cada uso fica registrado em [`DECLARACAO_IA.md`], e a declaração assinada por todos fica em `docs/DECLARACAO_IA.pdf`.
