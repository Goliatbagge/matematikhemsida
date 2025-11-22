# Animationer och Interaktivitet - Matematik 3c

Denna fil dokumenterar alla animationer och interaktiva funktioner på hemsidan.

## Översikt

Alla animationer är optimerade för **60fps prestanda** och använder:
- CSS Transforms (hardware-accelerated)
- Opacity transitions
- Intersection Observer API (istället för scroll events)
- `will-change` för GPU-acceleration
- `prefers-reduced-motion` respekt

---

## 🎬 Laddnings-animationer

### Body Fade-in
**Vad:** Hela sidan fade:ar in när den laddas
**Duration:** 0.4s
**CSS:** `body { animation: fadeIn 0.4s }`

### Header Slide-down
**Vad:** Headern glider ner från toppen
**Duration:** 0.6s
**Delay:** 0s
**CSS:** `header { animation: slideDown 0.6s }`

### Navigation Slide-down
**Vad:** Navigationen glider ner efter headern
**Duration:** 0.5s
**Delay:** 0.3s
**CSS:** `main-nav { animation: slideDown 0.5s 0.3s backwards }`

### Hero Content Fade-in & Slide-up
**Vad:** Hero-innehåll (rubrik, text, CTA) fade:ar in och glider upp
**Duration:** 0.8s
**Delay:** 0.2s
**CSS:** `hero-content { animation: fadeInUp 0.8s 0.2s backwards }`

### Hero Graphic Float
**Vad:** Hero-grafiken fade:ar in och sedan flyter subtilt
**Duration:** Fade-in 1.2s, Float 6s infinite
**Delay:** 0.4s (fade-in)
**CSS:** `hero-graphic img { animation: fadeIn 1.2s 0.4s backwards, float 6s infinite }`

---

## 📜 Scroll-animationer

### Content Sections
**Vad:** Innehållssektioner fade:ar in och glider upp när de scrollas in i viewport
**Trigger:** När 10% av elementet är synligt
**Duration:** 0.6s
**JavaScript:** Intersection Observer
**CSS:** `.content-section.visible { opacity: 1; transform: translateY(0); }`

### Graph Containers
**Vad:** Graf-containers fade:ar in och skalar upp
**Trigger:** Intersection Observer
**Duration:** 0.6s
**CSS:** `.graph-container.visible { opacity: 1; transform: scale(1); }`

### Info Boxes
**Vad:** Informationsrutor fade:ar in när de scrollas in
**Trigger:** Intersection Observer
**Duration:** 0.6s (samma som content sections)

### Separators
**Vad:** Separatorer expanderar från mitten (scaleX)
**Trigger:** Intersection Observer
**Duration:** 0.8s
**CSS:** `.separator.visible { opacity: 0.8; transform: scaleX(1); }`

---

## 🎯 Interaktiva animationer

### CTA Button Pulse
**Vad:** "Börja lära"-knappen pulsar subtilt
**Duration:** 2s infinite
**Effect:** Box-shadow växer och krymper
**CSS:** `@keyframes pulse`

### CTA Button Ripple Effect
**Vad:** Ripple-effekt när användaren klickar
**Duration:** 0.6s
**JavaScript:** `initRippleEffect()`
**CSS:** `@keyframes rippleAnimation`

### CTA Button Hover
**Vad:** Knappen lyfts och får starkare skugga
**Effect:** `translateY(-2px)` + större box-shadow
**Transition:** 200ms

---

## 🖱️ Hover-effekter

### Navigation Dropdown Items
**Effect:** Background-färg + border-left + padding
**Transition:** 200ms
**CSS:** `.dropbtn:hover`, `.dropdown-content a:hover`

### Navigation Icons
**Effect:** Scale + rotate
**CSS:** `.dropbtn:hover::before { transform: scale(1.1) rotate(5deg); }`

### Info Boxes (alla typer)
**Effect:** Lift + scale + enhanced shadow
**CSS:** `transform: translateY(-4px) scale(1.01)`
**Transition:** 200ms

### Chapter Icons
**Effect:** Scale + rotate + brightness
**CSS:** `.chapter-icon:hover { transform: scale(1.1) rotate(-5deg); filter: brightness(1.1); }`

### Graph Containers
**Effect:** Lift + shadow enhancement
**CSS:** `.graph-container:hover { transform: translateY(-2px); box-shadow: var(--shadow-lg); }`

---

## 🧭 Scroll-beteenden

### Navbar on Scroll
**Vad:** Navigation får bakgrund-blur och skugga när man scrollar
**Trigger:** `window.pageYOffset > 50`
**JavaScript:** `initNavbarScroll()`
**Effect:**
- `backdrop-filter: blur(10px)`
- `box-shadow: 0 4px 20px rgba(0,0,0,0.1)`
- `background: rgba(255,255,255,0.95)`

### Smooth Scroll to Anchors
**Vad:** Smooth scroll när man klickar på interna länkar
**JavaScript:** `initSmoothScroll()`
**Effect:** `scrollIntoView({ behavior: 'smooth' })`

### Parallax Hero Graphic
**Vad:** Hero-grafiken rör sig långsammare än scroll-hastigheten
**Speed:** 0.5x scroll speed
**JavaScript:** `initParallax()`

---

## ⚡ Prestanda-optimeringar

### Intersection Observer
**Varför:** Mer performant än scroll event listeners
**Användning:** Alla scroll-animationer
**Threshold:** 0.1 (10% synlighet)
**Root Margin:** `0px 0px -100px 0px`

### GPU Acceleration
**Metod:** `will-change: transform, opacity`
**Tillämpas på:** Content sections, graph containers, info boxes, hero
**Cleanup:** `will-change: auto` efter animation slutförd

### Passive Event Listeners
**Användning:** Scroll events
**Code:** `{ passive: true }`
**Nytta:** Förhindrar scroll-blocking

### Throttle & Debounce
**Funktioner:** Tillgängliga globalt
**Användning:** Scroll/resize events
**Code:** `throttle(func, 16)` för 60fps

---

## ♿ Tillgänglighet

### Prefers Reduced Motion
**Support:** Fullständigt
**Vad:** Alla animationer inaktiveras om användaren har reduced motion aktiverat
**CSS:** `@media (prefers-reduced-motion: reduce)`
**JavaScript:** `respectMotionPreferences()`

### Keyboard Navigation
**Support:** Alla interaktiva element
**Focus States:** Tydliga outlines med primär färg

---

## 🎨 Animation Keyframes

### `fadeIn`
```css
from { opacity: 0; }
to { opacity: 1; }
```

### `fadeInUp`
```css
from {
    opacity: 0;
    transform: translateY(30px);
}
to {
    opacity: 1;
    transform: translateY(0);
}
```

### `slideDown`
```css
from {
    transform: translateY(-100%);
    opacity: 0;
}
to {
    transform: translateY(0);
    opacity: 1;
}
```

### `pulse`
```css
0%, 100% {
    box-shadow: 0 4px 14px rgba(245, 158, 11, 0.4);
}
50% {
    box-shadow: 0 4px 20px rgba(245, 158, 11, 0.6);
}
```

### `float`
```css
0%, 100% {
    transform: translateY(-50%) translateX(0);
}
50% {
    transform: translateY(-50%) translateX(10px);
}
```

### `rippleAnimation`
```css
to {
    transform: scale(4);
    opacity: 0;
}
```

---

## 📦 JavaScript API

### Globala funktioner

```javascript
// Tillgängliga via window.MathAnimations

MathAnimations.debounce(func, wait)    // Debounce en funktion
MathAnimations.throttle(func, limit)   // Throttle en funktion
MathAnimations.initScrollAnimations()  // Initiera scroll-animationer
MathAnimations.initSmoothScroll()      // Aktivera smooth scroll
```

### Event Listeners

Alla event listeners använder `passive: true` där möjligt för bättre prestanda.

---

## 🔧 Anpassning

### Ändra animation-hastigheter

I `styles.css`:
```css
:root {
    --transition-fast: 150ms cubic-bezier(0.4, 0, 0.2, 1);
    --transition-base: 200ms cubic-bezier(0.4, 0, 0.2, 1);
    --transition-slow: 300ms cubic-bezier(0.4, 0, 0.2, 1);
}
```

### Inaktivera specifika animationer

Kommentera ut i `animations.js`:
```javascript
// initParallax();  // Inaktiverar parallax
```

### Justera Intersection Observer threshold

I `animations.js`:
```javascript
const options = {
    threshold: 0.2,  // Ändra från 0.1 till 0.2 (20% synlighet)
};
```

---

## 🐛 Felsökning

### Animationer fungerar inte
1. Kontrollera att `animations.js` är inkluderad
2. Öppna console och leta efter `✅ Animations initialized successfully`
3. Kontrollera att JavaScript är aktiverat i webbläsaren

### Animationer laggar
1. Öppna DevTools Performance tab
2. Spela in medan du scrollar
3. Kontrollera att FPS är >30
4. Om problem: inaktivera parallax eller reducera antal animerade element

### Intersection Observer fungerar inte i äldre browsers
- Fallback till native `scroll` events finns ej implementerat
- Överväg polyfill: `intersection-observer` npm package

---

## 📊 Performance Metrics

**Mål:**
- FPS: ≥60
- Scroll jank: 0
- First Paint: <1s
- Interactive: <2s

**Verktyg för mätning:**
- Chrome DevTools Lighthouse
- Performance tab i DevTools
- WebPageTest.org

---

## 🚀 Framtida förbättringar

Potentiella tillägg:
- Scroll progress bar
- Parallax för fler element
- Morphing animations mellan sektioner
- Animerade SVG-ikoner
- Lottie-animationer för komplexa effekter
- GSAP för mer avancerade timeline-animationer

---

**Skapad:** 2024-10-26
**Version:** 1.0
**Ansvarig:** Interaktivitets-agenten
