/* Registers the offline helper (sw.js) and runs the Install button on /app/.
   No tracking, no outside requests. */
(function () {
  if ('serviceWorker' in navigator) {
    window.addEventListener('load', function () {
      navigator.serviceWorker.register('/sw.js').catch(function () {});
    });
  }

  var btn = document.getElementById('install-app');
  var help = document.getElementById('install-help');
  var deferred = null;

  var standalone = (window.matchMedia && window.matchMedia('(display-mode: standalone)').matches) ||
    window.navigator.standalone === true;
  if (btn && standalone) { btn.style.display = 'none'; }

  // Chrome and Edge offer an install prompt; Safari and Firefox never do.
  window.addEventListener('beforeinstallprompt', function (e) {
    e.preventDefault();
    deferred = e;
  });
  window.addEventListener('appinstalled', function () {
    deferred = null;
    if (btn) { btn.style.display = 'none'; }
    if (help) { help.hidden = false; help.textContent = 'Installed. Open Carbon Ready from your home screen or app list.'; }
  });

  function steps() {
    var ua = navigator.userAgent || '';
    var iOS = /iPad|iPhone|iPod/.test(ua) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
    var android = /Android/.test(ua);
    var safari = /Safari/.test(ua) && !/Chrome|Chromium|CriOS|FxiOS|EdgiOS|Edg\//.test(ua);
    if (iOS && !safari) { return 'On iPhone or iPad, open this page in Safari, tap the Share button (the square with an arrow), then choose Add to Home Screen.'; }
    if (iOS) { return 'Tap the Share button (the square with an arrow) at the bottom or top of Safari, scroll down, then choose Add to Home Screen.'; }
    if (android) { return 'Open the browser menu (the three dots, top right) and choose Install app or Add to Home screen.'; }
    if (safari) { return 'In Safari on a Mac, open the File menu and choose Add to Dock.'; }
    return 'Use the install icon at the right of the address bar, or open the browser menu and choose Install or Add to Home screen. If there is no such option, this browser cannot install web apps: try Chrome, Edge or Safari.';
  }

  if (btn) {
    btn.addEventListener('click', function () {
      if (deferred) {
        deferred.prompt();
        if (deferred.userChoice && deferred.userChoice.then) {
          deferred.userChoice.then(function () { deferred = null; }, function () { deferred = null; });
        }
        return;
      }
      if (help) {
        help.textContent = steps();
        help.hidden = false;
        btn.setAttribute('aria-expanded', 'true');
        help.focus();
      }
    });
  }

  var off = document.getElementById('offline-note');
  function net() { if (off) { off.hidden = navigator.onLine; } }
  window.addEventListener('online', net);
  window.addEventListener('offline', net);
  net();
})();
