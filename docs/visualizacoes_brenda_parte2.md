# Parte 2 — Três visualizações de Brenda

## Uso de IA

ChatGPT (Codex) participou das sugestões de figuras e faixas, da implementação em
matplotlib, das conferências dos dados e da discussão e organização dos textos.
Brenda apresentou suas observações e aprovou as escolhas, justificativas e notas
registradas no [avd_log.md](avd_log.md). Este documento reúne esses registros no
mesmo formato do documento de André, preservando os textos aprovados.

As aprovações de Brenda registram suas decisões durante o trabalho. A conformidade
dos usos de IA e o alcance das autorizações específicas das professoras continuam
sujeitos à revisão do grupo e à declaração de uso de IA.

## Organização

| ID | Tipo | Finalidade | Responsável | Imagem |
|---|---|---|---|---|
| B01 | Exploratória | Examinar a qualidade dos dados pela proporção de votos sem SOURCE em faixas de votos recebidos | Brenda | [Faltantes por faixa](../out/parte2/brenda_01_faltantes_por_faixa.png) |
| B02 | Análise visual de desempenho | Comparar o comportamento das implementações de BFS e Dijkstra nos recortes | Brenda | [Tempos de BFS e Dijkstra](../out/parte2/brenda_02_tempos_bfs_dijkstra.png) |
| B03 | Explanatória | Explicar, no exemplo selecionado, como somar 1 por arco elimina a vantagem do caminho antes mais barato | Brenda | [Efeito da transformação](../out/parte2/brenda_03_efeito_transformacao.png) |

O código das três figuras está em [src/viz.py](../src/viz.py). As imagens têm
títulos, eixos identificados e fontes nos rodapés. Os dados de cada uma são
indicados nas seções abaixo.

## Paleta e acessibilidade

As figuras seguem a paleta usada nas [visualizações de André](visualizacoes_andre_parte2.md):
azul `#0072B2` e laranja-avermelhado `#D55E00`, com texto escuro e rodapés
`#52606d` sobre fundo branco.

| Figura | Azul | Laranja-avermelhado | Identificação adicional |
|---|---|---|---|
| B01 | Proporção de votos sem SOURCE | Não utilizado | Hachura de listras, percentuais e contagens escritos |
| B02 | BFS | Dijkstra | Círculos e linha contínua para BFS; quadrados e linha tracejada para Dijkstra |
| B03 | Custo em PESO | Custo em PESO + 1 | Listras para PESO, pontos para PESO + 1 e valores escritos, inclusive zero |

Esses recursos descrevem o padrão visual aprovado e implementado. As legendas,
formas, padrões e rótulos permitem identificar as séries além das cores.

## B01 — Votos sem origem identificada por faixa de votos recebidos

**Finalidade.** Examinar a qualidade dos dados pela proporção de votos sem
identificação do eleitor em grupos de candidatos com diferentes volumes de votos.

**Fonte.** `data/dataset_parte2/raw/wikiRfA.csv`, antes do tratamento, com 198.275
registros e 1.661 votos sem SOURCE. O agrupamento é feito por TARGET; o total de
votos de cada candidato define sua faixa. São mantidos todos os candidatos com
TARGET identificado, sem limite mínimo adicional.

**Escolha do gráfico e justificativa das faixas.**

> Adotei as faixas sugeridas durante a discussão com apoio de IA para comparar candidatos com diferentes volumes de votos em cinco grupos legíveis, mantendo também aqueles com poucos votos. Os cortes são uma escolha de apresentação, não limites estatísticos. Como sua definição influencia a aparência do gráfico, apresento os intervalos e as quantidades de candidatos, votos e registros sem SOURCE para contextualizar os percentuais.

As barras representam a proporção agregada de cada faixa:
`100 × soma dos votos sem SOURCE / soma de todos os votos da faixa`.
Não é calculada a média dos percentuais individuais dos candidatos.
Os intervalos têm larguras diferentes e são apresentados como categorias.

| Votos recebidos por candidato | Candidatos | Total de votos | Sem SOURCE | Percentual sem SOURCE |
|---|---:|---:|---:|---:|
| 1–4 | 219 | 577 | 23 | 3,99% |
| 5–19 | 862 | 9.736 | 147 | 1,51% |
| 20–99 | 1.877 | 100.190 | 829 | 0,83% |
| 100–499 | 531 | 82.397 | 642 | 0,78% |
| 500 ou mais | 8 | 5.375 | 20 | 0,37% |

**Nota analítica aprovada.**

> A primeira faixa apresenta o maior percentual de votos sem origem identificada, mas reúne apenas 577 votos, dos quais 23 estão sem SOURCE. Por isso, o percentual deve ser lido junto às quantidades absolutas: a barra mais alta não representa a maior quantidade de registros sem origem.

**Limites.** A figura não determina o mecanismo nem a causa da ausência de SOURCE.
Um voto sem origem identificada não é necessariamente um voto nulo. As faixas
agrupam candidatos e não eleições individuais: a versão utilizada do dataset não
possui datas nem identificadores de eleição. A altura de cada barra descreve sua
própria faixa e deve ser acompanhada pelas contagens.

## B02 — Tempos de BFS e Dijkstra por tamanho do grafo e fonte

**Finalidade.** Comparar o comportamento das implementações nos recortes de 10%,
50% e 100% dos arcos, para Siva1979, Gwynand e John Carter.

**Fonte e recorte da comparação.** `out/parte2/benchmark_bfs_dijkstra_mesmo_ambiente.json`.
Cada configuração possui cinco repetições medidas e um aquecimento fora do
cronômetro. A figura mostra médias em segundos e barras de mínimo–máximo.
Essas barras não são intervalos de confiança.

As medições atuais foram realizadas por André: Python 3.12.6, Windows
(versão registrada 10.0.26300), Intel Core i5-1335U e aproximadamente 16 GB de
memória. Esses metadados coincidem com os de DFS/Bellman-Ford. B02 apresenta
somente BFS e Dijkstra. O benchmark anterior continua preservado em
`benchmark_bfs_dijkstra.json`, mas não fornece os valores da imagem atual.

B02 é uma análise visual dos resultados dos algoritmos; não entra na contagem
de figuras exploratórias voltadas ao entendimento do dataset.

**Escolha do gráfico.**

> Escolhi três painéis, um por fonte, para facilitar a comparação dos tempos de BFS e Dijkstra em cada fonte e nos diferentes tamanhos de recorte. A mesma escala vertical permite também comparar os tempos entre os painéis.

As linhas e os marcadores apresentam as médias nos três tamanhos ordenados.
A escala vertical é linear e comum aos painéis. Cada rótulo horizontal informa
o percentual do recorte, o número de arcos e o número de outros usuários alcançados.

| Recorte | Arcos | Outros usuários alcançados por cada fonte |
|---|---:|---:|
| 10% | 19.661 | 2.661 |
| 50% | 98.307 | 3.360 |
| 100% | 196.614 | 3.443 |

O alcance exclui a própria fonte. Os conjuntos de usuários com distância finita
foram comparados separadamente entre BFS e Dijkstra nas nove configurações de
fonte e tamanho. A conferência está na seção 13 do notebook de experimentos,
fora da medição de tempo.

**Valores atuais para conferência.** Médias em segundos, extraídas do novo JSON:

| Fonte | Recorte | BFS | Dijkstra |
|---|---|---:|---:|
| Siva1979 | 10% | 0,025365 | 0,028914 |
| Siva1979 | 50% | 0,138694 | 0,111150 |
| Siva1979 | 100% | 0,309036 | 0,169753 |
| Gwynand | 10% | 0,026767 | 0,025690 |
| Gwynand | 50% | 0,137485 | 0,101892 |
| Gwynand | 100% | 0,282175 | 0,132150 |
| John Carter | 10% | 0,034100 | 0,026290 |
| John Carter | 50% | 0,141781 | 0,135927 |
| John Carter | 100% | 0,220787 | 0,111098 |

**Nota atualizada para revisão autoral.**

> Para Siva1979, BFS e Dijkstra apresentam tempos médios próximos no recorte de 10%. Nos recortes de 50% e 100%, a média do BFS fica acima da do Dijkstra. Para Gwynand e John Carter, o BFS apresenta média maior nos três tamanhos. Há sobreposição entre alguns intervalos mínimo–máximo; em 100%, o BFS apresenta maior amplitude entre as repetições nas três fontes. Esses resultados descrevem as implementações e o ambiente medidos, sem demonstrar uma vantagem geral de Dijkstra. Os conjuntos de usuários alcançados foram iguais entre os algoritmos em cada configuração.

**Apoio de IA na atualização.** A redação preserva as observações anteriormente
aprovadas por Brenda e substitui a referência à variabilidade do benchmark antigo
pelos intervalos do arquivo atual. Essa atualização factual foi feita com IA e
deve ser revisada por Brenda antes da entrega como nota autoral. A versão anterior
aprovada permanece no histórico do log e se refere às medições antigas.

**Limites.** BFS utiliza PESO, mas ignora seus valores na busca; Dijkstra utiliza
PESO + 1. O tempo inclui a chamada completa de cada implementação, incluindo
suas preparações internas. O gráfico não demonstra que Dijkstra seja geralmente
mais rápido que BFS nem identifica a causa exata da diferença observada.
As duas buscas alcançam os mesmos usuários, mas suas distâncias têm significados
diferentes: número de arcos no BFS e soma dos pesos transformados no Dijkstra.

## B03 — Custos dos caminhos antes e depois da transformação

**Finalidade.** Explicar o efeito de somar 1 a cada arco em um exemplo selecionado
do dataset, relacionado à pergunta de pesquisa sobre a transformação dos pesos.

**Fonte e recorte.** `out/parte2/estudo_transformacao.json`, produzido pelo estudo
de caso da seção 18 do notebook de experimentos. O subgrafo induzido contém
Siva1979, 9cds e Pilotguy, com todos os arcos internos preservados. São três arcos
reais e não há ciclos.

| Arco | PESO | PESO + 1 |
|---|---:|---:|
| Siva1979 → Pilotguy | 1 | 2 |
| Siva1979 → 9cds | −1 | 0 |
| 9cds → Pilotguy | 1 | 2 |

O deslocamento é aplicado a cada arco antes da execução de Dijkstra, em uma
versão separada do grafo. O CSV tratado e a coluna PESO são preservados.

**Escolha do gráfico.**

> Escolhi barras agrupadas para facilitar a comparação dos custos de cada caminho antes e depois de somar 1 a cada arco. Como o exemplo possui apenas dois caminhos e duas versões dos pesos, a figura permite visualizar os valores e o empate após a transformação com poucos elementos.

Cada grupo representa um caminho; as barras comparam as somas em PESO e PESO + 1.
O valor zero é escrito, embora sua barra tenha altura zero.

| Caminho | Quantidade de arcos | Custo em PESO | Custo em PESO + 1 |
|---|---:|---:|---:|
| Siva1979 → Pilotguy | 1 | 1 | 2 |
| Siva1979 → 9cds → Pilotguy | 2 | 0 | 2 |

**Nota analítica aprovada.**

> Neste exemplo, a transformação elimina a vantagem do caminho via 9cds, que tinha menor custo em PESO. Como esse caminho possui dois arcos, seu custo aumenta em 2, enquanto o direto aumenta em 1. Os caminhos passam a empatar, e o Dijkstra retorna o direto, cujo custo nos pesos anteriores à transformação é maior. Isso ilustra que somar uma constante a cada arco pode alterar o caminho retornado, sem preservar a preferência pelo caminho originalmente mais barato.

**Da exploração à explicação — texto aprovado.**

> Ao observar a distribuição de PESO e PESO + 1, surgiu a dúvida sobre se eliminar os pesos negativos também alteraria os caminhos mínimos. Para investigar essa questão, comparei os custos de dois caminhos antes e depois da transformação no subgrafo selecionado. A figura explanatória apresenta esse exemplo e mostra como caminhos com quantidades diferentes de arcos recebem acréscimos diferentes, chegando ao empate observado.

**Apoio de IA nesta nota.** Brenda confirmou que a dúvida surgiu da observação
da distribuição dos pesos. ChatGPT (Codex) organizou a redação acima, incluída
após sua aprovação.

**Limites e relação com a pesquisa.** O caminho direto foi retornado em uma situação
de empate nos pesos transformados; não se tornou exclusivamente melhor.
Ambas as alternativas são ótimas em PESO + 1. A figura ilustra um único par em um
subgrafo sem ciclo negativo e não estima a frequência de mudanças na rede inteira.
Foi mantida a decisão de não ampliar o experimento para vários pares nesta etapa.

## Reprodução e próximos passos

Na raiz do projeto, com os CSVs bruto e tratado, as métricas, os dois benchmarks
e o JSON do estudo de caso disponíveis:

```powershell
python -m src.viz --parte2
```

O comando gera as seis figuras de Brenda e André em `out/parte2/`, sem executar
algoritmos ou refazer o benchmark. Para escolher outra pasta de saída, use `--out`.
O comando padrão `python -m src.viz` continua gerando as figuras da Parte 1.

As notas e justificativas aprovadas estão registradas no log. A nota de B02 foi
atualizada para os novos dados e aguarda revisão autoral. A conferência manual de
BFS foi concluída em 24/11/2026 no recorte Siva1979 → Ceranthor → Salvio giuliano
→ 07bargem. Os testes em clone limpo e com alterações locais passaram: 81 em cada
execução, sem instalação de dependências. O relatório da Parte 2 reúne os textos
e figuras; a declaração de IA ainda depende da revisão, reflexão e assinaturas do grupo.
