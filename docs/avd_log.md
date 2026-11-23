## Etapa 2 — Tratamento de Dados

### Carregamento do CSV tratado — 20/11/2026

O carregador `carregar_dataset(caminho_csv, coluna_peso="PESO")`, em `src/graphs/io.py`, recebe o caminho do CSV tratado exportado pelo notebook. O arquivo deve conter `SOURCE`, `TARGET`, `VOTE`, `RESULT` e `PESO`, com o peso ajustado inteiro já calculado. O nome da coluna de peso pode ser informado pelo argumento `coluna_peso`.

O carregador preserva a direção, a ordem dos arcos, os laços e os arcos paralelos; inclui vértices que aparecem apenas como destino e não recalcula o incremento. O `VOTE` original permanece no CSV. A exportação do CSV com o peso ajustado está implementada no notebook e foi executada localmente em 21/11/2026.

**Apoio de IA:** ChatGPT (Codex) implementou o carregador e os testes em `tests/test_dataset_io.py`, após André informar que a professora permitiu essa implementação. O grupo deve conferir os resultados esperados dos testes e compreender o código.

### Registros sem SOURCE:
Registros sem o "SOURCE" indicam votos sem "votador" registrado e, pensando no contexto do nosso projeto, em que usaremos esses dados para formar um grafo, não seria possível identificar o vértice de origem desses arcos. Por isso, optamos por descartar esses registros. Não sabemos a causa da ausência desses dados. Encontramos 1.661 votos sem SOURCE, distribuídos entre 926 candidatos. Seis candidatos possuem todos os votos recebidos sem SOURCE. Analisei esses seis candidatos e desses: Meelar, Mrmewe e Sarge Baldy também aparecem como eleitores nos registros mantidos; porém Lionelisbest, Patrick e Stevertigo não aparecem nos registros restantes e, se o grafo incluir apenas usuários desses registros, eles não serão incluídos como vértices. Essa análise não permite determinar a causa da ausência nem afirmar que ela seja aleatória.

**Apoio de IA:** ChatGPT (Codex) auxiliou na revisão de clareza, na correção conceitual sobre vértices e arcos e ajudou na logica do pandas para conferência dos registros sem SOURCE. A decisão de excluir esses registros foi tomada por André.

### Linhas Repetidas:
Não removeremos as linhas repetidas, pois utilizamos uma versão resumida do dataset original, sem as datas das votações. Assim, não temos informações suficientes para comprovar que essas linhas sejam duplicações indevidas, e não o mesmo eleitor votando no mesmo candidato em eleições diferentes.

**Apoio de IA:** ChatGPT (Codex) auxiliou na conferência de linhas repetidas usando pandas e na revisão de clareza deste texto. A decisão de manter esses registros e sua justificativa foram elaboradas por André.

### Regra de peso para linhas idênticas

Conforme André confirmou em 20/11/2026, após conversar com Laura, que sugeriu o incremento, todos os registros serão preservados como arcos paralelos. Uma repetição é definida pela igualdade simultânea de SOURCE, TARGET, VOTE e RESULT.

Dentro de cada grupo de linhas idênticas, será usada a ordem original do CSV: a primeira ocorrência terá peso VOTE; a segunda, VOTE + 1; a terceira, VOTE + 2; e assim por diante. O incremento começa em zero para cada grupo e não é reiniciado entre ocorrências do mesmo grupo. Se qualquer uma das quatro colunas mudar, trata-se de outro grupo.

O VOTE original será preservado, e o peso ajustado será armazenado separadamente. Repetir apenas SOURCE e TARGET não basta para aplicar o incremento.

**Apoio de IA:** ChatGPT (Codex) auxiliou na redação do registro da regra informada e confirmada por André. A sugestão do incremento foi atribuída por André à professora Laura. Este registro documenta a decisão; não implementa o cálculo dos pesos.

### Registros em que SOURCE == TARGET:
Optamos por manter os registros em que SOURCE e TARGET são iguais, pois não possuímos informações suficientes para assegurar que sejam corretos ou incorretos. Como não foi possível verificar esses casos no arquivo original, preservaremos os registros e documentaremos essa incerteza.

**Apoio de IA:** ChatGPT (Codex) auxiliou na conferência dos registros usando pandas, no esclarecimento do conceito de laço e na revisão de clareza da justificativa. A decisão de manter os registros foi tomada por André.

### Validação dos valores

Conferimos os valores das colunas VOTE e RESULT após a retirada dos registros sem SOURCE e não encontramos valores fora dos conjuntos previstos. Também não encontramos dados ausentes nos registros restantes, logo não foi necessário realizar outro tratamento nessas colunas.

### Fechamento do tratamento

Após as conferências, optamos por retirar apenas os registros sem SOURCE, pois não seria possível identificar a origem desses arcos. Mantivemos as linhas repetidas e os registros em que SOURCE é igual a TARGET, pois não possuímos informações suficientes para assegurar que sejam erros. Com isso, passamos de 198.275 para 196.614 registros. Todos os pares repetidos serão mantidos como arcos paralelos. O incremento de peso será aplicado somente dentro dos grupos idênticos nas quatro colunas SOURCE, TARGET, VOTE e RESULT, seguindo a ordem original do CSV, conforme a regra registrada acima.

**Apoio de IA nos dois textos acima:** ChatGPT (Codex) preparou as prévias a partir das contagens verificadas e das decisões já informadas por André. As decisões são de André. Em 21/11/2026, a IA revisou a clareza do registro, sem acrescentar decisões ou interpretações.


### Conferência da exportação local — 21/11/2026

O CSV tratado foi gerado em `data/dataset_parte2/processed/wikiRfA_tratado.csv`, com 196.614 registros e as colunas `SOURCE`, `TARGET`, `VOTE`, `RESULT` e `PESO`, sem índice adicional. A conferência com pandas verificou a preservação da ordem e dos valores originais dos registros mantidos, a ausência de faltantes e a igualdade de `PESO` com `VOTE` mais o número da ocorrência dentro de cada grupo de quatro colunas idênticas. O CSV bruto permaneceu inalterado, conferido por SHA-256 antes e depois da execução.

**Apoio de IA:** ChatGPT (Codex) executou as células existentes de tratamento e exportação usando o arquivo bruto local, sem novo download; acrescentou a conferência com pandas e revisou os registros de clareza e estado de execução. Não foram acrescentadas decisões de tratamento, interpretações ou conclusões analíticas.

### Depuração do DFS para arcos paralelos — 21/11/2026

O registro de classificação passou de `(origem, destino)` para `(origem, destino, indice_na_adjacencia)`, com índice começando em zero. Assim, cada ocorrência tem uma chave própria, inclusive quando os extremos e o peso são iguais. O retorno continua sendo `d, f, p, classif, tem_ciclo`; as consultas diretas às chaves nos testes foram adaptadas. Os consumidores em `solve.py` e no servidor do front usam os valores das classificações e não precisam de alteração de formato.

**Apoio de IA:** ChatGPT (Codex) corrigiu a sobrescrita no código de DFS escrito por André, adaptou as consultas dos testes e reforçou as verificações dos dois casos de arcos paralelos já adicionados por André a partir de sugestões de IA. O grupo deve conferir os resultados e compreender a mudança de chave.

**Verificação:** na suíte completa executada com Python em modo UTF-8, 41 testes passaram e um falhou: `test_porta_sem_chave_correspondente_gera_erro_claro`, pois a validação de mapas não lançou o erro esperado. A falha ocorre no IO de mapas, cujo código não foi alterado nesta depuração.

### Execução técnica do DFS em três fontes — 22/11/2026

O notebook `experimentos_parte2.ipynb` passou a chamar o DFS existente a partir das mesmas três fontes registradas no BFS: `Siva1979`, `'sed` e `!---slappdash---!`. A seleção foi reutilizada para adiantar a execução e deve ser confirmada por André. Foram exportados ordem de descoberta, tempos de descoberta e término, predecessores, contagens dos quatro tipos de arco e indicação de ciclos em `out/parte2/dfs_fontes.json`.

As conferências técnicas verificaram a quantidade de arcos classificados, a quantidade de arcos de árvore, os conjuntos dos retornos e a concordância dos vértices alcançados com os resultados BFS salvos para cada fonte. O CSV e os JSONs anteriores de BFS, Dijkstra e métricas permaneceram inalterados, conferidos por SHA-256. Não foram realizadas medições de desempenho nem elaboradas interpretações dos resultados.

**Apoio de IA:** ChatGPT (Codex) acrescentou e executou chamadas e exportação do DFS já escrito pelo grupo, com verificações técnicas e marcadores nas células. Não alterou a implementação do algoritmo. A confirmação das fontes, a conferência pelo grupo e a interpretação autoral ficam com André.

### Casos mínimos de Bellman-Ford sugeridos — 22/11/2026

Após André solicitar também sugestões de recortes e fontes, Codex sugeriu dois subgrafos induzidos de dois usuários, preservando todos os registros entre eles e a coluna PESO. O primeiro usa Malleus Fatuorum e BDD, com fonte Malleus Fatuorum. O segundo usa Rcsprinter123 e Jasper Deng, com fonte Rcsprinter123. Os registros selecionados pertencem ao CSV tratado; suas posições e o SHA-256 da entrada constam em `out/parte2/bellman_ford_casos.json`.

Codex acrescentou e executou chamadas do Bellman-Ford existente, conferências técnicas e exportação no notebook de experimentos. A implementação do algoritmo não foi alterada. André informou autorização da professora para dispensar novos marcadores; os registros anteriores foram preservados. A escolha final, a conferência manual, as justificativas e a interpretação autoral permanecem com André. Não foram feitas medições de desempenho nem produzidas conclusões analíticas. Os dados e os JSONs anteriores foram preservados, conferidos por SHA-256.

### Integração da Parte 2 na CLI — 23/11/2026

Foram acrescentadas funções em `src/solve.py` para chamar os algoritmos existentes
no CSV tratado e reproduzir os experimentos registrados no notebook. Em `src/cli.py`,
foram adicionadas as opções `--dataset`, `--source`, `--target`, `--deslocamento`,
`--caso` e `--experimentos`, com validação das combinações. A execução dos mapas
permanece disponível. Fontes, pares, recortes e a transformação de Dijkstra são os
mesmos já registrados pelo grupo; nenhum algoritmo foi reimplementado.

O modo `--experimentos` reproduz as quatro saídas de BFS, DFS, Dijkstra e Bellman-Ford.
Os resultados foram comparados com os JSONs existentes e coincidiram integralmente
no campo `resultados`. Também foram executados comandos individuais dos quatro
algoritmos no CSV local. Essas verificações usaram saídas temporárias; o CSV e os
JSONs existentes permaneceram inalterados, conferidos por SHA-256.

O README foi atualizado com os comandos e as convenções das saídas. Os testes em
`tests/test_parte2_cli.py` cobrem integração, entradas inválidas, arcos paralelos,
distâncias inalcançáveis, recortes de Bellman-Ford, reprodução dos experimentos e
compatibilidade da CLI com mapas. O benchmark continua separado desta integração.

**Apoio de IA:** ChatGPT (Codex) implementou esta integração, seus testes e a documentação
após André autorizar expressamente a geração da implementação nesta conversa,
pedindo código limpo, simples e direto. Foram inseridos marcadores nas funções e
blocos correspondentes. O grupo deve compreender e conferir o código e registrar
esse apoio na declaração conjunta. Não foram geradas interpretações ou conclusões analíticas.

### Benchmark de DFS e Bellman-Ford e entrega para consolidação — 23/11/2026

Por solicitação de André, foram executadas medições dos algoritmos existentes
usando `criar_recortes`, `selecionar_fontes` e `medir_algoritmo`, de `src/benchmark.py`.
Foram preservados semente 42, recortes de 10%, 50% e 100% das ocorrências de arcos,
fontes Siva1979, Gwynand e John Carter e PESO sem deslocamento. Preparação, alcance
e exportação ficaram fora do cronômetro. Cada configuração concluída tem um
aquecimento completo e cinco repetições medidas.

André inicialmente escolheu três fontes também para Bellman-Ford. Durante a
execução, autorizou concluir somente Siva1979 em 100%, mantendo as três fontes
já medidas em 10% e 50%. DFS manteve três fontes nos três tamanhos. O conjunto
final contém 16 configurações e 80 tempos em `out/parte2/benchmark_dfs_bellman.json`,
com `completo: true`. O processo foi encerrado depois de salvar a última configuração
selecionada. O aquecimento iniciado para Gwynand em 100% foi interrompido e não
integra as medições ou estatísticas. A redução consta nos metadados do JSON e no executor.

As conferências verificaram o conjunto exato de configurações, cinco tempos finitos
por configuração, as estatísticas recalculadas e o SHA-256 do CSV. Tamanhos,
fontes, graus e alcances coincidiram com as configurações correspondentes do
benchmark de BFS/Dijkstra. Os 75 testes da suíte passaram após a execução.

O executor reproduzível está em `src/benchmark_dfs_bellman.py`; o roteiro de entrega
para Brenda está em `docs/entrega_benchmark_andre.md`. A consolidação em
`parte2_report.json` permanece com Brenda, conforme o cronograma. Os ambientes das
duas contribuições são diferentes e devem permanecer identificados. Não foram
produzidas interpretações de desempenho, comparações com a complexidade teórica
ou conclusões analíticas.

**Apoio de IA:** ChatGPT (Codex) preparou e executou as chamadas e exportações do
benchmark, acrescentou testes de integração e registrou as decisões expressas de
André. As implementações de DFS e Bellman-Ford não foram alteradas nesta tarefa.
André deve conferir e compreender o código e elaborar sua análise autoral.

### Três visualizações da Parte 2 — 23/11/2026

Após André informar que a professora autorizou a produção com IA, ChatGPT (Codex)
propôs e implementou três figuras em `src/viz.py`: distribuição dos graus de entrada
e saída, distribuição de VOTE/PESO/PESO + 1 e tempos de DFS/Bellman-Ford na fonte
Siva1979. A comparação de tempos usa somente as medições no mesmo ambiente e na
mesma fonte para os três tamanhos. As imagens foram geradas em `out/parte2/` e
inspecionadas visualmente. Os dados numéricos usados também foram exportados para
conferência em `dados_visualizacoes_andre.json`. Os 75 testes existentes passaram.

Finalidades, justificativas, notas e limites estão em
`docs/visualizacoes_andre_parte2.md`. Esses textos são rascunhos gerados com IA para
revisão de André, não análises atribuídas originalmente ao aluno. As demais figuras
do grupo e a incorporação ao PDF continuam pendentes.

**Apoio de IA efetivamente utilizado:** escolha dos gráficos, implementação em
matplotlib e pandas, conferência dos dados, interpretação e redação das notas,
além de ajustes visuais e documentação. André informou autorização da professora;
essa informação não é apresentada como uma permissão escrita anexada ao repositório.
A declaração conjunta deve registrar essas atividades, sem reduzi-las a apoio
conceitual ou revisão gramatical. André deve conferir os dados, compreender os
gráficos e revisar os textos antes da entrega.
