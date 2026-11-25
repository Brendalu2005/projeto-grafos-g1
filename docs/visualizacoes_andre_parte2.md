# Parte 2 — Quatro visualizações de André

## Uso de IA:
ChatGPT (Codex) ajudou na escolha das figuras,
implementação em matplotlib, conferência dos dados, na formatação do texto das justificativas. 
Tambem auxiliou em deixar as visualizações mais acessíveis as pessoas daltônicas.

## Organização

| ID | Tipo | Finalidade | Responsável pela revisão | Imagem |
|---|---|---|---|---|
| A01 | Exploratória | Examinar a distribuição dos graus dirigidos | André | [Distribuição dos graus](../out/parte2/andre_01_distribuicao_graus.png) |
| A02 | Exploratória | Comparar votos e duas versões dos pesos | André | [Distribuição dos pesos](../out/parte2/andre_02_distribuicao_pesos.png) |
| A03 | Explanatória | Comunicar a diferença de tempo observada entre os dois algoritmos no mesmo ambiente registrado | André | [Tempos de DFS e Bellman-Ford](../out/parte2/andre_03_tempos_dfs_bellman.png) |
| A04 | Exploratória | Examinar VOTE, PESO e volume recebido em relação a RESULT | André | [Atributos por RESULT](../out/parte2/andre_04_atributos_result.png) |

As figuras têm título, identificação dos eixos, legenda e indicação de fonte.
O código está em `src/viz.py`; os números usados nas figuras estão em
`out/parte2/dados_visualizacoes_andre.json` para conferência.

## Paleta e acessibilidade

As figuras usam azul `#0072B2`, laranja-avermelhado `#D55E00` e cinza escuro `#3E4756`,
conforme a implementação atual em `src/viz.py`. As barras têm preenchimento
sólido, sem hachuras. Os contornos usam `#263238` e os rodapés, em geral,
`#52606d`, sobre fundo branco.

**Critério de escolha.** O azul e o laranja-avermelhado foram escolhidos pensando
na acessibilidade para pessoas com daltonismo, com o objetivo de facilitar a
distinção das séries. As barras mantêm preenchimento sólido, sem textura, e a
identificação é complementada por posição, legendas, rótulos e, nos gráficos de
linhas, marcadores e traçados diferentes.

| Figura | Azul | Laranja-avermelhado | Cinza escuro |
|---|---|---|---|
| A01 | Grau de entrada | Grau de saída | — |
| A02 | PESO ajustado | PESO + 1 (Dijkstra) | VOTE original |
| A03 | DFS | Bellman-Ford | — |
| A04 | RESULT -1: rejeição | RESULT 1: aprovação | — |

**Uso das cores.** Azul e laranja-avermelhado identificam as duas séries comparadas. No A02,
o cinza identifica o voto
original como referência, enquanto as cores destacam as duas versões dos pesos.
As cores indicam categorias, sem atribuir sentido de bom ou ruim aos valores
ou algoritmos. Os rótulos usam texto escuro sobre fundo branco para manter
a leitura independente da cor das séries.

**Recursos de acessibilidade.** No A03, círculos e linha contínua identificam
DFS, enquanto quadrados e linha tracejada identificam Bellman-Ford; as anotações
também apresentam valores e nomes das séries. Nas barras agrupadas, a posição
fixa de cada série e a legenda apoiam a identificação; A01 e A04 também mostram
percentuais escritos. A02 utiliza legenda e ordem fixa das três séries, sem
valores escritos em todas as barras. Como as barras não têm padrões distintos,
a leitura em tons de cinza depende também da posição e da legenda. Não foi
registrada validação específica desta paleta para daltonismo ou contraste.

## A01 — Distribuição dos graus de entrada e saída

**Finalidade.** Explorar quantos usuários têm graus nulos, pequenos ou altos,
distinguindo votos recebidos de votos emitidos nos registros mantidos.

**Fonte.** `out/parte2/metricas_dataset.json`, com 11.376 vértices. Cada ocorrência
paralela conta no grau; um laço acrescenta uma unidade ao grau de entrada e outra
ao de saída.

**Escolha do gráfico.** Barras agrupadas permitem comparar entrada e saída dentro
dos mesmos intervalos. Os intervalos categóricos mantêm os zeros explícitos e
incluem a cauda de valores altos sem remover usuários. A altura representa o
percentual de usuários, não a densidade de um histograma com intervalos iguais.
O azul identifica entrada, e o laranja-avermelhado identifica saída, ambos com preenchimento
sólido. A posição lado a lado e os rótulos numéricos apoiam a comparação sem depender
somente das cores. Os intervalos têm larguras diferentes e não devem ser interpretados
como uma escala horizontal contínua.

**Nota analítica** A figura mostra como os usuários se distribuem
por quantidade de votos recebidos e emitidos. Dos 11.376 usuários, 7.885 (69,3%)
têm grau de entrada zero, enquanto 961 (8,4%) têm grau de saída zero. A faixa de
um a quatro votos emitidos reúne 6.144 usuários (54,0% do total). Na faixa de 500
ou mais, há oito usuários pelo grau de entrada e quinze pelo grau de saída.
Esses resultados mostram distribuições distintas para os dois papéis na rede;
a média de grau, aproximadamente 17,28, sozinha não descreve essa distribuição.
As barras foram escolhidas para tornar as diferenças entre direções visíveis
nos mesmos intervalos, mantendo explícitos os usuários de grau zero.

**Limites.** Grau zero se refere ao grafo tratado, não à ausência de atividade na
Wikipédia em geral. O gráfico não determina a causa dos graus altos nem comprova
que sejam erros. A agregação em intervalos não substitui a investigação individual
dos outliers. A conferência já realizada dos cinco maiores graus de cada direção
está descrita na seção “Conferência de valores extremos”; os demais sinalizados
pelo critério não foram todos conferidos individualmente.

## A02 — Distribuição de VOTE, PESO e PESO + 1

**Finalidade.** Examinar como a regra das repetições e o deslocamento para Dijkstra
alteram os valores usados como pesos, preservando o voto original para comparação.

**Fonte.** `data/dataset_parte2/processed/wikiRfA_tratado.csv`, com os mesmos 196.614
registros em cada versão. `PESO + 1` é calculado apenas para a figura, sem alterar
o CSV ou substituir a coluna original.

**Escolha do gráfico.** Barras agrupadas por valor inteiro permitem comparar as
frequências das três versões. A escala logarítmica no eixo vertical torna visíveis
tanto frequências acima de cem mil quanto valores com uma única ocorrência.
O cinza escuro identifica VOTE original; o azul identifica PESO ajustado; o laranja-avermelhado
identifica PESO + 1. As barras são sólidas, sem hachuras, e mantêm essa ordem
da esquerda para a direita em cada grupo, com identificação na legenda.
Valores com frequência zero não têm
barra; diferenças de altura nessa escala não representam diferenças absolutas
lineares de quantidade.

**Nota analítica** O voto original assume apenas -1, 0 e 1.
A regra de incremento modifica 2.834 registros em relação a VOTE, sem retirar
linhas, e amplia o suporte de PESO até 6. Os registros negativos passam de 40.667
em VOTE para 39.655 em PESO. O deslocamento adicional de uma unidade move toda a
distribuição de PESO para a direita: os valores -1 tornam-se zero e deixam de
existir pesos negativos na versão usada por Dijkstra. As barras agrupadas
permitem acompanhar esse deslocamento e distinguir o voto do custo ajustado.

**Limites e relação com a pesquisa.** Eliminar pesos negativos permite aplicar
Dijkstra, mas não garante preservar caminhos mínimos da versão anterior. Para
um caminho com k arcos, o custo em PESO + 1 é o custo em PESO mais k. O gráfico
documenta a mudança dos valores, não demonstra quais caminhos específicos mudam
nem compara mínimos finitos em regiões com ciclo negativo alcançável. Essa parte
da pergunta exige relacionar os resultados de caminhos aos experimentos do grupo.

## A03 — Tempos de DFS e Bellman-Ford na fonte Siva1979

**Finalidade.** Comunicar a diferença de tempo observada nas implementações
medidas no mesmo ambiente e mostrar os tempos nos três tamanhos disponíveis.

**Fonte e recorte da comparação.** `out/parte2/benchmark_dfs_bellman.json`, usando
somente Siva1979 para ambos os algoritmos em 10%, 50% e 100% dos arcos. Essa fonte
é a única de Bellman-Ford medida no grafo completo. A03 usa apenas este arquivo,
sem médias com quantidades diferentes de fontes. Há cinco repetições por
configuração e um aquecimento fora do cronômetro. O benchmark atual de BFS/Dijkstra
também foi realizado por André, no mesmo ambiente registrado, e é mostrado em B02.

**Da exploração à comunicação.** A conferência da tabela de tempos revelou uma
diferença de várias ordens de grandeza para a fonte comum. A figura destaca esse
resultado com um título quantitativo, mantém os três tamanhos para contexto e
mostra o intervalo observado nas cinco repetições. O azul, os círculos e a linha
contínua identificam DFS; o laranja-avermelhado, os quadrados e a linha tracejada
identificam Bellman-Ford. As anotações escuras apresentam as médias e os nomes
das séries no último ponto; não se omitem pontos para ampliar
a diferença visual.

**Escolha do gráfico.** Linhas com marcadores mostram a evolução entre os recortes
ordenados. O eixo vertical logarítmico permite exibir milissegundos e centenas de
segundos na mesma figura. As barras representam mínimo e máximo observados, não
intervalos de confiança. O eixo horizontal representa percentuais de arcos:
19.661, 98.307 e 196.614 ocorrências; não são percentuais dos vértices.

**Nota analítica** Para Siva1979, as médias de DFS foram cerca
de 0,009 s, 0,047 s e 0,152 s nos três tamanhos. As de Bellman-Ford foram 18,3 s,
300,0 s e 600,3 s. No grafo completo, a razão entre as médias é aproximadamente
3.957, apresentada no título como cerca de quatro mil vezes. A escala logarítmica
permite mostrar essa diferença e ainda observar o crescimento de cada série.
As barras também evidenciam variação nas repetições, especialmente em Bellman-Ford
no recorte intermediário.

**Limites.** A razão descreve esta implementação, fonte, dados e ambiente; não é
uma garantia geral. DFS explora e classifica arcos, enquanto Bellman-Ford considera
pesos e detecta ciclos negativos, portanto não são substitutos equivalentes.
O custo teórico de DFS é O(V + E) e o desta implementação de Bellman-Ford é O(VE),
mas três tamanhos e cinco tempos por configuração não bastam para demonstrar uma
lei assintótica ou explicar toda a variação observada. A figura não responde,
isoladamente, à pergunta sobre a transformação dos pesos para Dijkstra.

## A04 — Atributos por resultado da candidatura

**Finalidade e fonte.** Exploração de `VOTE`, `PESO` e volume recebido por TARGET
em relação a `RESULT`, no CSV tratado. A função `atributos_por_result_dataset`,
em `src/viz.py`, gera três painéis com percentuais normalizados separadamente
nos grupos de rejeição e aprovação. Os números estão em
`out/parte2/dados_visualizacoes_andre.json`, na chave `result`.

**Escolha implementada.** Barras agrupadas com preenchimento sólido, em azul para
RESULT -1 e laranja-avermelhado para RESULT 1. A posição fixa, a legenda e os percentuais escritos
complementam a identificação por cor. Os painéis mostram o voto original,
o peso ajustado agrupado e a faixa do total de votos recebidos pelo candidato.
Os tamanhos dos grupos aparecem no rodapé: 74.090 e 122.524 registros.

**Leitura técnica dos dados exportados.** No grupo RESULT -1, os votos favoráveis
são 32.184 de 74.090 registros (43,44%). No grupo RESULT 1, são 111.695 de 122.524
(91,16%). A unidade é o registro de voto, não a eleição ou um candidato único.
Há 236 TARGETs com mais de um valor de RESULT. Sem datas ou identificador de
eleição, não se deve atribuir um único resultado a cada candidato nem inferir
causalidade dessa comparação. A compilação teve apoio de IA; as análises foram
revisadas pelo grupo, conforme confirmação recebida.

## Conferência de valores extremos

`out/parte2/verificacao_outliers.json` registra a conferência reproduzível, sem
alterar o dataset. Para graus, foram usados os limites de 1,5 IQR, incluindo
vértices de grau zero: 2.150 usuários sinalizados na entrada e 1.718 na saída.
Os cinco maiores de cada direção foram conferidos com o CSV bruto mantido.
Para pesos, foram examinadas as 14 ocorrências com PESO >= 4, com valores até 6;
a regra de incremento foi conferida em todas as linhas. Nenhum registro adicional
foi removido: graus altos e pesos elevados não foram presumidos erros. Os pesos
elevados conferem com o incremento nos grupos idênticos. A decisão de manutenção
e a evidência técnica integram a análise revisada pelo grupo.

## Reprodução e próximos passos

Na raiz do projeto, com os CSVs bruto e tratado, `metricas_dataset.json`,
`benchmark_dfs_bellman.json`, `benchmark_bfs_dijkstra_mesmo_ambiente.json` e
`estudo_transformacao.json` nas pastas padrão:

```powershell
python -m src.viz --parte2
```

O comando gera as sete figuras da Parte 2 e atualiza `dados_visualizacoes_andre.json`.
Para outra pasta de saída, use `--out`; as entradas continuam sendo lidas das
pastas padrão do projeto. O comando padrão `python -m src.viz` continua gerando
as figuras da Parte 1. Não é necessário refazer o benchmark.

O conjunto atual possui sete figuras: quatro exploratórias de dados (A01, A02,
A04 e B01), duas explanatórias (A03 e B03) e uma análise visual de desempenho
(B02). As análises e justificativas foram revisadas pelo grupo, conforme
confirmação recebida; o uso de IA permanece registrado na documentação correspondente.
