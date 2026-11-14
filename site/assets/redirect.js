// Keep old bookmarks and query strings when a page moves.
const destination = new URL(document.querySelector('#destination').href);
destination.search = location.search;
if (location.hash === '#list-heading' && destination.pathname.endsWith('/seminars-events.html')) {
  if (!destination.hash) destination.hash = 'archive';
} else if (location.hash) {
  destination.hash = location.hash;
}
location.replace(destination.href);
