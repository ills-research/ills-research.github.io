document.querySelectorAll('[data-paper-carousel]').forEach((carousel) => {
  const track = carousel.querySelector('[data-paper-track]');
  const toggle = carousel.querySelector('[data-paper-toggle]');
  if (!track || !toggle) return;

  const cards = Array.from(track.querySelectorAll('.axis-paper-card'));
  if (cards.length < 2) return;

  const isFrench = document.documentElement.lang === 'fr';
  const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
  let userPaused = reducedMotion.matches;
  let hoverPaused = false;
  let focusPaused = false;
  let interactionTimer;
  let interval;

  const updateToggle = () => {
    const label = userPaused
      ? (isFrench ? 'Reprendre le carrousel' : 'Play carousel')
      : (isFrench ? 'Mettre le carrousel en pause' : 'Pause carousel');
    const visibleLabel = userPaused ? (isFrench ? 'Reprendre' : 'Play') : 'Pause';
    toggle.textContent = visibleLabel;
    toggle.setAttribute('aria-label', label);
  };

  const stop = () => {
    window.clearInterval(interval);
    interval = undefined;
  };

  const start = () => {
    stop();
    if (userPaused || hoverPaused || focusPaused) return;
    interval = window.setInterval(() => {
      const style = getComputedStyle(track);
      const gap = Number.parseFloat(style.columnGap) || 0;
      const step = cards[0].getBoundingClientRect().width + gap;
      const atEnd = track.scrollLeft + track.clientWidth >= track.scrollWidth - 3;
      track.scrollTo({
        left: atEnd ? 0 : Math.min(track.scrollLeft + step, track.scrollWidth - track.clientWidth),
        behavior: 'smooth',
      });
    }, 5500);
  };

  toggle.addEventListener('click', () => {
    userPaused = !userPaused;
    updateToggle();
    start();
  });

  carousel.addEventListener('pointerenter', () => {
    hoverPaused = true;
    stop();
  });
  carousel.addEventListener('pointerleave', () => {
    hoverPaused = false;
    start();
  });
  carousel.addEventListener('focusin', () => {
    focusPaused = true;
    stop();
  });
  carousel.addEventListener('focusout', (event) => {
    if (!carousel.contains(event.relatedTarget)) {
      focusPaused = false;
      start();
    }
  });

  track.addEventListener('pointerdown', () => {
    stop();
    window.clearTimeout(interactionTimer);
  });
  track.addEventListener('pointerup', () => {
    window.clearTimeout(interactionTimer);
    interactionTimer = window.setTimeout(start, 9000);
  });
  reducedMotion.addEventListener('change', (event) => {
    if (event.matches) userPaused = true;
    updateToggle();
    start();
  });

  updateToggle();
  start();
});
