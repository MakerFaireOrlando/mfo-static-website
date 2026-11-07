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

  // Optional ?category=<slug> deep link preselects the location filter.
  var params = new URLSearchParams(window.location.search);
  var cat = params.get('category');
  if (cat && catSel) catSel.value = '.' + cat;

  // Optional ?day=<friday|saturday|sunday> deep link, and ?day=all to force
  // the full three-day list on a day the page would otherwise narrow.
  var dayParam = (params.get('day') || '').toLowerCase();
  if (daySel && dayParam && dayParam !== 'all' && selectDay(dayParam)) {
    // handled
  } else if (daySel && !dayParam) {
    // During the Faire, open on today. Attendees are standing in the venue
    // reading this on a phone; the three-day list buries what's on now.
    // The event days come off the day headings (data-date), so this follows
    // whatever _data/schedule.json publishes rather than a hardcoded
    // weekend — and does nothing at all on the other 362 days of the year.
    // The dropdown shows the day it picked, so it isn't a hidden filter:
    // "show all" is one tap away.
    var now = new Date();
    var pad = function (n) { return (n < 10 ? '0' : '') + n; };
    var today = now.getFullYear() + '-' + pad(now.getMonth() + 1) + '-' + pad(now.getDate());
    days.some(function (day) {
      if (day.heading.getAttribute('data-date') !== today) return false;
      return selectDay(day.heading.getAttribute('data-day'));
    });
  }

  // Sets the day dropdown, but only to a day it actually offers — an unknown
  // ?day= or a heading with no matching option leaves it on "show all".
  function selectDay(slug) {
    if (!daySel || !slug) return false;
    var wanted = '.' + slug;
    for (var i = 0; i < daySel.options.length; i++) {
      if (daySel.options[i].value === wanted) {
        daySel.selectedIndex = i;
        return true;
      }
    }
    return false;
  }

  apply();
})();
