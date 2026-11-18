## Etapa 2 — Tratamento de Dados
### Registros sem SOURCE:
Registros sem o "SOURCE" indicam votos sem "votador" registrado e, pensando no contexto do nosso projeto, em que usaremos esses dados para formar um grafo, não seria possível identificar o vértice de origem desses arcos. Por isso, optamos por descartar esses registros. Não sabemos a causa da ausência desses dados. Encontramos 1.661 votos sem SOURCE, distribuídos entre 926 candidatos. Seis candidatos possuem todos os votos recebidos sem SOURCE. Analisei esses seis candidatos e desses: Meelar, Mrmewe e Sarge Baldy também aparecem como eleitores nos registros mantidos; porém Lionelisbest, Patrick e Stevertigo não aparecem nos registros restantes e, se o grafo incluir apenas usuários desses registros, eles não serão incluídos como vértices. Essa análise não permite determinar a causa da ausência nem afirmar que ela seja aleatória.

**Apoio de IA:** ChatGPT (Codex) auxiliou na revisão de clareza, na correção conceitual sobre vértices e arcos e ajudou na logica do pandas para conferência dos registros sem SOURCE. A decisão de excluir esses registros foi tomada por André.

### Linhas Repetidas:
Não removeremos as linhas repetidas, pois utilizamos uma versão resumida do dataset original, sem as datas das votações. Assim, não temos informações suficientes para comprovar que essas linhas sejam duplicações indevidas, e não o mesmo eleitor votando no mesmo candidato em eleições diferentes.

**Apoio de IA:** ChatGPT (Codex) auxiliou na conferência de linhas repetidas usando pandas e na revisão de clareza deste texto. A decisão de manter esses registros e sua justificativa foram elaboradas por André.

### Registros em que SOURCE == TARGET:
Optamos por manter os registros em que SOURCE e TARGET são iguais, pois não possuímos informações suficientes para assegurar que sejam corretos ou incorretos. Como não foi possível verificar esses casos no arquivo original, preservaremos os registros e documentaremos essa incerteza.

**Apoio de IA:** ChatGPT (Codex) auxiliou na conferência dos registros usando pandas, no esclarecimento do conceito de laço e na revisão de clareza da justificativa. A decisão de manter os registros foi tomada por André.

**### Validação dos valores**

Conferimos os valores das colunas VOTE e RESULT após a retirada dos registros sem SOURCE e não encontramos valores fora dos conjuntos previstos. Também não encontramos dados ausentes nos registros restantes, logo não foi necessário realizar outro tratamento nessas colunas.

**### Fechamento do tratamento — prévia a completar**

Após as conferências, optamos por retirar apenas os registros sem SOURCE, pois não seria possível identificar a origem desses arcos. Mantivemos as linhas repetidas e os registros em que SOURCE é igual a TARGET, pois não possuímos informações suficientes para assegurar que sejam erros. Com isso, passamos de 198.275 para 196.614 registros. Sobre os pares repetidos, decidimos mante-los e no grafo, colocaremos pesos diferentes, como foi conversado com Laura em sala.

**Apoio de IA nos dois textos acima:** ChatGPT (Codex) preparou as prévias a partir das contagens verificadas e das decisões já informadas por André. Os campos pendentes devem ser completados por André; o fechamento ainda não é definitivo.