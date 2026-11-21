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
