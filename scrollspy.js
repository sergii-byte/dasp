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
  const SKIP_CLASS_RX = /\b(cite|ref|tag|mono|t-mono)\b/i;

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

  /* ----- Deadline highlighter — wraps "10 bd" / "24 h" / "6 months" etc. ----- */
  // Matches:  <number><opt-decimal/range><opt-spaces><unit>
  //   units: bd | wd | h(ours?) | wk(s)? / week(s)? | mo(s)? / month(s)? | yr(s)? / year(s)? | day(s)?
  // Examples covered: 10 bd · 5wd · 24 h · 24 hours · 5 wd · 6 months · 15 yr · 8–12 months · 2–3 weeks
  const DEADLINE_RX = /(\b\d+(?:[.,]\d+)?(?:[–—\-]\d+(?:[.,]\d+)?)?)(\s|&nbsp;| )?(bd|wd|hr?|hours?|wk|weeks?|mo|months?|yr|years?|days?)\b/gi;

  const initDeadlines = function () {
    const root = document.body;
    if (!root) return;
    const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {
      acceptNode: function (node) {
        if (!node.nodeValue || !DEADLINE_RX.test(node.nodeValue)) return NodeFilter.FILTER_REJECT;
        DEADLINE_RX.lastIndex = 0; // reset stateful regex
        let p = node.parentNode;
        while (p && p !== root) {
          if (SKIP_TAGS.has(p.nodeName)) return NodeFilter.FILTER_REJECT;
          if (p.classList && (p.classList.contains('deadline') || SKIP_CLASS_RX.test(p.className || ''))) return NodeFilter.FILTER_REJECT;
          p = p.parentNode;
        }
        return NodeFilter.FILTER_ACCEPT;
      }
    });
    const targets = [];
    let n;
    while ((n = walker.nextNode())) targets.push(n);
    targets.forEach(function (textNode) {
      const text = textNode.nodeValue;
      const fragment = document.createDocumentFragment();
      let lastIndex = 0;
      let m;
      DEADLINE_RX.lastIndex = 0;
      while ((m = DEADLINE_RX.exec(text)) !== null) {
        const start = m.index;
        if (start > lastIndex) fragment.appendChild(document.createTextNode(text.slice(lastIndex, start)));
        const span = document.createElement('span');
        span.className = 'deadline';
        span.textContent = m[0];
        fragment.appendChild(span);
        lastIndex = start + m[0].length;
      }
      if (lastIndex < text.length) fragment.appendChild(document.createTextNode(text.slice(lastIndex)));
      if (fragment.childNodes.length) textNode.parentNode.replaceChild(fragment, textNode);
    });
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () { initSpy(); initQuotes(); initDeadlines(); });
  } else {
    initSpy(); initQuotes(); initDeadlines();
  }
})();
