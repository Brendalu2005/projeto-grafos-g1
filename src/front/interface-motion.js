/* [IA[  ChatGPT (Codex) - adaptação do Arrow Reveal Button do Originkit para o front HTML do projeto. */
/* Arrow Reveal Button — Originkit.
 * Adaptação do código React fornecido pelo usuário para o front HTML existente.
 * Mantém a geometria de cobertura, o percurso do ícone e o easing do componente.
 * Não lê dados do projeto nem interfere nos eventos de carregamento/reprodução.
 */
(() => {
  'use strict';
  const button = document.querySelector('#load-button');
  if (!button) return;
  const slot = button.querySelector('.origin-slot');
  const badge = button.querySelector('.origin-badge');
  const glyph = button.querySelector('.origin-arrow');
  const wrapper = button.closest('.origin-button-wrap');
  const stroke = wrapper?.querySelector('.origin-stroke');
  if (!slot || !badge || !glyph || !stroke) return;

  function measure() {
    const w = button.offsetWidth;
    const h = button.offsetHeight;
    if (!w || !h) return;
    // Fórmulas do componente original: raio em px, guarda de tangência e
    // distância até o canto mais distante a partir do centro do badge.
    const radius = Math.min(w, h) / 2;
    const badgeSize = Math.min(30, w, h);
    const rb = badgeSize / 2;
    const rawCx = slot.offsetLeft + slot.offsetWidth / 2;
    const cy = slot.offsetTop + slot.offsetHeight / 2;
    const fromEdge = Math.max(rb, radius);
    const cx = Math.min(Math.max(rawCx, fromEdge), w - fromEdge);
    const far = Math.hypot(Math.max(cx, w - cx), Math.max(cy, h - cy));
    const coverD = Math.ceil(2 * far * 1.02);
    const arrowSize = Math.min(18, Math.floor(badgeSize / Math.SQRT2));
    button.style.borderRadius = `${radius}px`;
    stroke.style.borderRadius = `${radius + 1}px`;
    button.style.setProperty('--origin-cover', String(coverD / badgeSize));
    button.style.setProperty('--origin-travel', `${w / 2 - cx}px`);
    Object.assign(badge.style, {
      width: `${badgeSize}px`, height: `${badgeSize}px`,
      left: `${cx}px`, top: `${cy}px`,
      marginLeft: `${-rb}px`, marginTop: `${-rb}px`
    });
    Object.assign(glyph.style, {
      width: `${arrowSize}px`, height: `${arrowSize}px`,
      left: `${cx}px`, top: `${cy}px`,
      marginLeft: `${-arrowSize / 2}px`, marginTop: `${-arrowSize / 2}px`
    });
    wrapper.classList.add('origin-ready');
  }
  measure();
  if ('ResizeObserver' in window) {
    const observer = new ResizeObserver(measure);
    observer.observe(button);
    observer.observe(slot);
    window.addEventListener('pagehide', () => observer.disconnect(), {once: true});
    window.addEventListener('pageshow', event => {
      if (event.persisted) { observer.observe(button); observer.observe(slot); measure(); }
    });
  } else {
    window.addEventListener('resize', measure, {passive: true});
  }
  if (document.fonts?.ready) document.fonts.ready.then(measure);
})();
