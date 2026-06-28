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

  // ---- Immersive FX scene (built once, on first invasion activation) ----
  var fxBuilt = false;
  function buildInvasionFx() {
    if (fxBuilt || document.querySelector(".mf-invasion-fx")) { fxBuilt = true; return; }
    // Only build the scene on pages that have the header nav — a bare layout
    // without it (e.g. the schedule app) would show an immersive scene the
    // visitor has no way to turn off. Gating on the nav (not the UFO button)
    // means /invasion/ still renders the full scene even when the UFO icon is
    // hidden via settings.theme_invasion_icon. The theme colors always apply.
    if (!document.getElementById("slide-nav")) { return; }
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
    fxBuilt = true;
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
    if (theme === "invasion") { buildInvasionFx(); }
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
