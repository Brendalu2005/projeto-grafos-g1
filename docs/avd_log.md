## Ligação entre exploração e figura explanatória B03 — 23/11/2026

Brenda confirmou que a observação da distribuição de PESO e PESO + 1 motivou
a dúvida sobre a preservação dos caminhos mínimos. Aprovou o texto abaixo,
incluído na seção B03 de [visualizacoes_brenda_parte2.md](visualizacoes_brenda_parte2.md).

> Ao observar a distribuição de PESO e PESO + 1, surgiu a dúvida sobre se eliminar os pesos negativos também alteraria os caminhos mínimos. Para investigar essa questão, comparei os custos de dois caminhos antes e depois da transformação no subgrafo selecionado. A figura explanatória apresenta esse exemplo e mostra como caminhos com quantidades diferentes de arcos recebem acréscimos diferentes, chegando ao empate observado.

**Checklist atualizado das atividades de Brenda:**
- [x] Conferir o BFS e preparar/testar o comando do benchmark.
- [x] Commit do benchmark — realizado por Brenda, conforme sua confirmação.
- [ ] Confirmar push e envio das instruções ao André.
- [ ] Consultar as professoras sobre Bellman-Ford com uma fonte em 100% — adiado.
- [ ] Juntar os resultados no `parte2_report.json` — aguarda novas medições.
- [ ] Reclassificar B02 como análise visual de desempenho — adiado.
- [x] Registrar a ligação entre achados exploratórios e a figura explanatória B03.
- [ ] Integrar ao PDF as seções de BFS, Dijkstra, transformação e resposta à pesquisa.
- [ ] Conferir BFS à mão e executar testes em clone limpo.
- [ ] Concluir registro de IA e reflexão.

**Apoio de IA:** ChatGPT (Codex) organizou o texto a partir da ligação confirmada
por Brenda e o registrou após sua aprovação. As figuras e os resultados não foram
alterados. Os checklists anteriores permanecem como histórico.

## Revisão do BFS e comando do benchmark — 23/11/2026

Seguindo a nova divisão de tarefas informada por Brenda, foi revisado o BFS
existente: usa `deque`, `popleft()` e dicionários para distâncias e predecessores.
A preparação percorre todos os arcos antes da busca e faz parte da chamada
medida. Não foi identificado erro que justificasse alterar o algoritmo; os tempos
observados não demonstram, por si só, erro nem uma vantagem geral de Dijkstra.
A causa exata da diferença de desempenho não foi isolada nesta revisão.

Após aprovação de Brenda, `src/benchmark.py` recebeu um comando executável para
BFS e Dijkstra. Reutiliza recortes e seleção de fontes com semente 42, mede uma
busca completa por fonte, com um aquecimento e cinco repetições. Compara os
conjuntos alcançados fora do cronômetro e registra hash do CSV, ambiente e status
de conclusão. São 18 configurações e 90 tempos medidos. Não sobrescreve uma saída
existente. A função de coleta do ambiente foi movida do executor de
DFS/Bellman-Ford para o módulo comum, mantendo o comportamento e evitando cópia.
Os algoritmos não foram alterados.

**Comando para André, na raiz do projeto:**

```powershell
python -m src.benchmark --dataset data/dataset_parte2/processed/wikiRfA_tratado.csv --out out/parte2/benchmark_bfs_dijkstra_mesmo_ambiente.json
```

**SHA-256 do CSV tratado:**
`de16066d90875782f2daffae3adbe5c513f0fa9743ad242d3e1fcbf5c635e7c2`.
O hash coincide com o registrado nas medições anteriores de DFS/Bellman-Ford.
André deve conferir o hash antes da execução e usar a versão alinhada do código,
Python e dependências na mesma máquina das medições anteriores.

**Verificação:** 32 testes de BFS, Dijkstra, preparação/medição e executores
passaram. Foram testadas a transformação dos pesos, a exportação, a recusa de
sobrescrita e a detecção de conjuntos diferentes mesmo com quantidades iguais.
O comando também foi executado no CSV real com saída temporária: 18 configurações,
90 tempos e alcances de 2.661, 3.360 e 3.443 nos recortes de 10%, 50% e 100%.
CSV, benchmarks anteriores e relatório consolidado foram preservados em bytes.
Os resultados temporários foram removidos e não são a medição oficial de André.

**Checklist das atividades de Brenda na nova divisão:**
- [x] Conferir o BFS e preparar/testar o comando do benchmark.
- [ ] Commit do benchmark — não realizado, conforme pedido de Brenda.
- [ ] Enviar comando e hash ao André — instruções prontas no README e neste log; envio por Brenda.
- [ ] Consultar as professoras sobre Bellman-Ford com uma fonte em 100%.
- [ ] Juntar os resultados no `parte2_report.json`, após receber as novas medições.
- [ ] Reclassificar B02 como análise visual de desempenho.
- [ ] Registrar a ligação entre achados exploratórios e explanatórias.
- [ ] Integrar ao PDF as seções de BFS, Dijkstra, transformação e resposta à pesquisa.
- [ ] Conferir BFS à mão e executar testes em clone limpo.
- [ ] Concluir registro de IA e reflexão.

**Apoio de IA:** ChatGPT (Codex) revisou os arquivos existentes, implementou o
executor e seus testes após aprovação e registrou comandos e resultados técnicos.
Não foi feito commit nem enviada mensagem ao André. A medição no ambiente de
André e a consulta às professoras continuam pendentes.

## Organização das visualizações de Brenda em documento próprio — 23/11/2026

A pedido de Brenda, as classificações, fontes, justificativas e notas já aprovadas
foram reunidas em [visualizacoes_brenda_parte2.md](visualizacoes_brenda_parte2.md),
seguindo a estrutura do documento de André: uso de IA, organização, paleta,
seções por figura, limites e reprodução. Os textos aprovados foram preservados;
os detalhes técnicos descrevem os dados e a implementação existentes.

**Checklist desta organização:**
- [x] Documento das três figuras criado no padrão do documento de André.
- [x] Justificativas e notas aprovadas reunidas, com fontes e limites.
- [x] Referência ao documento acrescentada ao README.
- [ ] Integração das figuras e textos ao PDF técnico.
- [ ] Conferência manual de BFS e conclusão da declaração de IA.

**Apoio de IA:** ChatGPT (Codex) organizou o documento solicitado a partir dos
registros existentes, sem alterar gráficos, algoritmos, medições ou interpretações
aprovadas. O histórico do log foi preservado.

## Justificativa aprovada das faixas de votos — 23/11/2026

**Figura:** `out/parte2/brenda_01_faltantes_por_faixa.png`.

**Faixas:** 1–4, 5–19, 20–99, 100–499 e 500 ou mais votos recebidos por candidato.

> Adotei as faixas sugeridas durante a discussão com apoio de IA para comparar candidatos com diferentes volumes de votos em cinco grupos legíveis, mantendo também aqueles com poucos votos. Os cortes são uma escolha de apresentação, não limites estatísticos. Como sua definição influencia a aparência do gráfico, apresento os intervalos e as quantidades de candidatos, votos e registros sem SOURCE para contextualizar os percentuais.

**Checklist atualizado desta etapa:**
- [x] Três figuras implementadas e conferidas.
- [x] Notas analíticas das três figuras aprovadas e registradas.
- [x] Justificativas das três figuras aprovadas e registradas, incluindo os cortes das faixas.
- [x] Classificação das figuras e resposta à pesquisa registradas.
- [x] README atualizado.
- [ ] Conferência manual de BFS.
- [ ] Consolidação do registro de IA para revisão — ainda não iniciada.

**Apoio de IA:** ChatGPT (Codex) sugeriu os cortes na discussão anterior e organizou a justificativa acima. Brenda aprovou as faixas e posteriormente aprovou este texto para registro. Não foram alterados os dados, as faixas ou a imagem nesta etapa. As pendências de justificativa nas entradas anteriores representam o histórico e foram resolvidas por esta aprovação.

## Classificação aprovada das visualizações — 23/11/2026

Brenda aprovou a classificação das suas três figuras conforme a finalidade de cada uma:

| Figura | Classificação | Finalidade |
|---|---|---|
| [Faltantes por faixa](../out/parte2/brenda_01_faltantes_por_faixa.png) | Exploratória | Examinar a qualidade dos dados. |
| [Tempos de BFS e Dijkstra](../out/parte2/brenda_02_tempos_bfs_dijkstra.png) | Exploratória | Comparar o comportamento das implementações nos recortes. |
| [Transformação dos pesos](../out/parte2/brenda_03_efeito_transformacao.png) | Explanatória | Explicar, no exemplo selecionado, como somar 1 por arco elimina a vantagem do caminho antes mais barato. |

Somadas às duas exploratórias e à explanatória registradas em `visualizacoes_andre_parte2.md`, as seis figuras ficam organizadas em quatro exploratórias e duas explanatórias. Essa contagem descreve a classificação aprovada, sem atestar o atendimento de todos os demais critérios de AVD. A figura de transformação ilustra um único caso e não sustenta uma conclusão sobre a frequência do comportamento na rede inteira.

**Checklist atualizado desta etapa:**
- [x] Três figuras implementadas e conferidas.
- [x] Notas analíticas das três figuras aprovadas e registradas.
- [x] Justificativas da segunda e terceira figuras aprovadas e registradas.
- [x] README atualizado com as aprovações e pendências.
- [x] Resposta à pergunta de pesquisa incluída no notebook.
- [x] Classificação das três figuras aprovada e registrada.
- [ ] Justificativa das faixas da primeira figura — adiada.
- [ ] Conferência manual de BFS.

**Apoio de IA:** ChatGPT (Codex) propôs a classificação conforme as finalidades discutidas e a registrou após aprovação de Brenda.

## Resposta à pergunta de pesquisa registrada no notebook — 23/11/2026

Brenda aprovou a síntese abaixo e sua inclusão ao final do estudo de caso no notebook de experimentos. No arquivo atual, o estudo está numerado como seção 18, anteriormente referido na conversa como seção 20. Foi acrescentada somente uma célula Markdown, sem executar código ou alterar resultados.

> No exemplo analisado, somar 1 a cada arco altera a preferência entre os caminhos: o caminho via 9cds, inicialmente mais barato, passa a empatar com o direto. O Dijkstra retorna um caminho ótimo nos pesos transformados, mas esse caminho tem custo maior em PESO do que o encontrado por Bellman-Ford. Portanto, a transformação permite executar Dijkstra, porém não garante preservar os caminhos mínimos anteriores. Como analisamos um único par em um subgrafo, não podemos afirmar com que frequência isso acontece na rede inteira.

**Checklist atualizado desta etapa:**
- [x] Três figuras implementadas e conferidas.
- [x] Notas analíticas das três figuras aprovadas e registradas.
- [x] Justificativas da segunda e terceira figuras aprovadas e registradas.
- [x] README atualizado com as aprovações e pendências.
- [x] Resposta à pergunta de pesquisa incluída no notebook.
- [ ] Justificativa das faixas da primeira figura — adiada.
- [ ] Conferência manual de BFS.

**Apoio de IA:** ChatGPT (Codex) organizou a síntese com base nas interpretações discutidas e aprovadas por Brenda e inseriu o texto após sua aprovação.

## Justificativa aprovada da figura de transformação dos pesos — 23/11/2026

**Figura:** `out/parte2/brenda_03_efeito_transformacao.png`.

> Escolhi barras agrupadas para facilitar a comparação dos custos de cada caminho antes e depois de somar 1 a cada arco. Como o exemplo possui apenas dois caminhos e duas versões dos pesos, a figura permite visualizar os valores e o empate após a transformação com poucos elementos.

A pedido de Brenda, foi mantido o estudo de caso existente, sem implementar a ampliação para vários pares. Permanece o limite de ilustração de um exemplo selecionado, sem generalização para a rede inteira.

**Checklist atualizado:**
- [x] Três figuras implementadas e conferidas.
- [x] Notas analíticas das três figuras aprovadas e registradas.
- [x] Justificativa da segunda figura aprovada e registrada.
- [x] Justificativa da terceira figura aprovada e registrada.
- [ ] Justificativa das faixas da primeira figura — adiada.
- [ ] Conferência manual de BFS.

**Apoio de IA:** Brenda explicou que as barras facilitam a comparação antes e depois da transformação por haver poucos elementos no exemplo. ChatGPT (Codex) organizou a redação e registrou o texto após sua aprovação.

## Justificativa aprovada da figura de tempos BFS e Dijkstra — 23/11/2026

**Figura:** `out/parte2/brenda_02_tempos_bfs_dijkstra.png`.

> Escolhi três painéis, um por fonte, para facilitar a comparação dos tempos de BFS e Dijkstra em cada fonte e nos diferentes tamanhos de recorte. A mesma escala vertical permite também comparar os tempos entre os painéis.

**Checklist atualizado:**
- [x] Figuras atualizadas com contagens e alcance conferido.
- [x] Notas analíticas das três figuras aprovadas e registradas.
- [x] Justificativa da figura de tempos aprovada e registrada.
- [ ] Justificativa das faixas da primeira figura — adiada.
- [ ] Justificativa da terceira figura.
- [ ] Conferência manual de BFS.

**Apoio de IA:** Brenda informou que escolheu a apresentação para comparação e aprovou a redação acima. ChatGPT (Codex) organizou e registrou o texto.

## Nota aprovada da figura de transformação dos pesos — 23/11/2026

**Figura:** `out/parte2/brenda_03_efeito_transformacao.png`.

**Nota analítica aprovada:**

> Neste exemplo, a transformação elimina a vantagem do caminho via 9cds, que tinha menor custo em PESO. Como esse caminho possui dois arcos, seu custo aumenta em 2, enquanto o direto aumenta em 1. Os caminhos passam a empatar, e o Dijkstra retorna o direto, cujo custo nos pesos anteriores à transformação é maior. Isso ilustra que somar uma constante a cada arco pode alterar o caminho retornado, sem preservar a preferência pelo caminho originalmente mais barato.

**Limite do estudo:** trata-se de um exemplo selecionado, sem ciclo negativo, que não estima a frequência desse comportamento na rede inteira. O caminho direto não se tornou exclusivamente melhor nos pesos transformados: ambas as alternativas têm custo 2.

**Checklist atualizado:**
- [x] Figuras atualizadas com contagens e alcance conferido.
- [x] Nota analítica da primeira figura aprovada e registrada.
- [x] Nota analítica da segunda figura aprovada e registrada.
- [x] Nota analítica da terceira figura aprovada e registrada.
- [ ] Justificativa das faixas da primeira figura — adiada.
- [ ] Demais justificativas de escolha das figuras.
- [ ] Conferência manual de BFS.

**Apoio de IA:** Brenda levantou a possibilidade de a transformação deixar de favorecer caminhos originalmente mais baratos. ChatGPT (Codex) explicou a diferença entre custo anterior e transformado, esclareceu o empate e organizou a nota acima, registrada após aprovação de Brenda.

## Nota aprovada da figura de tempos BFS e Dijkstra — 23/11/2026

**Figura:** `out/parte2/brenda_02_tempos_bfs_dijkstra.png`.

**Nota analítica aprovada:**

> Para Siva1979, BFS e Dijkstra apresentam tempos médios próximos no recorte de 10%. Nos recortes de 50% e 100%, a média do BFS fica acima da do Dijkstra. Para Gwynand e John Carter, o BFS apresenta média maior nos três tamanhos. Entretanto, há sobreposição entre alguns intervalos mínimo–máximo e grande variação do BFS em Gwynand a 10%. Esses resultados descrevem as implementações e o ambiente medidos, sem demonstrar uma vantagem geral de Dijkstra. Os conjuntos de usuários alcançados foram iguais entre os algoritmos em cada configuração.

**Checklist atualizado:**
- [x] Figuras atualizadas com contagens e alcance conferido.
- [x] Nota analítica da primeira figura aprovada e registrada.
- [x] Nota analítica da segunda figura aprovada e registrada.
- [ ] Justificativa das faixas da primeira figura — adiada.
- [ ] Nota analítica da terceira figura e demais justificativas.
- [ ] Conferência manual de BFS.

**Apoio de IA:** Brenda descreveu a proximidade inicial dos tempos para Siva1979 e as diferenças entre as médias nas outras configurações. ChatGPT (Codex) organizou a redação, acrescentou as ressalvas sobre variação, sobreposição dos intervalos e alcance conferido, e registrou o texto após aprovação de Brenda.

## Nota aprovada da figura de faltantes — 23/11/2026

**Figura:** `out/parte2/brenda_01_faltantes_por_faixa.png`.

**Nota analítica aprovada:**

> A primeira faixa apresenta o maior percentual de votos sem origem identificada, mas reúne apenas 577 votos, dos quais 23 estão sem SOURCE. Por isso, o percentual deve ser lido junto às quantidades absolutas: a barra mais alta não representa a maior quantidade de registros sem origem.

**Justificativa da escolha das faixas:** aprovada e registrada na entrada “Justificativa aprovada das faixas de votos”, acima.

**Checklist atualizado:**
- [x] Figuras atualizadas com contagens e alcance conferido.
- [x] Nota analítica da primeira figura aprovada e registrada.
- [ ] Justificativa das faixas da primeira figura — adiada.
- [ ] Justificativas e notas analíticas da segunda e terceira figuras.
- [ ] Conferência manual de BFS.

**Apoio de IA:** Brenda levantou a preocupação com o percentual da primeira faixa e aprovou o texto acima. ChatGPT (Codex) esclareceu o cálculo agregado, organizou a redação e registrou a versão aprovada.

## Contagens e alcance nos rótulos — 23/11/2026

Após aprovação de Brenda, a figura de faltantes passou a mostrar a quantidade absoluta sem SOURCE acima de cada barra, junto ao percentual: 23, 147, 829, 642 e 20 registros, totalizando 1.661. As faixas e a proporção agregada foram mantidas.

Na figura de tempos, cada rótulo do eixo horizontal agora informa percentual do recorte, quantidade de arcos e quantidade de outros usuários alcançados. O rodapé esclarece que o alcance exclui a fonte. Os valores foram conferidos independentemente entre BFS e Dijkstra na etapa anterior. As medições, os algoritmos, os ambientes separados e a escala comum dos três painéis foram mantidos.

**Checklist da revisão das figuras:**
- [x] Conferir independentemente os conjuntos alcançados por BFS e Dijkstra.
- [x] Acrescentar números absolutos sem SOURCE à figura de faltantes.
- [x] Acrescentar alcance aos rótulos da figura de tempos.
- [ ] Registrar justificativas e notas analíticas autorais, incluindo a variabilidade das medições e o empate no estudo de caso.
- [ ] Fazer a conferência manual de BFS.

**Apoio de IA:** ChatGPT (Codex) ajustou os rótulos aprovados em `src/viz.py` e atualizou este registro, sem novas medições ou interpretação analítica.

## Conferência independente do alcance — 23/11/2026

Após aprovação de Brenda, foi executada uma conferência separada de BFS em PESO e Dijkstra em PESO + 1 nos recortes do benchmark, com a mesma semente e as mesmas fontes. A conferência compara os conjuntos completos de usuários com distância finita, excluindo a fonte, e não apenas suas quantidades. Não mede tempos e não altera os algoritmos ou o benchmark existente.

As nove comparações passaram. Para cada uma das três fontes, foram alcançados 2.661 outros usuários em 10%, 3.360 em 50% e 3.443 em 100%. Os conjuntos são iguais entre os algoritmos, e contagens e tamanhos conferem com o benchmark. O arquivo do benchmark permaneceu idêntico em bytes durante a conferência.

A pedido de Brenda, o script separado e seu JSON adicional foram removidos. A conferência foi incorporada à célula existente da seção 13 do notebook de experimentos: executa os dois algoritmos e usa `assert` para comparar os conjuntos, mantendo `alcances_benchmark` para as etapas seguintes. Para repetir, execute a preparação da seção 12 e a célula da seção 13. Nenhum arquivo adicional é criado. Esta conferência automática não substitui a conferência manual de BFS, que continua pendente.

**Checklist da revisão das figuras:**
- [x] Conferir independentemente os conjuntos alcançados por BFS e Dijkstra.
- [ ] Acrescentar números absolutos sem SOURCE à figura de faltantes.
- [ ] Acrescentar alcance aos rótulos da figura de tempos.
- [ ] Registrar justificativas e notas analíticas autorais, incluindo a variabilidade das medições e o empate no estudo de caso.
- [ ] Fazer a conferência manual de BFS.

**Apoio de IA:** ChatGPT (Codex) executou a conferência aprovada, registrou o resultado técnico e, a pedido de Brenda, transferiu a verificação para a célula existente da seção 13, removendo os arquivos extras. Não alterou algoritmos ou medições.

## Figura do estudo de caso implementada — 23/11/2026

Brenda aprovou barras agrupadas por caminho, comparando PESO (azul `#0072B2`, hachura `///`) e PESO + 1 (laranja-avermelhado `#D55E00`, hachura `..`), com valores escritos inclusive no custo zero. A função `efeito_transformacao`, em `src/viz.py`, lê somente `out/parte2/estudo_transformacao.json` e salva `brenda_03_efeito_transformacao.png`. O comando `python -m src.viz --parte2` agora gera as seis figuras, sem executar novamente algoritmos ou benchmarks.

Os valores salvos são 1 e 2 para o caminho direto e 0 e 2 para o caminho via 9cds, respectivamente em PESO e PESO + 1. O rodapé identifica o empate, os caminhos retornados no experimento e o escopo de exemplo selecionado. A figura não apresenta uma estimativa de frequência para a rede inteira.

**Checklist desta etapa:**
- [x] Centralizar as seis figuras em `src/viz.py`.
- [x] Implementar a terceira figura com os dados já exportados.
- [x] Executar o gerador conjunto e conferir visualmente os rótulos, o zero e o empate da terceira figura.
- [ ] Registrar a justificativa autoral da escolha e escrever a nota analítica de cada uma das três figuras adicionais.
- [ ] Fazer a conferência manual de BFS, mantida pendente a pedido de Brenda.

**Apoio de IA:** ChatGPT (Codex) implementou o desenho aprovado e atualizou as instruções de geração e este registro. As justificativas e interpretações autorais continuam pendentes.

## Geração conjunta das figuras em viz.py — 23/11/2026

Brenda aprovou manter as funções de todas as figuras em `src/viz.py`, gerar as cinco figuras implementadas pelo comando `python -m src.viz --parte2` e retirar apenas as quatro células de título e desenho das seções 18 e 19 do notebook. O estudo de caso da seção 20 e todos os experimentos foram preservados. A figura do estudo de caso continua pendente.

O comando usa os CSVs bruto e tratado e os JSONs já salvos. Não executa algoritmos ou novas medições. Mantém a paleta e os arquivos de André e acrescenta `brenda_01_faltantes_por_faixa.png` e `brenda_02_tempos_bfs_dijkstra.png`. O arquivo `dados_visualizacoes_andre.json` continua contendo os dados das três figuras de André. As chamadas pelo notebook descritas nos registros anteriores foram substituídas por essa geração conjunta.

**Apoio de IA:** ChatGPT (Codex) integrou as chamadas existentes, removeu as quatro células autorizadas e atualizou a documentação, sem mudar as medidas ou escrever novas interpretações.

## Padronização visual e nomes das figuras — 23/11/2026

Brenda pediu que suas figuras acompanhassem a paleta e a nomeação das figuras de André e confirmou os nomes `brenda_01_faltantes_por_faixa.png` e `brenda_02_tempos_bfs_dijkstra.png`. As referências do notebook e deste log foram atualizadas.

O padrão usa azul `#0072B2`, laranja-avermelhado `#D55E00`, texto escuro e rodapés `#52606d`. A figura de faltantes usa azul com hachuras; a de tempos distingue BFS por círculo e linha contínua e Dijkstra por quadrado e linha tracejada. Títulos alinhados à esquerda e separadores decimais com vírgula acompanham o padrão existente. Foram mantidas as medidas, as faixas e as escalas previamente aprovadas, incluindo a escala linear comum dos três painéis de BFS/Dijkstra.

**Apoio de IA:** ChatGPT (Codex) ajustou a apresentação e as referências de arquivos e gerou novamente as duas imagens com os mesmos dados, sem novas medições ou interpretação analítica. As saídas antigas das duas células de figuras foram limpas para não exibir imagens incorporadas desatualizadas; as demais células foram preservadas.

## Preparação do estudo de caso da transformação — 23/11/2026

Brenda aprovou simplificar a comparação para um único recorte pequeno, com origem, destino e dois caminhos alternativos. Foi apresentado e aprovado o subgrafo induzido de `Siva1979`, `9cds` e `Pilotguy`, contendo exatamente três arcos reais: Siva1979 → Pilotguy (PESO 1), Siva1979 → 9cds (PESO -1) e 9cds → Pilotguy (PESO 1). Todos os arcos entre esses usuários são preservados. Não há ciclos nessa estrutura.

A busca do exemplo usou a fonte Siva1979, intermediários e destinos em ordem lexicográfica e selecionou o primeiro subgrafo induzido com exatamente os três arcos do triângulo dirigido, algum peso negativo e nenhuma outra ocorrência. Não foi exigida mudança do caminho para selecionar o caso.

As células da seção 20 chamam os algoritmos existentes no mesmo recorte: Bellman-Ford em PESO e Dijkstra em PESO + 1. O caminho de Dijkstra é avaliado também em PESO e comparado ao mínimo de Bellman-Ford. As duas alternativas são registradas para explicitar o empate nos custos transformados. O resultado previsto para exportação é `out/parte2/estudo_transformacao.json`, separado dos casos obrigatórios e do benchmark. Essas células foram adicionadas sem execução nesta etapa; a figura ainda não foi implementada.

**Justificativa da escolha:** aprovada e registrada na entrada “Justificativa aprovada da figura de transformação dos pesos”, acima. **Nota analítica:** aprovada e registrada na entrada “Nota aprovada da figura de transformação dos pesos”, acima. O estudo é um exemplo selecionado e não uma estimativa do comportamento dos caminhos na rede inteira.

**Apoio de IA:** ChatGPT (Codex) localizou o exemplo no CSV por leitura, apresentou os arcos para aprovação e acrescentou as chamadas, conferências e exportação no notebook. Não reimplementou os algoritmos e não executou essas novas células.

## Visualização de faltantes por faixa de votos — 23/11/2026

Brenda escolheu agrupamento dos candidatos por faixas e confirmou barras simples nas faixas 1–4, 5–19, 20–99, 100–499 e 500 ou mais votos. A medida aprovada é a proporção agregada: 100 × soma dos votos sem SOURCE / soma dos votos da faixa. Não é a média dos percentuais individuais dos candidatos. A quantidade de candidatos e de votos é indicada em cada faixa, sem limite mínimo adicional.

As faixas usam o total de registros por TARGET no CSV original, antes da exclusão dos registros sem SOURCE. A função `faltantes_por_faixa`, em `src/viz.py`, não altera os dados e devolve a tabela usada para desenhar as barras. Valores ausentes são identificados pela leitura do CSV em pandas, de forma consistente com o notebook de tratamento. Faixas vazias ficam sem percentual.

Saída: `out/parte2/brenda_01_faltantes_por_faixa.png`. A geração foi conferida quanto à legibilidade e à preservação dos totais: 198.275 votos, 1.661 registros sem SOURCE e 3.497 candidatos. A seção 19 do notebook de experimentos contém a chamada reproduzível e a exibição da tabela; essa nova célula foi adicionada sem execução no notebook. O CSV original permaneceu apenas como entrada de leitura.

**Justificativa da escolha das faixas:** aprovada e registrada na entrada “Justificativa aprovada das faixas de votos”, acima. **Nota analítica:** aprovada e registrada na entrada “Nota aprovada da figura de faltantes”, acima. A figura não determina, por si só, o mecanismo ou a causa dos dados ausentes.

**Apoio de IA:** ChatGPT (Codex) implementou a agregação e o desenho em pandas e matplotlib, gerou a prévia, conferiu totais e legibilidade e acrescentou a chamada ao notebook após a aprovação explícita das faixas e da proporção. As justificativas e interpretações permanecem com o grupo.

## Visualização de desempenho de BFS e Dijkstra — 23/11/2026

Brenda escolheu três painéis, um por fonte, para apresentar BFS e Dijkstra. A escolha foi informada na conversa antes da implementação. A figura lê apenas `out/parte2/benchmark_bfs_dijkstra.json`, mantendo os dois algoritmos no mesmo ambiente. Não mistura os tempos de DFS e Bellman-Ford obtidos em outra máquina.

A função `tempo_bfs_dijkstra`, em `src/viz.py`, mostra médias e barras de mínimo–máximo das cinco repetições, em segundos, nos recortes de 10%, 50% e 100% dos arcos. A escala vertical é linear e comum aos painéis. As barras não são intervalos de confiança. Cores e marcadores distinguem as séries, e o rodapé identifica a fonte dos dados, os pesos e o ambiente.

Saída: `out/parte2/brenda_02_tempos_bfs_dijkstra.png`. A seção 18 do notebook de experimentos contém a chamada reproduzível, adicionada sem execução no notebook. A figura foi gerada separadamente e inspecionada para conferir legibilidade; nenhum algoritmo ou benchmark foi executado nessa geração.

**Justificativa da escolha:** aprovada e registrada na entrada “Justificativa aprovada da figura de tempos BFS e Dijkstra”, acima. **Nota analítica:** aprovada e registrada na entrada “Nota aprovada da figura de tempos BFS e Dijkstra”, acima.

**Apoio de IA:** ChatGPT (Codex) implementou o desenho em matplotlib, gerou a prévia, conferiu a legibilidade e acrescentou a chamada ao notebook após a escolha da apresentação. As escolhas e interpretações finais devem ser conferidas e registradas pelo grupo.

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
