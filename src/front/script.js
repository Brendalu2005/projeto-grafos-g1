// [IA[  Vercel v0 - geração original da interface interativa.
// [IA[  ChatGPT (Codex) - adaptação do script aos dados de src.solve.
(() => {
  'use strict';
  const $ = selector => document.querySelector(selector);
  const mapSelect = $('#map-select');
  const algorithmSelect = $('#algorithm-select');
  const names = { BFS: 'BFS', DFS: 'DFS', DIJKSTRA: 'Dijkstra', BELLMAN_FORD: 'Bellman-Ford' };
  let maps = [], steps = [], index = 0, timer = null, cycle = false, analysis = false, exploring = false, request = 0;
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
    $('#moves-value').previousElementSibling.textContent = exploring ? 'ESTADOS VISITADOS' : 'MOVIMENTOS';
    $('#moves-value').textContent = step ? exploring ? index + 1 : index : '—';
    $('#step-value').textContent = steps.length ? index : 0;
    $('#step-total').textContent = Math.max(steps.length - 1, 0);
    $('#timeline').max = Math.max(steps.length - 1, 0);
    $('#timeline').value = index;
    $('#timeline-percent').textContent = `${steps.length > 1 ? Math.round(index / (steps.length - 1) * 100) : 0}%`;
    // [IA[  ChatGPT (Codex) - distingue visualmente a busca DFS de um percurso até o alvo.
    $('.timeline-labels').lastElementChild.textContent = exploring ? 'FIM DA BUSCA' : 'ALVO';
    $('.legend-cell.path').parentElement.lastChild.textContent = exploring ? ' Visitados' : ' Percurso';
    controls();
  }
  // [IA[  ChatGPT (Codex) - exibe as camadas oficiais do mapa selecionado na seção de análises.
  function layersView(map, data) {
    const container = $('#graph-view');
    const layers = data?.camadas?.camadas;
    $('#graph-tag').textContent = map.mapa;
    container.replaceChildren();
    if (!data) { container.textContent = 'Carregando camadas do mapa…'; return; }
    if (!Array.isArray(layers) || !layers.length) {
      container.textContent = 'Camadas ainda não exportadas para este mapa.';
      return;
    }
    const summary = document.createElement('p');
    summary.className = 'layer-summary';
    const total = layers.reduce((sum, layer) => sum + Number(layer.ordem || 0), 0);
    summary.textContent = `${layers.length} ${layers.length === 1 ? 'camada' : 'camadas'} · ${total} estados · ${data.camadas.arcos_entre_camadas} arcos entre camadas`;
    container.append(summary);
    const list = document.createElement('div');
    list.className = 'layer-list';
    const max = Math.max(...layers.map(layer => Number(layer.ordem || 0)), 1);
    for (const layer of layers) {
      const row = document.createElement('div');
      row.className = 'layer-row';
      const label = document.createElement('span');
      label.className = 'layer-name';
      label.textContent = layer.chaves === '-' ? 'Sem chaves' : `Chaves ${layer.chaves}`;
      const bar = document.createElement('span');
      bar.className = 'layer-track';
      const fill = document.createElement('span');
      fill.className = 'layer-fill';
      fill.style.width = `${Math.max(0, Math.min(100, Number(layer.ordem || 0) / max * 100))}%`;
      bar.append(fill);
      const size = document.createElement('span');
      size.className = 'layer-size';
      size.textContent = `${layer.ordem} estados`;
      row.append(label, bar, size);
      list.append(row);
    }
    container.append(list);
  }
  function extras(map, data) {
    layersView(map, data);
    const counts = map.classificacao_arcos || data?.classificacao_arcos;
    $('.arc-legend p').textContent = counts
      ? Object.entries(counts).map(([kind, total]) => `${kind}: ${total}`).join(' · ')
      : data ? 'Classificação DFS ainda não exportada para este mapa.' : 'Carregando classificação dos arcos…';
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
    stop(); index = 0; steps = []; cycle = false; analysis = false; exploring = false; controls();
    const name = mapSelect.value;
    if (!name) return;
    $('#map-label').textContent = name;
    $('#algorithm-note').textContent = 'Carregando o resultado selecionado.';
    ['position-value','keys-value','bonus-value','cost-value','moves-value'].forEach(id => $(`#${id}`).textContent = '—');
    $('#maze-container').textContent = 'Carregando mapa…';
    status('Carregando', 'Consultando o mapa e os resultados exportados.');
    try {
      const map = await FrontData.map(name);
      if (currentRequest !== request) return;
      maps[maps.findIndex(item => item.mapa === name)] = map;
      extras(map); render();
      const [result, analysisData] = await Promise.all([
        FrontData.result(name, algorithm(), map.grade), FrontData.analyses(name)
      ]);
      if (currentRequest !== request) return;
      map.classificacao_arcos = result?.classificacao_arcos || analysisData.classificacao_arcos;
      extras(map, analysisData);
      if (!result) {
        $('#algorithm-note').textContent = 'O servidor de resultados não está disponível.';
        status('Conexão com os algoritmos indisponível', 'Inicie o projeto com python -m src.front.server e recarregue esta página.', 'warning');
      } else {
        $('#algorithm-note').textContent = result.mensagem;
        cycle = result.status === 'ciclo_negativo';
        analysis = result.status === 'classificacao';
        exploring = result.status === 'exploracao';
        steps = cycle ? result.ciclo_negativo : result.passos;
        if (result.status === 'sucesso') status('Resultado carregado', `${names[algorithm()]} · ${result.movimentos} movimentos · custo total ${result.custo_total ?? 'indisponível'}. ${result.aviso || result.mensagem}`, result.aviso ? 'warning' : '');
        else if (exploring) status('Exploração DFS pronta', result.mensagem);
        // [IA[  ChatGPT (Codex) - apresenta a classificação DFS oficial sem sugerir um percurso inexistente.
        else if (analysis) status('Classificação DFS carregada', result.mensagem);
        else status(cycle ? 'Ciclo negativo detectado' : result.status === 'sem_caminho' ? 'Sem solução' : result.status === 'pendente' ? 'DFS ainda pendente' : 'Execução recusada', result.mensagem, 'warning');
      }
      render();
    } catch (error) {
      if (currentRequest !== request) return;
      status('Não foi possível carregar', `${error.message} Inicie o projeto com python -m src.front.server.`, 'error');
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
  // [IA[  ChatGPT (Codex) - mostra ou oculta as análises sem repetir o carregamento automático do mapa.
  const analysesButton = $('#load-button');
  analysesButton.addEventListener('click', () => {
    const section = $('#analises');
    const show = section.hidden;
    section.hidden = !show;
    analysesButton.setAttribute('aria-expanded', String(show));
    analysesButton.querySelector('.origin-label').textContent = show ? 'Ocultar análises' : 'Ver análises';
    if (!show) return;
    const behavior = window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth';
    section.scrollIntoView({behavior, block: 'start'});
    section.focus({preventScroll: true});
  });
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
