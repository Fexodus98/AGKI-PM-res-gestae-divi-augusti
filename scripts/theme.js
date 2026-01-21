(() => {
  const storageKey = 'theme';
  const root = document.documentElement;

  const getPreferredTheme = () => {
    const stored = localStorage.getItem(storageKey);
    if (stored === 'light' || stored === 'dark') return stored;
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  };

  const applyTheme = (theme) => {
    root.setAttribute('data-theme', theme);
    const btn = document.querySelector('.theme-toggle');
    if (btn) btn.textContent = theme === 'dark' ? 'Light' : 'Dark';
  };

  const setupToggle = () => {
    const btn = document.querySelector('.theme-toggle');
    if (!btn) return;
    btn.addEventListener('click', () => {
      const next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      localStorage.setItem(storageKey, next);
      applyTheme(next);
    });
  };

  const init = () => {
    applyTheme(getPreferredTheme());
    setupToggle();
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
