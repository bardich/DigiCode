(() => {
  const payload = document.getElementById('marketing-config');
  const banner = document.getElementById('marketing-consent');
  if (!payload || !banner) return;
  let config;
  try { config = JSON.parse(payload.textContent); } catch { return; }
  if (!config.fingerprint || !Array.isArray(config.snippets)) return;
  const key = 'digicode.marketing-consent.v1';
  const duration = 180 * 24 * 60 * 60 * 1000;
  const preferences = document.querySelector('[data-marketing-preferences]');
  let choice = null;
  let started = false;
  let stopped = false;
  let returnFocus = false;
  try {
    const stored = JSON.parse(localStorage.getItem(key));
    if (stored && stored.fingerprint === config.fingerprint &&
        ['accepted', 'rejected'].includes(stored.choice) &&
        Number.isFinite(stored.expires) && stored.expires > Date.now() &&
        stored.expires <= Date.now() + duration + 60000) choice = stored.choice;
  } catch { /* Storage refusal means an unknown choice, never implicit consent. */ }
  function save(value) {
    choice = value;
    try { localStorage.setItem(key, JSON.stringify({choice:value, fingerprint:config.fingerprint, expires:Date.now() + duration})); }
    catch { /* The current page still respects the explicit visitor choice. */ }
  }
  function insert(script, position) {
    if (position === 'body_start') {
      const anchor = [...document.body.childNodes].find(node => node.nodeType === 8 && node.textContent.trim() === 'digicode-marketing-body-start');
      document.body.insertBefore(script, anchor || document.body.firstChild);
    } else {
      document.head.appendChild(script);
    }
  }
  function loadScript(definition, position) {
    return new Promise(resolve => {
      if (stopped || choice !== 'accepted') { resolve(); return; }
      const script = document.createElement('script');
      const attrs = definition.attributes || {};
      for (const [name, value] of Object.entries(attrs)) script.setAttribute(name, value === null ? '' : value);
      script.textContent = definition.text || '';
      const external = Object.hasOwn(attrs, 'src');
      const module = attrs.type === 'module';
      const asynchronous = Object.hasOwn(attrs, 'async');
      // Dynamic classic scripts default to async. Restore sequential execution
      // unless the pasted snippet explicitly opted into async loading.
      if (external && !asynchronous) script.async = false;
      const waiting = (external || module) && !asynchronous;
      let timer;
      const finish = () => { clearTimeout(timer); script.onload = null; script.onerror = null; resolve(); };
      if (waiting) {
        script.onload = finish;
        script.onerror = finish;
        // A stalled vendor cannot indefinitely block subsequent independent tags.
        timer = setTimeout(finish, 8000);
      }
      try { insert(script, position); } catch { finish(); return; }
      if (!waiting) finish();
    });
  }
  async function activate() {
    if (started || choice !== 'accepted') return;
    started = true;
    for (const snippet of config.snippets) {
      for (const script of snippet.scripts || []) {
        if (stopped || choice !== 'accepted') return;
        await loadScript(script, snippet.position);
      }
    }
  }
  function closeBanner() {
    banner.hidden = true;
    if (returnFocus) preferences?.focus({preventScroll:true});
    returnFocus = false;
  }
  banner.querySelectorAll('[data-marketing-choice]').forEach(button => {
    button.addEventListener('click', () => {
      const value = button.dataset.marketingChoice;
      if (!['accepted', 'rejected'].includes(value)) return;
      save(value);
      closeBanner();
      if (value === 'accepted') activate();
      else {
        stopped = true;
        if (started) location.reload();
      }
    });
  });
  if (preferences) {
    preferences.hidden = false;
    preferences.addEventListener('click', () => {
      returnFocus = true;
      banner.hidden = false;
      banner.querySelector('button').focus({preventScroll:true});
    });
  }
  banner.hidden = choice !== null;
  if (choice === 'accepted') activate();
})();
