/**
 * Animations.js - Smooth scroll animations and interactions
 * Optimized for 60fps performance using Intersection Observer
 */

// ============================================
// INTERSECTION OBSERVER FOR SCROLL ANIMATIONS
// ============================================

/**
 * Initialize scroll animations using Intersection Observer
 * More performant than scroll event listeners
 */
function initScrollAnimations() {
    // Options for Intersection Observer
    const options = {
        root: null, // viewport
        rootMargin: '0px 0px -100px 0px', // Trigger 100px before element enters viewport
        threshold: 0.1 // Trigger when 10% of element is visible
    };

    // Callback when element enters/exits viewport
    const callback = (entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                // Add 'visible' class to trigger CSS animation
                entry.target.classList.add('visible');

                // Optional: Stop observing after animation (one-time animation)
                // observer.unobserve(entry.target);
            }
        });
    };

    // Create observer
    const observer = new IntersectionObserver(callback, options);

    // Observe all content sections
    const contentSections = document.querySelectorAll('.content-section');
    contentSections.forEach(section => observer.observe(section));

    // Observe graph containers
    const graphContainers = document.querySelectorAll('.graph-container');
    graphContainers.forEach(container => observer.observe(container));

    // Observe info boxes
    const infoBoxes = document.querySelectorAll(
        '.definition-box, .info-box, .formula-box, .method-box, ' +
        '.important-box, .example-box, .derivation-box, .pattern-box, .summary-box'
    );
    infoBoxes.forEach(box => observer.observe(box));

    // Observe separators
    const separators = document.querySelectorAll('.separator');
    separators.forEach(sep => observer.observe(sep));
}

// ============================================
// SMOOTH SCROLL TO ANCHOR
// ============================================

/**
 * Enhance anchor link behavior with smooth scroll
 */
function initSmoothScroll() {
    // Get all anchor links
    const anchorLinks = document.querySelectorAll('a[href^="#"]');

    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');

            // Skip if href is just "#"
            if (href === '#') return;

            const target = document.querySelector(href);

            if (target) {
                e.preventDefault();

                // Smooth scroll to target
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });

                // Update URL without jumping
                history.pushState(null, null, href);
            }
        });
    });
}

// ============================================
// NAVBAR SCROLL BEHAVIOR
// ============================================

/**
 * Add backdrop blur and shadow to navbar on scroll
 */
function initNavbarScroll() {
    const navbar = document.querySelector('.main-nav');
    let lastScroll = 0;

    window.addEventListener('scroll', () => {
        const currentScroll = window.pageYOffset;

        // Add shadow when scrolled down
        if (currentScroll > 50) {
            navbar.style.boxShadow = '0 4px 20px rgba(0, 0, 0, 0.1)';
            navbar.style.backdropFilter = 'blur(10px)';
            navbar.style.backgroundColor = 'rgba(255, 255, 255, 0.95)';
        } else {
            navbar.style.boxShadow = '0 2px 10px rgba(0, 0, 0, 0.05)';
            navbar.style.backdropFilter = 'none';
            navbar.style.backgroundColor = 'white';
        }

        lastScroll = currentScroll;
    }, { passive: true }); // Passive for better scroll performance
}

// ============================================
// PERFORMANCE OPTIMIZATION
// ============================================

/**
 * Debounce function for event listeners
 * Reduces function calls for better performance
 */
function debounce(func, wait = 100) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Throttle function for continuous events
 * Ensures function runs at most once per interval
 */
function throttle(func, limit = 100) {
    let inThrottle;
    return function(...args) {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// ============================================
// PREFERS REDUCED MOTION
// ============================================

/**
 * Respect user's motion preferences
 * Disable animations if user prefers reduced motion
 */
function respectMotionPreferences() {
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');

    if (prefersReducedMotion.matches) {
        // Disable animations
        document.body.style.setProperty('--transition-fast', '0s');
        document.body.style.setProperty('--transition-base', '0s');
        document.body.style.setProperty('--transition-slow', '0s');

        // Remove animation classes
        document.querySelectorAll('[class*="animate"]').forEach(el => {
            el.style.animation = 'none';
        });

        console.log('Animations disabled: User prefers reduced motion');
    }
}

// ============================================
// LOADING OPTIMIZATIONS
// ============================================

/**
 * Lazy load images and graphs for better performance
 */
function initLazyLoading() {
    // Native lazy loading for images
    const images = document.querySelectorAll('img[data-src]');

    images.forEach(img => {
        img.setAttribute('src', img.getAttribute('data-src'));
        img.onload = () => {
            img.removeAttribute('data-src');
        };
    });
}

/**
 * Show initial content immediately, fade in rest
 */
function staggerContentReveal() {
    // Immediately show first section
    const firstSection = document.querySelector('.content-section');
    if (firstSection) {
        firstSection.classList.add('visible');
    }
}

// ============================================
// INTERACTIVE ENHANCEMENTS
// ============================================

/**
 * Add ripple effect to buttons and interactive elements
 */
function initRippleEffect() {
    const buttons = document.querySelectorAll('.cta-button, button');

    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            // Skip if already has ripple
            if (this.querySelector('.ripple')) return;

            const ripple = document.createElement('span');
            ripple.classList.add('ripple');

            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;

            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';

            this.appendChild(ripple);

            setTimeout(() => ripple.remove(), 600);
        });
    });
}

/**
 * Parallax effect for hero graphic
 */
function initParallax() {
    const heroGraphic = document.querySelector('.hero-graphic');

    if (!heroGraphic) return;

    const handleParallax = throttle((e) => {
        const scrolled = window.pageYOffset;
        const parallaxSpeed = 0.5;

        if (scrolled < window.innerHeight) {
            heroGraphic.style.transform = `translateY(calc(-50% + ${scrolled * parallaxSpeed}px))`;
        }
    }, 16); // ~60fps

    window.addEventListener('scroll', handleParallax, { passive: true });
}

// ============================================
// INITIALIZATION
// ============================================

/**
 * Initialize all animations and interactions when DOM is ready
 */
function init() {
    console.log('🎨 Initializing animations and interactions...');

    // Check motion preferences first
    respectMotionPreferences();

    // Initialize core features
    initScrollAnimations();
    initSmoothScroll();
    initNavbarScroll();

    // Performance enhancements
    initLazyLoading();
    staggerContentReveal();

    // Interactive features
    initRippleEffect();
    initParallax();

    console.log('✅ Animations initialized successfully');
}

// Run when DOM is fully loaded
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}

// ============================================
// EXPORT FOR EXTERNAL USE
// ============================================

// Make functions available globally if needed
window.MathAnimations = {
    debounce,
    throttle,
    initScrollAnimations,
    initSmoothScroll
};
