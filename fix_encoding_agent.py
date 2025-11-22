#!/usr/bin/env python3
"""
Autonom Encoding-Fix Agent
===========================

Denna agent hittar och fixar automatiskt alla encoding-problem (å, ä, ö)
på hemsidan utan manuell intervention.

Funktioner:
- Skannar alla HTML-filer i alla kurser
- Upptäcker ISO-8859-1/Windows-1252 encoding
- Konverterar automatiskt till UTF-8
- Verifierar att svenska tecken renderas korrekt
- Skapar backup innan ändringar
- Genererar detaljerad rapport

Användning:
    python fix_encoding_agent.py                  # Fixa alla kurser
    python fix_encoding_agent.py --course mat-2c  # Fixa specifik kurs
    python fix_encoding_agent.py --dry-run        # Testa utan att ändra
    python fix_encoding_agent.py --no-backup      # Skippa backup

Författare: Claude Code
Version: 1.0
"""

import os
import sys
import shutil
from pathlib import Path
from typing import List, Tuple, Dict
from dataclasses import dataclass, field
from datetime import datetime
import re

# Sätt encoding för Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Färgkoder
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

@dataclass
class EncodingIssue:
    """Representerar ett encoding-problem"""
    file_path: Path
    current_encoding: str
    target_encoding: str = "UTF-8"
    status: str = "pending"  # pending, fixed, failed, skipped
    error_message: str = ""
    swedish_chars_found: List[str] = field(default_factory=list)

@dataclass
class FixReport:
    """Rapport över alla fixar"""
    total_files_scanned: int = 0
    files_with_issues: int = 0
    files_fixed: int = 0
    files_failed: int = 0
    files_skipped: int = 0
    issues: List[EncodingIssue] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

class EncodingFixAgent:
    """Autonom agent för att fixa encoding-problem"""

    def __init__(self, base_dir: str = "C:/claude/Hemsida", dry_run: bool = False,
                 create_backup: bool = True, verbose: bool = False):
        self.base_dir = Path(base_dir)
        self.dry_run = dry_run
        self.create_backup = create_backup
        self.verbose = verbose
        self.report = FixReport()

        # Kurser att kontrollera
        self.courses = [
            'matematik-1b', 'matematik-1c', 'matematik-2b',
            'matematik-2c', 'matematik-3b', 'matematik-3c',
            'fysik-1', 'fysik-2'
        ]

        # Encoding att testa (i prioritetsordning)
        self.encodings_to_try = [
            'utf-8',
            'iso-8859-1',
            'windows-1252',
            'cp1252',
        ]

        # Svenska tecken att leta efter
        self.swedish_chars = ['å', 'ä', 'ö', 'Å', 'Ä', 'Ö']

    def print_status(self, message: str, level: str = 'info'):
        """Skriv ut färgkodad status"""
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

    def detect_encoding(self, file_path: Path) -> Tuple[str, str]:
        """
        Upptäck vilken encoding en fil har
        Returnerar: (detected_encoding, content)
        """
        for encoding in self.encodings_to_try:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    content = f.read()

                # Verifiera att det inte finns felaktiga replacement characters
                if '�' in content:
                    continue

                return (encoding, content)
            except (UnicodeDecodeError, UnicodeError):
                continue

        # Om ingen encoding fungerade
        return (None, None)

    def find_swedish_chars(self, content: str) -> List[str]:
        """Hitta alla svenska tecken i innehållet"""
        found = []
        for char in self.swedish_chars:
            if char in content:
                found.append(char)
        return list(set(found))

    def scan_file(self, file_path: Path) -> EncodingIssue:
        """Skanna en fil för encoding-problem"""
        self.report.total_files_scanned += 1

        # Försök läsa med UTF-8 först
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Kontrollera om det finns felaktiga replacement characters
            if '�' not in content:
                # Filen är redan korrekt UTF-8
                swedish = self.find_swedish_chars(content)
                if self.verbose and swedish:
                    self.print_status(
                        f"{file_path.name}: OK (UTF-8) - svenska tecken: {', '.join(swedish)}",
                        'success'
                    )
                return None
        except (UnicodeDecodeError, UnicodeError):
            pass

        # Filen har encoding-problem, upptäck korrekt encoding
        detected_encoding, content = self.detect_encoding(file_path)

        if detected_encoding and detected_encoding != 'utf-8':
            swedish = self.find_swedish_chars(content)
            issue = EncodingIssue(
                file_path=file_path,
                current_encoding=detected_encoding,
                swedish_chars_found=swedish
            )
            self.report.files_with_issues += 1
            self.print_status(
                f"{file_path.name}: Encoding-problem ({detected_encoding} → UTF-8) - "
                f"svenska tecken: {', '.join(swedish) if swedish else 'inga'}",
                'warning'
            )
            return issue
        elif not detected_encoding:
            # Kunde inte läsa filen med någon encoding
            issue = EncodingIssue(
                file_path=file_path,
                current_encoding="unknown",
                status="failed",
                error_message="Kunde inte detektera encoding"
            )
            self.report.files_failed += 1
            self.print_status(f"{file_path.name}: Kunde inte läsa filen", 'error')
            return issue

        return None

    def fix_file(self, issue: EncodingIssue) -> bool:
        """Fixa encoding för en fil"""
        try:
            # Läs med korrekt encoding
            with open(issue.file_path, 'r', encoding=issue.current_encoding) as f:
                content = f.read()

            # Skapa backup om önskat
            if self.create_backup and not self.dry_run:
                backup_path = issue.file_path.with_suffix('.html.bak')
                shutil.copy2(issue.file_path, backup_path)
                if self.verbose:
                    self.print_status(f"Backup skapad: {backup_path.name}", 'info')

            # Skriv om till UTF-8
            if not self.dry_run:
                with open(issue.file_path, 'w', encoding='utf-8') as f:
                    f.write(content)

                # Verifiera att det fungerade
                with open(issue.file_path, 'r', encoding='utf-8') as f:
                    verified_content = f.read()

                if verified_content == content:
                    issue.status = "fixed"
                    self.report.files_fixed += 1
                    self.print_status(f"{issue.file_path.name}: Fixad! ✓", 'success')
                    return True
                else:
                    issue.status = "failed"
                    issue.error_message = "Verifiering misslyckades"
                    self.report.files_failed += 1
                    self.print_status(f"{issue.file_path.name}: Verifiering misslyckades", 'error')
                    return False
            else:
                # Dry run - simulera fix
                issue.status = "skipped"
                self.report.files_skipped += 1
                self.print_status(
                    f"{issue.file_path.name}: Skulle fixas (dry-run mode)",
                    'info'
                )
                return True

        except Exception as e:
            issue.status = "failed"
            issue.error_message = str(e)
            self.report.files_failed += 1
            self.print_status(f"{issue.file_path.name}: Fel vid fix - {str(e)}", 'error')
            return False

    def scan_course(self, course_name: str) -> List[EncodingIssue]:
        """Skanna alla HTML-filer i en kurs"""
        issues = []
        sections_dir = self.base_dir / course_name / "sections"

        if not sections_dir.exists():
            if self.verbose:
                self.print_status(f"{course_name}: Ingen sections-mapp", 'info')
            return issues

        html_files = sorted(sections_dir.glob("*.html"))

        if not html_files:
            if self.verbose:
                self.print_status(f"{course_name}: Inga HTML-filer", 'info')
            return issues

        self.print_status(f"Skannar {course_name}: {len(html_files)} filer...", 'header')

        for html_file in html_files:
            issue = self.scan_file(html_file)
            if issue:
                issues.append(issue)

        return issues

    def run(self, specific_course: str = None):
        """Kör agenten"""
        self.print_status("Autonom Encoding-Fix Agent v1.0", 'header')
        self.print_status(
            f"Mode: {'DRY RUN (inga ändringar)' if self.dry_run else 'LIVE (kommer att ändra filer)'}",
            'warning' if not self.dry_run else 'info'
        )
        self.print_status(
            f"Backup: {'Aktiverad' if self.create_backup else 'Inaktiverad'}",
            'info'
        )

        # Skanna kurser
        courses_to_scan = [specific_course] if specific_course else self.courses

        all_issues = []
        for course in courses_to_scan:
            if course in self.courses or specific_course:
                issues = self.scan_course(course)
                all_issues.extend(issues)
                self.report.issues.extend(issues)

        # Fixa problem
        if all_issues:
            self.print_status(f"\nHittade {len(all_issues)} filer med encoding-problem", 'warning')
            self.print_status("Startar automatisk fix...", 'info')

            for issue in all_issues:
                if issue.status != "failed":
                    self.fix_file(issue)

        # Generera rapport
        self.generate_report()

    def generate_report(self):
        """Generera slutrapport"""
        self.print_status("RAPPORT", 'header')

        print(f"\n{Colors.BOLD}Sammanfattning:{Colors.ENDC}")
        print(f"  Filer skannade: {self.report.total_files_scanned}")
        print(f"  {Colors.WARNING}Problem hittade: {self.report.files_with_issues}{Colors.ENDC}")
        print(f"  {Colors.OKGREEN}Fixade: {self.report.files_fixed}{Colors.ENDC}")
        print(f"  {Colors.FAIL}Misslyckades: {self.report.files_failed}{Colors.ENDC}")

        if self.dry_run:
            print(f"  {Colors.OKCYAN}Skulle fixas (dry-run): {self.report.files_skipped}{Colors.ENDC}")

        # Visa detaljer om fixade filer
        if self.report.files_fixed > 0:
            print(f"\n{Colors.OKGREEN}{Colors.BOLD}FIXADE FILER:{Colors.ENDC}")
            for issue in self.report.issues:
                if issue.status == "fixed":
                    swedish = ', '.join(issue.swedish_chars_found) if issue.swedish_chars_found else 'inga'
                    print(f"  ✓ {issue.file_path.name}")
                    print(f"    {issue.current_encoding} → UTF-8")
                    print(f"    Svenska tecken: {swedish}")

        # Visa detaljer om misslyckade
        if self.report.files_failed > 0:
            print(f"\n{Colors.FAIL}{Colors.BOLD}MISSLYCKADE FILER:{Colors.ENDC}")
            for issue in self.report.issues:
                if issue.status == "failed":
                    print(f"  ✗ {issue.file_path.name}")
                    print(f"    Fel: {issue.error_message}")

        # Spara rapport till fil
        self.save_report_to_file()

    def save_report_to_file(self):
        """Spara rapport till markdown-fil"""
        report_file = self.base_dir / f"ENCODING_FIX_RAPPORT_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"

        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(f"# Encoding-Fix Rapport\n\n")
            f.write(f"**Datum:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Mode:** {'Dry-run' if self.dry_run else 'Live'}\n\n")

            f.write(f"## Sammanfattning\n\n")
            f.write(f"- **Filer skannade:** {self.report.total_files_scanned}\n")
            f.write(f"- **Problem hittade:** {self.report.files_with_issues}\n")
            f.write(f"- **Fixade:** {self.report.files_fixed}\n")
            f.write(f"- **Misslyckades:** {self.report.files_failed}\n")
            if self.dry_run:
                f.write(f"- **Skulle fixas:** {self.report.files_skipped}\n")
            f.write("\n")

            # Fixade filer
            if self.report.files_fixed > 0:
                f.write(f"## Fixade filer ({self.report.files_fixed})\n\n")
                for issue in self.report.issues:
                    if issue.status == "fixed":
                        f.write(f"### {issue.file_path.name}\n\n")
                        f.write(f"- **Före:** {issue.current_encoding}\n")
                        f.write(f"- **Efter:** UTF-8\n")
                        f.write(f"- **Svenska tecken:** {', '.join(issue.swedish_chars_found) if issue.swedish_chars_found else 'inga'}\n")
                        f.write(f"- **Status:** ✓ Fixad\n\n")

            # Misslyckade
            if self.report.files_failed > 0:
                f.write(f"## Misslyckade filer ({self.report.files_failed})\n\n")
                for issue in self.report.issues:
                    if issue.status == "failed":
                        f.write(f"### {issue.file_path.name}\n\n")
                        f.write(f"- **Fel:** {issue.error_message}\n\n")

            # Backup-information
            if self.create_backup and not self.dry_run and self.report.files_fixed > 0:
                f.write(f"## Backup-filer\n\n")
                f.write(f"Backup-filer har skapats med `.bak`-ändelse.\n")
                f.write(f"För att återställa en fil:\n")
                f.write(f"```bash\n")
                f.write(f"mv filnamn.html.bak filnamn.html\n")
                f.write(f"```\n\n")

        self.print_status(f"Rapport sparad: {report_file.name}", 'success')

def main():
    """Huvudfunktion"""
    import argparse

    parser = argparse.ArgumentParser(description='Autonom Encoding-Fix Agent')
    parser.add_argument('--course', type=str, help='Fixa specifik kurs (t.ex. matematik-2c)')
    parser.add_argument('--dry-run', action='store_true', help='Testa utan att ändra filer')
    parser.add_argument('--no-backup', action='store_true', help='Skippa backup av filer')
    parser.add_argument('--verbose', '-v', action='store_true', help='Detaljerad output')

    args = parser.parse_args()

    agent = EncodingFixAgent(
        dry_run=args.dry_run,
        create_backup=not args.no_backup,
        verbose=args.verbose
    )

    agent.run(specific_course=args.course)

if __name__ == "__main__":
    main()
