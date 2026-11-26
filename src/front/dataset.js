// [IA] ChatGPT (Codex) – Canvas da rede real; algoritmos executados pelo servidor existente.
(() => {
  'use strict';
  const $ = id => document.getElementById(id);
  const canvas = $('rede-canvas'), ctx = canvas.getContext('2d');
  const cores = {normal: '#3e4756', negativo: '#8c1f4e', resultado: '#0081cf'};
  let dados, carregando = false, nos = [], indice = new Map(), caso = null, algoritmo = '';
  let escala = 1, deslocX = 0, deslocY = 0, largura = 1, altura = 1, selecionado = null;
  let arraste = null, quadro = null;
  let foco = null, nosFoco = [], indiceFoco = new Map(), pedidoSelecao = 0;
  const textos = {
    BFS: ['Executar 3 fontes', 'BFS no grafo completo: menor número de arcos; pesos ignorados.'],
    DFS: ['Executar 3 fontes', 'DFS no grafo completo: ordem de descoberta, classificação de arcos e alcance; pesos ignorados.'],
    DIJKSTRA: ['Executar 5 pares', 'Dijkstra no grafo completo com PESO + 1. O mínimo passa de −1 para 0; a transformação pode mudar os caminhos preferidos.'],
    BELLMAN_FORD: ['Executar 2 cenários', 'Bellman-Ford em dois subgrafos reais pequenos: peso negativo sem ciclo e ciclo negativo.'],
  };
  const numero = n => n.toLocaleString('pt-BR');

  async function consultar(url) {
    const resposta = await fetch(url);
    if (!resposta.headers.get('content-type')?.includes('application/json')) {
      throw new Error('Inicie a interface com python -m src.front.server e abra o endereço exibido.');
    }
    const valor = await resposta.json();
    if (!resposta.ok) throw new Error(valor.erro || 'Não foi possível consultar o dataset.');
    return valor;
  }

  // Distribuição inicial determinística; acomodação curta apenas para a visualização.
  function posicionar() {
    nos = dados.nos.map((no, i) => ({...no, x: Math.cos(i * 2.39996) * Math.sqrt(i) * 22,
      y: Math.sin(i * 2.39996) * Math.sqrt(i) * 22}));
    indice = new Map(nos.map(no => [no.id, no]));
    const ligacoes = dados.arcos.map(([u, v]) => [indice.get(u), indice.get(v)]);
    for (let passo = 0; passo < 35; passo++) {
      const forcas = nos.map(() => ({x: 0, y: 0}));
      for (let i = 0; i < nos.length; i++) {
        for (let j = i + 1; j < nos.length; j++) {
          const dx = nos[i].x - nos[j].x, dy = nos[i].y - nos[j].y;
          const distancia = Math.max(25, dx * dx + dy * dy);
          const fx = dx * 35 / distancia, fy = dy * 35 / distancia;
          forcas[i].x += fx; forcas[i].y += fy;
          forcas[j].x -= fx; forcas[j].y -= fy;
        }
      }
      for (const [u, v] of ligacoes) {
        const dx = (v.x - u.x) * .0007, dy = (v.y - u.y) * .0007;
        u.x += dx; u.y += dy; v.x -= dx; v.y -= dy;
      }
      nos.forEach((no, i) => {
        no.x += Math.max(-8, Math.min(8, forcas[i].x));
        no.y += Math.max(-8, Math.min(8, forcas[i].y));
      });
    }
  }

  function agendar() {
    if (quadro === null) quadro = requestAnimationFrame(() => { quadro = null; desenhar(); });
  }

  function ajustar() {
    const ret = canvas.getBoundingClientRect();
    if (!ret.width || !ret.height) return;
    largura = ret.width; altura = ret.height;
    const pixel = Math.min(window.devicePixelRatio || 1, 2);
    canvas.width = Math.round(largura * pixel); canvas.height = Math.round(altura * pixel);
    ctx.setTransform(pixel, 0, 0, pixel, 0, 0);
    agendar();
  }

  function centralizar() {
    if (largura < 120 || altura < 120) return;
    const visiveis = foco ? nosFoco : caso && $('rede-somente').checked ? caso.nos.map(u => indice.get(u)).filter(Boolean) : nos;
    if (!visiveis.length) return;
    const xs = visiveis.map(n => n.x), ys = visiveis.map(n => n.y);
    const minX = Math.min(...xs), maxX = Math.max(...xs), minY = Math.min(...ys), maxY = Math.max(...ys);
    escala = Math.min(4, (largura - 100) / Math.max(80, maxX - minX), (altura - 100) / Math.max(80, maxY - minY));
    deslocX = largura / 2 - (minX + maxX) / 2 * escala;
    deslocY = altura / 2 - (minY + maxY) / 2 * escala;
    agendar();
  }

  function arco(u, v, seta) {
    const x = u.x * escala + deslocX, y = u.y * escala + deslocY;
    const tx = v.x * escala + deslocX, ty = v.y * escala + deslocY;
    ctx.moveTo(x, y);
    if (u === v) {
      ctx.moveTo(x + 10, y - 9); ctx.arc(x, y - 9, 10, 0, Math.PI * 2);
    } else {
      ctx.lineTo(tx, ty);
      if (seta) {
        const angulo = Math.atan2(ty - y, tx - x);
        const pontaX = tx - Math.cos(angulo) * 6, pontaY = ty - Math.sin(angulo) * 6;
        ctx.moveTo(pontaX - Math.cos(angulo - .5) * 7, pontaY - Math.sin(angulo - .5) * 7);
        ctx.lineTo(pontaX, pontaY);
        ctx.lineTo(pontaX - Math.cos(angulo + .5) * 7, pontaY - Math.sin(angulo + .5) * 7);
      }
    }
  }

  function desenhar() {
    ctx.clearRect(0, 0, largura, altura);
    if (!dados) return;
    if (foco) { desenharConexoes(); return; }
    const negativos = $('rede-negativos').checked, somente = $('rede-somente').checked && caso;
    const destacados = new Set(caso?.nos || []);
    if (!somente) {
      for (const negativo of [false, true]) {
        if (negativos && !negativo) continue;
        ctx.strokeStyle = negativo ? cores.negativo : cores.normal;
        ctx.globalAlpha = .13; ctx.lineWidth = .6; ctx.beginPath();
        for (const [u, v, peso] of dados.arcos) if ((peso < 0) === negativo) arco(indice.get(u), indice.get(v), false);
        ctx.stroke();
      }
    }
    ctx.globalAlpha = .85; ctx.lineWidth = 1.5; ctx.strokeStyle = cores.resultado; ctx.beginPath();
    for (const [u, v, peso] of caso?.arcos || []) if (!negativos || peso < 0) arco(indice.get(u), indice.get(v), true);
    ctx.stroke(); ctx.globalAlpha = 1;
    for (const no of nos) {
      if (somente && !destacados.has(no.id)) continue;
      const x = no.x * escala + deslocX, y = no.y * escala + deslocY;
      const destaque = destacados.has(no.id), fonte = no.id === caso?.fonte;
      ctx.fillStyle = destaque ? cores.resultado : cores.normal;
      ctx.beginPath(); ctx.arc(x, y, fonte ? 7 : destaque ? 4 : 2.5, 0, Math.PI * 2); ctx.fill();
      if (fonte || selecionado === no.id) {
        ctx.lineWidth = 2; ctx.strokeStyle = cores.negativo; ctx.stroke();
      }
      if (selecionado === no.id || fonte || (somente && destacados.size <= 12)) {
        ctx.font = '12px system-ui'; ctx.fillStyle = getComputedStyle(canvas).color;
        ctx.fillText(no.id, x + 10, y - 8);
      }
    }
  }

  function desenharConexoes() {
    // Todas as ocorrências são desenhadas; paralelos podem se sobrepor.
    for (const entrada of [false, true]) {
      ctx.globalAlpha = .5; ctx.lineWidth = 1.2;
      ctx.strokeStyle = entrada ? cores.negativo : cores.resultado; ctx.beginPath();
      for (const [u, v] of foco.arcos) {
        if ((v === foco.usuario) === entrada) arco(indiceFoco.get(u), indiceFoco.get(v), true);
      }
      ctx.stroke();
    }
    ctx.globalAlpha = 1;
    const corTexto = getComputedStyle(canvas).color;
    for (const no of nosFoco) {
      const x = no.x * escala + deslocX, y = no.y * escala + deslocY;
      if (x < -200 || x > largura + 20 || y < -20 || y > altura + 20) continue;
      const centro = no.id === foco.usuario;
      ctx.fillStyle = centro ? cores.negativo : cores.resultado;
      ctx.beginPath(); ctx.arc(x, y, centro ? 8 : 4, 0, Math.PI * 2); ctx.fill();
      ctx.font = centro ? 'bold 13px system-ui' : '12px system-ui';
      ctx.fillStyle = corTexto; ctx.fillText(no.id, x + 10, y - 6);
    }
  }

  function limparFoco() {
    ++pedidoSelecao; foco = null; nosFoco = []; indiceFoco.clear(); selecionado = null;
    $('rede-vizinhos').hidden = true; $('rede-vizinhos').replaceChildren();
    $('rede-voltar').hidden = true;
    $('rede-negativos').disabled = false; $('rede-somente').disabled = false;
    $('rede-legenda').textContent = 'Cores do grafo: cinza = conexões da rede; vinho = arcos com PESO negativo; azul = resultado do algoritmo. As setas apontam de quem votou para quem recebeu o voto.';
    $('rede-usuario').textContent = 'Clique em um usuário para mostrar somente suas conexões de entrada e saída, com os nomes dos vizinhos.';
    centralizar();
  }

  let resultadoBfs = null, linhasBfs = [], paginaBfs = 0;
  const tamanhoPaginaBfs = 50;

  function tabelaBfs() {
    const busca = $('rede-bfs-busca').value.trim().toLocaleLowerCase('pt-BR');
    const filtro = $('rede-bfs-filtro').value;
    const linhas = linhasBfs.filter(([usuario, distancia]) => usuario.toLocaleLowerCase('pt-BR').includes(busca)
      && (filtro === 'todos' || (filtro === 'alcancados' ? distancia !== null : distancia === null)));
    const paginas = Math.max(1, Math.ceil(linhas.length / tamanhoPaginaBfs));
    paginaBfs = Math.max(0, Math.min(paginaBfs, paginas - 1));
    const inicio = paginaBfs * tamanhoPaginaBfs;
    const visiveis = linhas.slice(inicio, inicio + tamanhoPaginaBfs);
    $('rede-bfs-usuarios').replaceChildren(...visiveis.map(([usuario, distancia]) => {
      const linha = document.createElement('tr');
      const situacao = distancia === null ? 'Inalcançável' : usuario === resultadoBfs.fonte ? 'Fonte' : 'Alcançado';
      const predecessor = resultadoBfs.predecessores[usuario];
      for (const valor of [usuario, distancia ?? '—', predecessor ?? '—', situacao]) {
        const celula = document.createElement('td'); celula.textContent = valor; linha.append(celula);
      }
      return linha;
    }));
    if (!visiveis.length) {
      const linha = document.createElement('tr'), celula = document.createElement('td');
      celula.colSpan = 4; celula.textContent = 'Nenhum usuário encontrado para estes filtros.';
      linha.append(celula); $('rede-bfs-usuarios').append(linha);
    }
    $('rede-bfs-pagina').textContent = `Página ${paginaBfs + 1} de ${paginas} · ${linhas.length ? inicio + 1 : 0}–${inicio + visiveis.length} de ${numero(linhas.length)} usuários`;
    $('rede-bfs-anterior').disabled = paginaBfs === 0;
    $('rede-bfs-proxima').disabled = paginaBfs >= paginas - 1;
  }

  function mostrarBfs(resultado) {
    resultadoBfs = resultado; paginaBfs = 0;
    $('rede-bfs').hidden = !resultado;
    $('rede-resumo').hidden = !!resultado;
    if (!resultado) {
      linhasBfs = []; $('rede-bfs-resumo').replaceChildren(); $('rede-bfs-usuarios').replaceChildren();
      return;
    }
    linhasBfs = Object.entries(resultado.distancias).sort(([a, da], [b, db]) => {
      if (da === null && db !== null) return 1;
      if (db === null && da !== null) return -1;
      return (da ?? 0) - (db ?? 0) || a.localeCompare(b, 'pt-BR');
    });
    const metricas = [
      ['Fonte', resultado.fonte], ['Grau de saída da fonte', numero(resultado.grau_saida_fonte)],
      ['Outros usuários alcançados', numero(resultado.outros_usuarios_alcancados)],
      ['Maior distância (arcos)', numero(resultado.maior_distancia_finita)],
      ['Total de usuários', numero(linhasBfs.length)],
      ['Usuários inalcançáveis', numero(linhasBfs.filter(([, distancia]) => distancia === null).length)],
    ];
    $('rede-bfs-resumo').replaceChildren(...metricas.map(([rotulo, valor]) => {
      const item = document.createElement('div'), termo = document.createElement('dt'), descricao = document.createElement('dd');
      termo.textContent = rotulo; descricao.textContent = valor; item.append(termo, descricao); return item;
    }));
    $('rede-bfs-busca').value = ''; $('rede-bfs-filtro').value = 'todos';
    tabelaBfs();
  }

  function selecionarCaso(resposta, indiceCaso) {
    limparFoco();
    caso = resposta.casos[indiceCaso];
    nos = nos.filter(no => no.grau !== null);
    indice = new Map(nos.map(no => [no.id, no]));
    // Caminhos e cenários podem incluir ocorrências fora dos 20 mil arcos exibidos.
    // Eles são sobrepostos integralmente e não substituem o recorte base.
    for (const id of caso.nos) if (!indice.has(id)) {
      const no = {id, grau: null, x: Math.cos(nos.length * 2.39996) * 350, y: Math.sin(nos.length * 2.39996) * 350};
      nos.push(no); indice.set(id, no);
    }
    $('rede-negativos').checked = false;
    $('rede-somente').checked = ['DIJKSTRA', 'BELLMAN_FORD'].includes(algoritmo);
    $('rede-nota').textContent = resposta.nota + ' Arcos do teste fora do recorte base são sobrepostos em azul; não entram na contagem de 20 mil.';
    $('rede-resumo').textContent = JSON.stringify(caso.resumo, null, 2);
    mostrarBfs(algoritmo === 'BFS' ? caso.resultado_bfs || null : null);
    $('rede-arcos').replaceChildren(...caso.arcos.slice(0, 30).map(([u, v, peso]) => {
      const linha = document.createElement('tr');
      for (const valor of [u, v, peso, algoritmo === 'DIJKSTRA' ? peso + 1 : '—']) {
        const celula = document.createElement('td'); celula.textContent = valor; linha.append(celula);
      }
      return linha;
    }));
    $('rede-tabela-nota').textContent = `${caso.arcos.length} arcos no destaque; tabela mostra os primeiros ${Math.min(30, caso.arcos.length)}. PESO é o peso ajustado para duplicados, antes do +1 do Dijkstra.`;
    [...$('rede-casos').children].forEach((botao, i) => botao.setAttribute('aria-pressed', String(i === indiceCaso)));
    centralizar();
  }

  function atualizarEscopo() {
    const [botao, escopo] = textos[$('rede-alg').value];
    $('rede-executar').textContent = botao; $('rede-escopo').textContent = escopo;
  }

  $('rede-executar').addEventListener('click', async () => {
    const botao = $('rede-executar'); botao.disabled = true; $('rede-alg').disabled = true;
    $('rede-status').textContent = 'Executando os casos no servidor…';
    try {
      const escolhido = $('rede-alg').value;
      const resposta = await consultar(`/api/dataset/executar?alg=${encodeURIComponent(escolhido)}`);
      algoritmo = escolhido;
      $('rede-resultados-titulo').textContent = `Execuções · ${$('rede-alg').selectedOptions[0].textContent}`;
      $('rede-casos').replaceChildren(...resposta.casos.map((item, i) => {
        const botaoCaso = document.createElement('button'); botaoCaso.type = 'button'; botaoCaso.className = 'ghost-button';
        botaoCaso.textContent = item.titulo; botaoCaso.addEventListener('click', () => selecionarCaso(resposta, i));
        return botaoCaso;
      }));
      selecionarCaso(resposta, 0);
      $('rede-status').textContent = `${resposta.casos.length} execuções de ${$('rede-alg').selectedOptions[0].textContent} concluídas. Selecione um resultado abaixo do grafo.`;
    } catch (erro) { $('rede-status').textContent = erro.message; }
    finally { botao.disabled = false; $('rede-alg').disabled = false; }
  });
  $('rede-bfs-busca').addEventListener('input', () => { paginaBfs = 0; tabelaBfs(); });
  $('rede-bfs-filtro').addEventListener('change', () => { paginaBfs = 0; tabelaBfs(); });
  $('rede-bfs-anterior').addEventListener('click', () => { paginaBfs--; tabelaBfs(); });
  $('rede-bfs-proxima').addEventListener('click', () => { paginaBfs++; tabelaBfs(); });
  $('rede-alg').addEventListener('change', atualizarEscopo);
  $('rede-reset').addEventListener('click', centralizar);
  $('rede-negativos').addEventListener('change', agendar);
  $('rede-somente').addEventListener('change', centralizar);
  async function selecionarUsuario(id) {
    if (!id || !dados) return;
    const pedido = ++pedidoSelecao;
    $('rede-usuario').textContent = `Buscando todas as conexões de ${id} no dataset…`;
    try {
      const resposta = await consultar(`/api/dataset/conexoes?usuario=${encodeURIComponent(id)}`);
      if (pedido !== pedidoSelecao) return;
      foco = resposta; selecionado = id;
      $('rede-legenda').textContent = `Conexões de ${id}: vinho = votos recebidos; azul = votos enviados. As setas apontam de quem votou para quem recebeu o voto.`;
      nosFoco = [{id, x: 0, y: 0}, ...resposta.vizinhos.filter(u => u !== id).map((usuario, i) => {
        const raio = 160 + Math.sqrt(i + 1) * 95;
        return {id: usuario, x: Math.cos(i * 2.39996) * raio, y: Math.sin(i * 2.39996) * raio};
      })];
      indiceFoco = new Map(nosFoco.map(no => [no.id, no]));
      const contagens = new Map(resposta.vizinhos.map(u => [u, {entrada: 0, saida: 0}]));
      for (const [u, v] of resposta.arcos) {
        if (v === id) contagens.get(u).entrada++;
        if (u === id) contagens.get(v).saida++;
      }
      $('rede-vizinhos').replaceChildren(...resposta.vizinhos.map(usuario => {
        const botao = document.createElement('button'), contagem = contagens.get(usuario);
        botao.type = 'button'; botao.className = 'ghost-button';
        botao.textContent = `${usuario} · ${numero(contagem.entrada)} entrada / ${numero(contagem.saida)} saída`;
        botao.addEventListener('click', () => selecionarUsuario(usuario));
        return botao;
      }));
      $('rede-vizinhos').hidden = false; $('rede-voltar').hidden = false;
      $('rede-negativos').disabled = true; $('rede-somente').disabled = true;
      $('rede-usuario').textContent = `${id} · ${numero(resposta.entradas)} arcos de entrada (vinho), ${numero(resposta.saidas)} de saída (azul), ${numero(resposta.lacos)} laços. ${numero(resposta.arcos.length)} ocorrências incidentes no dataset completo, incluindo conexões fora do recorte. Cada laço conta na entrada e na saída. Amplie para ler os nomes ou use a lista abaixo. Clique em um vizinho para explorar suas conexões.`;
      centralizar();
    } catch (erro) {
      if (pedido === pedidoSelecao) $('rede-usuario').textContent = erro.message;
    }
  }
  $('rede-voltar').addEventListener('click', limparFoco);
  $('rede-localizar').addEventListener('click', () => selecionarUsuario($('rede-busca').value.trim()));
  $('rede-busca').addEventListener('keydown', e => { if (e.key === 'Enter') selecionarUsuario(e.target.value.trim()); });
  canvas.addEventListener('pointerdown', e => {
    arraste = {x: e.clientX, y: e.clientY, inicioX: e.clientX, inicioY: e.clientY}; canvas.setPointerCapture(e.pointerId);
  });
  canvas.addEventListener('pointermove', e => {
    if (!arraste) return;
    deslocX += e.clientX - arraste.x; deslocY += e.clientY - arraste.y;
    arraste.x = e.clientX; arraste.y = e.clientY; agendar();
  });
  canvas.addEventListener('pointerup', e => {
    if (arraste && Math.hypot(e.clientX - arraste.inicioX, e.clientY - arraste.inicioY) < 5) {
      const ret = canvas.getBoundingClientRect(), x = e.clientX - ret.left, y = e.clientY - ret.top;
      const candidato = (foco ? nosFoco : nos.filter(n => !$('rede-somente').checked || !caso || caso.nos.includes(n.id)))
        .find(n => Math.hypot(n.x * escala + deslocX - x, n.y * escala + deslocY - y) < 10);
      if (candidato) selecionarUsuario(candidato.id);
    }
    arraste = null;
  });
  canvas.addEventListener('pointercancel', () => { arraste = null; });
  canvas.addEventListener('wheel', e => {
    e.preventDefault(); const ret = canvas.getBoundingClientRect();
    const x = e.clientX - ret.left, y = e.clientY - ret.top;
    const nova = Math.max(.02, Math.min(12, escala * (e.deltaY < 0 ? 1.15 : 1 / 1.15)));
    deslocX = x - (x - deslocX) * nova / escala; deslocY = y - (y - deslocY) * nova / escala;
    escala = nova; agendar();
  }, {passive: false});
  new ResizeObserver(ajustar).observe(canvas.parentElement);
  atualizarEscopo();
  window.DatasetGraph = {async open() {
    if (dados) { ajustar(); centralizar(); return; }
    if (carregando) return;
    carregando = true; $('rede-status').textContent = 'Carregando os arcos reais e organizando a visualização…';
    try {
      dados = await consultar('/api/dataset/grafo'); posicionar(); ajustar(); centralizar();
      $('rede-contagem').textContent = `${numero(dados.nos.length)} usuários · ${numero(dados.arcos.length)} arcos no recorte`;
      $('rede-regra').textContent = `${dados.regra} Grafo completo: ${numero(dados.vertices_total)} usuários e ${numero(dados.arcos_total)} arcos.`;
      $('rede-status').textContent = 'Recorte pronto. Escolha um algoritmo e execute seus casos.';
      $('rede-executar').disabled = false;
    } catch (erro) { dados = null; $('rede-status').textContent = erro.message; }
    finally { carregando = false; }
  }};
})();
