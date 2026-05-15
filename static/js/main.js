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
const reveals = document.querySelectorAll(
  '.stats, .about-grid, .service-card, .why-card, .testi-card, .portfolio-item, .contact-grid'
);

reveals.forEach(el => el.classList.add('reveal'));

const observer = new IntersectionObserver((entries) => {

  entries.forEach((entry, i) => {

    if (entry.isIntersecting) {

      setTimeout(() => {

        entry.target.classList.add('visible');

      }, i * 80);

      observer.unobserve(entry.target);

    }

  });

}, { threshold: 0.1 });

document.querySelectorAll('.reveal').forEach(el => observer.observe(el));


// CONTACT FORM
document.getElementById('contactForm').addEventListener('submit', function(e) {

  e.preventDefault();

  const name = this.querySelector('input[type="text"]').value;

  const service = this.querySelector('select').value;

  const msg = this.querySelector('textarea').value;

  const text =
`Halo N&N Capture!
Nama saya *${name}*.

Layanan: *${service}*

Pesan:
${msg}`;

  const url =
`https://wa.me/6285709799920?text=${encodeURIComponent(text)}`;

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


/* =========================
   PORTFOLIO SLIDER
========================= */

document.querySelectorAll('.portfolio-slider').forEach(wrapper => {

  const slider = wrapper.querySelector('.portfolio-slides');
  const count  = wrapper.querySelector('.portfolio-count');
  const items  = wrapper.querySelectorAll('.portfolio-slide');
  const total  = items.length;

  if (!slider || total === 0) return;

  let current   = 0;
  let autoTimer = null;
  let isDown    = false;
  let startX    = 0;
  let scrollStart = 0;
  let touchStartX = 0;

  /* GOTO SLIDE */

  function goTo(index) {

    if (index < 0) index = total - 1;
    if (index >= total) index = 0;

    current = index;

    const slideWidth = items[0].offsetWidth;

    slider.scrollTo({ left: slideWidth * current, behavior: 'smooth' });

    if (count) count.textContent = `${current + 1} / ${total}`;

  }

  function next() { goTo(current + 1); }
  function prev() { goTo(current - 1); }


  /* AUTO SLIDE */

  function startAutoSlide() {

    stopAutoSlide();

    autoTimer = setInterval(next, 4000);

  }

  function stopAutoSlide() {

    clearInterval(autoTimer);

  }


  /* DESKTOP DRAG */

  slider.addEventListener('mousedown', (e) => {

    isDown = true;

    startX = e.pageX;

    scrollStart = slider.scrollLeft;

    slider.classList.add('active');

    stopAutoSlide();

  });

  slider.addEventListener('mousemove', (e) => {

    if (!isDown) return;

    e.preventDefault();

    slider.scrollLeft = scrollStart - (e.pageX - startX);

  });

  slider.addEventListener('mouseup', (e) => {

    if (!isDown) return;

    isDown = false;

    slider.classList.remove('active');

    const diff = e.pageX - startX;

    if (Math.abs(diff) > 50) {

      diff < 0 ? next() : prev();

    } else {

      goTo(current);

    }

    startAutoSlide();

  });

  slider.addEventListener('mouseleave', () => {

    if (isDown) {

      isDown = false;

      slider.classList.remove('active');

      goTo(current);

    }

    startAutoSlide();

  });


  /* PAUSE SAAT HOVER */

  wrapper.addEventListener('mouseenter', stopAutoSlide);

  wrapper.addEventListener('mouseleave', startAutoSlide);


  /* MOBILE TOUCH */

  slider.addEventListener('touchstart', (e) => {

    touchStartX  = e.touches[0].clientX;

    scrollStart  = slider.scrollLeft;

    stopAutoSlide();

  }, { passive: true });

  slider.addEventListener('touchmove', (e) => {

    const walk = touchStartX - e.touches[0].clientX;

    slider.scrollLeft = scrollStart + walk;

  }, { passive: true });

  slider.addEventListener('touchend', (e) => {

    const diff = e.changedTouches[0].clientX - touchStartX;

    if (Math.abs(diff) > 50) {

      diff < 0 ? next() : prev();

    } else {

      goTo(current);

    }

    startAutoSlide();

  });


  /* INIT */

  goTo(0);

  startAutoSlide();

});


/* =========================
   AUTO DETECT IMAGE ORIENTATION
========================= */

document.querySelectorAll('.portfolio-slide img').forEach(img => {

  function setOrientation() {

    const slide = img.closest('.portfolio-slide');

    if (!slide) return;

    if (img.naturalHeight > img.naturalWidth) {

      slide.classList.add('portrait');

      slide.classList.remove('landscape');

    } else {

      slide.classList.add('landscape');

      slide.classList.remove('portrait');

    }

  }

  if (img.complete) {

    setOrientation();

  } else {

    img.onload = setOrientation;

  }

});