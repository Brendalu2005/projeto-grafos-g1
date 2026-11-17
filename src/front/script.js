// [IA[  Vercel v0 - geração original da interface interativa.
// [IA[  ChatGPT (Codex) - adaptação do script aos dados de src.solve.
(() => {
  'use strict';
  const $ = selector => document.querySelector(selector);
  const mapSelect = $('#map-select');
  const algorithmSelect = $('#algorithm-select');
  const names = { BFS: 'BFS', DFS: 'DFS', DIJKSTRA: 'Dijkstra', BELLMAN_FORD: 'Bellman-Ford' };
  let maps = [], steps = [], index = 0, timer = null, cycle = false, request = 0;
  const algorithm = () => algorithmSelect.value.toUpperCase().replaceAll('-', '_');
  const selected = () => maps.find(map => map.mapa === mapSelect.value);
  const escape = value => String(value).replace(/[&<>"']/g, char => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[char]);
  function status(title, detail, type = '') {
    const box = $('#status-message');
    box.className = `status-message ${type}`;
    box.innerHTML = `<span class="status-icon" aria-hidden="true">${type ? '△' : '⌁'}</span><span><strong>${escape(title)}</strong><small>${escape(detail)}</small></span>`;
  }
  function stop() {
    clearInterval(timer); timer = null;
    $('#play-icon').textContent = '▶';
    $('#play-button').setAttribute('aria-label', 'Iniciar animação');
  }
  function controls() {
    for (const id of ['restart-button', 'back-button', 'play-button', 'next-button', 'timeline']) $(`#${id}`).disabled = steps.length < 2;
  }
  function render() {
    const map = selected(); if (!map?.grade) return;
    const container = $('#maze-container');
    const containerStyle = getComputedStyle(container);
    const availableWidth = container.clientWidth - parseFloat(containerStyle.paddingLeft) - parseFloat(containerStyle.paddingRight);
    const minimumSize = window.innerWidth <= 620 ? 22 : 25;
    const cellSize = Math.max(minimumSize, Math.min(48, Math.floor((availableWidth - 3 * (map.colunas - 1)) / map.colunas)));
    const step = steps[index];
    const visited = new Map();
    for (const item of steps.slice(0, index + 1)) visited.set(`${item.linha},${item.coluna}`, item);
    const cells = map.grade.map((row, r) => [...row].map((symbol, c) => {
      const type = symbol === '#' ? 'wall' : symbol === 'S' ? 'start' : symbol === 'G' ? 'goal'
        : /^[a-d]$/.test(symbol) ? 'key' : /^[A-D]$/.test(symbol) ? 'door'
        : symbol === '+' ? 'bonus' : symbol === '*' ? 'fountain'
        : symbol === ',' ? 'mud' : symbol === '~' ? 'water' : /[><^v]/.test(symbol) ? 'conveyor' : '';
      const visit = visited.get(`${r},${c}`);
      const current = step?.linha === r && step?.coluna === c;
      const color = visit ? `hsl(${visit.chaves.reduce((mask, key) => mask | (1 << (key.charCodeAt(0) - 97)), 0) * 137.5 % 360} 58% 66%)` : null;
      const label = symbol === '#' || symbol === '.' ? '' : symbol;
      return `<div class="maze-cell ${type} ${visit ? 'visited' : ''} ${current ? 'current' : ''}" ${color ? `style="box-shadow:inset 0 0 0 2px ${color}"` : ''} title="Linha ${r}, coluna ${c} · ${escape(symbol)}">${escape(label)}</div>`;
    }).join('')).join('');
    container.innerHTML = `<div class="maze-grid" role="img" aria-label="Mapa ${escape(map.mapa)}" style="--cell-size:${cellSize}px;grid-template-columns:repeat(${map.colunas}, var(--cell-size))">${cells}</div>`;
    $('#position-value').textContent = step ? `${step.linha} / ${step.coluna}` : '— / —';
    $('#keys-value').textContent = step ? step.chaves.join(', ') || 'Nenhuma' : '—';
    $('#bonus-value').textContent = step ? step.bonus_consumidos.length : '—';
    $('#bonus-value').title = step ? `IDs consumidos: ${step.bonus_consumidos.join(', ') || 'nenhum'}` : '';
    $('#cost-value').textContent = step?.custo_acumulado ?? '—';
    $('#moves-value').textContent = step ? index : '—';
    $('#step-value').textContent = steps.length ? index : 0;
    $('#step-total').textContent = Math.max(steps.length - 1, 0);
    $('#timeline').max = Math.max(steps.length - 1, 0);
    $('#timeline').value = index;
    $('#timeline-percent').textContent = `${steps.length > 1 ? Math.round(index / (steps.length - 1) * 100) : 0}%`;
    $('#run-state').textContent = !steps.length ? 'SEM PERCURSO' : cycle ? 'CICLO NEGATIVO' : index === steps.length - 1 ? 'FINALIZADO' : 'EM EXPLORAÇÃO';
    controls();
  }
  function extras(map) {
    $('#graph-view').textContent = 'Grafo em camadas ainda não exportado.';
    const counts = map.classificacao_arcos;
    $('.arc-legend p').textContent = counts
      ? Object.entries(counts).map(([kind, total]) => `${kind}: ${total}`).join(' · ')
      : 'Selecione DFS para ver a classificação dos arcos.';
    function figure(id, filename, description) {
      const container = $(id);
      container.replaceChildren();
      if (!filename) { container.textContent = 'Figura ainda não exportada para este mapa.'; return; }
      const image = document.createElement('img');
      image.alt = description; image.src = FrontData.output(filename).href;
      image.addEventListener('error', () => { container.textContent = 'Figura ainda não disponível.'; });
      container.append(image);
    }
    figure('#tree-view', map.mapa === 'm02_uma_chave' ? 'arvore_bfs_m02.png' : null, 'Árvore BFS do m02');
    figure('#heatmap-view', map.mapa === 'm08_grande' ? 'heatmap_multiplicidade_m08.png' : null, 'Estados por casa do m08');
  }
  async function load() {
    const currentRequest = ++request;
    stop(); index = 0; steps = []; cycle = false; controls();
    const name = mapSelect.value;
    if (!name) return;
    $('#map-label').textContent = name;
    $('#run-state').textContent = 'CARREGANDO';
    $('#algorithm-note').textContent = 'Carregando o resultado selecionado.';
    ['position-value','keys-value','bonus-value','cost-value','moves-value'].forEach(id => $(`#${id}`).textContent = '—');
    $('#maze-container').textContent = 'Carregando mapa…';
    status('Carregando', 'Consultando o mapa e os resultados exportados.');
    try {
      const map = await FrontData.map(name);
      if (currentRequest !== request) return;
      maps[maps.findIndex(item => item.mapa === name)] = map;
      extras(map); render();
      const result = await FrontData.result(name, algorithm(), map.grade);
      if (currentRequest !== request) return;
      if (!result) {
        $('#algorithm-note').textContent = 'O servidor de resultados não está disponível.';
        status('Conexão com os algoritmos indisponível', 'Inicie o projeto com python -m src.front.server e recarregue esta página.', 'warning');
      } else {
        $('#algorithm-note').textContent = result.mensagem;
        cycle = result.status === 'ciclo_negativo';
        steps = cycle ? result.ciclo_negativo : result.passos;
        map.classificacao_arcos = result.classificacao_arcos;
        extras(map);
        if (result.status === 'sucesso') status('Resultado carregado', `${names[algorithm()]} · ${result.movimentos} movimentos · custo total ${result.custo_total ?? 'indisponível'}. ${result.aviso || result.mensagem}`, result.aviso ? 'warning' : '');
        else status(cycle ? 'Ciclo negativo detectado' : result.status === 'sem_caminho' ? 'Sem solução' : result.status === 'pendente' ? 'DFS ainda pendente' : 'Execução recusada', result.mensagem, 'warning');
      }
      render();
    } catch (error) {
      if (currentRequest !== request) return;
      status('Não foi possível carregar', `${error.message} Inicie o projeto com python -m src.front.server.`, 'error');
      $('#run-state').textContent = 'INDISPONÍVEL';
      controls();
    }
  }
  function move(value) { stop(); index = Math.max(0, Math.min(value, steps.length - 1)); render(); }
  function play() {
    if (timer) { stop(); return; }
    if (steps.length < 2) return;
    if (index === steps.length - 1) index = 0;
    render();
    $('#play-icon').textContent = 'Ⅱ';
    $('#play-button').setAttribute('aria-label', 'Pausar animação');
    timer = setInterval(() => {
      index = Math.min(index + 1, steps.length - 1); render();
      if (index === steps.length - 1) stop();
    }, Number($('#speed-range').value));
  }
  $('#load-button').addEventListener('click', load);
  mapSelect.addEventListener('change', load);
  algorithmSelect.addEventListener('change', load);
  let resizeFrame;
  window.addEventListener('resize', () => {
    cancelAnimationFrame(resizeFrame);
    resizeFrame = requestAnimationFrame(() => { if (selected()?.grade) render(); });
  });
  $('#play-button').addEventListener('click', play);
  $('#restart-button').addEventListener('click', () => move(0));
  $('#back-button').addEventListener('click', () => move(index - 1));
  $('#next-button').addEventListener('click', () => move(index + 1));
  $('#timeline').addEventListener('input', event => move(Number(event.target.value)));
  $('#speed-range').addEventListener('input', event => {
    const speed = Number(event.target.value);
    $('#speed-value').textContent = speed < 350 ? 'Rápida' : speed > 800 ? 'Lenta' : 'Normal';
    if (timer) { stop(); play(); }
  });
  $('#data-file').accept = '.csv,.txt,.json,text/csv,text/plain,application/json';
  $('#data-file').addEventListener('change', async event => {
    const file = event.target.files?.[0]; if (!file) return;
    stop(); ++request;
    try {
      const rows = await FrontData.importFile(file);
      for (const row of rows) if (!maps.some(map => map.mapa === row.mapa)) {
        maps.push({mapa:row.mapa});
        mapSelect.append(new Option(row.mapa, row.mapa));
      }
      if (rows.length) {
        mapSelect.value = rows[0].mapa;
        algorithmSelect.value = rows[0].algoritmo.toLowerCase().replaceAll('_','-');
      }
      await load();
    } catch (error) { status('Arquivo inválido', error.message, 'error'); }
    finally { event.target.value = ''; }
  });
  controls();
  FrontData.list().then(names => {
    maps = names.map(mapa => ({mapa}));
    mapSelect.replaceChildren(...names.map(name => new Option(name,name)));
    return load();
  }).catch(error => status('Falha ao carregar dados', error.message, 'error'));
})();
