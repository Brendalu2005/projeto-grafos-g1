// [IA] Claude – nova interface: galeria de mapas, desenho em canvas, modo de um algoritmo e corrida dos quatro.
(() => {
  'use strict';
  const $ = selector => document.querySelector(selector);
  const ALGS = [
    {id: 'BFS', nome: 'BFS', desc: 'Menos movimentos', cor: '--alg-bfs'},
    {id: 'DFS', nome: 'DFS', desc: 'Explora em profundidade', cor: '--alg-dfs'},
    {id: 'DIJKSTRA', nome: 'Dijkstra', desc: 'Menor custo, sem peso negativo', cor: '--alg-dijkstra'},
    {id: 'BELLMAN_FORD', nome: 'Bellman-Ford', desc: 'Menor custo, aceita peso negativo', cor: '--alg-bf'},
  ];
  const NOMES = {
    m01_terreno: 'Terreno', m02_uma_chave: 'Uma chave', m03_tres_chaves: 'Três chaves', m04_esteiras: 'Esteiras',
    m05_bonus: 'Bônus', m06_fonte: 'Fonte', m07_impossivel: 'Impossível', m08_grande: 'Grande',
    grupo_rotas: 'Rotas', grupo_armadilhas: 'Armadilhas',
  };
  const SETAS = {'^': '↑', '>': '→', 'v': '↓', '<': '←'};
  const S = {maps: [], map: null, alg: 'BFS', fonte: false, mode: 'single', page: 'inicio', steps: [], kind: 'path', index: 0, race: null, timer: null, request: 0,
    visual:null, camada:'all', destacarArmadilhas:true};

  // [IA] ChatGPT (Codex) – figuras existentes agrupadas conforme a classificação da equipe.
  const FIGURAS = {
    exploratorias: [
      ['A01', 'Distribuição dos graus', 'andre_01_distribuicao_graus.png'],
      ['A02', 'Distribuição dos votos e pesos', 'andre_02_distribuicao_pesos.png'],
      ['A04', 'Atributos por resultado', 'andre_04_atributos_result.png'],
      ['B01', 'Votos sem origem por faixa', 'brenda_01_faltantes_por_faixa.png'],
    ],
    explanatorias: [
      ['A03', 'Tempos de DFS e Bellman-Ford', 'andre_03_tempos_dfs_bellman.png'],
      ['B03', 'Efeito da transformação dos pesos', 'brenda_03_efeito_transformacao.png'],
    ],
    desempenho: [['B02', 'Tempos de BFS e Dijkstra', 'brenda_02_tempos_bfs_dijkstra.png']],
  };
  let categoriaFigura = 'exploratorias', indiceFigura = 0;

  function mostrarFigura(indice) {
    const figuras = FIGURAS[categoriaFigura];
    indiceFigura = Math.max(0, Math.min(indice, figuras.length - 1));
    const [id, nome, arquivo] = figuras[indiceFigura];
    const url = new URL(`../parte2/${arquivo}`, FrontData.output('')).href;
    $('#dataset-figure-id').textContent = id;
    $('#dataset-figure-title').textContent = nome;
    $('#dataset-figure-count').textContent = `${indiceFigura + 1} de ${figuras.length}`;
    $('#dataset-image-error').hidden = true;
    $('#dataset-image').hidden = false;
    $('#dataset-image').alt = `${id} · ${nome}`;
    $('#dataset-image').src = url;
    $('#figure-open').href = url;
    $('#dataset-caption').textContent = 'Figura gerada pelo projeto a partir dos dados e resultados da Parte 2.';
    $('#figure-prev').disabled = indiceFigura === 0;
    $('#figure-next').disabled = indiceFigura === figuras.length - 1;
    document.querySelectorAll('[data-figure]').forEach(button => button.setAttribute('aria-pressed', String(Number(button.dataset.figure) === indiceFigura)));
  }

  function mostrarCategoria(categoria) {
    categoriaFigura = categoria;
    $('#figure-category').textContent = {exploratorias:'Exploratórias', explanatorias:'Explanatórias', desempenho:'Desempenho'}[categoria];
    $('#dataset-figures').replaceChildren(...FIGURAS[categoria].map(([id, nome], indice) => {
      const button = document.createElement('button');
      button.type = 'button'; button.dataset.figure = indice;
      button.innerHTML = `<span>${id}</span>${escape(nome)}`;
      button.addEventListener('click', () => mostrarFigura(indice));
      return button;
    }));
    mostrarFigura(0);
  }

  // [IA] ChatGPT (Codex) – alterna telas sem empilhar seções na mesma página.
  function mostrarPagina() {
    const aliases = {mapas:'parte1', palco:'parte1', explorar:'parte1', parte2:'exploratorias'};
    const hash = location.hash.slice(1) || 'inicio';
    const pagina = aliases[hash] || hash;
    const paginasParte1 = ['parte1', 'comparar', 'analises', 'figuras'];
    const parte2 = Object.hasOwn(FIGURAS, pagina) || pagina === 'grafo';
    S.page = parte2 || paginasParte1.includes(pagina) ? pagina : 'inicio';
    stop(); ++S.request;
    const tela = S.page === 'grafo' ? 'grafo' : parte2 ? 'parte2' : S.page === 'comparar' ? 'palco' : S.page;
    // [IA] ChatGPT (Codex) – seleção de mapas e exploração compartilham a tela da Parte 1.
    document.querySelectorAll('[data-page]').forEach(section => {
      section.hidden = section.dataset.page !== tela && !(S.page === 'parte1' && section.dataset.page === 'palco');
    });
    $('#trocar-mapa').hidden = S.page !== 'comparar';
    $('#nav-parte1').hidden = !paginasParte1.includes(S.page);
    $('#nav-parte2').hidden = !parte2;
    document.querySelectorAll('.nav-links a, .section-nav a').forEach(link => {
      const destino = link.getAttribute('href').slice(1);
      const ativo = destino === S.page || (destino === 'parte1' && link.closest('.nav-links') && paginasParte1.includes(S.page))
        || (destino === 'parte2' && parte2);
      if (ativo) link.setAttribute('aria-current', 'page'); else link.removeAttribute('aria-current');
    });
    window.scrollTo({top: 0, behavior: 'instant'});
    if (S.page === 'grafo') DatasetGraph.open();
    else if (parte2) mostrarCategoria(S.page);
    else if (S.page === 'analises' || S.page === 'figuras') { if (current()) loadAnalyses(); }
    else if (S.page === 'parte1' || S.page === 'comparar') {
      if (S.page === 'parte1') requestAnimationFrame(drawThumbs);
      if (current()) {
        const modo = S.page === 'comparar' ? 'compare' : 'single';
        if (S.mode !== modo) setMode(modo); else load();
      }
    }
  }

  const escape = value => String(value).replace(/[&<>"']/g, char => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'})[char]);
  const css = name => getComputedStyle(document.documentElement).getPropertyValue(name).trim();
  const algInfo = id => ALGS.find(alg => alg.id === id);
  const current = () => S.maps.find(map => map.mapa === S.map);
  const titulo = name => {
    const numero = /^m\d+/.exec(name)?.[0];
    const nome = NOMES[name] || name.replace(/^grupo_/, '').replaceAll('_', ' ');
    return numero ? `${numero} · ${nome}` : nome;
  };
  const numero = (value, digits = 0) => Number(value).toLocaleString('pt-BR', {maximumFractionDigits: digits});
  function tempo(ms) {
    if (ms === null || ms === undefined || Number.isNaN(ms)) return '—';
    if (ms < 1) return `${numero(ms * 1000)} µs`;
    if (ms < 1000) return `${numero(ms, ms < 10 ? 2 : 1)} ms`;
    return `${numero(ms / 1000, 2)} s`;
  }

  function status(title, detail, type = '') {
    const box = $('#status-message');
    box.className = `status ${type}`;
    box.innerHTML = `<strong>${escape(title)}</strong><span>${escape(detail)}</span>`;
  }

  // ---------- desenho do mapa ----------
  function drawMaze(canvas, grade, options = {}) {
    const {width = 600, maxHeight = Infinity, maxCell = 36, minCell = 2, steps = [], upto = -1, kind = 'path', color = null, visual = null} = options;
    const rows = grade.length, cols = grade[0].length;
    const cell = Math.max(minCell, Math.min(maxCell, Math.floor(width / cols), Math.floor(maxHeight / rows)));
    const w = cols * cell, h = rows * cell, dpr = window.devicePixelRatio || 1;
    canvas.width = Math.round(w * dpr); canvas.height = Math.round(h * dpr);
    canvas.style.width = `${w}px`; canvas.style.height = `${h}px`;
    const ctx = canvas.getContext('2d');
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    const cor = {wall: css('--wall'), floor: css('--floor'), grid: css('--grid'), mud: css('--mud'), water: css('--water'),
      key: css('--key'), door: css('--door'), bonus: css('--bonus'), fonte: css('--fonte'), conveyor: css('--conveyor'), symbol: css('--symbol')};
    const gap = cell >= 10 ? 1 : 0;
    ctx.fillStyle = cor.grid; ctx.fillRect(0, 0, w, h);
    for (let r = 0; r < rows; r++) for (let c = 0; c < cols; c++) {
      const s = grade[r][c];
      if (s === '#') { ctx.fillStyle = cor.wall; ctx.fillRect(c * cell, r * cell, cell, cell); continue; }
      ctx.fillStyle = s === ',' ? cor.mud : s === '~' ? cor.water : /[a-d]/.test(s) ? cor.key : /[A-D]/.test(s) ? cor.door
        : s === '+' ? cor.bonus : s === '*' ? cor.fonte : SETAS[s] ? cor.conveyor : cor.floor;
      ctx.fillRect(c * cell, r * cell, cell - gap, cell - gap);
    }
    const centro = (r, c) => [c * cell + (cell - gap) / 2, r * cell + (cell - gap) / 2];
    // [IA] ChatGPT (Codex) – filtro e realce visuais dos estados já presentes nos CSVs.
    const naCamada = estado => !visual || S.camada === 'all' || (estado.chaves.join('') || '-') === S.camada;
    if (visual) {
      const estadosCamada = visual.estados.filter(naCamada);
      const casasCamada = new Set(estadosCamada.map(estado => `${estado.linha},${estado.coluna}`));
      if (S.camada !== 'all') {
        ctx.fillStyle = css('--bg'); ctx.globalAlpha = 0.8;
        for (let r = 0; r < rows; r++) for (let c = 0; c < cols; c++) {
          if (grade[r][c] !== '#' && !casasCamada.has(`${r},${c}`)) ctx.fillRect(c * cell, r * cell, cell - gap, cell - gap);
        }
        ctx.globalAlpha = 1;
      }
      if (S.destacarArmadilhas) {
        const casasArmadilha = new Set(estadosCamada.filter(estado => visual.armadilhas.has(estado.estado)).map(estado => `${estado.linha},${estado.coluna}`));
        ctx.strokeStyle = css('--bad'); ctx.lineWidth = Math.max(2, cell * 0.08); ctx.setLineDash([4, 2]);
        for (const casa of casasArmadilha) {
          const [r, c] = casa.split(',').map(Number);
          ctx.strokeRect(c * cell + 2, r * cell + 2, Math.max(1, cell - 5), Math.max(1, cell - 5));
        }
        ctx.setLineDash([]);
      }
    }
    const camada = step => css(`--layer-${Math.min(step.chaves.length, 4)}`);
    const ultimo = Math.min(upto, steps.length - 1);
    if (ultimo >= 0 && kind === 'explore') {
      ctx.fillStyle = color; ctx.globalAlpha = 0.38;
      for (let i = 0; i <= ultimo; i++) if (naCamada(steps[i])) ctx.fillRect(steps[i].coluna * cell, steps[i].linha * cell, cell - gap, cell - gap);
      ctx.globalAlpha = 1;
    } else if (ultimo >= 1) {
      ctx.lineCap = 'round'; ctx.lineJoin = 'round'; ctx.lineWidth = Math.max(2, cell * 0.28);
      for (let i = 1; i <= ultimo; i++) {
        if (!naCamada(steps[i - 1]) || !naCamada(steps[i])) continue;
        const [x1, y1] = centro(steps[i - 1].linha, steps[i - 1].coluna), [x2, y2] = centro(steps[i].linha, steps[i].coluna);
        ctx.strokeStyle = color || camada(steps[i]);
        ctx.beginPath(); ctx.moveTo(x1, y1); ctx.lineTo(x2, y2); ctx.stroke();
      }
    }
    if (cell >= 14) {
      ctx.fillStyle = cor.symbol; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
      ctx.font = `600 ${Math.round(cell * 0.5)}px ${css('--font')}`;
      for (let r = 0; r < rows; r++) for (let c = 0; c < cols; c++) {
        const s = grade[r][c];
        if (s === '#' || s === '.' || s === ',' || s === '~') continue;
        const [x, y] = centro(r, c);
        ctx.fillText(SETAS[s] || s, x, y + 1);
      }
    }
    if (ultimo >= 0 && naCamada(steps[ultimo])) {
      const step = steps[ultimo];
      const [x, y] = centro(step.linha, step.coluna);
      ctx.beginPath(); ctx.arc(x, y, Math.max(3, cell * 0.34), 0, Math.PI * 2);
      ctx.fillStyle = color || camada(step); ctx.fill();
      ctx.lineWidth = Math.max(1.5, cell * 0.08); ctx.strokeStyle = css('--surface'); ctx.stroke();
    }
  }

  // ---------- galeria ----------
  function buildGallery() {
    for (const [id, grupo] of [['#mapas-oficiais', false], ['#mapas-equipe', true]]) {
      const row = $(id);
      row.replaceChildren();
      for (const map of S.maps.filter(item => item.grupo === grupo)) {
        const card = document.createElement('button');
        card.type = 'button'; card.className = `map-card${grupo ? ' equipe' : ''}`;
        card.setAttribute('role', 'option'); card.dataset.mapa = map.mapa;
        const chaves = new Set(map.grade.join('').match(/[a-d]/g) || []).size;
        card.innerHTML = `<span class="map-thumb"><canvas aria-hidden="true"></canvas></span><span class="map-name">${escape(titulo(map.mapa))}</span><span class="map-meta">${map.linhas}×${map.colunas} · ${chaves ? `${chaves} ${chaves === 1 ? 'chave' : 'chaves'}` : 'sem chaves'}</span>`;
        card.addEventListener('click', () => selectMap(map.mapa, true));
        row.append(card);
      }
      if (!row.children.length) row.innerHTML = '<p class="map-meta">Nenhum mapa nesta pasta.</p>';
    }
    drawThumbs();
  }
  function drawThumbs() {
    document.querySelectorAll('.map-card').forEach(card => {
      const map = S.maps.find(item => item.mapa === card.dataset.mapa);
      const canvas = card.querySelector('canvas');
      drawMaze(canvas, map.grade, {width: card.querySelector('.map-thumb').clientWidth - 12, maxHeight: 76, maxCell: 12, minCell: 1});
    });
  }
  function selectMap(name, abrir = false) {
    S.map = name;
    document.querySelectorAll('.map-card').forEach(card => card.setAttribute('aria-selected', String(card.dataset.mapa === name)));
    $('#palco-mapa').textContent = titulo(name) + (current()?.grupo ? ' · mapa da equipe' : '');
    if (abrir && S.page !== 'parte1') { location.hash = 'parte1'; return; }
    if (S.page === 'analises' || S.page === 'figuras') return loadAnalyses();
    if (S.page === 'parte1' || S.page === 'comparar') return load();
  }

  // ---------- controles ----------
  function buildPills() {
    const box = $('#alg-pills');
    box.replaceChildren(...ALGS.map(alg => {
      const button = document.createElement('button');
      button.type = 'button'; button.className = 'alg-pill'; button.setAttribute('role', 'radio');
      button.style.setProperty('--c', `var(${alg.cor})`);
      button.dataset.alg = alg.id;
      button.innerHTML = `<strong>${alg.nome}</strong><small>${alg.desc}</small>`;
      button.addEventListener('click', () => { S.alg = alg.id; syncPills(); load(); });
      return button;
    }));
    syncPills();
  }
  function syncPills() {
    document.querySelectorAll('.alg-pill').forEach(pill => pill.setAttribute('aria-checked', String(pill.dataset.alg === S.alg)));
  }
  function setMode(mode) {
    if (S.mode === mode) return;
    S.mode = mode;
    document.querySelectorAll('[data-mode]').forEach(button => button.setAttribute('aria-checked', String(button.dataset.mode === mode)));
    $('#modo-single').hidden = mode !== 'single';
    $('#modo-compare').hidden = mode !== 'compare';
    $('#palco-titulo').textContent = mode === 'single' ? 'Siga cada passo.' : 'Os quatro, lado a lado.';
    load();
  }
  function buildLegend() {
    const itens = [['--wall', 'Parede'], ['--floor', 'Chão'], ['--mud', 'Lama · 3'], ['--water', 'Água · 5'], ['--key', 'Chave'], ['--door', 'Porta'],
      ['--bonus', 'Bônus · −4'], ['--fonte', 'Fonte · −2'], ['--conveyor', 'Esteira']];
    const camadas = [0, 1, 2, 3, 4].map(n => `<i style="background:var(--layer-${n});border:0;width:10px"></i>`).join('');
    $('#legenda').innerHTML = itens.map(([v, nome]) => `<span><i style="background:var(${v})"></i>${nome}</span>`).join('')
      + `<span>${camadas} Percurso: a cor muda a cada chave</span>`;
  }

  // ---------- reprodução ----------
  function total() {
    if (S.mode === 'single') return S.steps.length;
    return S.race ? Math.max(0, ...S.race.lanes.map(lane => lane.steps.length)) : 0;
  }
  function stop() {
    clearInterval(S.timer); S.timer = null;
    $('#play-icon').innerHTML = '<path d="M6.5 4.2v11.6L16 10z" fill="currentColor"/>';
    $('#play-button').setAttribute('aria-label', 'Reproduzir');
  }
  function play() {
    if (S.timer) { stop(); return; }
    if (total() < 2) return;
    if (S.index >= total() - 1) S.index = 0;
    $('#play-icon').innerHTML = '<path d="M6 4h3v12H6zM11 4h3v12h-3z" fill="currentColor"/>';
    $('#play-button').setAttribute('aria-label', 'Pausar');
    S.timer = setInterval(() => {
      S.index = Math.min(S.index + 1, total() - 1);
      draw();
      if (S.index >= total() - 1) stop();
    }, Number($('#speed-range').value));
    draw();
  }
  function move(value) { stop(); S.index = Math.max(0, Math.min(value, total() - 1)); draw(); }
  function updatePlayer() {
    const n = total();
    for (const id of ['restart-button', 'back-button', 'play-button', 'next-button', 'timeline']) $(`#${id}`).disabled = n < 2;
    $('#timeline').max = Math.max(n - 1, 0);
    $('#timeline').value = S.index;
    $('#step-label').textContent = `${n ? S.index : 0} de ${Math.max(n - 1, 0)}`;
    $('#end-label').textContent = S.mode === 'compare' ? 'Último a terminar' : S.kind === 'explore' ? 'Fim da busca' : S.kind === 'cycle' ? 'Fim do ciclo' : 'Alvo';
  }
  function draw() {
    if (S.mode === 'single') renderSingle(); else renderRace();
    updatePlayer();
  }

  // ---------- modo de um algoritmo ----------
  function renderSingle() {
    const map = current(); if (!map) return;
    const wrap = $('#single-wrap');
    drawMaze($('#single-canvas'), map.grade, {width: wrap.clientWidth, maxHeight: Math.max(320, window.innerHeight * 0.62), maxCell: 44, minCell: 6,
      steps: S.steps, upto: S.index, kind: S.kind, color: S.kind === 'explore' ? css('--alg-dfs') : null, visual:S.visual});
    const step = S.steps[S.index];
    $('#position-value').textContent = step ? `linha ${step.linha}, coluna ${step.coluna}` : '—';
    $('#keys-value').textContent = step ? step.chaves.join(', ') || 'nenhuma' : '—';
    $('#bonus-value').textContent = step ? step.bonus_consumidos.length : '—';
    $('#cost-value').textContent = step?.custo_acumulado ?? '—';
    $('#moves-label').textContent = S.kind === 'explore' ? 'Estados visitados' : 'Movimentos';
    $('#moves-value').textContent = step ? (S.kind === 'explore' ? S.index + 1 : S.index) : '—';
  }
  async function loadSingle(ticket) {
    const map = current();
    S.steps = []; S.kind = 'path';
    ['position-value', 'keys-value', 'bonus-value', 'cost-value', 'moves-value'].forEach(id => { $(`#${id}`).textContent = '—'; });
    $('#algorithm-note').textContent = 'Carregando o resultado.';
    draw();
    status('Carregando', `${algInfo(S.alg).nome} no mapa ${titulo(map.mapa)}.`);
    const result = await FrontData.result(map.mapa, S.alg, map.grade, S.fonte);
    if (ticket !== S.request) return;
    if (!result) {
      $('#algorithm-note').textContent = 'Nenhum resultado encontrado para esta combinação.';
      status('Resultado indisponível', 'Rode python -m src.front.server na raiz do projeto e recarregue a página.', 'warning');
      return draw();
    }
    S.kind = result.status === 'exploracao' ? 'explore' : result.status === 'ciclo_negativo' ? 'cycle' : 'path';
    S.steps = S.kind === 'cycle' ? result.ciclo_negativo : result.passos;
    // [IA] ChatGPT (Codex) – mantém a origem importada visível após carregar o resultado.
    const nota = result.aviso || result.mensagem;
    $('#algorithm-note').textContent = result.arquivo_importado
      ? `Arquivo importado: ${result.arquivo_importado}. ${nota}` : nota;
    if (result.status === 'sucesso') status(`${algInfo(S.alg).nome} encontrou o caminho`, `${result.movimentos} movimentos, custo total ${result.custo_total ?? 'indisponível'}.`, result.aviso ? 'warning' : '');
    else if (S.kind === 'explore') status('Exploração da DFS pronta', `${S.steps.length} estados na ordem em que foram descobertos.`);
    else if (result.status === 'classificacao') status('Classificação da DFS carregada', result.mensagem);
    else status(S.kind === 'cycle' ? 'Ciclo negativo encontrado' : result.status === 'sem_caminho' ? 'Sem solução' : 'Execução recusada',
      S.kind === 'cycle' && result.custo_ciclo !== null ? `${result.mensagem} Custo do ciclo: ${result.custo_ciclo}.` : result.mensagem, 'warning');
    draw();
  }

  // ---------- corrida dos quatro ----------
  function laneState(lane, index) {
    const r = lane.resultado;
    if (!r) return {texto: 'Sem dados', classe: ''};
    if (r.status === 'peso_negativo_recusado') return {texto: 'Recusou', classe: 'warn'};
    if (r.status === 'sem_caminho') return {texto: 'Sem caminho', classe: 'warn'};
    if (r.status === 'classificacao') return {texto: 'Só classificação', classe: ''};
    const fim = index >= lane.steps.length - 1;
    if (r.status === 'ciclo_negativo') return {texto: fim ? 'Fechou o ciclo' : 'Ciclo negativo', classe: fim ? 'done' : 'warn'};
    if (lane.kind === 'explore') return {texto: fim ? 'Busca completa' : 'Explorando', classe: fim ? 'done' : ''};
    return {texto: fim ? `Chegou em ${lane.steps.length - 1} passos` : 'Andando', classe: fim ? 'done' : 'ok'};
  }
  function buildRace(data) {
    const map = current();
    S.race = {medido: data.medido, lanes: data.algoritmos.map(entry => {
      const r = entry.resultado;
      const kind = r?.status === 'exploracao' ? 'explore' : r?.status === 'ciclo_negativo' ? 'cycle' : 'path';
      return {...entry, kind, steps: !r ? [] : kind === 'cycle' ? r.ciclo_negativo : r.passos};
    })};
    const validos = S.race.lanes.filter(lane => lane.tempo_ms !== null && lane.resultado && lane.resultado.status !== 'peso_negativo_recusado');
    const vencedor = validos.length ? validos.reduce((a, b) => (b.tempo_ms < a.tempo_ms ? b : a)) : null;
    $('#race').replaceChildren(...S.race.lanes.map(lane => {
      const alg = algInfo(lane.algoritmo), r = lane.resultado;
      const el = document.createElement('article');
      el.className = 'lane'; el.style.setProperty('--c', `var(${alg.cor})`);
      const explorar = lane.kind === 'explore';
      const stats = [
        [explorar ? 'Estados descobertos' : 'Movimentos', explorar ? lane.steps.length : r?.movimentos ?? '—'],
        [explorar ? 'Arcos classificados' : 'Custo', explorar ? Object.values(r?.classificacao_arcos || {}).reduce((a, b) => a + b, 0) || '—' : r?.custo_total ?? '—'],
        ['Tempo', tempo(lane.tempo_ms)],
      ];
      el.innerHTML = `<div class="lane-head"><h3>${alg.nome}${lane === vencedor ? ' <span class="pill done">Mais rápido</span>' : ''}</h3><span class="pill" data-pill></span></div>
        <div class="canvas-wrap"><canvas aria-label="${escape(alg.nome)} no mapa ${escape(titulo(map.mapa))}"></canvas></div>
        <dl class="lane-stats">${stats.map(([k, v]) => `<div><dt>${k}</dt><dd>${escape(v)}</dd></div>`).join('')}</dl>
        <p class="lane-note">${escape(r ? (r.aviso || r.mensagem) : 'Resultado não encontrado.')}</p>`;
      lane.el = el;
      return el;
    }));
    renderScoreboard(vencedor);
  }
  function renderRace() {
    const map = current(); if (!map || !S.race) return;
    for (const lane of S.race.lanes) {
      const wrap = lane.el.querySelector('.canvas-wrap');
      drawMaze(lane.el.querySelector('canvas'), map.grade, {width: wrap.clientWidth, maxHeight: 360, maxCell: 30, minCell: 3,
        steps: lane.steps, upto: Math.min(S.index, lane.steps.length - 1), kind: lane.kind, color: css(algInfo(lane.algoritmo).cor), visual:S.visual});
      const estado = laneState(lane, S.index);
      const pill = lane.el.querySelector('[data-pill]');
      pill.textContent = estado.texto; pill.className = `pill ${estado.classe}`;
    }
  }
  function renderScoreboard(vencedor) {
    const lanes = S.race.lanes;
    const caminhos = lanes.filter(lane => lane.resultado?.status === 'sucesso');
    const melhores = (lista, campo) => {
      const validos = lista.filter(lane => lane.resultado[campo] !== null);
      if (!validos.length) return [];
      const melhor = Math.min(...validos.map(lane => lane.resultado[campo]));
      return validos.filter(lane => lane.resultado[campo] === melhor);
    };
    const menosPassos = melhores(caminhos, 'movimentos');
    const menorCusto = melhores(caminhos, 'custo_total');
    const nomes = lista => lista.map(lane => algInfo(lane.algoritmo).nome).join(', ');
    const destaque = (rotulo, quem, valor) => `<div class="highlight"><span>${rotulo}</span><strong>${escape(quem)}</strong><small>${escape(valor)}</small></div>`;
    $('#destaques').innerHTML = destaque('Mais rápido', vencedor ? algInfo(vencedor.algoritmo).nome : '—',
      vencedor ? `${tempo(vencedor.tempo_ms)} · média de ${vencedor.execucoes} ${vencedor.execucoes === 1 ? 'execução' : 'execuções'}` : S.race.medido ? 'Nenhum algoritmo concluiu.' : 'Precisa do servidor para medir.')
      + destaque(menosPassos.length > 1 ? 'Menos movimentos (empate)' : 'Menos movimentos', menosPassos.length ? nomes(menosPassos) : '—',
        menosPassos.length ? `${menosPassos[0].resultado.movimentos} movimentos` : 'Nenhum caminho até a saída.')
      + destaque(menorCusto.length > 1 ? 'Menor custo (empate)' : 'Menor custo', menorCusto.length ? nomes(menorCusto) : '—',
        menorCusto.length ? `custo ${menorCusto[0].resultado.custo_total}` : 'Nenhum custo calculado.');
    $('#placar-nota').textContent = S.race.medido ? 'Tempo de execução de cada algoritmo, medido agora no servidor.' : 'Sem servidor, os tempos não podem ser medidos. Rode python -m src.front.server.';
    const medidos = lanes.filter(lane => lane.tempo_ms !== null).sort((a, b) => {
      const ra = a.resultado?.status === 'peso_negativo_recusado', rb = b.resultado?.status === 'peso_negativo_recusado';
      return ra - rb || a.tempo_ms - b.tempo_ms;
    });
    const maximo = Math.max(...medidos.filter(l => l.resultado?.status !== 'peso_negativo_recusado').map(l => l.tempo_ms), 0.000001);
    $('#barras').innerHTML = medidos.map(lane => {
      const recusou = lane.resultado?.status === 'peso_negativo_recusado';
      const largura = recusou ? 0 : Math.max(1.5, lane.tempo_ms / maximo * 100);
      const vezes = vencedor && !recusou && lane !== vencedor ? ` · ${numero(lane.tempo_ms / vencedor.tempo_ms, 1)}×` : '';
      return `<li class="bar${lane === vencedor ? ' first' : ''}${recusou ? ' out' : ''}" style="--c:var(${algInfo(lane.algoritmo).cor})">
        <span class="bar-name">${algInfo(lane.algoritmo).nome}</span>
        <span class="bar-track"><span class="bar-fill" style="width:${largura}%"></span></span>
        <span class="bar-value">${recusou ? 'recusou' : tempo(lane.tempo_ms) + vezes}</span></li>`;
    }).join('');
  }
  async function loadRace(ticket) {
    const map = current();
    S.race = null;
    $('#race').innerHTML = ALGS.map(alg => `<article class="lane" style="--c:var(${alg.cor})"><div class="lane-head"><h3>${alg.nome}</h3><span class="pill">Medindo</span></div><p class="lane-note">Rodando o algoritmo no servidor…</p></article>`).join('');
    $('#destaques').innerHTML = ''; $('#barras').innerHTML = '';
    draw();
    status('Medindo os quatro algoritmos', map.mapa === 'm08_grande' ? 'O Bellman-Ford leva alguns segundos no m08.' : `Mapa ${titulo(map.mapa)}.`);
    const data = await FrontData.compare(map.mapa, map.grade, S.fonte);
    if (ticket !== S.request) return;
    buildRace(data);
    S.index = 0;
    draw();
    status(data.medido ? 'Corrida pronta' : 'Resultados carregados sem tempos', data.medido ? 'Aperte reproduzir para ver os quatro andando ao mesmo tempo.' : 'Rode python -m src.front.server para medir o tempo de cada algoritmo.', data.medido ? '' : 'warning');
  }

  async function load() {
    if (!['parte1', 'comparar'].includes(S.page)) return;
    const ticket = ++S.request;
    stop(); S.index = 0;
    if (!current()) return;
    try {
      const visual = await FrontData.visualizacao(S.map, S.fonte);
      if (ticket !== S.request) return;
      if (S.visual?.mapa !== visual.mapa || S.visual?.fonte !== visual.fonte) S.camada = 'all';
      S.visual = visual;
      $('#layer-filter').replaceChildren(...['all', ...visual.camadas].map(camada => {
        const option = document.createElement('option');
        option.value = camada;
        option.textContent = camada === 'all' ? 'Todas as camadas' : camada === '-' ? 'Sem chaves' : `Chaves ${camada}`;
        return option;
      }));
      $('#layer-filter').value = S.camada;
      $('#layer-filter').disabled = !visual.disponivel;
      $('#trap-toggle').disabled = !visual.disponivel;
      atualizarNotaEstrutura();
      if (S.mode === 'single') await loadSingle(ticket); else await loadRace(ticket);
    } catch (error) {
      if (ticket !== S.request) return;
      status('Não foi possível carregar', `${error.message} Rode python -m src.front.server na raiz do projeto.`, 'error');
    }
  }

  function atualizarNotaEstrutura() {
    const visual = S.visual;
    if (!visual?.disponivel) {
      $('#structure-note').textContent = 'CSVs de estados ou armadilhas indisponíveis para este mapa e regra.';
      return;
    }
    const estados = visual.estados.filter(estado => S.camada === 'all' || (estado.chaves.join('') || '-') === S.camada);
    const armadilhas = estados.filter(estado => visual.armadilhas.has(estado.estado)).length;
    $('#structure-note').textContent = `${estados.length} estados na seleção, ${armadilhas} estados-armadilha. A borda vermelha tracejada indica casas com pelo menos um estado-armadilha na seleção. O filtro muda o desenho, não o resultado do algoritmo.`;
  }

  // ---------- análises ----------
  async function loadAnalyses() {
    const map = current(); if (!map) return;
    const data = await FrontData.analyses(map.mapa, S.fonte);
    if (S.map !== map.mapa) return;
    const camadas = data?.camadas?.camadas;
    if (Array.isArray(camadas) && camadas.length) {
      const max = Math.max(...camadas.map(c => Number(c.ordem)), 1);
      const estados = camadas.reduce((soma, c) => soma + Number(c.ordem), 0);
      $('#graph-view').innerHTML = `<p class="summary">${camadas.length} ${camadas.length === 1 ? 'camada' : 'camadas'}, ${estados} estados e ${data.camadas.arcos_entre_camadas} arcos que trocam de camada.</p><div class="rows">`
        + camadas.map((c, i) => `<div class="row" style="--c:var(--layer-${Math.min(i, 4)})"><span>${c.chaves === '-' ? 'Sem chaves' : `Chaves ${escape(c.chaves)}`}</span><span class="row-track"><span class="row-fill" style="width:${Number(c.ordem) / max * 100}%"></span></span><span class="row-value">${c.ordem} estados</span></div>`).join('') + '</div>';
    } else $('#graph-view').textContent = 'Camadas ainda não exportadas para este mapa.';
    const arcos = data?.classificacao_arcos;
    if (arcos) {
      const nomes = {arvore: 'Árvore', retorno: 'Retorno', avanco: 'Avanço', cruzamento: 'Cruzamento'};
      const cores = {arvore: '--alg-bfs', retorno: '--alg-bf', avanco: '--alg-dijkstra', cruzamento: '--alg-dfs'};
      const max = Math.max(...Object.values(arcos), 1);
      $('#arc-view').innerHTML = `<p class="summary">${arcos.retorno ? 'Há arcos de retorno, então o grafo tem ciclos.' : 'Sem arcos de retorno: nenhum ciclo alcançável.'}</p><div class="rows">`
        + Object.entries(arcos).map(([k, v]) => `<div class="row" style="--c:var(${cores[k]})"><span>${nomes[k]}</span><span class="row-track"><span class="row-fill" style="width:${v / max * 100}%"></span></span><span class="row-value">${v}</span></div>`).join('') + '</div>';
    } else $('#arc-view').textContent = 'Classificação DFS ainda não exportada para este mapa.';
    const candidatas = [
      [`percurso_${map.mapa}.png`, 'Percurso de menor custo, com a cor mudando a cada chave'],
      ['arvore_bfs_m02.png', 'Árvore BFS do m02, com os níveis visíveis', 'm02_uma_chave'],
      ['grafo_estados_camadas_m02.png', 'Grafo de estados do m02 organizado em camadas', 'm02_uma_chave'],
      ['heatmap_multiplicidade_m08.png', 'Quantos estados caem em cada casa do m08', 'm08_grande'],
    ].filter(([, , dono]) => !dono || dono === map.mapa);
    const box = $('#figures-view');
    box.replaceChildren();
    let restantes = candidatas.length;
    const vazio = () => { if (--restantes === 0 && !box.children.length) box.innerHTML = '<p class="card-body">Este mapa não tem figuras exportadas. As figuras pedidas no enunciado são do m02, do m03 e do m08.</p>'; };
    for (const [arquivo, legenda] of candidatas) {
      const fig = document.createElement('figure');
      const img = new Image();
      img.alt = legenda;
      img.addEventListener('load', () => { box.append(fig); vazio(); }, {once: true});
      img.addEventListener('error', vazio, {once: true});
      img.src = FrontData.output(arquivo).href;
      fig.append(img);
      fig.insertAdjacentHTML('beforeend', `<figcaption>${escape(legenda)}</figcaption>`);
    }
  }

  // ---------- eventos ----------
  window.addEventListener('hashchange', mostrarPagina);
  $('#layer-filter').addEventListener('change', event => { S.camada = event.target.value; atualizarNotaEstrutura(); draw(); });
  $('#trap-toggle').addEventListener('change', event => { S.destacarArmadilhas = event.target.checked; draw(); });
  $('#figure-prev').addEventListener('click', () => mostrarFigura(indiceFigura - 1));
  $('#figure-next').addEventListener('click', () => mostrarFigura(indiceFigura + 1));
  $('#dataset-image').addEventListener('error', () => { $('#dataset-image').hidden = true; $('#dataset-image-error').hidden = false; });
  document.querySelectorAll('[data-mode]').forEach(button => button.addEventListener('click', () => { location.hash = button.dataset.mode === 'single' ? 'parte1' : 'comparar'; }));
  document.querySelectorAll('[data-fonte]').forEach(button => button.addEventListener('click', () => {
    S.fonte = button.dataset.fonte === 'true';
    document.querySelectorAll('[data-fonte]').forEach(b => b.setAttribute('aria-checked', String(b === button)));
    if (S.page === 'analises' || S.page === 'figuras') loadAnalyses();
    if (S.page === 'parte1' || S.page === 'comparar') load();
  }));
  $('#play-button').addEventListener('click', play);
  $('#restart-button').addEventListener('click', () => move(0));
  $('#back-button').addEventListener('click', () => move(S.index - 1));
  $('#next-button').addEventListener('click', () => move(S.index + 1));
  $('#timeline').addEventListener('input', event => move(Number(event.target.value)));
  $('#speed-range').addEventListener('input', event => {
    const valor = Number(event.target.value);
    $('#speed-value').textContent = valor < 200 ? 'Rápida' : valor > 600 ? 'Lenta' : 'Normal';
    if (S.timer) { stop(); play(); }
  });
  document.addEventListener('keydown', event => {
    if (event.target.closest('input, select, textarea') || event.metaKey || event.ctrlKey || event.altKey) return;
    if (event.key === 'ArrowRight') { move(S.index + 1); event.preventDefault(); }
    else if (event.key === 'ArrowLeft') { move(S.index - 1); event.preventDefault(); }
  });
  $('#data-file').addEventListener('change', async event => {
    const file = event.target.files?.[0]; if (!file) return;
    try {
      const rows = await FrontData.importFile(file);
      // [IA] ChatGPT (Codex) – prioriza a seleção atual e aguarda sua atualização.
      const disponiveis = rows.filter(row => S.maps.some(map => map.mapa === row.mapa));
      const selecionado = disponiveis.find(row => row.mapa === S.map && row.algoritmo === S.alg)
        || disponiveis.find(row => row.mapa === S.map) || disponiveis[0];
      if (!selecionado) throw new Error('Nenhum resultado corresponde aos mapas disponíveis na interface.');
      S.alg = selecionado.algoritmo; syncPills();
      await selectMap(selecionado.mapa, true);
    } catch (error) { status('Arquivo inválido', error.message, 'error'); }
    finally { event.target.value = ''; }
  });
  let frame;
  const redraw = () => { cancelAnimationFrame(frame); frame = requestAnimationFrame(() => { drawThumbs(); draw(); }); };
  window.addEventListener('resize', redraw);
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', redraw);

  // ---------- início ----------
  async function start() {
    buildPills(); buildLegend(); updatePlayer();
    mostrarPagina();
    FrontData.online().then(on => {
      const pill = $('#server-pill');
      pill.className = `server-pill ${on ? 'on' : 'off'}`;
      pill.lastElementChild.textContent = on ? 'Servidor ativo' : 'Sem servidor';
    });
    try {
      const names = await FrontData.list();
      const maps = await Promise.all(names.map(name => FrontData.map(name).catch(() => null)));
      S.maps = maps.filter(Boolean);
      if (!S.maps.length) throw new Error('Nenhum mapa encontrado em data/mapas/.');
      buildGallery();
      selectMap(S.maps.some(map => map.mapa === 'm02_uma_chave') ? 'm02_uma_chave' : S.maps[0].mapa);
      mostrarPagina();
    } catch (error) {
      status('Falha ao carregar os mapas', `${error.message} Rode python -m src.front.server na raiz do projeto.`, 'error');
    }
  }
  start();
})();
