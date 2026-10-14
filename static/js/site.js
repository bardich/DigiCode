(() => {
  const header = document.querySelector('.site-header');
  const toggle = document.querySelector('#menu-toggle');
  const nav = document.querySelector('#mobile-nav');
  const mobile = matchMedia('(max-width:1180px)');
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
  document.querySelectorAll('[data-showcase]').forEach(showcase => {
    const slides = [...showcase.querySelectorAll('[data-slide]')];
    const controls = showcase.querySelector('[data-showcase-controls]');
    if (slides.length < 2 || !controls) return;
    const dots = [...showcase.querySelectorAll('[data-slide-to]')];
    const pause = showcase.querySelector('[data-slide-pause]');
    const playIcon = showcase.querySelector('[data-play-icon]');
    const announcement = showcase.querySelector('[data-slide-announcement]');
    const counter = showcase.querySelector('[data-slide-counter]');
    let current = 0;
    let paused = motion.matches;
    let hovered = false;
    let focused = false;
    let visible = true;
    let timer;
    let transitionTimer;
    const interval = 6500;
    controls.hidden = false;

    function updatePause() {
      pause.setAttribute('aria-pressed', String(paused));
      pause.setAttribute('aria-label', paused ? showcase.dataset.playLabel : showcase.dataset.pauseLabel);
      playIcon.textContent = paused ? '▷' : 'Ⅱ';
      showcase.querySelector('.showcase-stage').setAttribute('aria-live', paused ? 'polite' : 'off');
    }
    function schedule() {
      clearTimeout(timer);
      if (!paused && !hovered && !focused && visible && !document.hidden) {
        timer = setTimeout(() => show(current + 1, false), interval);
      }
    }
    function show(index, manual = true) {
      const next = (index + slides.length) % slides.length;
      if (manual) paused = true;
      clearTimeout(transitionTimer);
      slides.forEach((slide, i) => {
        slide.classList.remove('is-entering', 'is-outgoing');
        slide.hidden = i !== current;
        slide.inert = i !== current;
      });
      if (next !== current) {
        const previous = slides[current];
        previous.classList.remove('is-active');
        previous.classList.add('is-outgoing');
        previous.inert = true;
        current = next;
        const active = slides[current];
        active.hidden = false;
        active.inert = false;
        active.classList.add('is-active', 'is-entering');
        transitionTimer = setTimeout(() => {
          previous.hidden = true;
          previous.classList.remove('is-outgoing');
          active.classList.remove('is-entering');
        }, motion.matches ? 0 : 560);
      }
      dots.forEach((dot, i) => dot.setAttribute('aria-pressed', String(i === current)));
      counter.textContent = `${String(current + 1).padStart(2, '0')} / ${String(slides.length).padStart(2, '0')}`;
      if (manual) announcement.textContent = slides[current].querySelector('.showcase-project-caption strong').textContent;
      updatePause();
      schedule();
    }
    dots.forEach((dot, i) => dot.addEventListener('click', () => show(i)));
    showcase.querySelector('[data-slide-prev]').addEventListener('click', () => show(current - 1));
    showcase.querySelector('[data-slide-next]').addEventListener('click', () => show(current + 1));
    pause.addEventListener('click', () => { paused = !paused; updatePause(); schedule(); });
    showcase.addEventListener('mouseenter', () => { hovered = true; schedule(); });
    showcase.addEventListener('mouseleave', () => { hovered = false; schedule(); });
    // Focus stops rotation until the visitor explicitly resumes it.
    showcase.addEventListener('focusin', event => {
      focused = true;
      if (event.target !== pause) paused = true;
      updatePause(); schedule();
    });
    showcase.addEventListener('focusout', () => {
      setTimeout(() => { focused = showcase.contains(document.activeElement); schedule(); }, 0);
    });
    controls.addEventListener('keydown', event => {
      if (!['ArrowLeft', 'ArrowRight'].includes(event.key)) return;
      const rtl = document.documentElement.dir === 'rtl';
      const forward = event.key === (rtl ? 'ArrowLeft' : 'ArrowRight');
      event.preventDefault();
      show(current + (forward ? 1 : -1));
      dots[current].focus();
    });
    document.addEventListener('visibilitychange', schedule);
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(entries => {
        visible = entries[0].isIntersecting;
        schedule();
      }, {threshold:0.15}).observe(showcase);
    }
    motion.addEventListener('change', () => {
      if (motion.matches) paused = true;
      updatePause(); schedule();
    });
    slides.forEach((slide, i) => { slide.inert = i !== current; });
    updatePause(); schedule();
  });
  const alert = document.querySelector('.form-alert, .success-message');
  if (alert) {alert.setAttribute('tabindex','-1'); alert.focus({preventScroll:true});}
})();
