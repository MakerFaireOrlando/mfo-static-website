/*
 * Main-nav dropdown behaviour (desktop only, >= 768px).
 *
 * The legacy theme opened these with a bare CSS :hover (see the override in
 * assets/css/mfo-redesign.css §3). A `display` flip can't carry a delay, so
 * the panel died the instant the pointer left the <li> — and because the
 * header isn't sticky, one notch of the wheel slid the nav out from under a
 * stationary cursor and closed the menu mid-reach. This script owns the open
 * state instead, so the close can be delayed and a scroll can be ignored.
 *
 * The CSS keeps a plain :hover fallback, so if this file fails to load the
 * menus still open on hover exactly as they did before.
 *
 * Below 768px none of the pointer handling runs — the slide-out drawer keeps
 * using Bootstrap's click toggle, untouched.
 */
(function () {
  "use strict";

  var menu = document.getElementById("slidemenu");
  if (!menu) { return; }  // e.g. _layouts/schedule-app.html renders no nav

  var desktop = window.matchMedia("(min-width: 768px)");

  // The grace period after the pointer leaves. The CSS has no transition of
  // its own, so this timer is the single place the delay is tuned.
  var CLOSE_DELAY = 400;
  // How long after the last scroll event the page counts as "still settling".
  var SCROLL_SETTLE = 600;

  var openItem = null;
  var closeTimer = null;
  var settleTimer = null;
  var scrolling = false;

  function setExpanded(item, state) {
    var toggle = item.querySelector(".dropdown-toggle");
    if (toggle) { toggle.setAttribute("aria-expanded", state ? "true" : "false"); }
  }

  function close() {
    clearTimeout(closeTimer);
    if (!openItem) { return; }
    openItem.classList.remove("mf-nav-open");
    // Bootstrap's click class, in case a click opened this one.
    openItem.classList.remove("open");
    setExpanded(openItem, false);
    openItem = null;
  }

  function open(item) {
    clearTimeout(closeTimer);
    item.classList.remove("mf-nav-dismissed");
    if (openItem === item) { return; }
    close();
    item.classList.add("mf-nav-open");
    setExpanded(item, true);
    openItem = item;
  }

  function scheduleClose() {
    clearTimeout(closeTimer);
    closeTimer = setTimeout(close, CLOSE_DELAY);
  }

  // Esc / a click outside. The CSS opens on :hover and :focus-within too, so
  // closing has to be asserted with a class or the panel just stays put while
  // the pointer (or the focused toggle) is still inside the item.
  function dismiss() {
    var item = openItem;
    if (!item) { return; }
    close();
    var toggle = item.querySelector(".dropdown-toggle");
    // Focus first: focusin clears the flag, so set it afterwards.
    if (toggle && item.contains(document.activeElement)) { toggle.focus(); }
    item.classList.add("mf-nav-dismissed");
  }

  // After a scroll settles the pointer may already be off the menu, and
  // mouseleave has been and gone. Let the next deliberate movement decide.
  function resumeOnMove(e) {
    if (openItem && !openItem.contains(e.target)) { scheduleClose(); }
  }

  function onScroll() {
    if (!openItem) { return; }
    // Moving the page is not an intent to dismiss: hold the menu open.
    scrolling = true;
    clearTimeout(closeTimer);
    clearTimeout(settleTimer);
    settleTimer = setTimeout(function () {
      scrolling = false;
      if (!openItem) { return; }
      if (openItem.getBoundingClientRect().bottom < 0) {
        close();  // the header has left the viewport; the menu is unreachable
      } else {
        document.removeEventListener("mousemove", resumeOnMove);
        document.addEventListener("mousemove", resumeOnMove, { once: true });
      }
    }, SCROLL_SETTLE);
  }

  Array.prototype.forEach.call(menu.querySelectorAll("li.dropdown"), function (item) {
    item.addEventListener("mouseenter", function () {
      item.classList.remove("mf-nav-dismissed");
      if (desktop.matches) { open(item); }
    });

    item.addEventListener("mouseleave", function () {
      item.classList.remove("mf-nav-dismissed");
      if (desktop.matches && !scrolling) { scheduleClose(); }
    });

    // Tabbing back to a dismissed item should open it again.
    item.addEventListener("focusin", function () {
      item.classList.remove("mf-nav-dismissed");
    });

    var toggle = item.querySelector(".dropdown-toggle");
    if (!toggle) { return; }

    toggle.addEventListener("click", function (e) {
      if (!desktop.matches) { return; }  // let Bootstrap drive the mobile drawer
      e.preventDefault();
      // Bootstrap 3 binds its dropdown data-api on document, so stopping
      // propagation here keeps it from opening a second, uncoordinated panel.
      e.stopPropagation();
      if (item === openItem) { dismiss(); } else { open(item); }
    });
  });

  document.addEventListener("click", function (e) {
    if (openItem && !openItem.contains(e.target)) { dismiss(); }
  });

  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" || e.key === "Esc") { dismiss(); }
  });

  window.addEventListener("scroll", onScroll, { passive: true });

  // Crossing the breakpoint hands control back to Bootstrap (or takes it).
  if (desktop.addEventListener) {
    desktop.addEventListener("change", close);
  } else if (desktop.addListener) {
    desktop.addListener(close);
  }
})();
