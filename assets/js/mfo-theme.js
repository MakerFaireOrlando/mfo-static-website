/*
 * Maker Faire Orlando — Theme controller
 * --------------------------------------------------------------
 * Two header controls drive a single <html data-theme="..."> value:
 *
 *   • #theme-mode-toggle  (sun/moon) — permanent light <-> dark switch.
 *   • #theme-toggle       (UFO)      — TEMPORARY: toggles the 2026 "Maker
 *                                      Invasion" neon skin on/off.
 *
 * Themes: "light" | "dark" | "invasion" (invasion is dark-based).
 *
 * - The chosen theme is written to localStorage('mfo-theme'); the inline script
 *   in _includes/head.html applies it BEFORE paint (no flash) and seeds the
 *   first-visit default from the OS prefers-color-scheme. localStorage('mfo-base')
 *   remembers the light/dark choice so turning Invasion OFF returns to it.
 * - The immersive FX scene is built lazily, only the first time Invasion runs.
 *
 * To retire the 2026 skin: delete the #theme-toggle button (in topnav.html) and
 * the invasion CSS/assets. This controller degrades gracefully — the sun/moon
 * mode toggle keeps working on its own.
 * --------------------------------------------------------------
 */
(function () {
  "use strict";

  var THEME_KEY = "mfo-theme";
  var BASE_KEY  = "mfo-base";   // last light/dark choice (to restore after invasion)
  var VALID = ["light", "dark", "invasion"];

  var root = document.documentElement;

  function currentTheme() {
    var t = root.getAttribute("data-theme");
    return VALID.indexOf(t) === -1 ? "light" : t;
  }
  function store(key, val) {
    try { localStorage.setItem(key, val); } catch (e) { /* private mode */ }
  }
  function read(key) {
    try { return localStorage.getItem(key); } catch (e) { return null; }
  }

  // ---- Immersive FX scene -------------------------------------------------
  // Read a numeric setting from the build-time global, falling back to `dflt`.
  function fxSetting(key, dflt) {
    var v = (window.MFO_THEME || {})[key];
    return (typeof v === "number" && isFinite(v)) ? v : dflt;
  }

  var fxTimers = [];
  function clearFxTimers() {
    for (var i = 0; i < fxTimers.length; i++) { clearTimeout(fxTimers[i]); }
    fxTimers = [];
  }
  // Remove the scene + cancel any pending wind-down. Called when leaving invasion
  // so re-entering rebuilds a fresh scene (and stale timers can't mutate it).
  function teardownInvasionFx() {
    clearFxTimers();
    var existing = document.querySelector(".mf-invasion-fx");
    if (existing && existing.parentNode) { existing.parentNode.removeChild(existing); }
  }

  function fadeOutSaucers(fx) {
    fx.classList.add("mf-invasion-fx--calm");            // CSS fades the saucers out
    var remove = function () {
      var ufos = fx.querySelectorAll(".mf-ufo");          // remove them (stops their animations)
      for (var i = 0; i < ufos.length; i++) {
        if (ufos[i].parentNode) { ufos[i].parentNode.removeChild(ufos[i]); }
      }
      fx.classList.add("mf-invasion-fx--ambient");        // drop the layer behind the content
    };
    var first = fx.querySelector(".mf-ufo");
    if (!first) { remove(); return; }
    // Drive removal off the fade's transitionend (decoupled from the CSS duration),
    // with a timed fallback in case transitionend never fires.
    var done = false;
    var finish = function () { if (done) { return; } done = true; remove(); };
    first.addEventListener("transitionend", finish);
    fxTimers.push(setTimeout(finish, 2500));
  }

  // Build the scene fresh on each invasion activation (page load or toggle-on).
  function buildInvasionFx() {
    // Only build on pages that have the header nav — a bare layout without it
    // (e.g. the schedule app) would show a scene the visitor can't turn off.
    // Gating on the nav (not the UFO button) means /invasion/ still renders the
    // full scene even when the UFO icon is hidden via settings.
    if (!document.getElementById("slide-nav")) { return; }
    teardownInvasionFx();   // clear any prior scene/timers so a re-toggle restarts cleanly
    var fx = document.createElement("div");
    fx.className = "mf-invasion-fx";
    fx.setAttribute("aria-hidden", "true");
    fx.innerHTML =
      '<div class="mf-stars mf-stars--far"></div>' +
      '<div class="mf-stars mf-stars--near"></div>' +
      '<div class="mf-ufo mf-ufo--a"><div class="mf-ufo-craft"></div></div>' +
      '<div class="mf-ufo mf-ufo--b"><div class="mf-ufo-craft"><div class="mf-makey"></div></div></div>' +
      '<div class="mf-ufo mf-ufo--c"><div class="mf-ufo-craft"></div></div>';
    document.body.insertBefore(fx, document.body.firstChild);

    // Two-phase wind-down so the scene is a fun burst, then the page reads
    // cleanly (a fresh page load — or toggle-off/on — rebuilds it):
    //   phase A @ d1s        — stop looping: on-screen UFOs finish, none re-enter.
    //   phase B @ (d1+d2)s   — fade the saucers out + remove them, then drop the
    //                          FX layer behind the content.
    // d1 = invasionFxSeconds (0 = run indefinitely); d2 = invasionFxFadeoutSeconds.
    var d1 = fxSetting("invasionFxSeconds", 10);
    var d2 = Math.max(fxSetting("invasionFxFadeoutSeconds", 10), 0);
    if (d1 > 0) {
      if (d2 > 0) {   // a 0 fadeout means "fade immediately at d1" — skip the no-op phase A
        fxTimers.push(setTimeout(function () { fx.classList.add("mf-invasion-fx--noloop"); }, d1 * 1000));
      }
      fxTimers.push(setTimeout(function () { fadeOutSaucers(fx); }, (d1 + d2) * 1000));
    }
  }

  function syncButtons(theme) {
    var mode = document.getElementById("theme-mode-toggle");
    if (mode) {
      var goingDark = theme === "light";   // light → click goes to dark
      mode.setAttribute("aria-label", goingDark ? "Switch to dark mode" : "Switch to light mode");
      mode.setAttribute("title", goingDark ? "Switch to dark mode" : "Switch to light mode");
      mode.setAttribute("aria-pressed", theme === "light" ? "false" : "true");
    }
    var ufo = document.getElementById("theme-toggle");
    if (ufo) {
      var on = theme === "invasion";
      ufo.setAttribute("aria-pressed", on ? "true" : "false");
      ufo.setAttribute("aria-label", on ? "Exit Maker Invasion mode" : "Activate Maker Invasion mode");
      ufo.setAttribute("title", on ? "Exit Maker Invasion mode" : "Activate Maker Invasion mode");
    }
  }

  function applyTheme(theme) {
    root.setAttribute("data-theme", theme);
    if (theme === "invasion") { buildInvasionFx(); } else { teardownInvasionFx(); }
    syncButtons(theme);
  }

  function init() {
    applyTheme(currentTheme());

    // Light/dark mode toggle. From invasion, the sun/moon returns to plain light.
    var mode = document.getElementById("theme-mode-toggle");
    if (mode) {
      mode.addEventListener("click", function () {
        var next = currentTheme() === "light" ? "dark" : "light";
        store(BASE_KEY, next);
        applyTheme(next);
        store(THEME_KEY, next);
      });
    }

    // Invasion on/off. Remembers the light/dark base to come back to.
    var ufo = document.getElementById("theme-toggle");
    if (ufo) {
      ufo.addEventListener("click", function () {
        var next;
        if (currentTheme() === "invasion") {
          var base = read(BASE_KEY);
          next = (base === "dark" || base === "light") ? base : "light";
        } else {
          store(BASE_KEY, currentTheme());   // remember light/dark to restore later
          next = "invasion";
        }
        applyTheme(next);
        store(THEME_KEY, next);
      });
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
