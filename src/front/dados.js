// [IA[  ChatGPT (Codex) - leitura das saídas oficiais para a interface originalmente gerada pelo Vercel v0.
(() => {
  'use strict';
  const root = new URL('../../', document.currentScript.src);
  const output = name => new URL(`out/parte1/${name}`, root);
  const known = ['m01_terreno','m02_uma_chave','m03_tres_chaves','m04_esteiras','m05_bonus','m06_fonte','m07_impossivel','m08_grande'];
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
  // O CLI atual imprime repr(dict). Leitura limitada a campos escalares, sem eval.
  function cliRow(text) {
    const row = {};
    const fields = /'([a-z_]+)'\s*:\s*(?:'((?:\\.|[^'\\])*)'|(-?\d+(?:\.\d+)?))/g;
    for (const match of text.matchAll(fields)) row[match[1]] = match[2] !== undefined
      ? match[2].replace(/\\([\\'nrt])/g, (_, char) => ({n:'\n',r:'\r',t:'\t'}[char] ?? char)) : Number(match[3]);
    if (!row.mapa || !row.algoritmo || !row.status) throw new Error('Selecione uma saída válida da CLI ou solucoes.csv.');
    return row;
  }
  function records(text, name) {
    if (name.endsWith('.csv')) return csv(text);
    if (name.endsWith('.json')) { const data = JSON.parse(text); return Array.isArray(data) ? data : [data]; }
    return [cliRow(text)];
  }
  const imported = new Map();
  const edgeCache = new Map();
  async function list() {
    let names = known;
    try {
      const metrics = JSON.parse(await read(output('metricas_global.json')));
      names = [...new Set([...known, ...metrics.map(row => row.mapa)])];
    } catch { /* os oito mapas fornecidos continuam disponíveis */ }
    return names.filter(name => /^[\w-]+$/.test(name));
  }
  async function map(name) {
    let text = await optional(new URL(`data/mapas/${name}.txt`, root));
    if (text === null) text = await optional(new URL(`data/mapas_grupo/${name}.txt`, root));
    if (text === null) throw new Error(`Mapa ${name} não encontrado em data/mapas/ ou data/mapas_grupo/.`);
    const grade = text.replace(/\r/g, '').split('\n').filter(row => row && !row.startsWith(';'));
    if (!grade.length || !grade.every(row => row.length === grade[0].length)) throw new Error('Grade vazia ou não retangular.');
    return {mapa: name, grade, colunas: grade[0].length};
  }
  async function edges(name) {
    if (!edgeCache.has(name)) {
      const text = await optional(output(`arestas_${name}.csv`));
      edgeCache.set(name, new Map(text ? csv(text).map(row => [`${row.origem}\n${row.destino}`, Number(row.peso)]) : []));
    }
    return edgeCache.get(name);
  }
  async function result(name, algorithm, grade) {
    let row = imported.get(`${name}/${algorithm}`);
    if (!row) {
      try {
        const response = await fetch(new URL(`api/resultado?mapa=${encodeURIComponent(name)}&alg=${encodeURIComponent(algorithm)}`, root));
        if (response.ok) row = await response.json();
      } catch { /* servidor comum: usar os arquivos exportados abaixo */ }
    }
    if (!row) {
      const text = await optional(output(`solucao_${name}_${algorithm}.txt`));
      if (text !== null) row = cliRow(text);
    }
    if (!row) {
      const text = await optional(output('solucoes.csv'));
      if (text !== null) row = csv(text).find(row => row.mapa === name && row.algoritmo === algorithm);
    }
    if (!row) return null;
    if (row.mapa !== name || row.algoritmo !== algorithm) throw new Error('A saída selecionada pertence a outro mapa ou algoritmo.');
    const statuses = {OK:'sucesso', RECUSA:'peso_negativo_recusado', SEM_SOLUCAO:'sem_caminho', CICLO_NEGATIVO:'ciclo_negativo', PENDENTE:'pendente'};
    if (!statuses[row.status]) throw new Error(`Status desconhecido: ${row.status}`);
    const messages = {OK: algorithm === 'BFS' ? 'Menor número de movimentos.' : 'Percurso de menor custo.', RECUSA:'Dijkstra recusou o grafo com pesos negativos.', SEM_SOLUCAO:'Não há caminho até a saída.', CICLO_NEGATIVO:'O código oficial detectou um ciclo negativo, mas ainda não exporta os estados do ciclo.', PENDENTE:'A função oficial da DFS ainda não exporta um resultado para o front.'};
    const steps = row.status === 'OK' ? String(row.caminho).split(/\s*->\s*/).filter(label => label && label !== 'ALVO').map(state) : [];
    const cycle = row.status === 'CICLO_NEGATIVO' && Array.isArray(row.ciclo) ? row.ciclo.map(state) : [];
    if (row.status === 'OK' && !steps.length) throw new Error('Resultado OK sem caminho exportado.');
    const weights = await edges(name);
    let cost = 0, complete = true;
    function addCosts(sequence) { sequence.forEach((step, i) => {
      if (!grade[step.linha] || grade[step.linha][step.coluna] === undefined || grade[step.linha][step.coluna] === '#') throw new Error('O percurso contém posição inválida no mapa.');
      const weight = i ? weights.get(`${sequence[i-1].estado}\n${step.estado}`) : 0;
      if (weight === undefined) complete = false;
      if (complete) cost += weight;
      step.custo_acumulado = complete ? cost : null;
    }); }
    addCosts(steps);
    const total = row.custo === '' ? null : Number(row.custo);
    if (complete && steps.length && total !== null && cost !== total) {
      complete = false;
      steps.forEach((step, i) => { step.custo_acumulado = i ? null : 0; });
    }
    if (cycle.length) { cost = 0; complete = true; addCosts(cycle); }
    return {status: statuses[row.status], mensagem: messages[row.status], passos:steps,
      ciclo_negativo:cycle, classificacao_arcos:row.classificacao_arcos || null,
      movimentos:steps.length ? steps.length-1 : null, custo_total:total,
      aviso: !complete ? 'Os CSVs de arestas estão ausentes ou não correspondem ao custo desta execução. O custo por passo fica indisponível; o custo total vem da saída oficial.' : ''};
  }
  async function importFile(file) {
    const rows = records(decode(await file.arrayBuffer()), file.name.toLowerCase());
    for (const row of rows) if (!/^[\w-]+$/.test(row.mapa || '') || !['BFS','DFS','DIJKSTRA','BELLMAN_FORD'].includes(row.algoritmo) || !['OK','RECUSA','SEM_SOLUCAO','CICLO_NEGATIVO'].includes(row.status)) throw new Error('Use solucoes.csv ou a saída da CLI com mapa, algoritmo, status e caminho.');
    for (const row of rows) imported.set(`${row.mapa}/${row.algoritmo}`, row);
    return rows;
  }
  window.FrontData = {list, map, result, importFile, output};
})();
