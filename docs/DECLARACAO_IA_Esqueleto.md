# Declaração de uso de IA — registro do projeto

Registro atualizado em 24/11/2026 com base nas marcações `[IA]` no código, nos
testes e nos notebooks, no log e nas confirmações da equipe. Este arquivo é a
base editável para o formulário conjunto e não contém assinaturas.

## Participação da IA e responsabilidade pelas decisões

Conforme informado pela equipe, a IA apresentou sugestões, exemplos, explicações
e alternativas, além de apoiar a implementação, a depuração, os testes, as
visualizações e a documentação. As decisões sobre adotar, modificar ou rejeitar
as sugestões foram tomadas pelos membros da equipe, e não pela IA de forma
autônoma. A escolha das soluções incorporadas e a validação do conteúdo entregue
couberam aos integrantes responsáveis.

Isso inclui as decisões sobre tratamento dos dados, regra de pesos, transformação
para Dijkstra, recortes e fontes, escopo dos experimentos, apresentação dos
gráficos e redação das análises. A IA apresentou possibilidades e executou tarefas
de apoio conforme solicitações e orientações recebidas; não foi responsável pelas
decisões finais do projeto. As análises e justificativas foram revisadas pelo
grupo, conforme confirmação recebida.

Essa distinção não significa que o uso tenha se limitado a sugestões textuais.
Houve geração e adaptação de trechos de código, testes, figuras e redação técnica
com IA, conforme discriminado abaixo. A equipe mantém o registro dessas
contribuições e assume a responsabilidade pelas decisões e pelo conteúdo entregue.

| Decisão humana registrada | Responsável ou evidência |
|---|---|
| Excluir linhas sem SOURCE apenas do grafo; manter repetições e laços | Decisões de André registradas no log |
| Aplicar a regra de incremento para PESO, preservando VOTE | Regra informada e confirmada por André, com sugestão inicial atribuída por ele à professora Laura |
| Usar PESO + 1 em uma cópia para Dijkstra | Transformação definida por Brenda, conforme marcador em `src/solve.py` |
| Usar recortes aninhados, semente 42 e seleção determinística de fontes | Regras aprovadas pela equipe, conforme marcadores em `src/benchmark.py` |
| Concluir Bellman-Ford em 100% com uma fonte | Redução do plano autorizada por André, conforme o log |
| Usar três painéis em B02, empilhamento em B01 e tabela de arcos em B03 | Escolhas e alterações solicitadas pelos integrantes, conforme o log e `src/viz.py` |
| Restaurar azul e laranja, sem textura, pensando em pessoas com daltonismo | Escolha expressa de Brenda nesta conversa |

## 1. Identificação a completar pelo grupo

- Turma e número do grupo: preencher.
- Repositório: https://github.com/Brendalu2005/projeto-grafos-g1
- Data de entrega da declaração: preencher.
- Nomes completos, matrículas e pacotes de todos os integrantes: preencher.
- Responsáveis conhecidos da Parte 2: Brenda e André, conforme a divisão registrada.

## 2. Ferramentas efetivamente registradas

| Ferramenta | Uso documentado | Versão / plano |
|---|---|---|
| ChatGPT / Codex | Código de integração, tratamento e conferência, benchmark, visualizações, sugestões, explicações e redação técnica | Confirmar nas conversas; não inferir versões históricas |
| Claude | Há marcadores no código, testes e configuração do projeto; cada integrante deve identificar seu uso | Confirmar pelo integrante |

## 3. Registro dos usos da Parte 2

Os registros abaixo relacionam as marcações atuais dos arquivos, os notebooks,
o avd_log.md e as conversas. Descrevem o apoio efetivamente aproveitado sob
orientação da equipe, distinguindo a produção assistida das decisões humanas.

| ID | Parte do projeto | O que foi aproveitado / como foi conferido |
|---|---|---|
| P2-01 | Notebook de tratamento | Apoio em pandas, conferências de faltantes, repetições, laços e incremento; preservação do bruto e comparação de todas as linhas tratadas |
| P2-02 | src/graphs/io.py e tests/test_dataset_io.py | Apoio ao carregador registrado no log após autorização específica relatada por André; testes marcados para direção, nomes, paralelos e preservação dos pesos. A função atual carregar_dataset não contém marcador local [IA]; o uso permanece declarado com base no histórico |
| P2-03 | src/graphs/metricas_dataset.py | Métricas e testes com exemplo pequeno; conferência das somas dos graus e exportação |
| P2-04 | Notebook de experimentos, src/solve.py e src/cli.py | Chamadas e organização dos resultados dos algoritmos existentes, exportação dos casos e integração da CLI; testes e comparação com os resultados salvos |
| P2-05 | src/benchmark.py, src/benchmark_dfs_bellman.py, tests/test_benchmark.py e tests/test_benchmark_dfs_bellman.py | Código de recortes, seleção, medição, ambiente, hash e complemento do benchmark; aquecimento excluído, estatísticas conferidas e testes de preservação. Os marcadores também registram captura do ciclo negativo no aquecimento para novas medições; isso não significa que os arquivos históricos tenham sido reexecutados |
| P2-06 | src/viz.py e documentos de visualizações | Sugestões de figuras e faixas, implementação, acessibilidade, conferência, discussão e organização das notas; incorporação conforme decisões dos integrantes. Ajustes solicitados incluem rótulos, barras 100% empilhadas de B01, tabela de arcos de B03 e azul/laranja sem textura. Participação de IA além de revisão ortográfica |
| P2-07 | Estudo da transformação | Localização do exemplo real, preparação do recorte e comparação; discussão do empate, explicação e redação aprovadas por Brenda |
| P2-08 | Consolidação e verificações finais | Inclusão dos casos no relatório, leitura do benchmark comum, hashes, ambientes, cobertura, cenários inválidos e testes em clone isolado |
| P2-09 | src/verificar_parte2.py e tests/test_verificar_parte2.py | Conferências técnicas de RESULT, outliers e DFS geradas com apoio de IA; testes de normalização e rastreabilidade. O JSON de DFS identifica explicitamente que a conferência é automática |
| P2-10 | README, log, relatório da Parte 2, documentos de visualizações e esta declaração | Atualizações, síntese, redação e compilação técnica com apoio de IA; análises e justificativas revisadas pela equipe conforme confirmação recebida |
| P2-11 | src/front/dataset.py, src/front/dataset.js e tests/test_front_dataset.py | Recorte visual da rede real, integração HTTP e desenho em Canvas; algoritmos existentes executados pelo servidor. Testes da ponte entre servidor e visualização |

Nos notebooks, as marcações registram apoio no download e no destino dos arquivos,
uso de pandas para qualidade dos dados, aplicação da regra de incremento confirmada
pelo grupo, exportação e releitura do CSV, chamadas aos algoritmos existentes,
sugestões de casos reais mínimos de Bellman-Ford, conferência de alcance,
consolidação e estudo da transformação. Os arquivos são
`data/dataset_parte2/preparacao_dataset_wikiRfA.ipynb` e
`data/dataset_parte2/experimentos_parte2.ipynb`.

### Usos da Parte 1 e de componentes compartilhados

As marcações atuais também registram os seguintes usos, que integram a declaração
conjunta do projeto:

| ID | Arquivos e trechos | Apoio de IA registrado |
|---|---|---|
| G-01 | src/graphs/algorithms.py, função dfs | Claude: apoio ao uso de grafo.get e sugestão de retorno com tempos e predecessores. ChatGPT (Codex): depuração e documentação da identidade individual de arcos paralelos. São alterações pontuais registradas, não evidência de geração integral dos quatro algoritmos |
| G-02 | tests/test_bfs.py, test_dfs.py, test_dijkstra.py e test_bellman_ford.py | Sugestões de casos e estrutura de testes; adaptação à identidade dos arcos, laços e paralelos, pesos zero e negativos. Os marcadores distinguem sugestões e valores esperados conferidos pelo grupo |
| G-03 | tests/test_estados.py e tests/test_io.py | Sugestões de casos e estrutura; ampliação da cobertura de transições, mensagens de validação e portas sem chave |
| G-04 | src/cli.py e src/solve.py, trechos da Parte 1 | Apoio em argparse, pathlib, CSV e montagem de caminhos; geração/adaptação das exportações e tabela de comparação; soma dos pesos do ciclo já retornado e correção da contagem para excluir o arco virtual até ALVO |
| G-05 | src/viz.py, trechos da Parte 1 | Ajustes de estrutura e erros, desenho do grafo de estados em camadas e compatibilização dos nomes das imagens |
| G-06 | src/front/index.html, style.css, script.js e dados.js | Claude: interface a partir da versão do grupo, galeria, Canvas e comparação dos algoritmos. ChatGPT (Codex): homepage, navegação, agrupamento das figuras segundo a classificação da equipe, filtros de camada e armadilhas e exibição de resultados já exportados |
| G-07 | src/front/server.py e tests/test_solve.py | Aquecimento e cinco medições na interface, inclusive recusas; consultas da rede, homepage e variante de regra; testes com relógio simulado e regressões de exportação e movimentos |
| G-08 | requirements.txt e pytest.ini | Claude: apoio à lista de dependências e à configuração para os testes encontrarem o pacote src |

Os comentários de autoria dos algoritmos identificam BFS com Clarissa Lopes,
DFS com André Avelino, Dijkstra com Brenda e Bellman-Ford com Vinícius. Essa
identificação difere da responsabilidade por executar os experimentos da Parte 2
e não elimina os apoios pontuais marcados nos arquivos.

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

As marcações identificam a ferramenta e a finalidade do apoio; não permitem
inferir, sozinhas, o modelo, a versão, o plano ou o integrante responsável por
cada uso. Esses campos devem acompanhar os registros reais das conversas.

## 5. Trechos de código

As funções de preparação e medição estão em src/benchmark.py; execução e
complemento em src/benchmark_dfs_bellman.py; carregamento em carregar_dataset;
métricas em src/graphs/metricas_dataset.py; integração em src/solve.py e src/cli.py;
figuras em src/viz.py; verificações em src/verificar_parte2.py. Os notebooks têm
marcadores nas células correspondentes. O grupo deve preencher a Seção 6 do
formulário com o ID do uso e o integrante que sabe explicar cada trecho.
Nenhuma assinatura ou confirmação de domínio foi presumida por esta compilação.

Para localizar os marcadores em código, testes e configuração:

```powershell
rg -n '\[IA\]' src tests requirements.txt pytest.ini
```

As marcações das células devem ser consultadas também nos dois notebooks.

## 6. Reflexão autoral do grupo — a preencher

O formulário exige 10 a 15 linhas escritas pelo grupo. Não foi gerado um relato
pessoal em nome dos integrantes. Para completar, o grupo deve relatar onde a IA
ajudou, onde sugeriu algo inadequado, como verificou os resultados e o que aprendeu.
Exemplos de ocorrências para recordar, não um texto pronto: diferença entre VOTE
e PESO; empate após somar 1 por arco; comparação entre máquinas; exigências de
quantidade de figuras e fontes; necessidade de conferir os critérios diretamente.

## 7. Fechamento obrigatório

- [ ] Completar identificação, ferramentas/planos e links ou blocos de uso.
- [ ] Anexar as conversas ou os registros individuais e as referências às autorizações recebidas.
- [ ] Inserir a reflexão pessoal do grupo no formulário.
- [ ] Preencher e assinar o formulário oficial por todos os integrantes.
- [ ] Salvar a versão final assinada em docs/DECLARACAO_IA.pdf e realizar a entrega no Classroom.

## Orientações de registro e relação com a disciplina

Cada integrante junta as próprias conversas com IA e escreve um documento com o seu uso. Depois juntamos os cinco num só, que vira a declaração em `docs/DECLARACAO_IA.pdf`. Até lá, ninguém apaga conversa.

A marca no código não fica para o fim: todo trecho feito com apoio de IA leva `# [IA] <ferramenta> – <finalidade>` no mesmo commit em que entra. É por ela que cada um vai achar os próprios trechos para a Seção 6 da declaração.

Permitido: dúvidas conceituais, entender erros e depurar código do grupo, sugerir testes e mapas extras (conferidos pelo grupo), sintaxe de pandas e das bibliotecas de visualização, revisão de ortografia.

O enunciado restringe a geração das implementações dos algoritmos e da construção
do grafo de estados, análises, discussões, conclusões, notas analíticas, prova do
m05 e soluções dos mapas, além da escolha e interpretação dos gráficos e da
história explanatória. O log registra autorizações específicas relatadas pelos
integrantes. Este inventário descreve o uso efetivo, sem presumir autorização
geral a partir de uma exceção específica.

O fato de as decisões finais terem sido humanas não altera a natureza do apoio
registrado nem substitui as orientações recebidas das professoras. Os registros
das autorizações podem acompanhar as conversas no formulário. A declaração de
conformidade deve corresponder às orientações efetivamente recebidas e aos usos
aqui discriminados.

<!-- [IA] ChatGPT (Codex) — atualização a partir das marcações atuais, notebooks e log; distinção entre sugestões/produção assistida e decisões finais da equipe conforme confirmação da usuária. -->
