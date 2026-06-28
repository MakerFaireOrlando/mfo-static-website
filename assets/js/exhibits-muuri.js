/* Exhibits masonry grid — Muuri (vanilla, no jQuery), replacing Isotope.
   Keeps: masonry/collage layout, shuffle, quick search, and the server-side
   category filtering (the dropdown navigates to /exhibits/categories/<slug>/). */
(function () {
  var gridEl = document.querySelector('#exhibits');
  if (!gridEl) return;

  // Reveal a simple flow grid (instead of a blank page) whenever Muuri can't
  // run — whether the script never loaded OR it throws during init.
  function fallback() {
    gridEl.classList.remove('muuri-active');
    gridEl.classList.add('muuri-fallback');
  }
  if (typeof Muuri === 'undefined') { fallback(); return; }

  // Small shared debounce (used by resize + search).
  function debounce(fn, wait) {
    var t;
    return function () {
      clearTimeout(t);
      t = setTimeout(fn, wait);
    };
  }

  var grid;
  try {
    gridEl.classList.add('muuri-active');
    grid = new Muuri(gridEl, {
      items: '.item',
      layoutOnInit: true,
      layoutOnResize: false,   // handled below (needs refreshItems for breakpoints)
      layoutDuration: 300,
      layoutEasing: 'ease',
      layout: { fillGaps: true, rounding: false }
    });
  } catch (e) {
    fallback();
    return;
  }
  requestAnimationFrame(function () { gridEl.classList.add('muuri-shown'); });

  var noResults = document.querySelector('#exhibits-no-results');
  function updateNoResults() {
    if (!noResults) return;
    var anyVisible = grid.getItems().some(function (it) { return it.isVisible(); });
    noResults.style.display = anyVisible ? 'none' : '';
  }
  updateNoResults();   // cover a server-rendered empty grid on first load

  // Each card carries an inline aspect-ratio, so the masonry is already correct
  // before images decode — no per-image relayout needed. A single pass once
  // everything has loaded just corrects any rounding drift.
  window.addEventListener('load', function () { grid.refreshItems().layout(); });

  // Re-measure + re-layout on resize (debounced) so the column count reflows
  // cleanly when the viewport crosses a breakpoint (1 → … → 6 columns).
  window.addEventListener('resize', debounce(function () { grid.refreshItems().layout(); }, 150));

  // Quick search — plain case-insensitive substring over each card's text
  // (title + hidden description). No regex, so user input can't break it.
  var search = document.querySelector('#maker-search-input');
  if (search) {
    search.addEventListener('input', debounce(function () {
      var q = search.value.trim().toLowerCase();
      grid.filter(function (item) {
        return !q || item.getElement().textContent.toLowerCase().indexOf(q) !== -1;
      });
      updateNoResults();
    }, 180));
  }

  // Shuffle — true Fisher-Yates over the items, then apply that order.
  var shuffleBtn = document.querySelector('#shuffle');
  if (shuffleBtn) {
    shuffleBtn.addEventListener('click', function () {
      var items = grid.getItems().slice();
      for (var i = items.length - 1; i > 0; i--) {
        var j = Math.floor(Math.random() * (i + 1));
        var tmp = items[i]; items[i] = items[j]; items[j] = tmp;
      }
      grid.sort(items);
    });
  }

  // Category dropdown → navigate to the server-rendered category page.
  var catSelect = document.querySelector('.filters-select');
  if (catSelect) {
    if (window.location.pathname.indexOf('/categories/') !== -1) {
      var slug = window.location.pathname.split('/').filter(Boolean).pop();
      catSelect.value = '.' + slug;
    }
    catSelect.addEventListener('change', function () {
      var v = this.value;
      window.location = (v === '*') ? '/exhibits/' : '/exhibits/categories/' + v.replace(/^\./, '') + '/';
    });
  }
})();
