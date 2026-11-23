# Parte 2 — Entrega das medições de André para consolidação

Responsável: André. Consolidação do relatório final: Brenda, com revisão de André.

**Situação: medições concluídas e conferidas.** O JSON está com `completo: true`:
16 configurações, 80 tempos medidos, cinco repetições e um aquecimento completo
por configuração. As médias, medianas, mínimos e desvios padrão amostrais foram
recalculados para conferência. As estatísticas e os tempos originais foram preservados.

| Algoritmo | Fontes em 10% | Fontes em 50% | Fontes em 100% | Configurações |
|---|---:|---:|---:|---:|
| DFS | 3 | 3 | 3 | 9 |
| Bellman-Ford | 3 | 3 | 1 | 7 |
| Total | 6 | 6 | 4 | 16 |

## Arquivos

- Executor reproduzível: [src/benchmark_dfs_bellman.py](../src/benchmark_dfs_bellman.py).
- Medições: [benchmark_dfs_bellman.json](../out/parte2/benchmark_dfs_bellman.json).
- Procedimento comum: [src/benchmark.py](../src/benchmark.py).
- Contribuição anterior de Brenda: [benchmark_bfs_dijkstra.json](../out/parte2/benchmark_bfs_dijkstra.json).

## Procedimento

São usados os mesmos recortes aninhados por ocorrências de arcos, semente 42 e
seleção de fontes do procedimento de Brenda: `Siva1979`, `Gwynand` e `John Carter`.
Os tamanhos são 10%, 50% e 100% dos arcos, com o número efetivo de vértices
registrado em cada configuração. Laços e ocorrências paralelas são preservados.

DFS e Bellman-Ford recebem a coluna PESO, sem deslocamento. Cada configuração
contém um aquecimento fora do cronômetro e cinco chamadas medidas. Leitura,
preparação dos recortes, contagem de alcance e exportação ficam fora do intervalo.
As implementações dos algoritmos não foram alteradas nesta tarefa.

Em 23/11/2026, André inicialmente confirmou três fontes para Bellman-Ford e,
posteriormente, autorizou concluir apenas `Siva1979` no grafo completo, preservando
as três fontes já medidas em 10% e 50%. DFS mantém três fontes nos três tamanhos.
O conjunto final contém 16 configurações, 80 tempos medidos e 16 aquecimentos.
Essa diferença de quantidade de fontes deve ser preservada na consolidação;
não há medições de Gwynand ou John Carter para Bellman-Ford em 100%.

A execução original chegou a iniciar o aquecimento de Gwynand em 100% antes
do encerramento controlado. Essa chamada foi interrompida e não integra os tempos,
as estatísticas ou os 16 aquecimentos completos registrados. O ajuste de escopo
consta no próprio JSON, sem alterar os valores medidos.

## Como verificar a entrega

- O arquivo é atualizado após cada configuração concluída.
- **Somente `completo: true` confirma que todas as 16 configurações selecionadas terminaram.**
- Conferir 16 combinações distintas de algoritmo, percentual e fonte, observando
  `fontes_bellman_por_percentual` e a redução autorizada em 100%.
- Conferir cinco tempos, um aquecimento e unidade em segundos em cada configuração.
- Comparar fonte, percentual, tamanho, grau de saída e alcance com as configurações
  correspondentes de BFS/Dijkstra.
- Conferir o SHA-256 do CSV de entrada e preservar a identificação dos pesos.

## Ambiente e consolidação

O ambiente das medições deve ser lido do próprio JSON. A execução de André usa
Python 3.12.6, Windows, Intel Core i5-1335U e aproximadamente 16 GB de memória.
O arquivo entregue anteriormente por Brenda registra Python 3.12.10, Windows,
Intel Core i5-1235U e aproximadamente 8 GB de memória.

Os ambientes são diferentes. Ao consolidar `out/parte2/parte2_report.json`,
preservar o ambiente de cada contribuição. Não atribuir as medições de André
à máquina de Brenda, nem apresentar diferenças de tempo entre essas contribuições
como se o ambiente fosse controlado. Se a comparação exigir o mesmo ambiente,
repetir as medições necessárias em uma única máquina pelo procedimento comum.
Essa escolha e sua discussão devem ser feitas pelo grupo.

Brenda deve incorporar os registros de `medicoes` após a conferência de conclusão,
mantendo os campos de repetição, tempos, estatísticas, tarefa, fonte, tamanho,
versão dos pesos e semente. André revisa a consolidação. Este documento não cria
o relatório final, não substitui a discussão crítica e não envia mensagens a Brenda.

## Reprodução

Na raiz do projeto, com o CSV tratado gerado pelo notebook:

```powershell
python -m src.benchmark_dfs_bellman --out out/parte2/benchmark_dfs_bellman_nova_execucao.json
```

O executor exige um destino que ainda não exista, para preservar as medições
anteriores. Bellman-Ford pode levar horas nos maiores recortes, pois a implementação
atual realiza todas as passagens. Não substituir esse tempo por extrapolação nem
misturar chamadas interrompidas com as cinco repetições concluídas.

## Uso de IA

ChatGPT (Codex) auxiliou nas chamadas dos algoritmos existentes, na execução das
medições, na exportação e neste registro técnico, por solicitação de André.
Os códigos correspondentes têm marcadores de IA. A interpretação dos resultados,
a comparação com a complexidade teórica e as conclusões são responsabilidade do grupo.
