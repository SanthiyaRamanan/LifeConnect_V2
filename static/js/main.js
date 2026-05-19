// ── LifeConnect Main JS ────────────────────────────────────────────────────

// Flash message auto-dismiss + close button
document.querySelectorAll('.flash').forEach(flash => {
  const close = flash.querySelector('.flash-close');
  if (close) close.addEventListener('click', () => flash.remove());
  setTimeout(() => flash && flash.remove(), 5000);
});

// Hamburger menu toggle
const hamburger = document.getElementById('hamburger');
const navLinks  = document.querySelector('.nav-links');
if (hamburger) {
  hamburger.addEventListener('click', () => navLinks.classList.toggle('open'));
}

// Animated counter for stat numbers
function animateCounter(el) {
  const target = parseInt(el.dataset.target, 10);
  if (isNaN(target) || target === 0) { el.textContent = '0'; return; }
  const duration = 1400;
  const step     = Math.ceil(target / (duration / 16));
  let current    = 0;
  const timer = setInterval(() => {
    current += step;
    if (current >= target) { current = target; clearInterval(timer); }
    el.textContent = current.toLocaleString();
  }, 16);
}

const statNums = document.querySelectorAll('.stat-num[data-target]');
if (statNums.length) {
  const observer = new IntersectionObserver(entries => {
    entries.forEach(e => { if (e.isIntersecting) { animateCounter(e.target); observer.unobserve(e.target); } });
  }, { threshold: 0.4 });
  statNums.forEach(el => observer.observe(el));
}

// Confirm before critical actions
document.querySelectorAll('[data-confirm]').forEach(el => {
  el.addEventListener('click', e => {
    if (!confirm(el.dataset.confirm)) e.preventDefault();
  });
});

// Active nav link highlight
const path = window.location.pathname;
document.querySelectorAll('.nav-links a').forEach(a => {
  if (a.getAttribute('href') === path) a.style.color = '#ff6b81';
});
