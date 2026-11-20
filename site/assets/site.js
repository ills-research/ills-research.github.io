// Navigation stays visible without JavaScript.
const toggle = document.querySelector('.menu-toggle');
const nav = document.querySelector('.main-nav');
if (toggle && nav) {
  document.documentElement.classList.add('js');
  const show = open => {
    toggle.setAttribute('aria-expanded', String(open));
    nav.classList.toggle('is-open', open);
  };
  toggle.addEventListener('click', () => show(toggle.getAttribute('aria-expanded') !== 'true'));
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') {
      show(false); toggle.focus();
    }
  });
  document.addEventListener('click', event => {
    if (!nav.contains(event.target) && !toggle.contains(event.target)) show(false);
  });
  matchMedia('(min-width: 1041px)').addEventListener('change', () => show(false));
}
const alternate = document.querySelector('.lang-link');
function syncLanguageLink() {
  if (!alternate) return;
  const url = new URL(alternate.href);
  url.hash = location.hash;
  alternate.href = url.href;
}
syncLanguageLink();
addEventListener('hashchange', syncLanguageLink);

// Static HTML supplies the calendar on build day. Reclassify entries on later visits.
document.querySelectorAll('img.seminar-speaker-avatar, img.visitor-avatar').forEach((image) => {
  image.addEventListener('error', () => image.remove(), { once: true });
});

const calendar = document.querySelector('[data-calendar-date]');
if (calendar) {
  const today = new Intl.DateTimeFormat('en-CA', {
    timeZone: 'America/Toronto', year: 'numeric', month: '2-digit', day: '2-digit',
  }).formatToParts(new Date());
  const part = type => today.find(item => item.type === type).value;
  const date = [part('year'), part('month'), part('day')].join('-');
  if (date !== calendar.dataset.calendarDate) {
    const entries = Array.from(calendar.querySelectorAll('#upcoming [data-start], #archive [data-start]'));
    entries.sort((a, b) => a.dataset.start.localeCompare(b.dataset.start));
    const groups = [
      ['upcoming', entries.filter(entry => entry.dataset.end >= date)],
      ['archive', entries.filter(entry => entry.dataset.end < date).reverse()],
    ];
    for (const [id, rows] of groups) {
      const section = document.getElementById(id);
      section.querySelector('.notice-list').append(...rows);
      section.querySelector('.calendar-empty').hidden = rows.length > 0;
    }
    const seminars = Array.from(calendar.querySelectorAll('.seminar-talk'));
    for (const [group, upcoming] of [['upcoming-seminars', true], ['past-seminars', false]]) {
      const section = document.getElementById(group);
      const talks = seminars.filter(talk => (talk.dataset.start >= date) === upcoming);
      talks.sort((a, b) => {
        const days = a.dataset.start.localeCompare(b.dataset.start);
        return (upcoming ? days : -days) || a.dataset.time.localeCompare(b.dataset.time);
      });
      section.querySelector('.notice-list').append(...talks);
      section.hidden = talks.length === 0;
    }
  }
}
