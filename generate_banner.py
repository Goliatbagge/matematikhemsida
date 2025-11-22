import google.generativeai as genai

genai.configure(api_key='AIzaSyAQY2e5bV97Z61QKalq19Rs7zDpuNjMM8o')
model = genai.GenerativeModel('gemini-2.0-flash-exp')

prompt = """
Skapa en komplett SVG-banner (1200x400px) för en matematikutbildningsplattform kallad "Enkel matematik".

Krav:
- Storlek: viewBox="0 0 1200 400"
- Primärfärg: #4a90e2 (blå)
- Kompletterande färger: ljusblå (#7db3f5), vit, subtil orange (#f39c12) för kontrast
- Inkludera matematiska element:
  * En sinus/cosinus-kurva
  * Geometriska former (cirklar, trianglar, hexagoner)
  * Subtila matematiska symboler (integral, derivata, pi)
- Modern, minimalistisk stil
- Gradient-bakgrund från mörkblå till ljusblå
- Lämplig för en hero-section på en utbildningswebbplats
- Pedagogisk och inbjudande känsla
- Lagom komplexitet - inte för överfull

Ge mig ENDAST ren SVG-kod (börja med <svg> och sluta med </svg>), ingen extra text eller förklaring.
"""

response = model.generate_content(prompt)

# Ta bort eventuella markdown code blocks
svg_content = response.text
if '```' in svg_content:
    # Extrahera innehållet mellan ```
    lines = svg_content.split('\n')
    svg_lines = []
    in_code_block = False
    for line in lines:
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            continue
        if in_code_block or line.strip().startswith('<'):
            svg_lines.append(line)
    svg_content = '\n'.join(svg_lines)

with open('hero-banner.svg', 'w', encoding='utf-8') as f:
    f.write(svg_content.strip())

print('Banner skapad: hero-banner.svg')
