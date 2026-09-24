/* Schedule filtering — vanilla (no jQuery, no Isotope). The schedule is a plain
   vertical list of event rows; we just show/hide rows by category (location
   class) + day class + text search. Replaces schedule-isotope.js.
   Day headings (.day-heading) are hidden along with their day. */
(function () {
  var container = document.querySelector('#events');
  if (!container) return;
  var items = Array.prototype.slice.call(container.querySelectorAll('.item'));
  // Each day heading owns the rows that follow it up to the next heading, so a
  // heading can be hidden when its whole day is filtered away — otherwise
  // picking a single stage leaves "SUNDAY" sitting over nothing.
  var days = Array.prototype.slice.call(container.querySelectorAll('.day-heading'))
    .map(function (heading) {
      var members = [];
      var node = heading.nextElementSibling;
      while (node && !node.classList.contains('day-heading')) {
        if (node.classList.contains('item')) members.push(node);
        node = node.nextElementSibling;
      }
      return { heading: heading, items: members };
    });
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
    // is-first trims the top margin off whichever heading now leads the list.
    var seenFirst = false;
    days.forEach(function (day) {
      var dayVisible = day.items.some(function (item) { return item.style.display !== 'none'; });
      day.heading.style.display = dayVisible ? '' : 'none';
      day.heading.classList.toggle('is-first', dayVisible && !seenFirst);
      if (dayVisible) seenFirst = true;
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
