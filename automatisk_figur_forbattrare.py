"""
AUTOMATISK FIGUR FÖRBÄTTRARE
Går igenom alla befintliga figurer och förbättrar dem systematiskt
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Arc, FancyArrowPatch, Polygon, Circle, Rectangle, Wedge
import os
import re
from pathlib import Path

# Konfigurera matplotlib
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans']

class FigurForfattare:
    """Automatisk förbättrare för matematiska figurer"""

    def __init__(self, html_file='index.html'):
        self.html_file = html_file
        self.figurer_att_forbattra = []
        self.rapport = []

    def identifiera_alla_figurer(self):
        """Hitta alla img-taggar och graph-containers i HTML"""
        print("="*60)
        print("IDENTIFIERAR ALLA FIGURER I HEMSIDAN")
        print("="*60)

        with open(self.html_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Hitta alla img src
        img_pattern = r'<img\s+src="([^"]+)"'
        images = re.findall(img_pattern, content)

        # Hitta alla avsnitt och deras figurer
        section_pattern = r'<section id="(kap\d-\d\d)".*?(?=<section id=|</main>)'
        sections = re.findall(section_pattern, content, re.DOTALL)

        for section_id in ['kap1-01', 'kap1-02', 'kap1-03', 'kap1-04', 'kap1-05',
                          'kap2-01', 'kap2-02', 'kap2-03', 'kap2-04', 'kap2-05',
                          'kap3-01', 'kap3-02', 'kap3-03', 'kap3-04', 'kap3-05', 'kap3-06', 'kap3-07',
                          'kap4-01', 'kap4-02', 'kap4-03', 'kap4-04', 'kap4-05', 'kap4-06', 'kap4-07',
                          'kap5-01', 'kap5-02', 'kap5-03', 'kap5-04', 'kap5-05', 'kap5-06', 'kap5-07',
                          'kap6-01', 'kap6-02', 'kap6-03', 'kap6-04', 'kap6-05', 'kap6-06', 'kap6-07', 'kap6-08']:

            match = re.search(rf'<section id="{section_id}"(.*?)(?=<section id=|</main>)', content, re.DOTALL)
            if match:
                section_content = match.group(1)

                # Hitta titel
                title_match = re.search(r'<h2>(.*?)</h2>', section_content)
                title = title_match.group(1) if title_match else section_id

                # Hitta bilder i detta avsnitt
                section_images = re.findall(r'<img\s+src="([^"]+)"', section_content)

                for img_src in section_images:
                    self.figurer_att_forbattra.append({
                        'section_id': section_id,
                        'title': title,
                        'img_src': img_src,
                        'img_path': Path(img_src),
                        'exists': Path(img_src).exists()
                    })

        print(f"\nHittade {len(self.figurer_att_forbattra)} figurer att analysera")
        return self.figurer_att_forbattra

    def analysera_figur(self, figur_info):
        """Analysera en figur och bedöm om den behöver förbättras"""
        img_path = figur_info['img_path']

        # Kontrollera om filen finns
        if not img_path.exists():
            return {
                'status': 'SAKNAS',
                'prioritet': 'KRITISK',
                'beskrivning': f"Filen finns inte: {img_path}",
                'rekommendation': 'Skapa figur från scratch'
            }

        # Kontrollera filtyp och storlek
        file_ext = img_path.suffix.lower()
        file_size = img_path.stat().st_size if img_path.exists() else 0

        problem = []

        # SVG-filer från AI-generering är misstänkta
        if 'gemini' in str(img_path).lower() or 'generated' in str(img_path).lower():
            problem.append("AI-genererad (misstänkt felaktig)")

        # Kontrollera filstorlek
        if file_size > 500000:  # > 500KB
            problem.append(f"För stor fil ({file_size//1000}KB)")

        if file_size < 1000:  # < 1KB
            problem.append(f"Misstänkt liten fil ({file_size}B)")

        # Baserat på avsnitt, identifiera typ av figur
        section_id = figur_info['section_id']
        title = figur_info['title'].lower()

        # Kategorisera vad som behövs
        figur_typ = self._identifiera_figur_typ(section_id, title)

        if problem:
            return {
                'status': 'BEHÖVER FÖRBÄTTRAS',
                'prioritet': 'VIKTIG',
                'beskrivning': ', '.join(problem),
                'figur_typ': figur_typ,
                'rekommendation': f'Återskapa med matplotlib som {figur_typ}'
            }

        return {
            'status': 'OK (preliminärt)',
            'prioritet': 'LÅG',
            'beskrivning': 'Inga uppenbara problem',
            'figur_typ': figur_typ,
            'rekommendation': 'Manuell granskning rekommenderas'
        }

    def _identifiera_figur_typ(self, section_id, title):
        """Identifiera vilken typ av figur som behövs baserat på avsnitt"""

        # Kapitel 1: Rationella uttryck
        if section_id.startswith('kap1'):
            if '1.1' in section_id or 'förkortning' in title:
                return 'bråkförkortning'
            elif '1.2' in section_id or 'addition' in title:
                return 'bråkaddition'
            elif '1.4' in section_id or 'gränsvärde' in title:
                return 'gränsvärde_graf'

        # Kapitel 2: Derivatan
        elif section_id.startswith('kap2'):
            if '2.1' in section_id or 'sekant' in title:
                return 'sekant_lutning'
            elif '2.2' in section_id or 'tangent' in title:
                return 'tangent_derivata'
            elif '2.3' in section_id or 'definition' in title:
                return 'derivata_definition'

        # Kapitel 3: Derivatan av funktioner
        elif section_id.startswith('kap3'):
            if '3.1' in section_id or 'potens' in title:
                return 'potensfunktion_derivata'
            elif '3.2' in section_id or 'produkt' in title:
                return 'produktregeln'
            elif '3.3' in section_id or 'kvot' in title:
                return 'kvotregeln'
            elif '3.4' in section_id or 'e^x' in title:
                return 'exp_funktion'
            elif '3.5' in section_id or 'kedja' in title:
                return 'kedjeregeln'

        # Kapitel 4: Kurvanalys
        elif section_id.startswith('kap4'):
            if '4.1' in section_id or 'växande' in title:
                return 'monotonitet'
            elif '4.2' in section_id or 'nollställe' in title:
                return 'nollstallen_derivata'
            elif '4.3' in section_id or 'extremvärde' in title:
                return 'extrempunkter'
            elif '4.4' in section_id or 'andraderivata' in title:
                return 'konkavitet'
            elif '4.5' in section_id or 'kurvskiss' in title:
                return 'kurvskissning'

        # Kapitel 5: Integraler
        elif section_id.startswith('kap5'):
            if '5.1' in section_id or 'primitiv' in title:
                return 'primitiv_funktion'
            elif '5.3' in section_id or 'area' in title:
                return 'riemann_summa'
            elif '5.4' in section_id or 'fundamental' in title:
                return 'fundamentalsatsen'
            elif '5.6' in section_id or 'mellan kurvor' in title:
                return 'area_mellan_kurvor'

        # Kapitel 6: Trigonometri
        elif section_id.startswith('kap6'):
            if '6.1' in section_id or 'rätvinklig' in title:
                return 'triangel_ratvinklig'
            elif '6.2' in section_id or 'enhetscirkel' in title:
                return 'enhetscirkel'
            elif '6.5' in section_id or 'areasats' in title:
                return 'areasatsen'
            elif '6.6' in section_id or 'sinussats' in title:
                return 'sinussatsen'
            elif '6.7' in section_id or 'cosinussats' in title:
                return 'cosinussatsen'

        return 'okänd_typ'

    def skapa_rapport(self):
        """Skapa en komplett rapport över alla figurer"""
        print("\n" + "="*60)
        print("SKAPAR RAPPORT")
        print("="*60 + "\n")

        rapport_md = "# AUTOMATISK FIGURGRANSKNING\n\n"
        rapport_md += f"**Datum:** 2025-10-27\n\n"
        rapport_md += "---\n\n"

        # Sammanfattning
        total = len(self.figurer_att_forbattra)
        saknas = sum(1 for f in self.rapport if f['analys']['status'] == 'SAKNAS')
        behover_forbattras = sum(1 for f in self.rapport if f['analys']['status'] == 'BEHÖVER FÖRBÄTTRAS')
        ok = sum(1 for f in self.rapport if f['analys']['status'].startswith('OK'))

        rapport_md += "## 📊 Sammanfattning\n\n"
        rapport_md += f"- **Totalt antal figurer:** {total}\n"
        rapport_md += f"- **Saknas:** {saknas} ({saknas*100//total if total else 0}%)\n"
        rapport_md += f"- **Behöver förbättras:** {behover_forbattras} ({behover_forbattras*100//total if total else 0}%)\n"
        rapport_md += f"- **OK:** {ok} ({ok*100//total if total else 0}%)\n\n"
        rapport_md += "---\n\n"

        # Detaljerad lista
        rapport_md += "## 📋 Detaljerad lista\n\n"

        for figur in self.rapport:
            info = figur['info']
            analys = figur['analys']

            status_emoji = {
                'SAKNAS': '❌',
                'BEHÖVER FÖRBÄTTRAS': '⚠️',
                'OK (preliminärt)': '✅'
            }.get(analys['status'], '❓')

            rapport_md += f"### {status_emoji} {info['section_id']} - {info['title']}\n\n"
            rapport_md += f"**Fil:** `{info['img_src']}`\n\n"
            rapport_md += f"**Status:** {analys['status']}\n\n"
            rapport_md += f"**Prioritet:** {analys['prioritet']}\n\n"
            rapport_md += f"**Figurtyp:** {analys['figur_typ']}\n\n"
            rapport_md += f"**Beskrivning:** {analys['beskrivning']}\n\n"
            rapport_md += f"**Rekommendation:** {analys['rekommendation']}\n\n"
            rapport_md += "---\n\n"

        # Spara rapport
        with open('AUTOMATISK_FIGUR_RAPPORT.md', 'w', encoding='utf-8') as f:
            f.write(rapport_md)

        print(f"Rapport sparad: AUTOMATISK_FIGUR_RAPPORT.md")
        print(f"\nSammanfattning:")
        print(f"  - Totalt: {total}")
        print(f"  - Saknas: {saknas}")
        print(f"  - Behöver förbättras: {behover_forbattras}")
        print(f"  - OK: {ok}")

    def kör(self):
        """Huvudfunktion - kör hela analysen"""
        print("\n" + "="*60)
        print("AUTOMATISK FIGUR FÖRBÄTTRARE")
        print("="*60 + "\n")

        # Steg 1: Identifiera alla figurer
        self.identifiera_alla_figurer()

        # Steg 2: Analysera varje figur
        print("\n" + "="*60)
        print("ANALYSERAR FIGURER")
        print("="*60 + "\n")

        for i, figur_info in enumerate(self.figurer_att_forbattra, 1):
            print(f"[{i}/{len(self.figurer_att_forbattra)}] {figur_info['section_id']}: {figur_info['img_src']}")
            analys = self.analysera_figur(figur_info)
            self.rapport.append({
                'info': figur_info,
                'analys': analys
            })
            print(f"  Status: {analys['status']}")
            print(f"  Prioritet: {analys['prioritet']}")
            print()

        # Steg 3: Skapa rapport
        self.skapa_rapport()

        print("\n" + "="*60)
        print("KLART!")
        print("="*60)
        print("\nNästa steg:")
        print("1. Granska AUTOMATISK_FIGUR_RAPPORT.md")
        print("2. Använd /matematikviz för att återskapa prioriterade figurer")
        print("3. Eller använd matematisk_bildgenerator.py för batch-generering")


if __name__ == '__main__':
    forbattrare = FigurForfattare()
    forbattrare.kör()
