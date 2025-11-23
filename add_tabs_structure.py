#!/usr/bin/env python3
"""
Script för att lägga till flikstruktur till matematikkurssidor
UTAN att ta bort befintligt innehåll.
"""

import re
import sys
from pathlib import Path

def add_tab_structure(html_content, file_path):
    """
    Lägger till flikstruktur till en HTML-fil om den inte redan har det.
    Flyttar allt befintligt innehåll in i genomgångs-fliken.
    """

    # Kolla om filen redan har flikar
    if 'class="tabs"' in html_content:
        print(f"  [OK] Hoppar över {file_path.name} (har redan flikar)")
        return None

    # Hitta section-taggen och dess innehåll
    section_pattern = r'(<section[^>]*class="content-section"[^>]*>)\s*<h2>(.*?)</h2>(.*?)</section>'
    section_match = re.search(section_pattern, html_content, re.DOTALL)

    if not section_match:
        print(f"  [WARNING] Kunde inte hitta section i {file_path.name}")
        return None

    section_start = section_match.group(1)
    h2_content = section_match.group(2)
    section_body = section_match.group(3)

    # CSS för flikarna (ska läggas till i <style>-taggen)
    tab_css = """
   /* Flikstil */
        .tabs {
            display: flex;
            gap: 0.5rem;
            margin: 2rem 0 0 0;
            border-bottom: 2px solid #e5e7eb;
        }

        .tab-button {
            background: none;
            border: none;
            padding: 1rem 2rem;
            font-size: 1.1rem;
            font-family: 'Google Sans', 'Inter', sans-serif;
            font-weight: 500;
            cursor: pointer;
            color: #6b7280;
            border-bottom: 3px solid transparent;
            transition: all 0.3s ease;
            position: relative;
            bottom: -2px;
        }

        .tab-button:hover {
            color: #4a90e2;
            background: #f3f4f6;
        }

        .tab-button.active {
            color: #4a90e2;
            border-bottom-color: #4a90e2;
            font-weight: 600;
        }

        .tab-content {
            display: none;
            padding: 2rem 0;
            animation: fadeIn 0.3s ease;
        }

        .tab-content.active {
            display: block;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* Övningsuppgifter stil */
        .exercise {
            background: white;
            padding: 1.5rem;
            margin: 1.5rem 0;
            border-radius: 8px;
            border-left: 4px solid #4a90e2;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }

        .exercise-input {
            display: flex;
            gap: 1rem;
            align-items: center;
            margin: 1rem 0;
            flex-wrap: wrap;
        }

        .exercise-input input {
            padding: 0.75rem;
            border: 2px solid #e5e7eb;
            border-radius: 4px;
            font-size: 1rem;
            width: 150px;
            font-family: 'Inter', sans-serif;
        }

        .exercise-input input:focus {
            outline: none;
            border-color: #4a90e2;
        }

        .check-btn {
            background: #4a90e2;
            color: white;
            border: none;
            padding: 0.75rem 1.5rem;
            border-radius: 4px;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: background 0.3s ease;
        }

        .check-btn:hover {
            background: #357abd;
        }

        .feedback {
            margin-top: 1rem;
            padding: 1rem;
            border-radius: 4px;
            display: none;
        }

        .feedback.correct {
            background: #d1fae5;
            border: 2px solid #10b981;
            color: #065f46;
            display: block;
        }

        .feedback.incorrect {
            background: #fee2e2;
            border: 2px solid #ef4444;
            color: #991b1b;
            display: block;
        }

        .solution {
            background: #f3f4f6;
            padding: 1.5rem;
            margin-top: 1rem;
            border-radius: 4px;
            border-left: 4px solid #f39c12;
        }"""

    # Lägg till CSS om den inte redan finns
    if 'Flikstil' not in html_content:
        html_content = html_content.replace('</style>', tab_css + '\n  </style>')

    # JavaScript för flikhantering
    tab_js = """  <script>
   // Flikhantering
        function openTab(evt, tabName) {
            var i, tabContent, tabButtons;

            tabContent = document.getElementsByClassName("tab-content");
            for (i = 0; i < tabContent.length; i++) {
                tabContent[i].classList.remove("active");
            }

            tabButtons = document.getElementsByClassName("tab-button");
            for (i = 0; i < tabButtons.length; i++) {
                tabButtons[i].classList.remove("active");
            }

            document.getElementById(tabName).classList.add("active");
            evt.currentTarget.classList.add("active");
        }
  </script>"""

    # Skapa ny section med flikar och allt befintligt innehåll i genomgångs-fliken
    new_section = f"""{section_start}
    <h2>
     {h2_content}
    </h2>
    <!-- Flikar -->
    <div class="tabs">
     <button class="tab-button active" onclick="openTab(event, 'genomgang')">
      Genomgång
     </button>
     <button class="tab-button" onclick="openTab(event, 'exempel')">
      Exempel
     </button>
     <button class="tab-button" onclick="openTab(event, 'ovningar')">
      Övningsuppgifter
     </button>
    </div>
    <!-- Genomgång -->
    <div class="tab-content active" id="genomgang">
{section_body.strip()}
    </div>
    <!-- Exempel -->
    <div class="tab-content" id="exempel">
     <h3>
      Exempel kommer snart
     </h3>
     <p>
      Fullständiga exempel med pedagogiska lösningar kommer att läggas till här.
     </p>
    </div>
    <!-- Övningsuppgifter -->
    <div class="tab-content" id="ovningar">
     <h3>
      Övningsuppgifter kommer snart
     </h3>
     <p>
      Interaktiva övningsuppgifter med automatisk rättning kommer att läggas till här.
     </p>
    </div>
   </section>"""

    # Ersätt gamla section med nya
    html_content = html_content[:section_match.start()] + new_section + html_content[section_match.end():]

    # Lägg till JavaScript före </footer> om det inte redan finns
    if 'function openTab' not in html_content:
        html_content = html_content.replace('  <footer>', tab_js + '\n  <footer>')

    return html_content


def process_files(directory_pattern):
    """Processera alla HTML-filer i givna kataloger."""
    files = list(Path('.').glob(directory_pattern))

    print(f"\nHittade {len(files)} filer att bearbeta i {directory_pattern}")

    modified_count = 0
    skipped_count = 0

    for file_path in sorted(files):
        try:
            # Läs fil
            with open(file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()

            # Lägg till flikstruktur
            new_content = add_tab_structure(original_content, file_path)

            if new_content and new_content != original_content:
                # Skriv tillbaka
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"  [OK] Uppdaterade {file_path.name}")
                modified_count += 1
            else:
                skipped_count += 1

        except Exception as e:
            print(f"  [ERROR] Fel vid bearbetning av {file_path.name}: {e}")

    return modified_count, skipped_count


if __name__ == "__main__":
    print("=" * 60)
    print("Lägger till flikstruktur till matematikkurssidor")
    print("=" * 60)

    # Bearbeta alla matematik-kurser
    total_modified = 0
    total_skipped = 0

    for pattern in ['matematik-1c/sections/*.html',
                    'matematik-2c/sections/*.html',
                    'matematik-3c/sections/*.html']:
        modified, skipped = process_files(pattern)
        total_modified += modified
        total_skipped += skipped

    print("\n" + "=" * 60)
    print(f"Klart! Uppdaterade {total_modified} filer, hoppade över {total_skipped}")
    print("=" * 60)
