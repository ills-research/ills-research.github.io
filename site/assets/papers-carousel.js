document.querySelectorAll('[data-paper-carousel]').forEach((carousel) => {
  const track = carousel.querySelector('[data-paper-track]');
  const previous = carousel.querySelector('[data-paper-prev]');
  const next = carousel.querySelector('[data-paper-next]');
  if (!track || !previous || !next) return;
  const cards = Array.from(track.querySelectorAll('.axis-paper-card'));

  if (cards.length < 2) return;

  const updateControls = () => {
    previous.disabled = track.scrollLeft <= 2;
    next.disabled = track.scrollLeft + track.clientWidth >= track.scrollWidth - 2;
  };
  const move = direction => {
    const gap = Number.parseFloat(getComputedStyle(track).columnGap) || 0;
    const amount = cards[0].getBoundingClientRect().width + gap;
    track.scrollBy({
      left: direction * amount,
      behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth',
    });
  };

  previous.addEventListener('click', () => move(-1));
  next.addEventListener('click', () => move(1));
  track.addEventListener('scroll', updateControls, { passive: true });
  new ResizeObserver(updateControls).observe(track);
  updateControls();
});
