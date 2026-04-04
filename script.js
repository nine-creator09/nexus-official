/* ═══════════════════════════
   NEXUS ─ Official Website
   Premium JavaScript
   ═══════════════════════════ */

// ─── Hero Slideshow ───
(function () {
    const slides = document.querySelectorAll('.hero-slide');
    if (slides.length <= 1) return;
    let current = 0;
    setInterval(() => {
        slides[current].classList.remove('active');
        current = (current + 1) % slides.length;
        slides[current].classList.add('active');
    }, 5000);
})();

// ─── Header Scroll Effect ───
const header = document.getElementById('header');

window.addEventListener('scroll', () => {
    if (window.scrollY > 80) {
        header.classList.add('scrolled');
    } else {
        header.classList.remove('scrolled');
    }
});

// ─── Mobile Navigation ───
const hamburger = document.getElementById('hamburger');
const mobileNav = document.getElementById('mobileNav');

hamburger.addEventListener('click', () => {
    hamburger.classList.toggle('active');
    mobileNav.classList.toggle('open');
    document.body.style.overflow = mobileNav.classList.contains('open') ? 'hidden' : '';
});

function closeMobileNav() {
    hamburger.classList.remove('active');
    mobileNav.classList.remove('open');
    document.body.style.overflow = '';
}

// ─── Scroll Fade-In + Stagger Animation ───
const observerOptions = {
    root: null,
    rootMargin: '0px 0px -80px 0px',
    threshold: 0.05
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

document.querySelectorAll('.fade-in').forEach(el => {
    observer.observe(el);
});

// ─── Smooth Scroll for Navigation ───
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            const headerHeight = header.offsetHeight;
            const targetPos = target.getBoundingClientRect().top + window.pageYOffset - headerHeight;
            window.scrollTo({
                top: targetPos,
                behavior: 'smooth'
            });
        }
    });
});

// ─── Parallax on Hero ───
const heroBg = document.querySelector('.hero-bg');

window.addEventListener('scroll', () => {
    if (window.scrollY < window.innerHeight) {
        const offset = window.scrollY * 0.25;
        heroBg.style.transform = `translateY(${offset}px) scale(1.05)`;
    }
});

// ─── Hero Mouse Parallax (Desktop Only) ───
if (window.innerWidth > 768) {
    const hero = document.querySelector('.hero');
    hero.addEventListener('mousemove', (e) => {
        const rect = hero.getBoundingClientRect();
        const x = ((e.clientX - rect.left) / rect.width - 0.5) * 8;
        const y = ((e.clientY - rect.top) / rect.height - 0.5) * 8;
        heroBg.style.transform = `translate(${x}px, ${y}px) scale(1.05)`;
    });
}

// ═══════════════════════════
//  GOLD PARTICLE SYSTEM
// ═══════════════════════════
const canvas = document.getElementById('hero-particles');
if (canvas) {
    const ctx = canvas.getContext('2d');
    let particles = [];
    const PARTICLE_COUNT = 40;

    function resizeCanvas() {
        canvas.width = canvas.offsetWidth * window.devicePixelRatio;
        canvas.height = canvas.offsetHeight * window.devicePixelRatio;
        ctx.scale(window.devicePixelRatio, window.devicePixelRatio);
    }

    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);

    class Particle {
        constructor() {
            this.reset();
        }

        reset() {
            this.x = Math.random() * canvas.offsetWidth;
            this.y = Math.random() * canvas.offsetHeight;
            this.size = Math.random() * 2 + 0.5;
            this.speedX = (Math.random() - 0.5) * 0.3;
            this.speedY = (Math.random() - 0.5) * 0.2 - 0.1;
            this.opacity = Math.random() * 0.4 + 0.1;
            this.fadeSpeed = Math.random() * 0.003 + 0.001;
            this.growing = Math.random() > 0.5;
        }

        update() {
            this.x += this.speedX;
            this.y += this.speedY;

            if (this.growing) {
                this.opacity += this.fadeSpeed;
                if (this.opacity >= 0.5) this.growing = false;
            } else {
                this.opacity -= this.fadeSpeed;
                if (this.opacity <= 0.05) this.reset();
            }

            if (this.x < -20 || this.x > canvas.offsetWidth + 20 ||
                this.y < -20 || this.y > canvas.offsetHeight + 20) {
                this.reset();
            }
        }

        draw() {
            ctx.save();
            ctx.globalAlpha = this.opacity;

            // Gold glow
            const gradient = ctx.createRadialGradient(
                this.x, this.y, 0,
                this.x, this.y, this.size * 3
            );
            gradient.addColorStop(0, 'rgba(219, 177, 112, 0.8)');
            gradient.addColorStop(0.4, 'rgba(200, 149, 108, 0.3)');
            gradient.addColorStop(1, 'rgba(200, 149, 108, 0)');

            ctx.fillStyle = gradient;
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size * 3, 0, Math.PI * 2);
            ctx.fill();

            // Core dot
            ctx.fillStyle = 'rgba(252, 239, 212, 0.9)';
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size * 0.5, 0, Math.PI * 2);
            ctx.fill();

            ctx.restore();
        }
    }

    for (let i = 0; i < PARTICLE_COUNT; i++) {
        particles.push(new Particle());
    }

    function animateParticles() {
        ctx.clearRect(0, 0, canvas.offsetWidth, canvas.offsetHeight);
        particles.forEach(p => {
            p.update();
            p.draw();
        });
        requestAnimationFrame(animateParticles);
    }

    animateParticles();
}

// ═══════════════════════════
//  CARD MOUSE LIGHT EFFECT
// ═══════════════════════════
if (window.innerWidth > 768) {
    document.querySelectorAll('.arc-card, .music-card').forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            card.style.background = `
                radial-gradient(
                    300px circle at ${x}px ${y}px,
                    rgba(200, 149, 108, 0.06) 0%,
                    rgba(18, 18, 24, 0.4) 100%
                )
            `;
        });

        card.addEventListener('mouseleave', () => {
            card.style.background = '';
        });
    });
}

// ─── Language Toggle ───
function applyLang(lang) {
    const html = document.documentElement;
    html.setAttribute('lang', lang === 'ja' ? 'ja' : 'en');
    html.setAttribute('data-lang', lang);

    // data-jp / data-en 属性を持つ全要素のテキストを切り替え
    // lang='ja' → data-jp, lang='en' → data-en
    const attrKey = lang === 'ja' ? 'data-jp' : 'data-en';
    document.querySelectorAll('[data-jp][data-en]').forEach(el => {
        el.innerHTML = el.getAttribute(attrKey);
    });

    // ボタンのアクティブ状態を更新
    const btn = document.getElementById('langToggle');
    if (btn) {
        btn.querySelector('.lang-jp').classList.toggle('lang-active', lang === 'ja');
        btn.querySelector('.lang-en').classList.toggle('lang-active', lang === 'en');
    }

    localStorage.setItem('nexus-lang', lang);
}

function toggleLang() {
    const current = document.documentElement.getAttribute('data-lang') || 'ja';
    applyLang(current === 'ja' ? 'en' : 'ja');
}

// ページ読み込み時に保存済み言語を適用
(function () {
    const saved = localStorage.getItem('nexus-lang');
    if (saved === 'en') {
        applyLang('en');
    } else {
        applyLang('ja');
    }
})();


