# Declaração de uso de IA — registro preparado da Parte 2

**Estado: rascunho para revisão do grupo, sem assinaturas.** Este registro não
afirma que todos os usos estiveram nas situações permitidas. O PDF oficial traz
restrições à geração de análises, escolhas de gráficos e implementações. O log
contém autorizações específicas informadas por André, sem comprovação escrita
anexada. O alcance dessas exceções precisa ser confirmado com as professoras.

## 1. Identificação a completar pelo grupo

- Turma e número do grupo: preencher.
- Link do repositório e data de entrega: preencher.
- Nomes completos, matrículas e pacotes de todos os integrantes: preencher.
- Responsáveis conhecidos da Parte 2: Brenda e André, conforme a divisão registrada.

## 2. Ferramentas efetivamente registradas

| Ferramenta | Uso documentado | Versão / plano |
|---|---|---|
| ChatGPT / Codex | Código de integração, tratamento e conferência, benchmark, visualizações, sugestões, explicações e redação técnica | Confirmar nas conversas; não inferir versões históricas |
| Claude | Há marcadores no código, testes e configuração do projeto; cada integrante deve identificar seu uso | Confirmar pelo integrante |

## 3. Registro dos usos da Parte 2

Os registros abaixo são uma compilação do avd_log.md e das conversas. Não se deve
marcar a opção do formulário que afirma uso somente permitido sem conferir os
registros com as diretrizes e as autorizações efetivamente concedidas.

| ID | Parte do projeto | O que foi aproveitado / como foi conferido |
|---|---|---|
| P2-01 | Notebook de tratamento | Apoio em pandas, conferências de faltantes, repetições, laços e incremento; preservação do bruto e comparação de todas as linhas tratadas |
| P2-02 | src/graphs/io.py e testes do dataset | Carregador e testes produzidos com IA após autorização específica relatada por André; testes de direção, nomes, paralelos e preservação dos pesos |
| P2-03 | src/graphs/metricas_dataset.py | Métricas e testes com exemplo pequeno; conferência das somas dos graus e exportação |
| P2-04 | Notebook de experimentos, src/solve.py e src/cli.py | Chamadas e organização dos resultados dos algoritmos existentes, exportação dos casos e integração da CLI; testes e comparação com os resultados salvos |
| P2-05 | src/benchmark.py e src/benchmark_dfs_bellman.py | Código de recortes, seleção, medição, ambiente, hash e complemento do benchmark; aquecimento excluído, estatísticas conferidas e testes de preservação |
| P2-06 | src/viz.py e documentos de visualizações | Sugestões de figuras e faixas, implementação, acessibilidade, conferência, discussão e organização das notas; escolhas aprovadas na conversa, com participação de IA além de revisão ortográfica |
| P2-07 | Estudo da transformação | Localização do exemplo real, preparação do recorte e comparação; discussão do empate, explicação e redação aprovadas por Brenda |
| P2-08 | Consolidação e verificações finais | Inclusão dos casos no relatório, leitura do benchmark comum, hashes, ambientes, cobertura, cenários inválidos e testes em clone isolado |
| P2-09 | src/verificar_parte2.py | Conferências técnicas de RESULT, outliers e DFS geradas com apoio de IA; o JSON de DFS identifica explicitamente que a conferência é automática |
| P2-10 | README, log e relatório da Parte 2 | Atualizações, síntese e compilação técnica; notas aprovadas preservadas e textos novos/atualizados identificados para revisão autoral |

Datas e responsáveis por uso devem ser conciliados com as entradas de 20 a
24/11/2026 do log e os commits. A compilação não atribui a um integrante um uso
cuja autoria individual não foi confirmada na conversa.

## 4. Conversas e evidências

Escolher no formulário oficial: links completos compartilhados com as professoras
ou blocos individuais por uso. Preencher os links reais; nenhum foi inventado.

- Conversas de Brenda: inserir links completos ou anexos.
- Conversas de André: inserir links completos ou anexos.
- Conversas dos demais integrantes: reunir no documento conjunto.
- Evidências técnicas: avd_log.md, notebooks, testes, JSONs e histórico de commits.

## 5. Trechos de código

As funções de preparação e medição estão em src/benchmark.py; execução e
complemento em src/benchmark_dfs_bellman.py; carregamento em carregar_dataset;
métricas em src/graphs/metricas_dataset.py; integração em src/solve.py e src/cli.py;
figuras em src/viz.py; verificações em src/verificar_parte2.py. Os notebooks têm
marcadores nas células correspondentes. O grupo deve preencher a Seção 6 do
formulário com o ID do uso e o integrante que sabe explicar cada trecho.
Nenhuma assinatura ou confirmação de domínio foi presumida por esta compilação.

## 6. Reflexão autoral do grupo — a preencher

O formulário exige 10 a 15 linhas escritas pelo grupo. Não foi gerado um relato
pessoal em nome dos integrantes. Para completar, o grupo deve relatar onde a IA
ajudou, onde sugeriu algo inadequado, como verificou os resultados e o que aprendeu.
Exemplos de ocorrências para recordar, não um texto pronto: diferença entre VOTE
e PESO; empate após somar 1 por arco; comparação entre máquinas; exigências de
quantidade de figuras e fontes; necessidade de conferir os critérios diretamente.

## 7. Fechamento obrigatório

- [ ] Completar identificação, ferramentas/planos e links ou blocos de uso.
- [ ] Confirmar com as professoras a conformidade dos usos e o alcance das exceções.
- [ ] Cada integrante revisar seus trechos, registros e a reflexão do grupo.
- [ ] Preencher e assinar o formulário oficial por todos os integrantes.
- [ ] Substituir o rascunho em docs/DECLARACAO_IA.pdf pela versão final assinada e entregar no Classroom.

## Orientações anteriores preservadas

Cada integrante junta as próprias conversas com IA e escreve um documento com o seu uso. Depois juntamos os cinco num só, que vira a declaração em `docs/DECLARACAO_IA.pdf`. Até lá, ninguém apaga conversa.

A marca no código não fica para o fim: todo trecho feito com apoio de IA leva `# [IA] <ferramenta> – <finalidade>` no mesmo commit em que entra. É por ela que cada um vai achar os próprios trechos para a Seção 6 da declaração.

Permitido: dúvidas conceituais, entender erros e depurar código do grupo, sugerir testes e mapas extras (conferidos pelo grupo), sintaxe de pandas e das bibliotecas de visualização, revisão de ortografia.

Proibido: gerar io.py, estados.py, graph.py ou algorithms.py; gerar análises, notas analíticas ou a prova do m05; escolher ou interpretar gráficos; resolver os mapas.
