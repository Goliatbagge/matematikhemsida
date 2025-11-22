# Visuella Element - Matematik 3c Hemsida

Denna mapp innehåller alla SVG-grafiska element för hemsidan.

## Kapitel-ikoner (64x64px)

### `icon-chapter1.svg` - Rationella uttryck
Visar ett bråk med polynom i täljare och nämnare
- Färger: Blå (#2563EB) för algebra, orange (#F59E0B) för bråkstreck

### `icon-chapter2.svg` - Derivatans definition
Visar en kurva med sekant och tangent
- Blå kurva med punkter
- Grå streckad sekant
- Orange tangent

### `icon-chapter3.svg` - Derivatan
Visar derivata-operatorn f(x) → f'(x) med pil
- Blå text för funktioner
- Orange pil för transformation

### `icon-chapter4.svg` - Derivatan och funktioner
Visar en funktion med max- och minpunkter
- Blå kurva
- Orange markeringar för extrempunkter
- Gråa streckade tangenter

### `icon-chapter5.svg` - Integraler
Visar integral-symbolen med area under kurva
- Blå kurva och Riemann-summa rektanglar
- Orange integral-symbol ∫

### `icon-chapter6.svg` - Trigonometri
Visar enhetscirkeln med vinkel
- Blå enhetscirkel
- Orange vinkel (45°) och radie
- Gråa axlar och projektioner

## Section Separators

### `separator-wave.svg`
Vågformad separator med dekorativa cirklar
- Höjd: 60px
- Färger: Grå vågor med blå/orange accenter

### `separator-dots.svg`
Prickad linje med central hexagon-dekoration
- Höjd: 40px
- Streckad linje med geometrisk form i mitten

### `separator-minimal.svg`
Minimal separator med gradient-linje
- Höjd: 30px
- Gradient från transparent till blå till transparent

## Bakgrundsmönster (Tileable)

### `pattern-grid.svg` (200x200px)
Subtilt rutnät med dekorativa punkter
- Ljusgrå gridlinjer
- Små blå/orange punkter vid korsningar
- Används som standard body-bakgrund

### `pattern-symbols.svg` (300x300px)
Matematiska symboler (∫, Σ, π, Δ, ∂)
- Mycket låg opacity (4-5%)
- Blå och orange färger

### `pattern-geometric.svg` (400x400px)
Geometriska former (cirklar, hexagoner)
- Cirklar och polygoner i låg opacity
- Balanserad fördelning av former

## Hero Graphics

### `hero-graphics.svg` (400x400px)
Matematisk grafik för hero-sektionen
- Cirklar, triangel, hexagon
- Funktionskurva med tangent
- Mycket låg opacity för bakgrundsplacering

## Användning i HTML

### Kapitel-ikoner (automatiskt i navigation via CSS)
```css
/* Ikoner läggs automatiskt till i dropdown-menyer */
.dropdown:nth-child(1) .dropbtn::before {
    background-image: url('images/icon-chapter1.svg');
}
```

### Separators
```html
<div class="separator separator-wave"></div>
<div class="separator separator-dots"></div>
<div class="separator separator-minimal"></div>
```

### Bakgrundsmönster
```css
/* I body (standard) */
background-image: url('images/pattern-grid.svg');

/* Alternativa mönster */
.bg-pattern-symbols {
    background-image: url('images/pattern-symbols.svg');
}

.bg-pattern-geometric {
    background-image: url('images/pattern-geometric.svg');
}
```

## Färgpalett

- **Primär Blå:** #2563EB
- **Accent Orange:** #F59E0B
- **Grå 50:** #F9FAFB
- **Grå 100:** #F3F4F6
- **Grå 200:** #E5E7EB
- **Grå 400:** #9CA3AF

## Design-principer

1. **Minimalism:** Enkla former, rena linjer
2. **Låg opacity:** Bakgrundselement stör inte innehåll (3-10% opacity)
3. **Skalbarhet:** Alla SVG:er skalar perfekt
4. **Prestanda:** Små filstorlekar, inga externa beroenden
5. **Konsistens:** Samma färgpalett och stil genom alla element

## Framtida tillägg

Potentiella nya ikoner:
- Funktionsgrafer för specifika avsnitt
- Animerade SVG:er för interaktiva element
- Diagram för specifika matematiska koncept
- Fler separator-varianter
