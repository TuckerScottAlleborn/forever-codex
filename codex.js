// Forever Codex: behaviour shared by every page. The masthead's More menu closes like a menu should,
// and its links into the current page light up with their section. The sticky bar shows reading
// progress along its lower edge, fades whichever end of its links is scrolled out of view, and
// keeps the current section's link in view when it can't show them all.

// The masthead's More menu closes on a click outside it, on Escape, and once a section is picked.
(function () {
  var d = document, more = d.querySelector(".mast-more");
  if (!more) return;
  var sum = more.querySelector("summary");
  d.addEventListener("click", function (e) { if (more.open && !more.contains(e.target)) more.open = false; });
  d.addEventListener("keydown", function (e) { if (e.key === "Escape" && more.open) { more.open = false; sum.focus(); } });
  more.addEventListener("click", function (e) { if (e.target.closest(".mast-menu a")) more.open = false; });
})();
// Masthead links into this page's own sections (the world book's professions, dungeons and PvP)
// light up while their section is in view.
(function () {
  var d = document, path = function (p) { return p.replace(/index\.html$/, ""); }, here = path(location.pathname);
  var links = [].slice.call(d.querySelectorAll(".mast-books > a[data-spy]")).filter(function (a) { return path(a.pathname) === here; });
  if (!links.length || !("IntersectionObserver" in window)) return;
  var byId = {};
  links.forEach(function (a) { a.dataset.spy.split(" ").forEach(function (id) { byId[id] = a; }); });
  var io = new IntersectionObserver(function (es) {
    es.forEach(function (en) {
      if (!en.isIntersecting) return;
      var a = byId[en.target.id] || null;
      links.forEach(function (l) { if (l === a) l.setAttribute("aria-current", "location"); else l.removeAttribute("aria-current"); });
    });
  }, { rootMargin: "-40% 0px -55% 0px" });
  d.querySelectorAll("#top, main > section[id], main .sub-h[id]").forEach(function (s) { io.observe(s); });
})();
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
