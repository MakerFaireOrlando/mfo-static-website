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
 * - SESSION-only persistence: the active theme is kept in sessionStorage, so it
 *   survives reloads + navigation within the tab but resets to the default
 *   (settings.theme_default, currently "light") on a NEW session (window
 *   closed/reopened, fresh tab). Invasion is turned on by visiting /invasion/,
 *   which sets the session value and bounces home; _includes/head.html applies it
 *   before paint. Nothing is stored long-term (no localStorage/cookies).
 * - The immersive FX scene is built lazily, only when Invasion runs.
 *
 * To retire the 2026 skin: delete the #theme-toggle button (in topnav.html) and
 * the invasion CSS/assets. This controller degrades gracefully — the sun/moon
 * mode toggle keeps working on its own.
 * --------------------------------------------------------------
 */
(function () {
  "use strict";

  var VALID = ["light", "dark", "invasion"];
  var root = document.documentElement;

  function currentTheme() {
    var t = root.getAttribute("data-theme");
    return VALID.indexOf(t) === -1 ? "light" : t;
  }
  // Session-only persistence (cleared when the tab/window closes).
  function store(key, val) { try { sessionStorage.setItem(key, val); } catch (e) { /* blocked */ } }
  function read(key) { try { return sessionStorage.getItem(key); } catch (e) { return null; } }

  // The light/dark base to return to when exiting invasion: the remembered
  // session choice if any, else the configured default (settings.theme_default,
  // resolving "system"; "invasion"/unknown collapse to "light").
  function baseDefault() {
    var def = (window.MFO_THEME || {}).defaultTheme;
    if (def === "dark") { return "dark"; }
    if (def === "system") {
      return (window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches) ? "dark" : "light";
    }
    return "light";
  }
  function baseTheme() {
    var b = read("mfo-base");
    return (b === "dark" || b === "light") ? b : baseDefault();
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
    // Each saucer runs a beam pulling up a weighted-random abductee: Makey twice
    // as likely as the others. `prev` (when given) is excluded so a repeat
    // abduction pulls in a DIFFERENT object — weighting carries to what's left.
    var art = "/assets/images/site-branding/2026/invasion/";
    var ABDUCTEES = ["Makey", "Mothman", "Bigfoot"];
    // Warm the cache so the per-loop image swap never fetches/decodes mid-flight.
    for (var p = 0; p < ABDUCTEES.length; p++) {
      var pre = new Image();
      pre.src = art + "invasion_" + ABDUCTEES[p] + ".svg";
    }
    function pickAbductee(prev) {
      var pool = ["Makey", "Makey", "Mothman", "Bigfoot"].filter(function (x) { return x !== prev; });
      return pool[Math.floor(Math.random() * pool.length)];
    }
    function craft() {
      var who = pickAbductee();
      return '<div class="mf-ufo-craft">' +
        '<div class="mf-craft-beam">' +
          '<div class="mf-abductee" data-who="' + who + '" style="background-image:url(' + art + 'invasion_' + who + '.svg)"></div>' +
        '</div>' +
        '<div class="mf-craft-body"></div>' +
      '</div>';
    }
    fx.innerHTML =
      '<div class="mf-stars mf-stars--far"></div>' +
      '<div class="mf-stars mf-stars--near"></div>' +
      '<div class="mf-ufo mf-ufo--a">' + craft() + '</div>' +
      '<div class="mf-ufo mf-ufo--b">' + craft() + '</div>' +
      '<div class="mf-ufo mf-ufo--c">' + craft() + '</div>';
    document.body.insertBefore(fx, document.body.firstChild);

    // On each abduction loop the object is invisible at the boundary (opacity 0),
    // so swap in a new, different abductee there — the next pull-in differs from
    // the last. (Listeners die with the scene when teardownInvasionFx removes it.)
    var abductees = fx.querySelectorAll(".mf-abductee");
    for (var i = 0; i < abductees.length; i++) {
      abductees[i].addEventListener("animationiteration", function () {
        var next = pickAbductee(this.getAttribute("data-who"));
        this.setAttribute("data-who", next);
        this.style.backgroundImage = "url(" + art + "invasion_" + next + ".svg)";
      });
    }

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
    if (theme === "invasion") {
      buildInvasionFx();
    } else {
      teardownInvasionFx();
      // Reset the activate tab to OFF so it's ready (lever down) next time it shows.
      var act = document.querySelector(".mf-invasion-switch--activate");
      if (act) { act.classList.remove("is-on", "is-lit"); }
    }
    syncButtons(theme);
  }

  function reducedMotion() {
    return !!(window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches);
  }

  // Leave invasion for the remembered light/dark base. Reload so the page comes
  // back fully in the base theme (drops the invasion carousel slide too); the
  // base is read from sessionStorage by head.html before paint.
  function exitInvasion() {
    store("mfo-theme", baseTheme());
    window.location.reload();
  }

  // Enter invasion and LAND ON THE HOMEPAGE, so it loads fresh with the invasion
  // carousel slide showing (head.html applies the theme before paint).
  function enterInvasion() {
    store("mfo-base", currentTheme());
    store("mfo-theme", "invasion");
    window.location.assign((window.MFO_THEME || {}).homeUrl || "/");
  }

  // One guard for both switch cinematics. Each ends in a navigation/reload, so it
  // never needs resetting — it just blocks a second click (or another control)
  // from stacking a second timer chain + duplicate navigation during the window.
  var switching = false;

  // The tabs stay DOCKED until the UFO handle is clicked. Each handle toggles
  // .is-revealed on its own tab (both tabs render on every page; CSS shows the
  // one for the active theme). Blur on close so :focus-within doesn't pin it open.
  function wireTabHandles() {
    var handles = document.querySelectorAll(".mf-invasion-tab-handle");
    for (var i = 0; i < handles.length; i++) {
      handles[i].addEventListener("click", function () {
        var tab = this.closest(".mf-invasion-switch");
        if (!tab) { return; }
        var open = tab.classList.toggle("is-revealed");
        this.setAttribute("aria-expanded", open ? "true" : "false");
        if (!open) { this.blur(); }
      });
    }
  }

  // 2026 Maker Invasion ACTIVATE tab — the light/dark-mode switch that turns
  // invasion ON (markup: _includes/invasion-activate.html). Clicking throws the
  // lever UP; when it reaches the top jaws (after the ~1.5s throw) the theme flips
  // to invasion, where the kill switch (also lever-up) seamlessly takes over.
  function wireActivateSwitch() {
    var sw = document.querySelector(".mf-invasion-switch--activate");
    var btn = document.getElementById("invasion-activate-switch");
    if (!sw || !btn) { return; }
    btn.addEventListener("click", function () {
      if (switching || currentTheme() === "invasion") { return; }   // already on / mid-throw
      if (reducedMotion()) { enterInvasion(); return; } // skip the cinematic
      switching = true;
      var overlay = document.querySelector(".mf-invasion-powerdown");
      sw.classList.add("is-on");                                          // lever rises (still dark, no sparks)
      setTimeout(function () { sw.classList.add("is-lit"); }, 1500);      // contacts meet at the top → sign + sparks
      setTimeout(function () { if (overlay) { overlay.classList.add("is-on"); } }, 2100);  // black-out under cover of the spark burst
      setTimeout(function () { enterInvasion(); }, 2350);                 // power on → land on the homepage
    });
  }

  // 2026 Maker Invasion KILL SWITCH — the Frankenstein knife switch in the side
  // tab (markup: _includes/invasion-switch.html). Throwing it powers the neon
  // scene down, slides the tab back in, then reloads into the light/dark base. The
  // tab is CSS-hidden outside invasion, so the handler just guards on the active
  // theme and runs the power-down sequence.
  function wireKillSwitch() {
    // Scope past .mf-invasion-switch--activate (which also carries the base class)
    // so this stays correct regardless of include order in topnav.html.
    var sw = document.querySelector(".mf-invasion-switch:not(.mf-invasion-switch--activate)");
    var btn = document.getElementById("invasion-kill-switch");
    if (!sw || !btn) { return; }
    var overlay = document.querySelector(".mf-invasion-powerdown");
    btn.addEventListener("click", function () {
      if (switching || currentTheme() !== "invasion") { return; }   // nothing to power down / mid-throw
      if (reducedMotion()) { exitInvasion(); return; }      // skip the cinematic
      switching = true;
      // Throw (1.5s) → the gate seats in the bottom jaws, sparks + sign cut out →
      // hold the dead switch for 3s → the tab slides itself back in → black out and
      // reload into the light/dark base.
      sw.classList.add("is-off");                           // throw lever + kill arc/sign
      setTimeout(function () { sw.classList.add("is-retracting"); }, 4500);  // 1.5s throw + 3s pause → slide tab in
      setTimeout(function () { if (overlay) { overlay.classList.add("is-on"); } }, 5000);  // black out once it's gone
      setTimeout(function () { exitInvasion(); }, 5250);    // reload into the base theme under cover
    });
  }

  function init() {
    applyTheme(currentTheme());

    // Light/dark mode toggle (persisted for the session). From invasion, the
    // sun/moon returns to the light/dark base.
    var mode = document.getElementById("theme-mode-toggle");
    if (mode) {
      mode.addEventListener("click", function () {
        var next = currentTheme() === "light" ? "dark" : "light";
        store("mfo-base", next);
        applyTheme(next);
        store("mfo-theme", next);
      });
    }

    // Invasion on/off. The light/dark base lives in sessionStorage('mfo-base').
    var ufo = document.getElementById("theme-toggle");
    if (ufo) {
      ufo.addEventListener("click", function () {
        var next;
        if (currentTheme() === "invasion") {
          next = baseTheme();
        } else {
          store("mfo-base", currentTheme());   // remember light/dark to restore later
          next = "invasion";
        }
        applyTheme(next);
        store("mfo-theme", next);
      });
    }

    wireKillSwitch();
    wireActivateSwitch();
    wireTabHandles();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
