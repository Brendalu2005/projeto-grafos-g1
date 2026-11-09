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
```

## Como executar

Os comandos seguem o formato do enunciado e passam a funcionar quando `src/cli.py` estiver pronto.

```bash
# Parte 1 (labirintos)
python -m src.cli --mapa ./data/mapas/m03_tres_chaves.txt --alg BFS --out ./out/parte1/
python -m src.cli --mapa ./data/mapas/m03_tres_chaves.txt --alg DIJKSTRA --out ./out/parte1/
python -m src.cli --mapa ./data/mapas/m05_bonus.txt --alg BELLMAN_FORD --out ./out/parte1/
python -m src.cli --mapa ./data/mapas/m06_fonte.txt --alg BELLMAN_FORD --fonte-consumivel --out ./out/parte1/
python -m src.cli --mapa ./data/mapas/m04_esteiras.txt --armadilhas --out ./out/parte1/
python -m src.cli --mapa ./data/mapas/m03_tres_chaves.txt --interactive --out ./out/parte1/

# Parte 2 (dataset)
python -m src.cli --dataset ./data/dataset_parte2/ --alg DIJKSTRA --source A --target Z --out ./out/parte2/
python -m src.cli --dataset ./data/dataset_parte2/ --benchmark --out ./out/parte2/
```

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

A definir pelo grupo: como `graph.py` representa o grafo e o que cada algoritmo recebe e devolve (distâncias, predecessores e status).

## Dataset da Parte 2

Wiki-RfA: votos de usuários da Wikipédia nas eleições para administrador, de 2003 a maio de 2013. Fonte: [Kaggle](https://www.kaggle.com/datasets/boneacrabonjac/wiki-rfa), versão reduzida do [SNAP](https://snap.stanford.edu/data/wiki-RfA.html). Descrição e pergunta de pesquisa a preencher.

## Uso de IA

Seguimos as regras de IA do enunciado. Todo trecho de código feito com apoio de IA leva a marca `# [IA] <ferramenta> – <finalidade>`, cada uso fica registrado em [`docs/registro_ia.md`](docs/registro_ia.md), e a declaração assinada por todos fica em `docs/DECLARACAO_IA.pdf`.