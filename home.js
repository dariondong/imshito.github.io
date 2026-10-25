/* theez.top 个人主页 — 视差滚动与交互 */
(function () {
    'use strict';

    var root = document.documentElement;
    var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    var navbar = document.getElementById('navbar');
    var progressBar = document.getElementById('progressBar');
    var navToggle = document.getElementById('navToggle');
    var navLinks = document.getElementById('navLinks');
    var video = document.getElementById('bgVideo');
    var loader = document.getElementById('pageLoader');
    var heroInner = document.querySelector('.hero-inner');
    var modal = document.getElementById('wechatModal');

    /* ---------- 载入层 ---------- */
    var loaderGone = false;
    function hideLoader() {
        if (loaderGone || !loader) return;
        loaderGone = true;
        loader.classList.add('hidden');
        if (video && video.play) {
            var p = video.play();
            if (p && p.catch) p.catch(function () {});
        }
    }
    setTimeout(hideLoader, 600);
    window.addEventListener('load', hideLoader);

    /* ---------- 窄屏菜单 ---------- */
    if (navToggle && navLinks) {
        navToggle.addEventListener('click', function () {
            var open = navLinks.classList.toggle('open');
            navToggle.setAttribute('aria-expanded', open ? 'true' : 'false');
        });
        Array.prototype.forEach.call(navLinks.querySelectorAll('a'), function (a) {
            a.addEventListener('click', function () {
                navLinks.classList.remove('open');
                navToggle.setAttribute('aria-expanded', 'false');
            });
        });
    }

    /* ---------- 视差 ---------- */
    var layers = [];
    function collect() {
        layers = Array.prototype.map.call(document.querySelectorAll('[data-depth]'), function (el) {
            return { el: el, s: parseFloat(el.getAttribute('data-depth')) || 0, top: 0, h: 1 };
        });
        layers.forEach(function (it) { it.el.style.transform = ''; });
        layers.forEach(function (it) {
            var r = it.el.getBoundingClientRect();
            it.top = r.top + window.scrollY;
            it.h = r.height || 1;
        });
    }

    var LIMIT = 160;

    function paint() {
        var y = window.scrollY || window.pageYOffset;
        var vh = window.innerHeight;

        if (navbar) navbar.classList.toggle('scrolled', y > 40);

        if (progressBar) {
            var span = document.body.scrollHeight - vh;
            var ratio = span > 0 ? Math.min(1, Math.max(0, y / span)) : 0;
            progressBar.style.transform = 'scaleX(' + ratio.toFixed(4) + ')';
        }

        if (reduce) return;

        for (var i = 0; i < layers.length; i++) {
            var it = layers[i];
            var p = (it.top + it.h / 2 - (y + vh / 2)) / vh;
            var t = -p * it.s * vh;
            if (t > LIMIT) t = LIMIT;
            if (t < -LIMIT) t = -LIMIT;
            it.el.style.transform = 'translate3d(0,' + t.toFixed(1) + 'px,0)';
        }

        var hp = Math.min(1, Math.max(0, y / vh));
        if (heroInner) {
            heroInner.style.transform = 'translate3d(0,' + (hp * 70).toFixed(1) + 'px,0)';
            heroInner.style.opacity = String(Math.max(0, 1 - hp * 1.15).toFixed(3));
        }
        if (video) {
            video.style.transform = 'scale(' + (1 + hp * 0.08).toFixed(3) + ')';
        }
    }

    var ticking = false;
    function onScroll() {
        if (ticking) return;
        ticking = true;
        window.requestAnimationFrame(function () {
            ticking = false;
            paint();
        });
    }

    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', function () {
        window.requestAnimationFrame(function () {
            collect();
            paint();
        });
    });

    /* ---------- 进场 ---------- */
    var reveals = Array.prototype.slice.call(document.querySelectorAll('.reveal'));
    if (reveals.length) {
        if ('IntersectionObserver' in window && !reduce) {
            var io = new IntersectionObserver(function (entries) {
                entries.forEach(function (e) {
                    if (e.isIntersecting) {
                        e.target.classList.add('in');
                        io.unobserve(e.target);
                    }
                });
            }, { rootMargin: '0px 0px -10% 0px', threshold: 0.05 });
            reveals.forEach(function (el) { io.observe(el); });
        } else {
            reveals.forEach(function (el) { el.classList.add('in'); });
        }
    }

    /* ---------- 导航高亮 ---------- */
    var sections = Array.prototype.slice.call(document.querySelectorAll('main section[id]'));
    var linkOf = {};
    if (navLinks) {
        Array.prototype.forEach.call(navLinks.querySelectorAll('a[href^="#"]'), function (a) {
            linkOf[a.getAttribute('href').slice(1)] = a;
        });
    }
    if (sections.length && 'IntersectionObserver' in window) {
        var spy = new IntersectionObserver(function (entries) {
            entries.forEach(function (e) {
                if (!e.isIntersecting) return;
                var hit = linkOf[e.target.id];
                if (!hit) return;
                for (var k in linkOf) {
                    if (Object.prototype.hasOwnProperty.call(linkOf, k)) linkOf[k].classList.remove('active');
                }
                hit.classList.add('active');
            });
        }, { rootMargin: '-45% 0px -50% 0px' });
        sections.forEach(function (s) { spy.observe(s); });
    }

    /* ---------- 打字机 ---------- */
    var typed = document.querySelector('.typing-text');
    if (typed) {
        if (reduce) {
            typed.textContent = '即将发生';
        } else {
            (function () {
                var text = '即将发生';
                var i = 0;
                function step() {
                    if (i < text.length) {
                        typed.textContent = text.slice(0, ++i);
                        setTimeout(step, 160);
                    }
                }
                setTimeout(step, 1100);
            })();
        }
    }

    /* ---------- 微信二维码 ---------- */
    var lastFocus = null;
    function openModal() {
        if (!modal) return;
        lastFocus = document.activeElement;
        modal.classList.add('show');
        var btn = modal.querySelector('.wechat-modal-close');
        if (btn) btn.focus();
    }
    function closeModal() {
        if (!modal) return;
        modal.classList.remove('show');
        if (lastFocus && lastFocus.focus) lastFocus.focus();
    }
    Array.prototype.forEach.call(document.querySelectorAll('[data-wechat]'), function (el) {
        el.addEventListener('click', function (e) {
            e.preventDefault();
            openModal();
        });
    });
    if (modal) {
        modal.addEventListener('click', function (e) {
            if (e.target === modal) closeModal();
        });
        var closeBtn = modal.querySelector('.wechat-modal-close');
        if (closeBtn) closeBtn.addEventListener('click', closeModal);
        document.addEventListener('keydown', function (e) {
            if (e.key === 'Escape' && modal.classList.contains('show')) closeModal();
        });
    }

    /* ---------- 启动 ---------- */
    collect();
    paint();
    if (root) root.classList.add('ready');
})();
