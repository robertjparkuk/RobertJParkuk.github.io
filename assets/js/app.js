/* Registers the offline helper (sw.js) and wires the Install button on /app/.
   No tracking, no outside requests. */
(function () {
  if ('serviceWorker' in navigator) {
    window.addEventListener('load', function () {
      navigator.serviceWorker.register('/sw.js').catch(function () {});
    });
  }
  var deferred = null;
  var btn = document.getElementById('install-app');
  window.addEventListener('beforeinstallprompt', function (e) {
    e.preventDefault();
    deferred = e;
    if (btn) { btn.hidden = false; }
  });
  if (btn) {
    btn.addEventListener('click', function () {
      if (!deferred) { return; }
      deferred.prompt();
      deferred.userChoice.finally(function () { deferred = null; btn.hidden = true; });
    });
  }
  var off = document.getElementById('offline-note');
  function net() { if (off) { off.hidden = navigator.onLine; } }
  window.addEventListener('online', net); window.addEventListener('offline', net); net();
})();
