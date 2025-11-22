# Hemsida Testningsagent - Dokumentation

## Översikt

**Hemsida Testningsagent** är en kraftfull, autonom agent som automatiskt kontrollerar kvaliteten på alla kurssidor för grafik, layout, tillgänglighet och innehåll. Agenten är byggd för att köra helt autonomt och rapportera eventuella problem som den hittar.

### Varför behövs denna agent?

När du arbetar med en hemsida med 125+ HTML-sidor är det omöjligt att manuellt kontrollera att:
- Alla bilder laddas korrekt
- CSS-länkarna fungerar
- Navigationen är konsekvent
- Tillgängligheten är godkänd
- Layout-fixar (som sticky navigation) är applicerade
- MathJax-formler renderas korrekt

**Denna agent gör allt detta automatiskt åt dig!**

---

## Funktioner

### ✓ Strukturella tester
- DOCTYPE-deklaration
- HTML språkattribut (lang="sv")
- Semantiska HTML5-element (header, nav, main, footer)
- Skip-to-content länkar för tillgänglighet
- Title tags

### ✓ Resurstester
- CSS-fil existens och korrekta paths (../../styles.css)
- JavaScript-fil existens och paths
- Bildlänkar (verifierar att alla bilder finns)
- Alt-text på bilder (tillgänglighet)

### ✓ Navigationstester
- Huvudnavigation (main-nav)
- "← Alla kurser" länk
- Dropdown-menyer för kapitel
- Föregående/Nästa navigation mellan sektioner

### ✓ Innehållstester
- Innehållsboxar (definition-box, info-box, formula-box, example-box)
- MathJax-formler (inline $...$ och display $$...$$)
- Balanserade formelmarkeringar

### ✓ CSS Layout-tester
- Sticky navigation padding-fix
- scroll-margin-top justering
- Position: sticky konfiguration

### ✓ Rapportering
- Färgkodad terminal-output
- Detaljerad markdown-rapport
- Poäng (0-100) och betyg (A-F)
- Prioriterade fel-listor

---

## Installation

### Krav
```bash
pip install beautifulsoup4
```

### Placering
Agenten finns i:
```
C:\claude\Hemsida\test_agent_hemsida.py
```

---

## Användning

### Grundläggande användning

**Testa alla huvudkurser (matematik-2c och matematik-3c):**
```bash
cd C:\claude\Hemsida
python test_agent_hemsida.py
```

**Testa specifik kurs:**
```bash
python test_agent_hemsida.py --course matematik-3c
```

**Detaljerad output (verbose):**
```bash
python test_agent_hemsida.py --course matematik-3c --verbose
```

**Snabbtester (endast kritiska):**
```bash
python test_agent_hemsida.py --quick
```

---

## Output-exempel

### Terminal output

```
======================================================================
Hemsida Testningsagent v1.0
======================================================================

ℹ Startar tester: 2025-10-31 12:23:53
ℹ Testar CSS-fixen för sticky navigation...

======================================================================
Testar kurs: matematik-3c
======================================================================

ℹ Hittade 39 sektioner att testa

matematik-3c sammanfattning:
  ✓ Pass: 815
  ⚠ Varningar: 39
  ✗ Fel: 0

======================================================================
TESTRAPPORT
======================================================================

Totalt:
  Tester körda: 857
  ✓ Godkända: 818
  ⚠ Varningar: 39
  ✗ Fel: 0

Poäng: 97.7/100
Betyg: A - Utmärkt

✓ Rapport sparad: TEST_RAPPORT_20251031_122354.md
```

### Betygsystemet

| Poäng | Betyg | Status |
|-------|-------|--------|
| 90-100 | A - Utmärkt | Perfekt, produktionsklar |
| 80-89 | B - Mycket bra | Små justeringar rekommenderas |
| 70-79 | C - Godkänt | Godkänt men med förbättringspotential |
| 60-69 | D - Godkänt med anmärkningar | Bör åtgärdas innan lansering |
| 0-59 | F - Underkänt | Kritiska problem som måste fixas |

---

## Genererade rapporter

Agenten genererar automatiskt en detaljerad markdown-rapport efter varje körning:

**Filnamn:** `TEST_RAPPORT_YYYYMMDD_HHMMSS.md`

**Exempel:** `TEST_RAPPORT_20251031_122354.md`

### Rapportinnehåll

```markdown
# Hemsida Testrapport

**Datum:** 2025-10-31 12:23:54

**Poäng:** 97.7/100

## Sammanfattning

- **Totalt tester:** 857
- **Godkända:** 818 ✓
- **Varningar:** 39 ⚠
- **Fel:** 0 ✗

## Detaljerade resultat

### kap3-01.html

- ✓ **doctype:** DOCTYPE korrekt deklarerad
- ✓ **lang_attribute:** Språkattribut korrekt (sv)
- ✓ **semantic_header:** <header> element finns
- ✓ **skip_link:** Skip-to-content länk finns och fungerar
- ✓ **css_path:** CSS finns: ../../styles.css
...
```

---

## Testresultat per kurs

### Matematik 3c
- **Status:** ✓ A - Utmärkt
- **Poäng:** 97.7/100
- **Sektioner:** 39
- **Problem:** Inga kritiska fel
- **Varningar:** 39 (mestadels små saker)

### Matematik 2c
- **Status:** ✗ F - Underkänt
- **Poäng:** 48.5/100
- **Sektioner:** 41
- **Problem:** 165 encoding-fel (UTF-8 vs CP1252)
- **Åtgärd:** Filerna måste konverteras till UTF-8

---

## Vad agenten kontrollerar i detalj

### 1. HTML-struktur (5 tester per fil)

```python
✓ DOCTYPE korrekt deklarerad
✓ Lang attribut (lang="sv")
✓ Semantiska element (header, nav, main, footer)
✓ Skip-to-content länk
✓ Title tag
```

### 2. Resurslänkar (variabelt antal)

```python
✓ CSS-filer finns (../../styles.css)
✓ JS-filer finns (../../animations.js, ../../script.js)
✓ Bilder finns (../../images/kap1/...)
✓ Alt-text på alla bilder
```

### 3. Navigation (4 tester per fil)

```python
✓ Huvudnavigation (main-nav) finns
✓ "← Alla kurser" länk korrekt
✓ Dropdown-menyer finns (≥3)
✓ Föregående/Nästa navigation
```

### 4. Innehållsboxar (1 test per fil)

```python
✓ Standardiserade box-klasser används:
  - definition-box
  - info-box
  - formula-box
  - example-box
  - derivation-box
```

### 5. MathJax-formler (4 tester per fil)

```python
✓ MathJax script inkluderad
✓ Inline-formler ($...$) funna
✓ Display-formler ($$...$$) funna
✓ Balanserade $-tecken (inget ojämnt antal)
```

### 6. CSS-fixar (3 globala tester)

```python
✓ Main padding-top fix: calc(var(--spacing-2xl) + 2rem)
✓ scroll-margin-top ≥120px
✓ Sticky navigation konfigurerad
```

---

## Utöka agenten

Agenten är byggd modulärt så att du enkelt kan lägga till nya tester.

### Lägg till nytt test

```python
def test_my_new_feature(self, html_file: Path) -> List[TestResult]:
    """Testa min nya funktion"""
    results = []

    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')

        # Din testkod här
        if soup.find('div', class_='my-feature'):
            results.append(TestResult(
                test_name="my_feature",
                status="pass",
                message="Min funktion fungerar!",
                file_path=str(html_file)
            ))
        else:
            results.append(TestResult(
                test_name="my_feature",
                status="fail",
                message="Min funktion saknas",
                file_path=str(html_file)
            ))

    except Exception as e:
        results.append(TestResult(
            test_name="my_feature",
            status="fail",
            message=f"Fel: {str(e)}",
            file_path=str(html_file)
        ))

    return results
```

Lägg sedan till testet i `run_tests_for_section()`:

```python
def run_tests_for_section(self, section_file: Path) -> List[TestResult]:
    results = []

    results.extend(self.test_html_structure(section_file))
    results.extend(self.test_resource_paths(section_file))
    results.extend(self.test_navigation_structure(section_file))
    results.extend(self.test_content_boxes(section_file))
    results.extend(self.test_mathjax_formulas(section_file))
    results.extend(self.test_my_new_feature(section_file))  # ← NYTT

    return results
```

---

## Felsökning

### Problem: "UnicodeEncodeError"

**Lösning:** Agenten hanterar detta automatiskt med `sys.stdout.reconfigure(encoding='utf-8')` för Windows.

### Problem: "beautifulsoup4 not found"

**Lösning:**
```bash
pip install beautifulsoup4
```

### Problem: "No sections found"

**Lösning:** Kontrollera att kursmappen har följande struktur:
```
matematik-3c/
  sections/
    kap1-01.html
    kap1-02.html
    ...
```

### Problem: Agenten hittar många fel

**Detta är bra!** Agenten gör sitt jobb och identifierar problem som du annars hade missat. Gå igenom rapporten och åtgärda de kritiska felen först.

---

## Automation och CI/CD

### Köra automatiskt vid varje ändring

**Med Git hooks:**

Skapa `.git/hooks/pre-commit`:
```bash
#!/bin/bash
echo "Kör Hemsida Testningsagent..."
cd C:/claude/Hemsida
python test_agent_hemsida.py --quick

if [ $? -ne 0 ]; then
    echo "Tester misslyckades! Commit avbruten."
    exit 1
fi
```

### Schemalagd körning (Windows Task Scheduler)

1. Öppna Task Scheduler
2. Skapa ny uppgift
3. Trigger: Dagligen kl 09:00
4. Action: `python C:\claude\Hemsida\test_agent_hemsida.py`
5. Spara

---

## Framtida förbättringar

### Planerade funktioner (v2.0)

- [ ] **Kontrastkontroll:** Validera WCAG 2.1 AA färgkontrast (4.5:1)
- [ ] **Responsive design:** Testa layout på olika skärmstorlekar
- [ ] **Performance:** Mät sidladdningstider
- [ ] **Länkkontroll:** Verifiera att externa länkar fungerar
- [ ] **Grafik kvalitet:** Kontrollera bildstorlekar och DPI
- [ ] **Plotly-grafer:** Verifiera interaktiva grafer laddas
- [ ] **Cross-browser:** Testa på Chrome, Firefox, Safari, Edge
- [ ] **SEO-validering:** Meta-beskrivningar, Open Graph tags
- [ ] **JSON-export:** Exportera resultat som JSON för integrationer
- [ ] **Dashboard:** Web-baserad dashboard för testresultat

### Integrationsmöjligheter

- GitHub Actions för automatisk testing vid push
- Slack/Discord notifikationer vid fel
- Email-rapporter vid kritiska problem
- Grafana dashboard för trendanalys

---

## Best Practices

### 1. Kör tester regelbundet

```bash
# Varje morgon
python test_agent_hemsida.py

# Innan commit
git add .
python test_agent_hemsida.py --quick
git commit -m "Fix layout issues"
```

### 2. Åtgärda kritiska fel först

Prioritering:
1. **Fel (✗):** Måste fixas omedelbart
2. **Varningar (⚠):** Bör fixas inom kort
3. **Pass (✓):** Fortsätt som vanligt

### 3. Spara testrapporter

```bash
# Skapa mapp för historik
mkdir test_reports
mv TEST_RAPPORT_*.md test_reports/

# Jämför över tid
diff test_reports/TEST_RAPPORT_20251030_*.md test_reports/TEST_RAPPORT_20251031_*.md
```

### 4. Dokumentera kända problem

Om ett test alltid failar men det är acceptabelt:
```python
# I koden
if result.test_name == "known_issue_xyz" and result.status == "fail":
    result.status = "warning"
    result.message += " (Känt problem, accepterat)"
```

---

## Kontakt och Support

**Agent utvecklad av:** Claude Code
**Version:** 1.0
**Datum:** 2025-10-31

För frågor eller förbättringsförslag, uppdatera agenten direkt eller skapa en ny version.

---

## Licens

Fri att använda och modifiera för Hemsida-projektet.

---

## Changelog

### v1.0 (2025-10-31)
- ✓ Initial release
- ✓ HTML-struktur validering
- ✓ Resurs path-kontroller
- ✓ Navigation testing
- ✓ MathJax formula-validering
- ✓ CSS layout-fix verifiering
- ✓ Färgkodad terminal output
- ✓ Markdown rapport-generering
- ✓ Windows UTF-8 encoding fix

---

**Slutsats:** Med Hemsida Testningsagent behöver du aldrig mer manuellt kontrollera 125+ sidor. Låt agenten göra jobbet åt dig! 🚀
