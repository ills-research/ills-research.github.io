(() => {
  const catalogue = document.getElementById('publication-browser');
  const { papers, people } = JSON.parse(document.getElementById('bibliography').textContent);
  const control = id => document.getElementById('pub-' + id);
  const french = document.documentElement.lang === 'fr';
  const t = (en, fr) => french ? fr : en;
  const format = new Intl.NumberFormat(document.documentElement.lang).format;
  const member = control('member');
  const year = control('year');
  const search = control('search');
  const jointOnly = control('joint');
  const types = [...catalogue.querySelectorAll('[data-category]')];
  const categories = {
    preprint: t('Preprint', 'Prépublication'),
    journal: t('Journal paper', 'Article de revue'),
    proceedings: t('Conference proceedings', 'Actes de conférence')
  };
  const personIndex = new Map(people.map((p, i) => [p.pid.replace('https://dblp.org/pid/', ''), i]));
  const fold = value => value.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
  const searchable = papers.map(p => fold([p.title, p.venue, p.volume, ...p.authors,
    ...p.members.map(i => people[i].name)].join(' ')));
  const pageSize = 25;
  let category = '';
  let page = 0;
  let results = [];

  function element(tag, text, cls) {
    const node = document.createElement(tag);
    if (text) node.textContent = text;
    if (cls) node.className = cls;
    return node;
  }
  function link(label, href) {
    const node = element('a', label);
    node.href = href;
    return node;
  }
  function entry(paper) {
    const row = element('li');
    const details = element('div');
    const venue = paper.venue === 'CoRR' ? 'arXiv' : paper.venue;
    const meta = element('p', [categories[paper.category], venue].filter(Boolean).join(' · '), 'publication-venue');
    if (paper.volume) meta.title = paper.volume;
    if (paper.joint_source) {
      const badge = element('span', t('France–Canada co-authored', 'Cosignée France–Canada'), 'publication-joint-badge');
      badge.title = t('Coauthored by researchers affiliated with institutions in France and Canada.',
        'Cosignée par des chercheurs affiliés à des établissements en France et au Canada.');
      meta.append(badge);
    }
    const title = element('h4');
    const url = paper.category === 'preprint' ? (paper.arxiv || paper.paper) : (paper.paper || paper.arxiv);
    title.append(url ? link(paper.title, url) : paper.title);
    details.append(meta, title);
    const authors = paper.authors.join(', ');
    if (paper.authors.length > 9) {
      const byline = element('details', '', 'publication-authors');
      const rest = paper.authors.length - 4;
      byline.append(element('summary', paper.authors.slice(0, 4).join(', ') +
        t(' and ' + rest + ' more', ' et ' + rest + ' autres')), element('p', authors));
      details.append(byline);
    } else {
      details.append(element('p', authors, 'publication-authors'));
    }
    const resources = element('div', '', 'publication-resources');
    if (paper.arxiv) resources.append(link('arXiv', paper.arxiv));
    if (paper.paper) resources.append(link(t('Paper', 'Article'), paper.paper));
    const citation = element('details', '', 'publication-citation');
    const summary = element('summary', 'BibTeX');
    summary.setAttribute('aria-label', t('BibTeX for ', 'Référence BibTeX pour ') + paper.title);
    const download = link(t('Download .bib', 'Télécharger le fichier .bib'),
      'data:application/x-bibtex;charset=utf-8,' + encodeURIComponent(paper.bibtex + '\n'));
    download.download = paper.key.replaceAll('/', '-') + '.bib';
    citation.append(summary, element('pre', paper.bibtex), download);
    resources.append(citation);
    details.append(resources);
    row.append(element('span', String(paper.year), 'publication-date'), details);
    return row;
  }
  function drawPage() {
    const start = page * pageSize;
    const count = results.length;
    control('results').replaceChildren(...results.slice(start, start + pageSize).map(entry));
    const range = format(start + 1) + '–' + format(Math.min(start + pageSize, count));
    control('count').textContent = count ? range + t(' of ', ' sur ') + format(count) +
      (count === 1 ? ' publication' : ' publications') : t('No matching publications.', 'Aucune publication correspondante.');
    const pages = Math.ceil(count / pageSize);
    control('page').textContent = count ? 'Page ' + (page + 1) + t(' of ', ' sur ') + pages : '';
    catalogue.querySelector('.catalogue-pages').hidden = pages < 2;
    control('prev').disabled = page === 0;
    control('next').disabled = page + 1 >= pages;
    control('export').disabled = count === 0;
  }
  function applyFilters() {
    const words = fold(search.value).trim().split(/\s+/).filter(Boolean);
    const idx = personIndex.get(member.value);
    results = papers.filter((paper, i) => (!category || paper.category === category) &&
      (!year.value || paper.year === Number(year.value)) &&
      (!jointOnly.checked || Boolean(paper.joint_source)) &&
      (idx === undefined || paper.members.includes(idx)) && words.every(word => searchable[i].includes(word)));
    types.forEach(button => button.setAttribute('aria-pressed', String(category === button.dataset.category)));
    page = 0;
    drawPage();
  }
  function syncLinks() {
    const params = new URLSearchParams(location.search);
    for (const [name, value] of [['member', member.value], ['year', year.value], ['category', category],
      ['joint', jointOnly.checked ? '1' : ''], ['q', search.value]]) {
      if (value) params.set(name, value);
      else params.delete(name);
    }
    const url = new URL(location.href);
    url.search = params.toString();
    url.hash = 'publications';
    if (location.protocol !== 'file:') history.replaceState(null, '', url);
    const language = document.querySelector('.lang-link');
    const other = new URL(language.href);
    other.search = url.search;
    other.hash = url.hash;
    language.href = other;
  }
  function update() {
    applyFilters();
    syncLinks();
  }
  const params = new URLSearchParams(location.search);
  member.value = params.get('member') || '';
  year.value = params.get('year') || '';
  search.value = params.get('q') || '';
  jointOnly.checked = params.get('joint') === '1';
  category = types.find(button => button.dataset.category === params.get('category'))?.dataset.category || '';
  if (location.hash === '#publications') {
    const language = document.querySelector('.lang-link');
    const other = new URL(language.href);
    other.search = location.search;
    other.hash = location.hash;
    language.href = other;
  }
  search.addEventListener('input', update);
  member.addEventListener('change', update);
  year.addEventListener('change', update);
  jointOnly.addEventListener('change', update);
  types.forEach(button => button.addEventListener('click', () => {
    category = category === button.dataset.category ? '' : button.dataset.category;
    update();
  }));
  control('reset').addEventListener('click', () => {
    search.value = '';
    year.value = '';
    member.value = '';
    jointOnly.checked = false;
    category = '';
    update();
  });
  for (const [id, step] of [['prev', -1], ['next', 1]]) {
    control(id).addEventListener('click', () => {
      page += step;
      drawPage();
      control('count').focus();
    });
  }
  control('export').addEventListener('click', () => {
    const rows = [[t('Year', 'Année'), t('Category', 'Catégorie'), t('France–Canada joint', 'France–Canada conjoint'), t('Title', 'Titre'), t('Authors', 'Auteurs'),
      t('Venue', 'Lieu de publication'), t('Proceedings title', 'Titre des actes'), t('ILLS members', 'Membres de l’ILLS'), 'arXiv', t('Paper', 'Article'), 'BibTeX']];
    for (const paper of results) rows.push([paper.year, categories[paper.category], paper.joint_source ? t('Yes', 'Oui') : t('No', 'Non'), paper.title, paper.authors.join(', '),
      paper.venue, paper.volume, paper.members.map(i => people[i].name).join(', '), paper.arxiv, paper.paper, paper.bibtex]);
    const quote = (value, column) => {
      const text = column === 10 ? String(value) : String(value).replace(/^[=+@-]/, char => "'" + char);
      return '"' + text.replaceAll('"', '""') + '"';
    };
    const csv = rows.map(row => row.map(quote).join(',')).join('\r\n');
    const url = URL.createObjectURL(new Blob(['\uFEFF', csv], {type: 'text/csv;charset=utf-8'}));
    const download = link('CSV', url);
    download.download = 'ills-publications.csv';
    document.body.append(download);
    download.click();
    download.remove();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  });
  applyFilters();
  catalogue.hidden = false;
})();
