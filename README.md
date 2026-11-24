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

### Parte 2: dataset

Primeiro, execute `data/dataset_parte2/baixar_wikiRfA.ipynb` para obter o CSV bruto e
exportar `data/dataset_parte2/processed/wikiRfA_tratado.csv`. O arquivo tratado deve
conter `SOURCE`, `TARGET`, `VOTE`, `RESULT` e `PESO`. A CLI recebe o caminho desse
arquivo, não a pasta, e não reaplica o tratamento nem o incremento das repetições.

Na raiz do repositório:

```powershell
# Reproduzir os experimentos registrados: BFS/DFS em três fontes,
# Dijkstra em cinco pares com PESO + 1 e os dois recortes de Bellman-Ford.
python -m src.cli --dataset data/dataset_parte2/processed/wikiRfA_tratado.csv --experimentos --out out/parte2/

# Uma busca DFS ou BFS, sem considerar os pesos.
python -m src.cli --dataset data/dataset_parte2/processed/wikiRfA_tratado.csv --alg DFS --source Siva1979
python -m src.cli --dataset data/dataset_parte2/processed/wikiRfA_tratado.csv --alg BFS --source Siva1979

# Dijkstra com a transformação documentada por Brenda.
python -m src.cli --dataset data/dataset_parte2/processed/wikiRfA_tratado.csv --alg DIJKSTRA --source Siva1979 --target "Dieter Simon" --deslocamento 1

# Casos de Bellman-Ford já selecionados e conferidos no notebook.
python -m src.cli --dataset data/dataset_parte2/processed/wikiRfA_tratado.csv --alg BELLMAN_FORD --caso negativo_sem_ciclo
python -m src.cli --dataset data/dataset_parte2/processed/wikiRfA_tratado.csv --alg BELLMAN_FORD --caso ciclo_negativo
```

O destino padrão é `out/parte2/` para datasets e `out/parte1/` para mapas.
Uma execução individual grava `solucao_dataset_<ALGORITMO>.json`; Bellman-Ford
inclui também o nome do caso. Repetir a execução com o mesmo algoritmo e destino
sobrescreve esse arquivo; use pastas diferentes em `--out` para guardar execuções
individuais separadamente. `--experimentos` grava `bfs_fontes.json`, `dfs_fontes.json`,
`dijkstra_pares.json` e `bellman_ford_casos.json`, reproduzindo os resultados do notebook.
As métricas continuam sendo calculadas pelo notebook de tratamento.

O deslocamento é exclusivo do Dijkstra e vale zero por padrão: sem a opção,
o algoritmo recusa o grafo se houver peso negativo. Com `--deslocamento 1`, o custo
exportado usa `PESO + 1`, não os pesos originais. BFS e DFS ignoram os pesos.
O DFS exporta tempos de descoberta e término, que são contadores de eventos,
não medições de desempenho. Usuários inalcançáveis têm distância `null`.

Na CLI, Bellman-Ford executa somente os dois recortes registrados, com suas fontes
fixas e PESO sem deslocamento. A saída identifica cada arco do ciclo e seu custo;
não apresenta distâncias provisórias do caso com ciclo negativo como mínimos finitos.
Outros recortes devem ser definidos e conferidos pelo grupo antes de serem integrados.

Esta integração não executa o benchmark e não gera `parte2_report.json`.
As opções `--dataset` e `--mapa` são mutuamente exclusivas. Parâmetros específicos
dos mapas não são aceitos com dataset. Use `python -m src.cli --help` para consultar as opções.

**Apoio de IA:** ChatGPT (Codex) auxiliou na integração, nos testes e na documentação
da CLI da Parte 2, conforme autorização de André. Os algoritmos existentes não foram
reescritos. As escolhas de fontes, pares, recortes e transformação seguem o notebook.

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
│   ├── benchmark.py       recortes, seleção de fontes e medição da Parte 2
│   ├── viz.py             visualizações
│   └── graphs/
│       ├── io.py          leitura e validação dos mapas e do dataset
│       ├── estados.py     grafo de posições e grafo de estados
│       ├── graph.py       lista de adjacência dirigida
│       ├── metricas_dataset.py  métricas do dataset da Parte 2
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

O dataset Wiki-RfA reúne votos nas eleições para administrador da Wikipédia, de 2003 a maio de 2013. O arquivo utilizado vem do [Kaggle](https://www.kaggle.com/datasets/boneacrabonjac/wiki-rfa), em uma versão reduzida do dataset [SNAP](https://snap.stanford.edu/data/wiki-RfA.html). A aprovação pelas duas professoras foi confirmada pela equipe.

### Pergunta de pesquisa

Como a transformação dos pesos negativos para permitir o uso de Dijkstra altera os caminhos mínimos e a interpretação dos custos no grafo Wiki-RfA?

### Atributos e representação

| Coluna | Tipo e significado |
|---|---|
| `SOURCE` | Texto: usuário que votou; origem do arco. |
| `TARGET` | Texto: candidato que recebeu o voto; destino do arco. |
| `VOTE` | Inteiro: -1 para voto contrário, 0 para neutro e 1 para favorável. |
| `RESULT` | Inteiro: -1 para rejeição da candidatura e 1 para aprovação. |
| `PESO` | Inteiro calculado no tratamento, preservando `VOTE` separadamente. |

Cada usuário é um vértice e cada registro tratado é um arco dirigido de eleitor para candidato. Usuários que aparecem apenas como destino também entram no grafo. Laços e arcos paralelos são mantidos. Os valores negativos têm origem nos votos contrários.

O arquivo bruto tem 198.275 registros. Foram retirados do conjunto usado no grafo 1.661 registros sem `SOURCE`, restando 196.614. Esses registros continuam preservados no CSV original. As conferências de repetições, laços, faltantes e domínios estão no notebook de tratamento e em [docs/avd_log.md](docs/avd_log.md).

Para cada grupo idêntico em `SOURCE`, `TARGET`, `VOTE` e `RESULT`, o peso é `PESO = VOTE + número da ocorrência`, começando em zero e respeitando a ordem original. Nenhuma ocorrência é removida por essa regra. Para Dijkstra, outra versão do grafo usa `PESO + 1`, pois o menor `PESO` conferido é -1. Esse deslocamento pode mudar os caminhos mínimos e os custos: um caminho com k arcos recebe k unidades adicionais.

A versão reduzida não contém datas nem identificadores das eleições. Não é possível separar eleições diferentes apenas por candidato. A causa dos valores ausentes não foi determinada; as conclusões sobre o grafo se restringem aos registros mantidos.

### Caracterização do grafo tratado

| Métrica | Resultado |
|---|---:|
| Vértices | 11.376 |
| Arcos, incluindo paralelos e laços | 196.614 |
| Laços, contando ocorrências | 103 |
| Pares dirigidos distintos, incluindo laços | 188.077 |
| Pares dirigidos distintos sem laço | 187.984 |
| Densidade dos pares sem laço | 0,0014527 |
| Grau de entrada: mínimo / máximo / média | 0 / 978 / 17,2832 |
| Grau de saída: mínimo / máximo / média | 0 / 1.232 / 17,2832 |
| Votos originais negativos (`VOTE`) | 20,68% |
| Pesos ajustados negativos (`PESO`) | 20,169% |

Cada arco paralelo conta nos graus; um laço soma um ao grau de entrada e um ao de saída. A densidade usa pares distintos sem laço divididos por `|V| * (|V| - 1)`, não a quantidade total de arcos. Os resultados completos, incluindo distribuições de graus, estão em [metricas_dataset.json](out/parte2/metricas_dataset.json).

### Como reproduzir pelos notebooks

Com o ambiente virtual e as dependências instalados, abra os notebooks no VS Code com suporte a Jupyter e selecione o kernel Python da `.venv`:

1. Abra [baixar_wikiRfA.ipynb](data/dataset_parte2/baixar_wikiRfA.ipynb) e execute as células em ordem, com o diretório de trabalho em `data/dataset_parte2/`. O download usa `raw/`; o notebook trata os registros, calcula `PESO`, exporta `processed/wikiRfA_tratado.csv` e salva as métricas em `out/parte2/metricas_dataset.json`.
2. Abra [experimentos_parte2.ipynb](data/dataset_parte2/experimentos_parte2.ipynb). Execute a preparação e o carregamento das seções 1 e 2. Ele usa o CSV tratado e não depende das variáveis do primeiro notebook. Pode ser iniciado na raiz do projeto ou em uma pasta interna.
3. Execute em ordem as seções de BFS, transformação e Dijkstra para gerar os casos obrigatórios. As seções 8 a 11 contêm os experimentos de DFS e os casos de Bellman-Ford.
4. Para o benchmark de BFS e Dijkstra, execute as seções 12 a 15, após 1 e 2. Elas preparam recortes e fontes, calculam alcance fora do cronômetro, fazem as medições e exportam o ambiente e os resultados. Não é necessário executar DFS ou Bellman-Ford para essas medições.

O benchmark usa recortes aninhados de 10%, 50% e 100% dos arcos embaralhados com semente 42. As fontes selecionadas no menor recorte são `Siva1979`, `Gwynand` e `John Carter`. Cada configuração tem um aquecimento fora do cronômetro e cinco repetições medidas. O procedimento está nas seções 12 a 15 do [notebook de experimentos](data/dataset_parte2/experimentos_parte2.ipynb), com as funções de preparação e medição em [src/benchmark.py](src/benchmark.py).

A exportação do ambiente usa `psutil` opcionalmente para obter a memória. Se a biblioteca não estiver instalada, o campo fica `null` e deve ser completado antes da consolidação. Os CSVs são ignorados pelo Git; para uma nova instalação, gere o tratado pelo notebook. Executar as células de exportação novamente sobrescreve os respectivos arquivos de saída.

Para medir BFS e Dijkstra na máquina usada por André, execute na raiz do projeto,
com o ambiente virtual ativado e a mesma versão de Python e das dependências
usada nas medições de DFS/Bellman-Ford:

```powershell
Get-FileHash -LiteralPath data/dataset_parte2/processed/wikiRfA_tratado.csv -Algorithm SHA256
python -m src.benchmark --dataset data/dataset_parte2/processed/wikiRfA_tratado.csv --out out/parte2/benchmark_bfs_dijkstra_mesmo_ambiente.json
```

Confira o hash antes de medir. O CSV de referência tem SHA-256
`de16066d90875782f2daffae3adbe5c513f0fa9743ad242d3e1fcbf5c635e7c2`,
também registrado no benchmark anterior de DFS/Bellman-Ford. Se houver diferença,
alinhem o CSV antes de iniciar. As duas máquinas devem usar a mesma versão dos
algoritmos e das regras de recorte.

O comando reutiliza os algoritmos existentes, confere os conjuntos alcançados
fora do cronômetro e mede 18 configurações: dois algoritmos, três fontes e três
tamanhos. São um aquecimento e cinco repetições medidas por configuração.
O JSON registra o hash do CSV, ambiente, alcance, estatísticas e `completo`.
Somente `completo: true` indica o término das 18 configurações. A saída é
atualizada após cada configuração; o executor recusa uma saída já existente.
Ao terminar, André deve devolver `benchmark_bfs_dijkstra_mesmo_ambiente.json`
para conferência e consolidação. Essa execução não altera os JSONs anteriores,
as figuras ou `parte2_report.json`.

Para testar somente a estrutura do benchmark, na raiz do projeto:

```bash
python -m pytest tests/test_benchmark.py -v
```

### Resultados disponíveis e consolidação

| Arquivo em `out/parte2/` | Conteúdo |
|---|---|
| `metricas_dataset.json` | Caracterização do grafo tratado. |
| `bfs_fontes.json` | Resultados de BFS em três fontes. |
| `dijkstra_pares.json` | Caminhos e custos transformados de cinco pares. |
| `dfs_fontes.json` | Resultados de DFS em três fontes. |
| `bellman_ford_casos.json` | Casos pequenos com e sem ciclo negativo; não substituem o benchmark de escalabilidade. |
| `benchmark_bfs_dijkstra.json` | Histórico: primeira medição de BFS e Dijkstra, preservada na máquina de Brenda. |
| `benchmark_bfs_dijkstra_mesmo_ambiente.json` | Medição atual de BFS/Dijkstra na máquina de André: 18 configurações e 90 tempos. |
| `benchmark_dfs_bellman.json` | 16 configurações, 80 tempos medidos, estatísticas e ambiente de DFS e Bellman-Ford; apenas uma fonte de Bellman-Ford em 100%, conforme decisão de André. |
| `parte2_report.json` | Casos obrigatórios e 34 configurações dos quatro algoritmos, com 170 tempos e ambientes conferidos. |
| `estudo_transformacao.json` | Exemplo selecionado de dois caminhos, com empate após PESO + 1; não representa a rede inteira. |
| `verificacao_outliers.json` | Conferência do tratamento, pesos elevados e graus extremos contra o CSV bruto. |
| `conferencia_tecnica_dfs.json` | Conferência automática com valores esperados; não é uma conferência manual de André. |

O relatório `out/parte2/parte2_report.json` está consolidado. Para reproduzir sua
conferência e exportação, execute a seção 1 e depois as seções 16 e 17 do notebook
de experimentos: elas leem os JSONs existentes sem executar benchmarks. O
dicionário `arquivos_benchmark` seleciona os arquivos. Hashes, estatísticas,
fontes, tamanhos e alcance são conferidos antes da gravação.

Os quatro algoritmos têm medições em 10%, 50% e 100%, com cinco repetições por
configuração. Bellman-Ford tem uma fonte em 100%; três fontes são explicitamente
exigidas pelos critérios para BFS/DFS, não para cada tamanho de Bellman-Ford.
As duas fontes adicionais completariam o plano ampliado e podem ser acrescentadas
sem repetir as medições anteriores. Essa cobertura e suas limitações estão
registradas no relatório; não se considera a mera existência de `completo: true`
como comprovação de três fontes em 100%.

### Benchmark de DFS e Bellman-Ford

Na raiz do projeto, com o CSV tratado disponível:

```powershell
python -m src.benchmark_dfs_bellman
```

O executor usa `criar_recortes`, `selecionar_fontes` e `medir_algoritmo`, de
`src/benchmark.py`, com a mesma semente, recortes e fontes de BFS/Dijkstra.
DFS e Bellman-Ford recebem `PESO`, sem deslocamento. Apenas a chamada do algoritmo
entra no tempo: leitura, preparação, contagem de alcance e exportação ficam fora.
Cada configuração tem um aquecimento e cinco repetições medidas.

DFS usa três fontes nos três tamanhos. Por decisão de André durante a execução,
Bellman-Ford preserva as três fontes em 10% e 50% e usa apenas `Siva1979` em 100%.
São 16 configurações e 80 tempos medidos. Para reproduzir a alternativa de três
fontes também em 100%, use `--fontes-bellman-completo 3` com outro arquivo de saída.

As configurações concluídas são salvas em `out/parte2/benchmark_dfs_bellman.json`.
O campo `completo` fica falso durante a execução e só muda para verdadeiro após
concluir todas as configurações. Um arquivo parcial não atende à entrega completa.
O executor registra seu próprio ambiente; preserve os ambientes de cada contribuição
na consolidação. Ele não modifica o benchmark entregue por Brenda nem gera o
relatório final `parte2_report.json`.

Para preservar medições anteriores, o executor recusa uma saída que já existe.
Em uma nova execução, use outro nome:

```powershell
python -m src.benchmark_dfs_bellman --out out/parte2/benchmark_dfs_bellman_nova_execucao.json
```

Para completar apenas as duas fontes de Bellman-Ford ainda não medidas em 100%,
se o grupo mantiver esse plano ampliado, execute na mesma máquina e ambiente
registrados na base, sem sobrescrevê-la:

```powershell
python -m src.benchmark_dfs_bellman --complementar out/parte2/benchmark_dfs_bellman.json --out out/parte2/benchmark_dfs_bellman_completo.json
```

O complemento confere hash e ambiente, preserva os tempos existentes e exige novo
destino. Depois de concluído, selecione esse arquivo no dicionário da seção 16
do notebook e execute as seções 16 e 17. Isso não deve ser executado como etapa
automática de geração das figuras ou de revisão da entrega.

O Bellman-Ford atual faz todas as passagens pelo grafo; as configurações maiores
podem demorar. Os dois casos mínimos de correção não substituem estas medições.

<!-- [IA] ChatGPT (Codex) – documentação da execução de benchmark solicitada por André. -->

<!-- [IA] ChatGPT (Codex) – organização da documentação da Parte 2 com as decisões e os resultados já registrados pela equipe. -->

### Visualizações da Parte 2

Com os CSVs bruto e tratado, as métricas, os dois benchmarks e o
`estudo_transformacao.json` (seção 20 do notebook) já disponíveis,
gere as sete figuras implementadas, na raiz do projeto, sem executar novamente os algoritmos:

```powershell
python -m src.viz --parte2
```

As saídas são `andre_01_distribuicao_graus.png`, `andre_02_distribuicao_pesos.png`,
`andre_03_tempos_dfs_bellman.png`, `andre_04_atributos_result.png`, `brenda_01_faltantes_por_faixa.png`,
`brenda_02_tempos_bfs_dijkstra.png`, `brenda_03_efeito_transformacao.png`
e `dados_visualizacoes_andre.json`, em `out/parte2/`.
As duas primeiras são exploratórias; a terceira comunica os tempos de DFS e
Bellman-Ford para a fonte comum Siva1979 no mesmo ambiente. A comparação não mistura
as máquinas das duas contribuições de benchmark.

Finalidade, justificativas, fontes e notas estão em
[visualizacoes_andre_parte2.md](docs/visualizacoes_andre_parte2.md). Os textos são
rascunhos gerados com IA para revisão de André, conforme a autorização da professora
informada por ele. O registro de IA inclui escolha, código e interpretação.
As figuras de faltantes e de tempos de BFS/Dijkstra também são implementadas em
`src/viz.py`. A primeira lê o CSV bruto e mostra a proporção agregada sem SOURCE
nas faixas aprovadas. A segunda mantém três painéis, um por fonte, e usa
`benchmark_bfs_dijkstra_mesmo_ambiente.json`, com os mesmos metadados de ambiente
do benchmark de DFS/Bellman-Ford. A terceira figura adicional compara os custos
dos dois caminhos do estudo de caso em PESO e PESO + 1, incluindo o custo zero
e o empate após a transformação. A geração sobrescreve as sete imagens e os
dados de conferência de André; `--out` permite escolher outra pasta de saída.

As células de desenho das antigas seções 18 e 19 foram retiradas do notebook:
o comando acima centraliza a geração das figuras. O estudo de caso da seção 20
permanece no notebook e fornece o JSON para a figura de transformação. O exemplo
selecionado não mede a frequência de mudanças de caminhos na rede inteira.
As notas e justificativas aprovadas estão no [avd_log.md](docs/avd_log.md), com
indicação do apoio de IA. A nota de B02 foi atualizada para as novas medições e
aguarda revisão autoral. B02 é análise visual de desempenho; A01, A02, A04 e B01
são exploratórias de dados, e A03/B03 são explanatórias.
As fontes, justificativas, notas e limites dessas três figuras estão reunidos em
[visualizacoes_brenda_parte2.md](docs/visualizacoes_brenda_parte2.md).
A conferência automática de alcance entre BFS e Dijkstra está na seção 13 do
notebook. A conferência manual de BFS no pequeno recorte foi confirmada por
Brenda e registrada no log. A suíte passou com 81 testes em clone limpo e 81 com
as alterações locais copiadas, sem instalar dependências.

### Relatório técnico e declaração

O material da Parte 2 foi reunido em [RELATORIO_PARTE2.md](docs/RELATORIO_PARTE2.md)
e [RELATORIO_PARTE2.pdf](docs/RELATORIO_PARTE2.pdf), com dataset, tratamentos,
métricas, algoritmos, benchmark, comparação técnica, sete figuras, notas e limites.
É uma compilação técnica com apoio de IA para revisão e incorporação ao relatório
conjunto do grupo; não substitui a Parte 1 nem a revisão autoral dos integrantes.

[DECLARACAO_IA.md](docs/DECLARACAO_IA.md) reúne os usos conhecidos da Parte 2.
`docs/DECLARACAO_IA.pdf` é um rascunho sem assinaturas, com o formulário oficial
e esse registro. O grupo precisa completar identificação e links das conversas
ou blocos de uso, escrever a reflexão de 10–15 linhas, conferir o alcance das
autorizações com as professoras e assinar antes da entrega. Não é correto
considerar essas etapas cumpridas apenas porque o arquivo PDF existe.

## Uso de IA

Seguimos as regras de IA do enunciado. Todo trecho de código feito com apoio de IA leva a marca `# [IA] <ferramenta> – <finalidade>`, cada uso fica registrado em [DECLARACAO_IA.md](docs/DECLARACAO_IA.md), e a declaração assinada por todos fica em `docs/DECLARACAO_IA.pdf`.
