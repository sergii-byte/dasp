/* =========================================================
   Sidebar scroll-spy — highlights the sidebar link for the
   section currently in the upper viewport. Adds .is-active.
   Pure JS, no dependencies. Skips if no .sidebar present.
   ========================================================= */
(function () {
  if (typeof window === 'undefined') return;

  const initSpy = function () {
    const sidebar = document.querySelector('.sidebar');
    if (!sidebar) return;

    // Map sidebar links to their target sections.
    const linkToSection = new Map();
    sidebar.querySelectorAll('a[href^="#"]').forEach(function (a) {
      const id = a.getAttribute('href').slice(1);
      if (!id) return;
      const section = document.getElementById(id);
      if (section) linkToSection.set(a, section);
    });
    if (!linkToSection.size) return;

    const links = Array.from(linkToSection.keys());

    // IntersectionObserver-based spy — fires when section header crosses the
    // viewport top + 90px offset (just below the sticky topbar).
    const visible = new Map();
    const obs = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (e) {
          visible.set(e.target, e.intersectionRatio);
        });
        // Pick the first section whose intersectionRatio > 0, in DOM order.
        let activeLink = null;
        for (let i = 0; i < links.length; i++) {
          const sec = linkToSection.get(links[i]);
          if (visible.get(sec) > 0) {
            activeLink = links[i];
            break;
          }
        }
        if (activeLink) {
          links.forEach(function (l) {
            l.classList.toggle('is-active', l === activeLink);
            if (l === activeLink) l.setAttribute('aria-current', 'true');
            else l.removeAttribute('aria-current');
          });
        }
      },
      {
        rootMargin: '-90px 0px -60% 0px', // upper band of viewport
        threshold: [0, 0.01, 0.5, 1],
      }
    );

    linkToSection.forEach(function (sec) { obs.observe(sec); });
  };

  /* ----- Smart-quote text walker — converts straight " ' into curly  ' ----- */
  const SKIP_TAGS = new Set([
    'CODE', 'PRE', 'KBD', 'SAMP', 'SCRIPT', 'STYLE', 'TEXTAREA',
    'INPUT', 'OPTION', 'SELECT'
  ]);
  const SKIP_CLASS_RX = /\b(cite|ref|tag|mono|t-mono|num)\b/i;

  const curlyQuote = function (str) {
    // Double quotes: opening if preceded by start/space/punct, closing otherwise
    str = str.replace(/(^|[\s\(\[\{])"/g, '$1“');
    str = str.replace(/"/g, '”');
    // Single quotes: handle apostrophes (don't / it's) + opening + closing
    str = str.replace(/(\w)'(\w)/g, '$1’$2');                // apostrophe inside word
    str = str.replace(/(^|[\s\(\[\{])'/g, '$1‘');            // opening
    str = str.replace(/'/g, '’');                              // closing / trailing
    return str;
  };

  const initQuotes = function () {
    const root = document.body;
    if (!root) return;
    const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {
      acceptNode: function (node) {
        if (!node.nodeValue || !/['"]/.test(node.nodeValue)) return NodeFilter.FILTER_REJECT;
        let p = node.parentNode;
        while (p && p !== root) {
          if (SKIP_TAGS.has(p.nodeName)) return NodeFilter.FILTER_REJECT;
          if (p.classList && SKIP_CLASS_RX.test(p.className || '')) return NodeFilter.FILTER_REJECT;
          p = p.parentNode;
        }
        return NodeFilter.FILTER_ACCEPT;
      }
    });
    const updates = [];
    let n;
    while ((n = walker.nextNode())) updates.push(n);
    updates.forEach(function (n) { n.nodeValue = curlyQuote(n.nodeValue); });
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () { initSpy(); initQuotes(); });
  } else {
    initSpy(); initQuotes();
  }
})();
