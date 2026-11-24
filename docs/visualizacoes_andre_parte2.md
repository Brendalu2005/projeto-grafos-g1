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
| A03 | Explanatória | Comunicar a diferença de tempo observada em um ambiente controlado entre os dois algoritmos | André | [Tempos de DFS e Bellman-Ford](../out/parte2/andre_03_tempos_dfs_bellman.png) |
| A04 | Exploratória | Examinar VOTE, PESO e volume recebido em relação a RESULT | André | [Atributos por RESULT](../out/parte2/andre_04_atributos_result.png) |

As figuras têm título, identificação dos eixos, legenda e indicação de fonte.
O código está em `src/viz.py`; os números usados nas figuras estão em
`out/parte2/dados_visualizacoes_andre.json` para conferência.

## Paleta e acessibilidade

As figuras usam azul `#0072B2` e laranja-avermelhado `#D55E00` da paleta
Okabe–Ito, com cinza escuro `#595959` como referência neutra. A escolha segue
as recomendações de [Color Universal Design, de Okabe e Ito](https://jfly.uni-koeln.de/color/),
que consideram diferenças na percepção de cores.

| Figura | Azul | Laranja-avermelhado | Cinza escuro |
|---|---|---|---|
| A01 | Grau de entrada | Grau de saída | — |
| A02 | PESO ajustado | PESO + 1 (Dijkstra) | VOTE original |
| A03 | DFS | Bellman-Ford | — |

**Justificativa.** O par azul e laranja-avermelhado distingue categorias sem
depender da oposição entre vermelho e verde. No A02, o cinza identifica o voto
original como referência, enquanto as cores destacam as duas versões dos pesos.
As cores indicam categorias, sem atribuir sentido de bom ou ruim aos valores
ou algoritmos. Os rótulos usam texto escuro sobre fundo branco para manter
a leitura independente da cor das séries.

Nenhuma paleta garante distinção para todas as pessoas com daltonismo. Por isso,
as barras também têm padrões diferentes; no A03, círculos e linha contínua
identificam DFS, e quadrados e linha tracejada identificam Bellman-Ford.
Legendas, valores e nomes junto às séries complementam essas diferenças,
inclusive em impressão em tons de cinza. Essa redundância segue o princípio
de [não usar somente a cor para transmitir informação](https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html).

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
O azul com listras identifica entrada, e o laranja-avermelhado com pontos identifica
saída. A posição lado a lado e os rótulos numéricos apoiam a comparação sem depender
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
que sejam erros. A agregação em intervalos não substitui uma investigação
individual dos outliers que o grupo decida realizar.

## A02 — Distribuição de VOTE, PESO e PESO + 1

**Finalidade.** Examinar como a regra das repetições e o deslocamento para Dijkstra
alteram os valores usados como pesos, preservando o voto original para comparação.

**Fonte.** `data/dataset_parte2/processed/wikiRfA_tratado.csv`, com os mesmos 196.614
registros em cada versão. `PESO + 1` é calculado apenas para a figura, sem alterar
o CSV ou substituir a coluna original.

**Escolha do gráfico.** Barras agrupadas por valor inteiro permitem comparar as
frequências das três versões. A escala logarítmica no eixo vertical torna visíveis
tanto frequências acima de cem mil quanto valores com uma única ocorrência.
O cinza com listras identifica VOTE original; o azul com padrão cruzado identifica
PESO ajustado; o laranja-avermelhado com pontos identifica PESO + 1. A legenda
mostra cores e padrões para distinguir as versões. Valores com frequência zero não têm
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

**Escolha implementada.** Barras agrupadas, em azul com listras para RESULT -1 e
laranja-avermelhado com pontos para RESULT 1. Os painéis mostram o voto original,
o peso ajustado agrupado e a faixa do total de votos recebidos pelo candidato.
Os tamanhos dos grupos aparecem no rodapé: 74.090 e 122.524 registros.

**Leitura técnica dos dados exportados.** No grupo RESULT -1, os votos favoráveis
são 32.184 de 74.090 registros (43,44%). No grupo RESULT 1, são 111.695 de 122.524
(91,16%). A unidade é o registro de voto, não a eleição ou um candidato único.
Há 236 TARGETs com mais de um valor de RESULT. Sem datas ou identificador de
eleição, não se deve atribuir um único resultado a cada candidato nem inferir
causalidade dessa comparação. Esta leitura numérica foi compilada com IA para
revisão de André; não é apresentada como nota analítica autoral já aprovada.

## Conferência de valores extremos

`out/parte2/verificacao_outliers.json` registra a conferência reproduzível, sem
alterar o dataset. Para graus, foram usados os limites de 1,5 IQR, incluindo
vértices de grau zero: 2.150 usuários sinalizados na entrada e 1.718 na saída.
Os cinco maiores de cada direção foram conferidos com o CSV bruto mantido.
Para pesos, foram examinadas as 14 ocorrências com PESO >= 4, com valores até 6;
a regra de incremento foi conferida em todas as linhas. Nenhum registro adicional
foi removido: graus altos e pesos elevados não foram presumidos erros. Os pesos
elevados conferem com o incremento nos grupos idênticos. A decisão de manutenção
e a evidência técnica devem ser revisadas por André na versão autoral do relatório.

**Apoio de IA nesta atualização.** Compilação dos dados e verificações já produzidos
pelo código de André, atualização de fontes e redação técnica para revisão.

## Reprodução e próximos passos

Na raiz do projeto, após gerar o CSV tratado e ter as métricas e o benchmark:

```powershell
python -m src.viz --parte2
```

Para outra pasta de imagens, use `--out`. O comando padrão `python -m src.viz`
continua gerando as figuras da Parte 1. Não é necessário refazer o benchmark.

O conjunto atual possui sete figuras: quatro exploratórias de dados (A01, A02,
A04 e B01), duas explanatórias (A03 e B03) e uma análise visual de desempenho
(B02). Essa organização não dispensa a revisão autoral dos textos atualizados,
em especial A04 e a nova nota de B02, nem a declaração fiel do uso de IA.
