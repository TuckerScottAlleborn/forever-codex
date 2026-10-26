// Forever Codex: behaviour shared by every page. The sticky bar shows reading progress along
// its lower edge and fades whichever end of its links is scrolled out of view.
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
})();
