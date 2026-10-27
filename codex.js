// Forever Codex: behaviour shared by every page. The sticky bar shows reading progress along
// its lower edge, fades whichever end of its links is scrolled out of view, and keeps the
// current section's link in view when it can't show them all.
(function () {
  var d = document, bar = d.querySelector(".bar"), barIn = bar && bar.querySelector(".bar-in");
  if (!barIn) return;
  var ticking = false;
  var progress = function () {
    ticking = false;
    var h = d.documentElement.scrollHeight - window.innerHeight;
    bar.style.setProperty("--p", h > 0 ? Math.min(1, Math.max(0, window.scrollY / h)).toFixed(4) : "0");
  };
  window.addEventListener("scroll", function () { if (!ticking) { ticking = true; requestAnimationFrame(progress); } }, { passive: true });
  window.addEventListener("resize", progress);
  progress();
  var edges = function () {
    var max = barIn.scrollWidth - barIn.clientWidth;
    barIn.classList.toggle("fade-l", barIn.scrollLeft > 2);
    barIn.classList.toggle("fade-r", max > 2 && barIn.scrollLeft < max - 2);
  };
  barIn.addEventListener("scroll", edges, { passive: true });
  window.addEventListener("resize", edges);
  edges();
  // each book marks its current link "active"; centre that link whenever it changes
  var still = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var follow = function (a) {
    if (barIn.scrollWidth <= barIn.clientWidth) return;
    barIn.scrollTo({ left: Math.max(0, a.offsetLeft - (barIn.clientWidth - a.offsetWidth) / 2), behavior: still ? "auto" : "smooth" });
  };
  if ("MutationObserver" in window) {
    new MutationObserver(function (ms) {
      for (var i = 0; i < ms.length; i++) {
        var t = ms[i].target;
        if (t !== barIn && t.classList.contains("active")) { follow(t); return; }
      }
    }).observe(barIn, { subtree: true, attributes: true, attributeFilter: ["class"] });
  }
})();
