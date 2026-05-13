// NAV SCROLL
const navbar = document.getElementById('navbar');
window.addEventListener('scroll', () => {
  navbar.classList.toggle('scrolled', window.scrollY > 50);
});

// HAMBURGER
const hamburger = document.getElementById('hamburger');
const navLinks = document.querySelector('.nav-links');
hamburger.addEventListener('click', () => {
  navLinks.classList.toggle('open');
});
document.querySelectorAll('.nav-links a').forEach(a => {
  a.addEventListener('click', () => navLinks.classList.remove('open'));
});

// PORTFOLIO FILTER
const tabBtns = document.querySelectorAll('.tab-btn');
const portfolioItems = document.querySelectorAll('.portfolio-item');
tabBtns.forEach(btn => {
  btn.addEventListener('click', () => {
    tabBtns.forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    const filter = btn.dataset.filter;
    portfolioItems.forEach(item => {
      if (filter === 'all' || item.dataset.category === filter) {
        item.classList.remove('hidden');
      } else {
        item.classList.add('hidden');
      }
    });
  });
});

// SCROLL REVEAL
const reveals = document.querySelectorAll('.stats, .about-grid, .service-card, .why-card, .testi-card, .portfolio-item, .contact-grid');
reveals.forEach(el => el.classList.add('reveal'));

const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry, i) => {
    if (entry.isIntersecting) {
      setTimeout(() => entry.target.classList.add('visible'), i * 80);
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.1 });

document.querySelectorAll('.reveal').forEach(el => observer.observe(el));

// CONTACT FORM — redirect to WhatsApp
document.getElementById('contactForm').addEventListener('submit', function(e) {
  e.preventDefault();
  const name = this.querySelector('input[type="text"]').value;
  const service = this.querySelector('select').value;
  const msg = this.querySelector('textarea').value;
  const text = `Halo N&N Capture! Nama saya *${name}*.\nLayanan: *${service}*\nPesan: ${msg}`;
  const url = `https://wa.me/6285709799920?text=${encodeURIComponent(text)}`;
  window.open(url, '_blank');
});
// TESTIMONIAL FORM
const testimonialForm = document.getElementById('testimonialForm');

if (testimonialForm) {

  testimonialForm.addEventListener('submit', function(e) {

    const name = this
      .querySelector('input[name="name"]')
      .value
      .trim();

    const message = this
      .querySelector('textarea[name="message"]')
      .value
      .trim();

    if (name.length < 2) {

      e.preventDefault();

      alert('Nama terlalu pendek');

      return;
    }

    if (message.length < 10) {

      e.preventDefault();

      alert('Testimonial terlalu pendek');

      return;
    }

  });

}
// PORTFOLIO DRAG SCROLL ONLY

document.querySelectorAll('.portfolio-slides').forEach(slides => {

  let isDown = false;

  let startX;

  let scrollLeft;

  // DESKTOP DRAG

  slides.addEventListener('mousedown', (e) => {

    isDown = true;

    slides.classList.add('dragging');

    startX = e.pageX - slides.offsetLeft;

    scrollLeft = slides.scrollLeft;

  });

  slides.addEventListener('mouseleave', () => {

    isDown = false;

    slides.classList.remove('dragging');

  });

  slides.addEventListener('mouseup', () => {

    isDown = false;

    slides.classList.remove('dragging');

  });

  slides.addEventListener('mousemove', (e) => {

    if (!isDown) return;

    e.preventDefault();

    const x = e.pageX - slides.offsetLeft;

    const walk = (x - startX) * 1.5;

    slides.scrollLeft = scrollLeft - walk;

  });

  // MOBILE TOUCH SUPPORT

  let touchStartX = 0;

  let touchScrollLeft = 0;

  slides.addEventListener('touchstart', (e) => {

    touchStartX = e.touches[0].pageX;

    touchScrollLeft = slides.scrollLeft;

  });

  slides.addEventListener('touchmove', (e) => {

    const touchX = e.touches[0].pageX;

    const walk = (touchX - touchStartX) * 1.5;

    slides.scrollLeft = touchScrollLeft - walk;

  });

});