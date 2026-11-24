// [IA[  ChatGPT (Codex) - leitura das saídas oficiais para a interface originalmente gerada pelo Vercel v0.
// [IA] Claude – separação da normalização dos resultados e leitura da comparação dos quatro algoritmos.
(() => {
  'use strict';
  const root = new URL('../../', document.currentScript.src);
  const output = name => new URL(`out/parte1/${name}`, root);
  const known = ['m01_terreno','m02_uma_chave','m03_tres_chaves','m04_esteiras','m05_bonus','m06_fonte','m07_impossivel','m08_grande'];
  const ALGORITHMS = ['BFS', 'DFS', 'DIJKSTRA', 'BELLMAN_FORD'];
  const decode = buffer => {
    const bytes = new Uint8Array(buffer);
    const encoding = bytes[0] === 255 && bytes[1] === 254 ? 'utf-16le' : bytes[0] === 254 && bytes[1] === 255 ? 'utf-16be' : 'utf-8';
    return new TextDecoder(encoding).decode(bytes).replace(/^\uFEFF/, '');
  };
  async function read(url) {
    const response = await fetch(url, {cache: 'no-store'});
    if (!response.ok) throw new Error(`Arquivo não disponível (${response.status}).`);
    return decode(await response.arrayBuffer());
  }
  async function optional(url) { try { return await read(url); } catch { return null; } }
  function csv(text) {
    const rows = []; let row = [], field = '', quoted = false;
    for (let i = 0; i < text.length; i++) {
      const char = text[i];
      if (char === '"') {
        if (quoted && text[i + 1] === '"') { field += '"'; i++; } else quoted = !quoted;
      } else if (char === ',' && !quoted) { row.push(field); field = ''; }
      else if ((char === '\n' || char === '\r') && !quoted) {
        if (char === '\r' && text[i + 1] === '\n') i++;
        row.push(field); if (row.some(Boolean)) rows.push(row); row = []; field = '';
      } else field += char;
    }
    if (quoted) throw new Error('CSV contém aspas não fechadas.');
    row.push(field); if (row.some(Boolean)) rows.push(row);
    const headers = rows.shift() || [];
    return rows.map(values => Object.fromEntries(headers.map((name, i) => [name.trim(), values[i] ?? ''])));
  }
  function state(label) {
    const match = /^\((\d+),\s*(\d+)\)\|(-|[a-d]+)\|\{([\d,\s]*)\}$/.exec(label.trim());
    if (!match) throw new Error(`Rótulo de estado inválido: ${label}`);
    return {estado: label.trim(), linha: Number(match[1]), coluna: Number(match[2]), chaves: match[3] === '-' ? [] : [...match[3]], bonus_consumidos: match[4].trim() ? match[4].split(',').map(Number) : []};
  }
  function dfsRow(row) {
    const kinds = ['arvore', 'retorno', 'avanco', 'cruzamento'];
    if (!row?.mapa || !kinds.every(kind => Object.hasOwn(row, kind))) return row;
    return {...row, algoritmo:'DFS', status:'CLASSIFICACAO',
      classificacao_arcos:Object.fromEntries(kinds.map(kind => [kind, row[kind]]))};
  }
  function cliRow(text) {
    const row = {};
    const fields = /'([a-z_]+)'\s*:\s*(?:'((?:\\.|[^'\\])*)'|(-?\d+(?:\.\d+)?))/g;
    for (const match of text.matchAll(fields)) row[match[1]] = match[2] !== undefined
      ? match[2].replace(/\\([\\'nrt])/g, (_, char) => ({n:'\n',r:'\r',t:'\t'}[char] ?? char)) : Number(match[3]);
    const normalized = dfsRow(row);
    if (!normalized.mapa || !normalized.algoritmo || !normalized.status) throw new Error('Selecione uma saída válida da CLI ou um CSV oficial.');
    return normalized;
  }
  function records(text, name) {
    if (name.endsWith('.csv')) return csv(text).map(dfsRow);
    if (name.endsWith('.json')) { const data = JSON.parse(text); return (Array.isArray(data) ? data : [data]).map(dfsRow); }
    return [cliRow(text)];
  }
  const imported = new Map();
  const edgeCache = new Map();
  const compareCache = new Map();
  const visualCache = new Map();
  const dirOf = fonteConsumivel => fonteConsumivel ? 'fonte_consumivel/' : '';

  // [IA] ChatGPT (Codex) – prepara a visualização a partir dos CSVs já exportados, sem recalcular grafos.
  async function visualizacao(name, fonteConsumivel = false) {
    const chave = `${name}/${fonteConsumivel}`;
    if (!visualCache.has(chave)) {
      const dir = dirOf(fonteConsumivel);
      const [textoArestas, textoArmadilhas] = await Promise.all([
        optional(output(`${dir}arestas_${name}.csv`)), optional(output(`${dir}armadilhas_${name}.csv`)),
      ]);
      const rotulos = new Set();
      for (const arco of textoArestas ? csv(textoArestas) : []) {
        if (arco.origem !== 'ALVO') rotulos.add(arco.origem);
        if (arco.destino !== 'ALVO') rotulos.add(arco.destino);
      }
      const estados = [...rotulos].map(state);
      visualCache.set(chave, {mapa:name, fonte:fonteConsumivel, estados,
        camadas:[...new Set(estados.map(estado => estado.chaves.join('') || '-'))].sort(),
        armadilhas:new Set((textoArmadilhas ? csv(textoArmadilhas) : []).map(linha => linha.estado)),
        disponivel:textoArestas !== null && textoArmadilhas !== null});
    }
    return visualCache.get(chave);
  }

  async function analyses(name, fonteConsumivel = false) {
    const dir = dirOf(fonteConsumivel);
    const [layersText, dfsText] = await Promise.all([
      optional(output(`${dir}camadas.json`)), optional(output(`${dir}dfs_classificacao.csv`))
    ]);
    const layers = layersText ? JSON.parse(layersText) : {};
    const dfs = dfsText ? csv(dfsText) : [];
    const row = dfs.find(item => item.mapa === name);
    const kinds = ['arvore', 'retorno', 'avanco', 'cruzamento'];
    return {
      camadas: layers[name] || null,
      classificacao_arcos: row ? Object.fromEntries(kinds.map(kind => [kind, Number(row[kind])])) : null
    };
  }
  async function list() {
    let names = known;
    try {
      const metrics = JSON.parse(await read(output('metricas_global.json')));
      names = [...new Set([...known, ...metrics.map(row => row.mapa)])];
    } catch { /* os oito mapas fornecidos continuam disponíveis */ }
    return names.filter(name => /^[\w-]+$/.test(name));
  }
  async function map(name) {
    let grupo = false;
    let text = await optional(new URL(`data/mapas/${name}.txt`, root));
    if (text === null) { text = await optional(new URL(`data/mapas_grupo/${name}.txt`, root)); grupo = true; }
    if (text === null) throw new Error(`Mapa ${name} não encontrado em data/mapas/ ou data/mapas_grupo/.`);
    const grade = text.replace(/\r/g, '').split('\n').filter(row => row && !row.startsWith(';'));
    if (!grade.length || !grade.every(row => row.length === grade[0].length)) throw new Error('Grade vazia ou não retangular.');
    return {mapa: name, grade, colunas: grade[0].length, linhas: grade.length, grupo};
  }
  async function edges(name, fonteConsumivel = false) {
    const cacheKey = `${name}/${fonteConsumivel}`;
    if (!edgeCache.has(cacheKey)) {
      const text = await optional(output(`${dirOf(fonteConsumivel)}arestas_${name}.csv`));
      edgeCache.set(cacheKey, new Map(text ? csv(text).map(row => [`${row.origem}\n${row.destino}`, Number(row.peso)]) : []));
    }
    return edgeCache.get(cacheKey);
  }
  async function rawResult(name, algorithm, fonteConsumivel) {
    const dir = dirOf(fonteConsumivel);
    let row = imported.get(`${name}/${algorithm}`);
    if (!row) {
      try {
        const url = new URL('api/resultado', root);
        url.searchParams.set('mapa', name); url.searchParams.set('alg', algorithm);
        url.searchParams.set('fonte-consumivel', String(fonteConsumivel));
        const response = await fetch(url);
        if (response.ok) row = await response.json();
      } catch { /* servidor comum: usar os arquivos exportados abaixo */ }
    }
    if (!row) {
      const text = await optional(output(`${dir}solucao_${name}_${algorithm}.txt`));
      if (text !== null) row = cliRow(text);
    }
    if (!row) {
      const text = await optional(output(`${dir}solucoes.csv`));
      if (text !== null) row = csv(text).find(row => row.mapa === name && row.algoritmo === algorithm);
    }
    if (algorithm === 'DFS' && (!row || row.status === 'PENDENTE')) {
      const text = await optional(output(`${dir}dfs_classificacao.csv`));
      const found = text && csv(text).find(item => item.mapa === name);
      if (found) row = dfsRow(found);
    }
    return row || null;
  }
  async function normalize(row, name, algorithm, grade, fonteConsumivel) {
    const dir = dirOf(fonteConsumivel);
    if (algorithm === 'BELLMAN_FORD' && row?.status === 'CICLO_NEGATIVO' && !(Array.isArray(row.ciclo) && row.ciclo.length) && name === 'm06_fonte') {
      const cycleText = await optional(output(`${dir}ciclo_negativo_m06.json`));
      if (cycleText) row = {...row, ciclo: JSON.parse(cycleText).ciclo};
    }
    if (row.mapa !== name || row.algoritmo !== algorithm) throw new Error('A saída selecionada pertence a outro mapa ou algoritmo.');
    const statuses = {OK:'sucesso', RECUSA:'peso_negativo_recusado', SEM_SOLUCAO:'sem_caminho', CICLO_NEGATIVO:'ciclo_negativo', EXPLORACAO:'exploracao', CLASSIFICACAO:'classificacao', PENDENTE:'pendente'};
    if (!statuses[row.status]) throw new Error(`Status desconhecido: ${row.status}`);
    if (row.status === 'CLASSIFICACAO' || row.status === 'EXPLORACAO') {
      const kinds = ['arvore', 'retorno', 'avanco', 'cruzamento'];
      const source = row.classificacao_arcos;
      if (algorithm !== 'DFS' || !source || kinds.some(kind => !Number.isSafeInteger(Number(source[kind])) || Number(source[kind]) < 0)) {
        throw new Error('Classificação DFS inválida.');
      }
      const counts = Object.fromEntries(kinds.map(kind => [kind, Number(source[kind])]));
      const total = Object.values(counts).reduce((sum, value) => sum + value, 0);
      const visits = row.status === 'EXPLORACAO' && Array.isArray(row.exploracao) ? row.exploracao.map(state) : [];
      if (row.status === 'EXPLORACAO' && !visits.length) throw new Error('DFS sem estados de exploração.');
      for (const visit of visits) {
        if (!grade[visit.linha] || grade[visit.linha][visit.coluna] === undefined || grade[visit.linha][visit.coluna] === '#') {
          throw new Error('Exploração DFS contém posição inválida no mapa.');
        }
      }
      const animated = row.status === 'EXPLORACAO';
      return {status:animated ? 'exploracao' : 'classificacao',
        mensagem:animated ? `A DFS descobriu ${visits.length} estados e classificou ${total} arcos. A animação mostra a ordem de descoberta, não uma rota até a saída.`
          : `A DFS classificou ${total} arcos. Rode o servidor do front para animar a exploração.`,
        passos:visits, ciclo_negativo:[], classificacao_arcos:counts, movimentos:null, custo_total:null, aviso:''};
    }
    const messages = {OK: algorithm === 'BFS' ? 'Caminho com o menor número de movimentos.' : 'Caminho de menor custo.', RECUSA:'O Dijkstra recusou o grafo porque ele tem pesos negativos.', SEM_SOLUCAO:'Não existe caminho até a saída.', CICLO_NEGATIVO:'Ciclo negativo encontrado. A animação percorre os estados do ciclo.', PENDENTE:'Reinicie o servidor do front para carregar a classificação DFS atual.'};
    const steps = row.status === 'OK' ? String(row.caminho).split(/\s*->\s*/).filter(label => label && label !== 'ALVO').map(state) : [];
    const cycle = row.status === 'CICLO_NEGATIVO' && Array.isArray(row.ciclo) ? row.ciclo.filter(label => label !== 'ALVO').map(state) : [];
    if (row.status === 'OK' && !steps.length) throw new Error('Resultado OK sem caminho exportado.');
    const weights = await edges(name, fonteConsumivel);
    let cost = 0, complete = true;
    function addCosts(sequence) { sequence.forEach((step, i) => {
      if (!grade[step.linha] || grade[step.linha][step.coluna] === undefined || grade[step.linha][step.coluna] === '#') throw new Error('O percurso contém posição inválida no mapa.');
      const weight = i ? weights.get(`${sequence[i-1].estado}\n${step.estado}`) : 0;
      if (weight === undefined) complete = false;
      if (complete) cost += weight;
      step.custo_acumulado = complete ? cost : null;
    }); }
    addCosts(steps);
    const total = row.custo === '' || row.custo === undefined ? null : Number(row.custo);
    if (complete && steps.length && total !== null && cost !== total) {
      complete = false;
      steps.forEach((step, i) => { step.custo_acumulado = i ? null : 0; });
    }
    if (cycle.length) { cost = 0; complete = true; addCosts(cycle); }
    // [IA] ChatGPT (Codex) – exibe o custo calculado dos arcos do ciclo já exportado.
    const custoCiclo = cycle.length && complete ? cost : row.custo_ciclo ?? null;
    return {status: statuses[row.status], mensagem: messages[row.status], passos:steps,
      ciclo_negativo:cycle, custo_ciclo:custoCiclo, classificacao_arcos:row.classificacao_arcos || null,
      movimentos:steps.length ? steps.length-1 : null, custo_total:total,
      aviso: !complete ? 'Os CSVs de arestas estão ausentes ou não batem com o custo desta execução. O custo por passo fica indisponível; o custo total vem da saída oficial.' : ''};
  }
  async function result(name, algorithm, grade, fonteConsumivel = false) {
    const row = await rawResult(name, algorithm, fonteConsumivel);
    if (!row) return null;
    // [IA] ChatGPT (Codex) – identifica o arquivo realmente usado na exibição.
    return {...await normalize(row, name, algorithm, grade, fonteConsumivel),
      arquivo_importado: row.arquivo_importado || null};
  }
  async function compare(name, grade, fonteConsumivel = false) {
    const key = `${name}/${fonteConsumivel}`;
    if (compareCache.has(key)) return compareCache.get(key);
    let rows = null;
    try {
      const url = new URL('api/comparar', root);
      url.searchParams.set('mapa', name);
      url.searchParams.set('fonte-consumivel', String(fonteConsumivel));
      const response = await fetch(url);
      if (response.ok) rows = (await response.json()).algoritmos;
    } catch { /* sem servidor: os tempos ficam indisponíveis */ }
    const measured = Array.isArray(rows);
    const entries = await Promise.all(ALGORITHMS.map(async algorithm => {
      const row = measured ? rows.find(item => item.algoritmo === algorithm) : await rawResult(name, algorithm, fonteConsumivel);
      if (!row) return {algoritmo: algorithm, resultado: null, tempo_ms: null, execucoes: 0, estados_alcancados: null};
      return {algoritmo: algorithm, resultado: await normalize(row, name, algorithm, grade, fonteConsumivel),
        tempo_ms: measured ? Number(row.tempo_ms) : null, execucoes: measured ? Number(row.execucoes) : 0,
        estados_alcancados: measured ? Number(row.estados_alcancados) : null};
    }));
    const value = {medido: measured, algoritmos: entries};
    if (measured) compareCache.set(key, value);
    return value;
  }
  async function online() {
    try {
      const url = new URL('api/resultado', root);
      const response = await fetch(url);
      return response.headers.get('content-type')?.includes('application/json') ?? false;
    } catch { return false; }
  }
  async function importFile(file) {
    const rows = records(decode(await file.arrayBuffer()), file.name.toLowerCase());
    if (!rows.length) throw new Error('O arquivo não contém resultados.');
    for (const row of rows) if (!/^[\w-]+$/.test(row.mapa || '') || !ALGORITHMS.includes(row.algoritmo) || !['OK','RECUSA','SEM_SOLUCAO','CICLO_NEGATIVO','CLASSIFICACAO','EXPLORACAO'].includes(row.status)) throw new Error('Use um CSV oficial ou a saída da CLI correspondente ao mapa e algoritmo.');
    for (const row of rows) imported.set(`${row.mapa}/${row.algoritmo}`, {...row, arquivo_importado: file.name});
    return rows;
  }
  window.FrontData = {list, map, result, compare, analyses, visualizacao, importFile, output, online};
})();
