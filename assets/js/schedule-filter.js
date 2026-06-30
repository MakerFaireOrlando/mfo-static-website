/* Schedule filtering — vanilla (no jQuery, no Isotope). The schedule is a plain
   vertical list of event rows; we just show/hide rows by category (location
   class) + day class + text search. Replaces schedule-isotope.js. */
(function () {
  var container = document.querySelector('#events');
  if (!container) return;
  var items = Array.prototype.slice.call(container.querySelectorAll('.item'));
  var catSel = document.querySelector('.schedule-filters-select');
  var daySel = document.querySelector('.schedule-filters-select-day');
  var search = document.querySelector('#maker-search-input');
  var noResults = document.querySelector('#schedule-no-results');

  function debounce(fn, wait) {
    var t;
    return function () { clearTimeout(t); t = setTimeout(fn, wait); };
  }

  function apply() {
    // option values are like ".main-stage" / ".friday"; the rows carry the
    // bare class ("main-stage" / "friday").
    var catClass = catSel && catSel.value ? catSel.value.replace(/^\./, '') : '';
    var dayClass = daySel && daySel.value ? daySel.value.replace(/^\./, '') : '';
    var q = search ? search.value.trim().toLowerCase() : '';
    var anyVisible = false;
    items.forEach(function (item) {
      var show = true;
      if (catClass && !item.classList.contains(catClass)) show = false;
      if (show && dayClass && !item.classList.contains(dayClass)) show = false;
      if (show && q && item.textContent.toLowerCase().indexOf(q) === -1) show = false;
      item.style.display = show ? '' : 'none';
      if (show) anyVisible = true;
    });
    if (noResults) noResults.style.display = anyVisible ? 'none' : '';
  }

  // Category/day selects clear the search box (search is independent of them).
  if (catSel) catSel.addEventListener('change', function () { if (search) search.value = ''; apply(); });
  if (daySel) daySel.addEventListener('change', function () { if (search) search.value = ''; apply(); });

  // Searching resets the dropdowns to "show all" and filters across everything.
  if (search) {
    search.addEventListener('input', debounce(function () {
      if (catSel) catSel.selectedIndex = 0;
      if (daySel) daySel.selectedIndex = 0;
      apply();
    }, 180));
  }

  // Optional ?category=<slug> deep link preselects the category filter.
  var cat = new URLSearchParams(window.location.search).get('category');
  if (cat && catSel) catSel.value = '.' + cat;

  apply();
})();
