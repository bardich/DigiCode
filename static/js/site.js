(() => {
  const header = document.querySelector('.site-header');
  const toggle = document.querySelector('#menu-toggle');
  const nav = document.querySelector('#mobile-nav');
  const mobile = matchMedia('(max-width:1000px)');
  if (header && toggle && nav) {
    toggle.hidden = !mobile.matches;
    nav.hidden = true;
    function closeMenu(returnFocus = false) {
      nav.hidden = true;
      toggle.setAttribute('aria-expanded', 'false');
      if (returnFocus) toggle.focus();
    }
    toggle.addEventListener('click', () => {
      const open = toggle.getAttribute('aria-expanded') === 'true';
      nav.hidden = open;
      toggle.setAttribute('aria-expanded', String(!open));
      if (!open) nav.querySelector('a')?.focus();
    });
    header.addEventListener('keydown', event => {
      if (event.key === 'Escape') closeMenu(true);
    });
    header.addEventListener('focusout', () => {
      setTimeout(() => { if (!header.contains(document.activeElement)) closeMenu(); }, 0);
    });
    nav.addEventListener('click', event => { if (event.target.closest('a')) closeMenu(); });
    document.addEventListener('click', event => { if (!header.contains(event.target)) closeMenu(); });
    mobile.addEventListener('change', () => { toggle.hidden = !mobile.matches; closeMenu(); });
    const updateHeader = () => header.classList.toggle('scrolled', scrollY > 16);
    updateHeader();
    addEventListener('scroll', updateHeader, {passive:true});
  }
  const motion = matchMedia('(prefers-reduced-motion: reduce)');
  if ('IntersectionObserver' in window && !motion.matches) {
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          observer.unobserve(entry.target);
        }
      });
    }, {threshold:0.08});
    document.querySelectorAll('[data-reveal]').forEach(element => {
      // Leave initially visible content painted; enhance only below the fold.
      if (element.getBoundingClientRect().top > innerHeight) {
        element.classList.add('reveal-pending');
        observer.observe(element);
      }
    });
    motion.addEventListener('change', () => {
      if (motion.matches) {
        observer.disconnect();
        document.querySelectorAll('.reveal-pending').forEach(el => el.classList.add('is-visible'));
      }
    });
  }
  const alert = document.querySelector('.form-alert, .success-message');
  if (alert) {alert.setAttribute('tabindex','-1'); alert.focus({preventScroll:true});}
})();
