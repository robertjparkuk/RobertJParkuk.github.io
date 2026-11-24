/* Carbon Ready – Two Regimes: offline support for robertjpark.co.uk.
   Same-origin only. Nothing is sent anywhere: this file only keeps copies of
   this site's own pages on the device so the tools open without a signal.
   Pages are fetched fresh whenever there is a connection (network first), so
   dated regulatory wording is never served stale while online.
   Bump CACHE when the list below changes. */
const CACHE = 'carbon-ready-v1';
const SHELL = [
  '/app/',
  '/cbam-desk/is-it-a-cbam-good/',
  '/cbam-desk/checklist/',
  '/tools/uk-cbam-countdown.html',
  '/tools/dashboards/cbam-exposure-tracker.html',
  '/tools/carbon-ready-reckoner.html',
  '/tools/which-eu-rules-apply.html',
  '/tools/incoterms.html',
  '/assets/style.css',
  '/assets/fonts/fonts.css',
  '/assets/fonts/source-sans-3.woff',
  '/assets/fonts/source-sans-3-italic.woff',
  '/assets/fonts/source-serif-4.woff',
  '/assets/fonts/fraunces.woff',
  '/assets/fonts/ibm-plex-mono-regular.woff',
  '/assets/fonts/ibm-plex-mono-medium.woff',
  '/assets/logo-header.png',
  '/assets/mark.png',
  '/assets/tools-mark.svg',
  '/assets/app/icon-192.png',
  '/assets/js/app.js'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE)
      .then(cache => Promise.all(SHELL.map(url => cache.add(url).catch(() => null))))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(k => k.startsWith('carbon-ready-') && k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', event => {
  const req = event.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return;

  const isPage = req.mode === 'navigate' || (req.headers.get('accept') || '').includes('text/html');
  if (isPage) {
    // Network first: always the current page when online; the saved copy only when offline.
    event.respondWith(
      fetch(req)
        .then(res => {
          if (res && res.ok) { const copy = res.clone(); caches.open(CACHE).then(c => c.put(req, copy)); }
          return res;
        })
        .catch(() => caches.match(req, { ignoreSearch: true }).then(hit => hit || caches.match('/app/')))
    );
    return;
  }
  // Styles, fonts, images, scripts: saved copy first, refreshed in the background.
  event.respondWith(
    caches.match(req).then(hit => {
      const fresh = fetch(req).then(res => {
        if (res && res.ok) { const copy = res.clone(); caches.open(CACHE).then(c => c.put(req, copy)); }
        return res;
      }).catch(() => hit);
      return hit || fresh;
    })
  );
});
