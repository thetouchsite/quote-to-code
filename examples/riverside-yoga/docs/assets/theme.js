/* The button writes `data-theme` on the root and remembers it. With no
   saved choice the system setting wins, which is the common case. */
(function () {
  var r = document.documentElement, b = document.querySelector('.tema');
  if (!b) return;
  b.addEventListener('click', function () {
    var scuro = r.dataset.theme
      ? r.dataset.theme === 'dark'
      : matchMedia('(prefers-color-scheme: dark)').matches;
    r.dataset.theme = scuro ? 'light' : 'dark';
    try { localStorage.setItem('tema', r.dataset.theme); } catch (e) {}
  });
})();
