# Teoria dos Grafos: labirintos e Wiki-RfA

Projeto de Teoria dos Grafos e Análise e Visualização de Dados — CESAR School, 2026.2.

- **Parte 1:** modelagem de labirintos como grafos de estados, considerando posição, chaves e bônus.
- **Parte 2:** análise de votos da Wikipédia com o dataset Wiki-RfA.

As duas partes utilizam BFS, DFS, Dijkstra e Bellman-Ford. O `networkx` é usado somente nos testes, como referência para conferir os resultados.

## Instalação

Requer Python 3.11 ou superior. Clone o repositório e crie o ambiente virtual:

```bash
git clone https://github.com/Brendalu2005/projeto-grafos-g1.git
cd projeto-grafos-g1
python -m venv .venv
```

Ative o ambiente conforme seu sistema:

```powershell
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
```

```bash
# Linux ou macOS
source .venv/bin/activate
```

Instale as dependências:

```bash
python -m pip install -r requirements.txt
```

Execute os comandos abaixo **na raiz do repositório**, com o ambiente ativado.

## Parte 1 — Labirintos

Para gerar os resultados de todos os mapas:

```bash
python -m src.cli --todos
```

Os resultados ficam em `out/parte1/`. Para abrir a interface interativa das duas partes:

```bash
python -m src.front.server
```

Acesse [a interface do projeto](http://127.0.0.1:8766/): a Parte 1 reúne os labirintos; a Parte 2, as figuras e o grafo interativo do dataset. Para resolver apenas um mapa, consulte `python -m src.cli --help`.

## Parte 2 — Dataset Wiki-RfA

O [Wiki-RfA no Kaggle](https://www.kaggle.com/datasets/boneacrabonjac/wiki-rfa) é uma versão reduzida do dataset [SNAP](https://snap.stanford.edu/data/wiki-RfA.html), com votos em candidaturas a administrador da Wikipédia.

Cada usuário é um vértice e cada voto é um arco dirigido do eleitor para o candidato. O grafo tratado tem **11.376 vértices e 196.614 arcos**, preservando laços e arcos paralelos.

| Coluna | Significado |
|---|---|
| `SOURCE` | Usuário que votou; origem do arco. |
| `TARGET` | Candidato que recebeu o voto; destino do arco. |
| `VOTE` | Voto original: −1 contrário, 0 neutro e 1 favorável. |
| `RESULT` | Resultado da candidatura: −1 rejeição e 1 aprovação. |
| `PESO` | Peso calculado no tratamento, separado do voto original. |

O CSV bruto contém 198.275 registros. Os 1.661 sem `SOURCE` são excluídos da construção do grafo e preservados no arquivo bruto. Para linhas idênticas em `SOURCE`, `TARGET`, `VOTE` e `RESULT`, o peso recebe um incremento por ocorrência: `VOTE`, `VOTE + 1`, `VOTE + 2` e assim por diante, na ordem original.

**Pergunta de pesquisa:** como a transformação dos pesos negativos para permitir o uso de Dijkstra altera os caminhos mínimos e a interpretação dos custos no Wiki-RfA?

Dijkstra utiliza `PESO + 1` para eliminar os pesos negativos. Essa transformação pode mudar os caminhos mínimos, pois acrescenta uma unidade por arco percorrido. BFS e DFS ignoram os pesos; Bellman-Ford utiliza `PESO`.

### Preparar os dados e executar

No VS Code, abra os notebooks com suporte a Jupyter e selecione o Python da `.venv`:

1. [preparacao_dataset_wikiRfA.ipynb](data/dataset_parte2/preparacao_dataset_wikiRfA.ipynb): execute as células em ordem, com o diretório de trabalho em `data/dataset_parte2/`. Ele baixa os dados, faz o tratamento, calcula os pesos e exporta o CSV tratado e as métricas.
2. [experimentos_parte2.ipynb](data/dataset_parte2/experimentos_parte2.ipynb): reúne os casos dos algoritmos, o benchmark e a consolidação. Para consolidar os resultados já salvos, execute somente a seção 1 e depois as seções 16 e 17, sem repetir as medições.

Os CSVs não são versionados. O arquivo necessário para os experimentos é `data/dataset_parte2/processed/wikiRfA_tratado.csv`.

Como alternativa ao notebook, reproduza os casos dos quatro algoritmos pela CLI:

```bash
python -m src.cli --dataset data/dataset_parte2/processed/wikiRfA_tratado.csv --experimentos
```

As saídas ficam em `out/parte2/`. Esse comando gera os casos, sem executar o benchmark. Para gerar as sete figuras, com os CSVs e os JSONs de resultados disponíveis:

```bash
python -m src.viz --parte2
```

As exportações e as figuras substituem os arquivos de mesmo nome. Use `--out outra_pasta` para salvar uma execução separadamente. Os procedimentos específicos de benchmark estão no notebook de experimentos.

## Testes

```bash
python -m pytest -q
```

## Estrutura do projeto

```text
projeto-grafos-g1/
├── data/
│   ├── mapas/                       mapas fornecidos
│   ├── mapas_grupo/                 mapas criados pela equipe
│   └── dataset_parte2/
│       ├── preparacao_dataset_wikiRfA.ipynb
│       ├── experimentos_parte2.ipynb
│       ├── raw/                     CSV bruto, gerado pelo notebook
│       └── processed/               CSV tratado, gerado pelo notebook
├── src/
│   ├── cli.py                       execução pela linha de comando
│   ├── solve.py                     integração dos algoritmos e resultados
│   ├── graphs/                      representação, leitura, métricas e algoritmos
│   ├── benchmark.py                 benchmark de BFS e Dijkstra
│   ├── benchmark_dfs_bellman.py      benchmark de DFS e Bellman-Ford
│   ├── viz.py                       geração das figuras
│   └── front/                       interface interativa das Partes 1 e 2
├── out/
│   ├── parte1/                      resultados e interface dos labirintos
│   └── parte2/                      casos, métricas, benchmarks, figuras e relatório JSON
├── docs/                            relatório, justificativas e registros de IA
├── tests/                           testes automatizados
├── requirements.txt                 dependências
└── pytest.ini                       configuração dos testes
```

## Documentação

- [Relatório G1 (PDF)](docs/Relat%C3%B3rio%20-%20G1.pdf)
- [Declaração de uso de IA assinada (PDF)](docs/DECLARACAO_USO_IA_2026-2.docx_assinado_assinado_assinado_assinado_assinado.pdf)

## Equipe

| Integrante | GitHub |
|---|---|
| Rafael Padilha | r7fael |
| André | avelinoandre |
| Clarissa | clarissalopes6 |
| Brenda | Brendalu2005 |
| Vinícius Spósito | nogsposito |
