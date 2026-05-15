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
   ULTRA SMOOTH PORTFOLIO
========================= */

document.querySelectorAll('.portfolio-slides').forEach(slider => {

  let isDown = false;
  let startX;
  let scrollLeft;

  let velocity = 0;
  let momentumID;

  let autoSlide;

  /* =========================
     AUTO SLIDE
  ========================= */

  function startAutoSlide() {

    stopAutoSlide();

    autoSlide = setInterval(() => {

      slider.scrollLeft += 1;

      // RESET KE AWAL
      if (
        slider.scrollLeft + slider.clientWidth >=
        slider.scrollWidth - 2
      ) {
        slider.scrollLeft = 0;
      }

    }, 15);

  }

  function stopAutoSlide() {

    clearInterval(autoSlide);

  }

  startAutoSlide();

  /* =========================
     MOMENTUM DESKTOP
  ========================= */

  function cancelMomentumTracking() {

    cancelAnimationFrame(momentumID);

  }

  function beginMomentumTracking() {

    cancelMomentumTracking();

    momentumID = requestAnimationFrame(momentumLoop);

  }

  function momentumLoop() {

    slider.scrollLeft += velocity;

    velocity *= 0.95;

    if (Math.abs(velocity) > 0.5) {

      momentumID = requestAnimationFrame(momentumLoop);

    }

  }

  /* =========================
     DESKTOP DRAG
  ========================= */

  slider.addEventListener('mousedown', (e) => {

    isDown = true;

    slider.classList.add('active');

    startX = e.pageX - slider.offsetLeft;

    scrollLeft = slider.scrollLeft;

    cancelMomentumTracking();

    stopAutoSlide();

  });

  slider.addEventListener('mouseleave', () => {

    isDown = false;

    slider.classList.remove('active');

    startAutoSlide();

  });

  slider.addEventListener('mouseup', () => {

    isDown = false;

    slider.classList.remove('active');

    beginMomentumTracking();

    startAutoSlide();

  });

  slider.addEventListener('mousemove', (e) => {

    if (!isDown) return;

    e.preventDefault();

    const x = e.pageX - slider.offsetLeft;

    const walk = (x - startX);

    const prevScroll = slider.scrollLeft;

    slider.scrollLeft = scrollLeft - walk;

    velocity = slider.scrollLeft - prevScroll;

  });

  /* =========================
     MOBILE TOUCH
  ========================= */

  let touchStartX = 0;

  let mobileVelocity = 0;

  let mobileMomentumID;

  function stopMobileMomentum() {

    cancelAnimationFrame(mobileMomentumID);

  }

  function startMobileMomentum() {

    stopMobileMomentum();

    mobileMomentumID = requestAnimationFrame(mobileMomentumLoop);

  }

  function mobileMomentumLoop() {

    slider.scrollLeft += mobileVelocity;

    mobileVelocity *= 0.95;

    if (Math.abs(mobileVelocity) > 0.5) {

      mobileMomentumID = requestAnimationFrame(mobileMomentumLoop);

    }

  }

  slider.addEventListener('touchstart', (e) => {

    touchStartX = e.touches[0].pageX;

    scrollLeft = slider.scrollLeft;

    stopMobileMomentum();

    stopAutoSlide();

  }, { passive: true });

  slider.addEventListener('touchmove', (e) => {

    const touchX = e.touches[0].pageX;

    const walk = (touchX - touchStartX);

    const prevScroll = slider.scrollLeft;

    slider.scrollLeft = scrollLeft - walk;

    mobileVelocity = slider.scrollLeft - prevScroll;

  }, { passive: true });

  slider.addEventListener('touchend', () => {

    startMobileMomentum();

    startAutoSlide();

  });

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