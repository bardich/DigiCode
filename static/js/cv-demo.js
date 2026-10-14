(() => {
  const header = document.querySelector('[data-demo-header]');
  const nav = document.querySelector('.demo-nav');
  const toggle = document.querySelector('[data-demo-menu-toggle]');
  const mobile = matchMedia('(max-width:1100px)');
  if (!header || !nav || !toggle) return;
  function closeMenu(focus = false) {
    if (mobile.matches) nav.hidden = true;
    toggle.setAttribute('aria-expanded', 'false');
    if (focus) toggle.focus();
  }
  function adaptMenu() {
    toggle.hidden = !mobile.matches;
    nav.classList.toggle('js-mobile', mobile.matches);
    nav.hidden = mobile.matches;
    toggle.setAttribute('aria-expanded', 'false');
  }
  adaptMenu();
  mobile.addEventListener('change', adaptMenu);
  toggle.addEventListener('click', () => {
    const open = toggle.getAttribute('aria-expanded') === 'true';
    nav.hidden = open;
    toggle.setAttribute('aria-expanded', String(!open));
    if (!open) nav.querySelector('a').focus();
  });
  header.addEventListener('keydown', event => {
    if (event.key === 'Escape') closeMenu(true);
  });
  document.addEventListener('click', event => { if (!header.contains(event.target)) closeMenu(); });
  header.addEventListener('focusout', () => {
    setTimeout(() => { if (!header.contains(document.activeElement)) closeMenu(); }, 0);
  });
  const links = [...nav.querySelectorAll('a[href^="#"]')];
  const sections = links.map(link => document.querySelector(link.getAttribute('href'))).filter(Boolean);
  function highlight(id) {
    links.forEach(link => {
      if (link.hash === '#' + id) link.setAttribute('aria-current', 'location');
      else link.removeAttribute('aria-current');
    });
  }
  links.forEach(link => link.addEventListener('click', () => {
    closeMenu();
    highlight(link.hash.slice(1));
    // Keep keyboard focus on the destination after closing the mobile menu.
    const destination = document.querySelector(link.hash);
    destination.setAttribute('tabindex', '-1');
    destination.focus({preventScroll:true});
  }));
  let queued = false;
  function updateSection() {
    queued = false;
    const edge = header.getBoundingClientRect().height + 90;
    let active = sections[0];
    sections.forEach(section => { if (section.getBoundingClientRect().top <= edge) active = section; });
    if (active) highlight(active.id);
  }
  addEventListener('scroll', () => {
    if (!queued) { queued = true; requestAnimationFrame(updateSection); }
  }, {passive:true});
  updateSection();
  const motion = matchMedia('(prefers-reduced-motion: reduce)');
  if ('IntersectionObserver' in window && !motion.matches) {
    const observer = new IntersectionObserver(entries => entries.forEach(entry => {
      if (entry.isIntersecting) { entry.target.classList.add('is-visible'); observer.unobserve(entry.target); }
    }), {threshold:0.08});
    document.querySelectorAll('[data-demo-reveal]').forEach(element => {
      if (element.getBoundingClientRect().top > innerHeight) {
        element.classList.add('demo-reveal-pending'); observer.observe(element);
      }
    });
    motion.addEventListener('change', () => {
      if (motion.matches) {
        observer.disconnect();
        document.querySelectorAll('.demo-reveal-pending').forEach(el => el.classList.add('is-visible'));
      }
    });
  }
})();
