#!/usr/bin/env python3
"""
Automatisk Hemsida Testningsagent
==================================

En omfattande agent som kontrollerar visuell kvalitet, layout, tillgänglighet
och innehåll på alla kurssidor.

Användning:
    python test_agent_hemsida.py                    # Kör alla tester
    python test_agent_hemsida.py --quick           # Snabb kontroll
    python test_agent_hemsida.py --course mat-3c   # Testa specifik kurs
    python test_agent_hemsida.py --verbose         # Detaljerad output

Författare: Claude Code
Version: 1.0
"""

import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Set
from dataclasses import dataclass, field
from datetime import datetime
from bs4 import BeautifulSoup
import json

# ANSI färgkoder för terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

@dataclass
class TestResult:
    """Representerar resultatet av ett enskilt test"""
    test_name: str
    status: str  # 'pass', 'warning', 'fail'
    message: str
    file_path: str = ""
    line_number: int = 0
    details: Dict = field(default_factory=dict)

@dataclass
class TestReport:
    """Sammanfattar alla testresultat"""
    total_tests: int = 0
    passed: int = 0
    warnings: int = 0
    failed: int = 0
    results: List[TestResult] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def add_result(self, result: TestResult):
        """Lägg till ett testresultat och uppdatera statistik"""
        self.results.append(result)
        self.total_tests += 1
        if result.status == 'pass':
            self.passed += 1
        elif result.status == 'warning':
            self.warnings += 1
        elif result.status == 'fail':
            self.failed += 1

    def get_score(self) -> float:
        """Beräkna totalt poäng (0-100)"""
        if self.total_tests == 0:
            return 0.0
        # Varningar räknas som 50% godkänt
        return ((self.passed + self.warnings * 0.5) / self.total_tests) * 100

class HemsidaTestAgent:
    """Huvudklassen för testningsagenten"""

    def __init__(self, base_dir: str = "C:/claude/Hemsida", verbose: bool = False):
        self.base_dir = Path(base_dir)
        self.verbose = verbose
        self.report = TestReport()

        # Kurser att testa
        self.courses = {
            'matematik-1b': {'chapters': 0, 'sections': []},  # Tom för nu
            'matematik-1c': {'chapters': 0, 'sections': []},
            'matematik-2b': {'chapters': 0, 'sections': []},
            'matematik-2c': {'chapters': 6, 'sections': []},  # 86+ sektioner
            'matematik-3b': {'chapters': 0, 'sections': []},
            'matematik-3c': {'chapters': 6, 'sections': []},  # 39 sektioner
            'fysik-1': {'chapters': 0, 'sections': []},
            'fysik-2': {'chapters': 0, 'sections': []},
        }

        # Design system färger (för kontrastkontroll)
        self.color_palette = {
            'primary-blue': '#2563EB',
            'primary-dark': '#1E40AF',
            'accent-orange': '#B45309',  # WCAG-kompatibel
            'old-accent-orange': '#F59E0B',  # WCAG-FAIL
            'white': '#FFFFFF',
            'gray-900': '#111827',
        }

        # Förväntade sektioner för Matematik 3c (baserat på tidigare analys)
        self.expected_sections_3c = {
            'kap1': 5,  # Rationella uttryck
            'kap2': 5,  # Derivatans definition
            'kap3': 7,  # Derivatan
            'kap4': 7,  # Derivatan och funktioner
            'kap5': 7,  # Integraler
            'kap6': 8,  # Trigonometri
        }

    def print_status(self, message: str, level: str = 'info'):
        """Skriv ut färgkodad status"""
        # Sätt encoding till UTF-8 för Windows-kompatibilitet
        import sys
        if sys.platform == 'win32':
            sys.stdout.reconfigure(encoding='utf-8')

        if level == 'success':
            print(f"{Colors.OKGREEN}✓ {message}{Colors.ENDC}")
        elif level == 'warning':
            print(f"{Colors.WARNING}⚠ {message}{Colors.ENDC}")
        elif level == 'error':
            print(f"{Colors.FAIL}✗ {message}{Colors.ENDC}")
        elif level == 'info':
            print(f"{Colors.OKCYAN}ℹ {message}{Colors.ENDC}")
        elif level == 'header':
            print(f"\n{Colors.BOLD}{Colors.HEADER}{'='*70}{Colors.ENDC}")
            print(f"{Colors.BOLD}{Colors.HEADER}{message}{Colors.ENDC}")
            print(f"{Colors.BOLD}{Colors.HEADER}{'='*70}{Colors.ENDC}\n")

    def discover_sections(self, course_name: str) -> List[Path]:
        """Hitta alla HTML-sektioner för en given kurs"""
        sections_dir = self.base_dir / course_name / "sections"
        if not sections_dir.exists():
            return []

        # Hitta alla HTML-filer som matchar kap[X]-[XX].html mönster
        html_files = []
        for file in sections_dir.glob("*.html"):
            if re.match(r'kap\d+-\d+\.html', file.name):
                html_files.append(file)

        return sorted(html_files)

    def test_file_exists(self, file_path: Path, description: str) -> TestResult:
        """Testa om en fil existerar"""
        if file_path.exists():
            return TestResult(
                test_name="file_exists",
                status="pass",
                message=f"{description} finns",
                file_path=str(file_path)
            )
        else:
            return TestResult(
                test_name="file_exists",
                status="fail",
                message=f"{description} saknas: {file_path.name}",
                file_path=str(file_path)
            )

    def test_html_structure(self, html_file: Path) -> List[TestResult]:
        """Testa HTML-struktur och semantik"""
        results = []

        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
                soup = BeautifulSoup(content, 'html.parser')

            # Test 1: DOCTYPE
            if content.strip().startswith('<!DOCTYPE html>'):
                results.append(TestResult(
                    test_name="doctype",
                    status="pass",
                    message="DOCTYPE korrekt deklarerad",
                    file_path=str(html_file)
                ))
            else:
                results.append(TestResult(
                    test_name="doctype",
                    status="fail",
                    message="DOCTYPE saknas eller felaktig",
                    file_path=str(html_file)
                ))

            # Test 2: Lang attribut
            html_tag = soup.find('html')
            if html_tag and html_tag.get('lang') == 'sv':
                results.append(TestResult(
                    test_name="lang_attribute",
                    status="pass",
                    message="Språkattribut korrekt (sv)",
                    file_path=str(html_file)
                ))
            else:
                results.append(TestResult(
                    test_name="lang_attribute",
                    status="fail",
                    message="Språkattribut saknas eller felaktigt",
                    file_path=str(html_file)
                ))

            # Test 3: Semantiska element
            required_elements = ['header', 'nav', 'main', 'footer']
            for element in required_elements:
                if soup.find(element):
                    results.append(TestResult(
                        test_name=f"semantic_{element}",
                        status="pass",
                        message=f"<{element}> element finns",
                        file_path=str(html_file)
                    ))
                else:
                    results.append(TestResult(
                        test_name=f"semantic_{element}",
                        status="warning",
                        message=f"<{element}> element saknas",
                        file_path=str(html_file)
                    ))

            # Test 4: Skip-to-content länk
            skip_link = soup.find('a', class_='skip-link')
            if skip_link and skip_link.get('href') == '#main-content':
                results.append(TestResult(
                    test_name="skip_link",
                    status="pass",
                    message="Skip-to-content länk finns och fungerar",
                    file_path=str(html_file)
                ))
            else:
                results.append(TestResult(
                    test_name="skip_link",
                    status="fail",
                    message="Skip-to-content länk saknas eller felaktig",
                    file_path=str(html_file)
                ))

            # Test 5: Title tag
            title = soup.find('title')
            if title and title.text.strip():
                results.append(TestResult(
                    test_name="title",
                    status="pass",
                    message=f"Titel finns: {title.text[:50]}...",
                    file_path=str(html_file)
                ))
            else:
                results.append(TestResult(
                    test_name="title",
                    status="fail",
                    message="Title tag saknas eller tom",
                    file_path=str(html_file)
                ))

        except Exception as e:
            results.append(TestResult(
                test_name="html_parsing",
                status="fail",
                message=f"Kunde inte parsa HTML: {str(e)}",
                file_path=str(html_file)
            ))

        return results

    def test_resource_paths(self, html_file: Path) -> List[TestResult]:
        """Testa att CSS, JS och bildlänkar fungerar"""
        results = []

        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f, 'html.parser')

            # Test CSS-länkar
            css_links = soup.find_all('link', rel='stylesheet')
            for link in css_links:
                href = link.get('href', '')
                if href.startswith('http'):
                    # Extern länk (CDN) - skippa
                    continue

                # Resolvera relativ path
                css_path = (html_file.parent / href).resolve()
                if css_path.exists():
                    results.append(TestResult(
                        test_name="css_path",
                        status="pass",
                        message=f"CSS finns: {href}",
                        file_path=str(html_file)
                    ))
                else:
                    results.append(TestResult(
                        test_name="css_path",
                        status="fail",
                        message=f"CSS saknas: {href}",
                        file_path=str(html_file),
                        details={'expected_path': str(css_path)}
                    ))

            # Test JS-scripts (lokala)
            scripts = soup.find_all('script', src=True)
            for script in scripts:
                src = script.get('src', '')
                if src.startswith('http'):
                    # Extern länk - skippa
                    continue

                js_path = (html_file.parent / src).resolve()
                if js_path.exists():
                    results.append(TestResult(
                        test_name="js_path",
                        status="pass",
                        message=f"JS finns: {src}",
                        file_path=str(html_file)
                    ))
                else:
                    results.append(TestResult(
                        test_name="js_path",
                        status="fail",
                        message=f"JS saknas: {src}",
                        file_path=str(html_file),
                        details={'expected_path': str(js_path)}
                    ))

            # Test bildlänkar
            images = soup.find_all('img')
            for img in images:
                src = img.get('src', '')
                if src.startswith('http') or src.startswith('data:'):
                    continue

                img_path = (html_file.parent / src).resolve()
                alt = img.get('alt', '')

                if img_path.exists():
                    results.append(TestResult(
                        test_name="image_path",
                        status="pass",
                        message=f"Bild finns: {src}",
                        file_path=str(html_file)
                    ))

                    # Kontrollera alt-text
                    if alt.strip():
                        results.append(TestResult(
                            test_name="image_alt",
                            status="pass",
                            message=f"Alt-text finns: {alt[:30]}...",
                            file_path=str(html_file)
                        ))
                    else:
                        results.append(TestResult(
                            test_name="image_alt",
                            status="warning",
                            message=f"Alt-text saknas för bild: {src}",
                            file_path=str(html_file)
                        ))
                else:
                    results.append(TestResult(
                        test_name="image_path",
                        status="fail",
                        message=f"Bild saknas: {src}",
                        file_path=str(html_file),
                        details={'expected_path': str(img_path)}
                    ))

        except Exception as e:
            results.append(TestResult(
                test_name="resource_parsing",
                status="fail",
                message=f"Kunde inte kontrollera resurser: {str(e)}",
                file_path=str(html_file)
            ))

        return results

    def test_navigation_structure(self, html_file: Path) -> List[TestResult]:
        """Testa navigationens struktur och länkar"""
        results = []

        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f, 'html.parser')

            # Test 1: Huvudnavigation
            main_nav = soup.find('nav', class_='main-nav')
            if main_nav:
                results.append(TestResult(
                    test_name="main_nav",
                    status="pass",
                    message="Huvudnavigation finns",
                    file_path=str(html_file)
                ))

                # Test 2: "← Alla kurser" länk
                all_courses_link = main_nav.find('a', string=re.compile(r'.*Alla kurser.*'))
                if all_courses_link:
                    href = all_courses_link.get('href', '')
                    if href == '../../index.html':
                        results.append(TestResult(
                            test_name="all_courses_link",
                            status="pass",
                            message="'Alla kurser' länk korrekt",
                            file_path=str(html_file)
                        ))
                    else:
                        results.append(TestResult(
                            test_name="all_courses_link",
                            status="warning",
                            message=f"'Alla kurser' länk felaktig: {href}",
                            file_path=str(html_file)
                        ))

                # Test 3: Dropdown-menyer
                dropdowns = main_nav.find_all('li', class_='dropdown')
                if len(dropdowns) >= 3:  # Minst "Byt kurs" + 2 kapitel
                    results.append(TestResult(
                        test_name="dropdown_menus",
                        status="pass",
                        message=f"{len(dropdowns)} dropdown-menyer finns",
                        file_path=str(html_file)
                    ))
                else:
                    results.append(TestResult(
                        test_name="dropdown_menus",
                        status="warning",
                        message=f"Endast {len(dropdowns)} dropdown-menyer (förväntat ≥3)",
                        file_path=str(html_file)
                    ))
            else:
                results.append(TestResult(
                    test_name="main_nav",
                    status="fail",
                    message="Huvudnavigation saknas",
                    file_path=str(html_file)
                ))

            # Test 4: Section navigation (föregående/nästa)
            section_nav = soup.find('div', class_='section-navigation')
            if section_nav:
                prev_link = section_nav.find('a', class_='prev')
                next_link = section_nav.find('a', class_='next')

                if prev_link or next_link:
                    results.append(TestResult(
                        test_name="section_navigation",
                        status="pass",
                        message="Föregående/Nästa navigation finns",
                        file_path=str(html_file)
                    ))
                else:
                    results.append(TestResult(
                        test_name="section_navigation",
                        status="warning",
                        message="Section navigation finns men inga länkar",
                        file_path=str(html_file)
                    ))

        except Exception as e:
            results.append(TestResult(
                test_name="navigation_parsing",
                status="fail",
                message=f"Kunde inte kontrollera navigation: {str(e)}",
                file_path=str(html_file)
            ))

        return results

    def test_content_boxes(self, html_file: Path) -> List[TestResult]:
        """Testa att innehållsboxar använder rätt klasser"""
        results = []

        valid_box_classes = [
            'definition-box',
            'info-box',
            'formula-box',
            'example-box',
            'derivation-box',
            'solution-box',
            'exercise-box',
            'math-figure'
        ]

        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f, 'html.parser')

            # Hitta alla div med box-klasser
            boxes_found = {}
            for box_class in valid_box_classes:
                boxes = soup.find_all(class_=box_class)
                if boxes:
                    boxes_found[box_class] = len(boxes)

            if boxes_found:
                results.append(TestResult(
                    test_name="content_boxes",
                    status="pass",
                    message=f"Innehållsboxar funna: {', '.join(f'{k}({v})' for k,v in boxes_found.items())}",
                    file_path=str(html_file),
                    details={'boxes': boxes_found}
                ))
            else:
                results.append(TestResult(
                    test_name="content_boxes",
                    status="warning",
                    message="Inga standardiserade innehållsboxar funna",
                    file_path=str(html_file)
                ))

        except Exception as e:
            results.append(TestResult(
                test_name="content_boxes_parsing",
                status="fail",
                message=f"Kunde inte kontrollera innehållsboxar: {str(e)}",
                file_path=str(html_file)
            ))

        return results

    def test_mathjax_formulas(self, html_file: Path) -> List[TestResult]:
        """Testa att MathJax-formler är korrekt formaterade"""
        results = []

        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Test 1: MathJax script inkluderad
            if 'mathjax' in content.lower():
                results.append(TestResult(
                    test_name="mathjax_included",
                    status="pass",
                    message="MathJax script inkluderad",
                    file_path=str(html_file)
                ))
            else:
                results.append(TestResult(
                    test_name="mathjax_included",
                    status="warning",
                    message="MathJax script saknas (behövs om formler finns)",
                    file_path=str(html_file)
                ))

            # Test 2: Inline formler ($...$)
            inline_formulas = re.findall(r'\$[^\$]+\$', content)
            if inline_formulas:
                results.append(TestResult(
                    test_name="inline_formulas",
                    status="pass",
                    message=f"{len(inline_formulas)} inline-formler funna",
                    file_path=str(html_file),
                    details={'count': len(inline_formulas)}
                ))

            # Test 3: Display formler ($$...$$)
            display_formulas = re.findall(r'\$\$[^\$]+\$\$', content)
            if display_formulas:
                results.append(TestResult(
                    test_name="display_formulas",
                    status="pass",
                    message=f"{len(display_formulas)} display-formler funna",
                    file_path=str(html_file),
                    details={'count': len(display_formulas)}
                ))

            # Test 4: Obalanserade $-tecken (potentiellt fel)
            dollar_count = content.count('$')
            if dollar_count % 2 != 0:
                results.append(TestResult(
                    test_name="formula_balance",
                    status="warning",
                    message=f"Ojämnt antal $-tecken ({dollar_count}) - möjligt fel",
                    file_path=str(html_file)
                ))

        except Exception as e:
            results.append(TestResult(
                test_name="mathjax_parsing",
                status="fail",
                message=f"Kunde inte kontrollera MathJax: {str(e)}",
                file_path=str(html_file)
            ))

        return results

    def test_css_sticky_nav_fix(self) -> List[TestResult]:
        """Testa att CSS-fixen för sticky navigation är applicerad"""
        results = []

        css_file = self.base_dir / "styles.css"

        if not css_file.exists():
            results.append(TestResult(
                test_name="css_file",
                status="fail",
                message="styles.css saknas",
                file_path=str(css_file)
            ))
            return results

        try:
            with open(css_file, 'r', encoding='utf-8') as f:
                css_content = f.read()

            # Test 1: padding-top fix i main
            if 'padding-top: calc(var(--spacing-2xl) + 2rem)' in css_content:
                results.append(TestResult(
                    test_name="main_padding_fix",
                    status="pass",
                    message="Main padding-top fix applicerad korrekt",
                    file_path=str(css_file)
                ))
            else:
                results.append(TestResult(
                    test_name="main_padding_fix",
                    status="fail",
                    message="Main padding-top fix saknas eller felaktig",
                    file_path=str(css_file)
                ))

            # Test 2: padding-top fix i hero
            if 'padding-top: calc(var(--spacing-3xl) + 2rem)' in css_content:
                results.append(TestResult(
                    test_name="hero_padding_fix",
                    status="pass",
                    message="Hero padding-top fix applicerad korrekt",
                    file_path=str(css_file)
                ))
            else:
                results.append(TestResult(
                    test_name="hero_padding_fix",
                    status="fail",
                    message="Hero padding-top fix saknas eller felaktig",
                    file_path=str(css_file)
                ))

            # Test 3: scroll-margin-top fix
            scroll_margin_match = re.search(r'scroll-margin-top:\s*(\d+)px', css_content)
            if scroll_margin_match:
                scroll_value = int(scroll_margin_match.group(1))
                if scroll_value >= 120:
                    results.append(TestResult(
                        test_name="scroll_margin_fix",
                        status="pass",
                        message=f"scroll-margin-top korrekt satt ({scroll_value}px)",
                        file_path=str(css_file)
                    ))
                else:
                    results.append(TestResult(
                        test_name="scroll_margin_fix",
                        status="warning",
                        message=f"scroll-margin-top för låg ({scroll_value}px, rekommenderat ≥120px)",
                        file_path=str(css_file)
                    ))

            # Test 4: Sticky navigation
            if 'position: sticky' in css_content and '.main-nav' in css_content:
                results.append(TestResult(
                    test_name="sticky_navigation",
                    status="pass",
                    message="Sticky navigation konfigurerad",
                    file_path=str(css_file)
                ))

        except Exception as e:
            results.append(TestResult(
                test_name="css_parsing",
                status="fail",
                message=f"Kunde inte kontrollera CSS: {str(e)}",
                file_path=str(css_file)
            ))

        return results

    def test_encoding(self, html_file: Path) -> List[TestResult]:
        """Testa att filen har korrekt UTF-8 encoding"""
        results = []

        try:
            # Försök läsa med UTF-8
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Kontrollera om det finns replacement characters (tecken på encoding-problem)
            if '�' in content:
                results.append(TestResult(
                    test_name="encoding_utf8",
                    status="fail",
                    message="Filen innehåller replacement characters (�) - encoding-problem",
                    file_path=str(html_file)
                ))
            else:
                results.append(TestResult(
                    test_name="encoding_utf8",
                    status="pass",
                    message="UTF-8 encoding korrekt",
                    file_path=str(html_file)
                ))

        except UnicodeDecodeError as e:
            # Filen är inte UTF-8
            results.append(TestResult(
                test_name="encoding_utf8",
                status="fail",
                message=f"Filen är inte UTF-8 kodad - kör fix_encoding_agent.py",
                file_path=str(html_file),
                details={'error': str(e)}
            ))

        return results

    def run_tests_for_section(self, section_file: Path) -> List[TestResult]:
        """Kör alla tester för en sektion"""
        results = []

        if self.verbose:
            self.print_status(f"Testar: {section_file.name}", 'info')

        # Kör alla testmetoder
        results.extend(self.test_encoding(section_file))
        results.extend(self.test_html_structure(section_file))
        results.extend(self.test_resource_paths(section_file))
        results.extend(self.test_navigation_structure(section_file))
        results.extend(self.test_content_boxes(section_file))
        results.extend(self.test_mathjax_formulas(section_file))

        return results

    def run_tests_for_course(self, course_name: str):
        """Kör alla tester för en kurs"""
        self.print_status(f"Testar kurs: {course_name}", 'header')

        # Hitta alla sektioner
        sections = self.discover_sections(course_name)

        if not sections:
            self.print_status(f"Inga sektioner funna för {course_name}", 'warning')
            return

        self.print_status(f"Hittade {len(sections)} sektioner att testa", 'info')

        # Testa varje sektion
        for section in sections:
            results = self.run_tests_for_section(section)
            for result in results:
                self.report.add_result(result)

        # Sammanfattning för kursen
        course_results = [r for r in self.report.results if course_name in r.file_path]
        course_passed = len([r for r in course_results if r.status == 'pass'])
        course_warnings = len([r for r in course_results if r.status == 'warning'])
        course_failed = len([r for r in course_results if r.status == 'fail'])

        print(f"\n{course_name} sammanfattning:")
        print(f"  {Colors.OKGREEN}✓ Pass: {course_passed}{Colors.ENDC}")
        print(f"  {Colors.WARNING}⚠ Varningar: {course_warnings}{Colors.ENDC}")
        print(f"  {Colors.FAIL}✗ Fel: {course_failed}{Colors.ENDC}")

    def run_all_tests(self, specific_course: str = None):
        """Kör alla tester för alla kurser (eller specifik kurs)"""
        self.print_status("Hemsida Testningsagent v1.0", 'header')
        self.print_status(f"Startar tester: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 'info')

        # Test 1: CSS-fixen
        self.print_status("Testar CSS-fixen för sticky navigation...", 'info')
        css_results = self.test_css_sticky_nav_fix()
        for result in css_results:
            self.report.add_result(result)

        # Test 2: Kurser
        courses_to_test = [specific_course] if specific_course else ['matematik-2c', 'matematik-3c']

        for course in courses_to_test:
            if course in self.courses:
                self.run_tests_for_course(course)

        # Generera slutrapport
        self.generate_report()

    def generate_report(self):
        """Generera och skriv ut slutrapport"""
        self.print_status("TESTRAPPORT", 'header')

        score = self.report.get_score()

        print(f"\n{Colors.BOLD}Totalt:{Colors.ENDC}")
        print(f"  Tester körda: {self.report.total_tests}")
        print(f"  {Colors.OKGREEN}✓ Godkända: {self.report.passed}{Colors.ENDC}")
        print(f"  {Colors.WARNING}⚠ Varningar: {self.report.warnings}{Colors.ENDC}")
        print(f"  {Colors.FAIL}✗ Fel: {self.report.failed}{Colors.ENDC}")
        print(f"\n{Colors.BOLD}Poäng: {score:.1f}/100{Colors.ENDC}")

        # Betyg
        if score >= 90:
            grade = f"{Colors.OKGREEN}A - Utmärkt{Colors.ENDC}"
        elif score >= 80:
            grade = f"{Colors.OKGREEN}B - Mycket bra{Colors.ENDC}"
        elif score >= 70:
            grade = f"{Colors.WARNING}C - Godkänt{Colors.ENDC}"
        elif score >= 60:
            grade = f"{Colors.WARNING}D - Godkänt med anmärkningar{Colors.ENDC}"
        else:
            grade = f"{Colors.FAIL}F - Underkänt{Colors.ENDC}"

        print(f"Betyg: {grade}\n")

        # Visa kritiska fel
        critical_failures = [r for r in self.report.results if r.status == 'fail']
        if critical_failures:
            print(f"\n{Colors.FAIL}{Colors.BOLD}KRITISKA FEL ({len(critical_failures)}):{Colors.ENDC}")
            for i, failure in enumerate(critical_failures[:10], 1):  # Visa max 10
                print(f"  {i}. {failure.message}")
                if failure.file_path:
                    print(f"     Fil: {Path(failure.file_path).name}")

            if len(critical_failures) > 10:
                print(f"  ... och {len(critical_failures) - 10} fler")

        # Spara rapport till fil
        self.save_report_to_file()

    def save_report_to_file(self):
        """Spara detaljerad rapport till markdown-fil"""
        report_file = self.base_dir / f"TEST_RAPPORT_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"

        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(f"# Hemsida Testrapport\n\n")
            f.write(f"**Datum:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"**Poäng:** {self.report.get_score():.1f}/100\n\n")

            f.write(f"## Sammanfattning\n\n")
            f.write(f"- **Totalt tester:** {self.report.total_tests}\n")
            f.write(f"- **Godkända:** {self.report.passed} ✓\n")
            f.write(f"- **Varningar:** {self.report.warnings} ⚠\n")
            f.write(f"- **Fel:** {self.report.failed} ✗\n\n")

            # Gruppera resultat per fil
            files_tested = {}
            for result in self.report.results:
                file_key = result.file_path if result.file_path else "Global"
                if file_key not in files_tested:
                    files_tested[file_key] = []
                files_tested[file_key].append(result)

            f.write(f"## Detaljerade resultat\n\n")

            for file_path, results in files_tested.items():
                f.write(f"### {Path(file_path).name if file_path != 'Global' else 'Globala tester'}\n\n")

                for result in results:
                    status_icon = "✓" if result.status == "pass" else ("⚠" if result.status == "warning" else "✗")
                    f.write(f"- {status_icon} **{result.test_name}:** {result.message}\n")

                f.write("\n")

        self.print_status(f"Rapport sparad: {report_file.name}", 'success')

def main():
    """Huvudfunktion"""
    import argparse

    parser = argparse.ArgumentParser(description='Hemsida Testningsagent')
    parser.add_argument('--course', type=str, help='Testa specifik kurs (t.ex. matematik-3c)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Detaljerad output')
    parser.add_argument('--quick', action='store_true', help='Snabbtester (endast kritiska)')

    args = parser.parse_args()

    agent = HemsidaTestAgent(verbose=args.verbose)

    if args.course:
        agent.run_all_tests(specific_course=args.course)
    else:
        agent.run_all_tests()

if __name__ == "__main__":
    main()
