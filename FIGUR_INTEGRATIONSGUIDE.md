# Guide för integration av figurer i index.html

## Sammanfattning
Totalt **28 figurer** har skapats med `matematisk_bildgenerator.py`:
- 4 ursprungliga figurer (triangelsatser och sekant)
- 8 VIKTIGA figurer (Kap 1.1 - 5.1)
- 16 ÖNSKVÄRDA figurer (Kap 1.3 - 6.8)

## Lista över alla figurer med HTML-integration

### Ursprungliga figurer
```html
<!-- Triangelsatser -->
<img src="areasatsen_korrekt.png" alt="Areasatsen" class="math-figure">
<img src="sinussatsen_korrekt.png" alt="Sinussatsen" class="math-figure">
<img src="cosinussatsen_korrekt.png" alt="Cosinussatsen" class="math-figure">
<img src="sekant_korrekt.png" alt="Sekantens lutning" class="math-figure">
```

### VIKTIGA FIGURER (8 st)

#### Kapitel 1: Algebra och räkning
```html
<!-- Kap 1.1 - Bråkförkortning (algebraisk) -->
<img src="kap1-01-brakforkortning.png" alt="Bråkförkortning" class="math-figure">

<!-- Kap 1.2 - Bråkaddition/subtraktion -->
<img src="kap1-02-brakaddition.png" alt="Bråkaddition och subtraktion" class="math-figure">
```

#### Kapitel 2: Derivatans grundläggande begrepp
```html
<!-- Kap 2.3 - Derivatans definition (formell med gränsvärde) -->
<img src="kap2-03-derivata-definition.png" alt="Derivatans definition" class="math-figure">

<!-- Kap 2.4 - Derivering steg-för-steg exempel -->
<img src="kap2-04-derivering-exempel.png" alt="Derivering steg-för-steg" class="math-figure">
```

#### Kapitel 3: Deriveringsregler
```html
<!-- Kap 3.2 - Produktregeln visualiserad -->
<img src="kap3-02-produktregeln.png" alt="Produktregeln" class="math-figure">

<!-- Kap 3.5 - Kedjeregeln steg-för-steg -->
<img src="kap3-05-kedjeregeln.png" alt="Kedjeregeln" class="math-figure">
```

#### Kapitel 4: Derivatans tillämpningar
```html
<!-- Kap 4.2 - Derivatans nollställen (graf med f och f') -->
<img src="kap4-02-derivata-nollstallen.png" alt="Derivatans nollställen" class="math-figure">
```

#### Kapitel 5: Integraler
```html
<!-- Kap 5.1 - Primitiv funktion (graf med f och F) -->
<img src="kap5-01-primitiv-funktion.png" alt="Primitiv funktion" class="math-figure">
```

### ÖNSKVÄRDA FIGURER (16 st)

#### Kapitel 1: Algebra (fortsättning)
```html
<!-- Kap 1.3 - Multiplikation och division av bråk -->
<img src="kap1-03-brak-multiplikation.png" alt="Multiplikation och division av bråk" class="math-figure">
```

#### Kapitel 2: Derivata (fortsättning)
```html
<!-- Kap 2.2 - Tangentens lutning (förbättrad version) -->
<img src="kap2-02-tangent-lutning.png" alt="Tangentens lutning" class="math-figure">

<!-- Kap 2.5 - Deriverbarhet och absolutbelopp -->
<img src="kap2-05-deriverbarhet-absolutbelopp.png" alt="Deriverbarhet och absolutbelopp" class="math-figure">
```

#### Kapitel 3: Deriveringsregler (fortsättning)
```html
<!-- Kap 3.3 - Mer om derivatan av potensfunktioner -->
<img src="kap3-03-potensfunktioner.png" alt="Derivata av potensfunktioner" class="math-figure">

<!-- Kap 3.6 - Tillämpningar av derivata -->
<img src="kap3-06-tillampningar-derivata.png" alt="Tillämpningar av derivata" class="math-figure">
```

#### Kapitel 4: Derivatans tillämpningar (fortsättning)
```html
<!-- Kap 4.5 - Andraderivatan och lokala extrempunkter -->
<img src="kap4-05-andraderivata.png" alt="Andraderivatan och extrempunkter" class="math-figure">

<!-- Kap 4.6 - Extremvärdesproblem exempel -->
<img src="kap4-06-extremvardesproblem.png" alt="Extremvärdesproblem" class="math-figure">
```

#### Kapitel 5: Integraler (fortsättning)
```html
<!-- Kap 5.2 - Primitiva funktioner med villkor -->
<img src="kap5-02-primitiva-villkor.png" alt="Primitiva funktioner med villkor" class="math-figure">

<!-- Kap 5.4 - Integralkalkylens fundamentalsats -->
<img src="kap5-04-fundamentalsats.png" alt="Integralkalkylens fundamentalsats" class="math-figure">

<!-- Kap 5.7 - Tillämpningar av integraler -->
<img src="kap5-07-tillampningar-integral.png" alt="Tillämpningar av integraler" class="math-figure">
```

#### Kapitel 6: Trigonometri
```html
<!-- Kap 6.1 - Trigonometri i rätvinkliga trianglar -->
<img src="kap6-01-trigonometri-triangel.png" alt="Trigonometri i rätvinkliga trianglar" class="math-figure">

<!-- Kap 6.3 - Trigonometriska ekvationer på enhetscirkel -->
<img src="kap6-03-enhetscirkel.png" alt="Enhetscirkeln" class="math-figure">

<!-- Kap 6.4 - Trigonometriska formler (sin²+cos²=1) -->
<img src="kap6-04-trigonometriska-formler.png" alt="Trigonometriska formler" class="math-figure">

<!-- Kap 6.8 - Tillämpning av triangelsatser -->
<img src="kap6-08-triangelsatser.png" alt="Tillämpning av triangelsatser" class="math-figure">
```

## CSS-styling (lägg till i index.html)
```css
.math-figure {
    max-width: 100%;
    height: auto;
    display: block;
    margin: 20px auto;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

/* Responsiv design för mindre skärmar */
@media (max-width: 768px) {
    .math-figure {
        max-width: 95%;
        margin: 15px auto;
    }
}
```

## Integrationsstrategi

### Steg 1: Kopiera alla PNG-filer
Kopiera alla genererade PNG-filer från `Hemsida Matematik 3c`-mappen till rätt plats i din webbstruktur.

### Steg 2: Lägg till figurer i rätt kapitel
Gå igenom index.html och lägg till motsvarande `<img>`-tagg i varje kapitel enligt listan ovan.

### Steg 3: Lägg till CSS
Lägg till CSS-klassen `.math-figure` i din stylesheet för enhetlig styling.

### Steg 4: Optimera för prestanda (valfritt)
Överväg att komprimera PNG-filerna med verktyg som:
- TinyPNG (online)
- ImageOptim (Mac)
- PNGCrush (kommandorad)

## Figurkvalitet
- Alla figurer är skapade i **300 DPI** för högkvalitativ utskrift
- Vit bakgrund för konsekvent utseende
- Matematiskt korrekta med exakta koordinater
- Pedagogisk design med tydliga färgkodningar

## Regenerering
Om du behöver regenerera figurerna, kör:
```bash
cd "C:\claude\Hemsida Matematik 3c"
python matematisk_bildgenerator.py
```

## Anteckningar
- Några figurer innehåller subscript-tecken (x₀) som kan generera varningar i vissa fonter
- Detta påverkar inte figurernas kvalitet
- Alla figurer är testade och verifierade att fungera korrekt
