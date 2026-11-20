## Etapa 2 — Tratamento de Dados

### Carregamento do CSV tratado — 20/11/2026

O carregador `carregar_dataset(caminho_csv, coluna_peso="PESO")`, em `src/graphs/io.py`, recebe o caminho do CSV tratado exportado pelo notebook. O arquivo deve conter `SOURCE`, `TARGET`, `VOTE`, `RESULT` e `PESO`, com o peso ajustado inteiro já calculado. O nome da coluna de peso pode ser informado pelo argumento `coluna_peso`.

O carregador preserva a direção, a ordem dos arcos, os laços e os arcos paralelos; inclui vértices que aparecem apenas como destino e não recalcula o incremento. O `VOTE` original permanece no CSV. A exportação do CSV com o peso ajustado ainda precisa ser implementada no notebook.

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

**### Validação dos valores**

Conferimos os valores das colunas VOTE e RESULT após a retirada dos registros sem SOURCE e não encontramos valores fora dos conjuntos previstos. Também não encontramos dados ausentes nos registros restantes, logo não foi necessário realizar outro tratamento nessas colunas.

**### Fechamento do tratamento — prévia a completar**

Após as conferências, optamos por retirar apenas os registros sem SOURCE, pois não seria possível identificar a origem desses arcos. Mantivemos as linhas repetidas e os registros em que SOURCE é igual a TARGET, pois não possuímos informações suficientes para assegurar que sejam erros. Com isso, passamos de 198.275 para 196.614 registros. Todos os pares repetidos serão mantidos como arcos paralelos. O incremento de peso será aplicado somente dentro dos grupos idênticos nas quatro colunas SOURCE, TARGET, VOTE e RESULT, seguindo a ordem original do CSV, conforme a regra registrada acima.

**Apoio de IA nos dois textos acima:** ChatGPT (Codex) preparou as prévias a partir das contagens verificadas e das decisões já informadas por André. Os campos pendentes devem ser completados por André; o fechamento ainda não é definitivo.
