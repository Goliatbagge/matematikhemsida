"""
Skapar hero-bild direkt med Gemini 2.5 Flash Image
"""

import google.generativeai as genai
from pathlib import Path

# API-nyckel
API_KEY = "AIzaSyAQY2e5bV97Z61QKalq19Rs7zDpuNjMM8o"
genai.configure(api_key=API_KEY)

# Skapa bildkatalog
script_dir = Path(__file__).parent
img_dir = script_dir / "images"
img_dir.mkdir(exist_ok=True)
output_path = img_dir / "hero_matematik.png"

# Hero-prompt
prompt = """A modern, inspiring educational hero image for a mathematics website.
Abstract mathematical patterns, geometric shapes (circles, triangles, hexagons) and
subtle calculus curves in the background. Color scheme: deep blue (#2c3e50) and
vibrant orange (#e67e22) gradients. Clean, minimalist style with plenty of negative
space. Professional and inviting atmosphere. 16:9 widescreen format. No text or
numbers visible. High quality, modern digital art style."""

print("=" * 70)
print("Skapar hero-bild för matematikhemsidan")
print("=" * 70)
print()
print(f"Modell: gemini-2.5-flash-image")
print(f"Output: {output_path}")
print()
print("Genererar bild...")
print()

try:
    model = genai.GenerativeModel('gemini-2.5-flash-image')

    response = model.generate_content([
        prompt,
        "Generate this as a high quality image."
    ])

    print("Svar mottaget!")
    print()

    # Försök hitta bilddatan
    bild_hittad = False

    if hasattr(response, 'parts'):
        for i, part in enumerate(response.parts):
            print(f"Del {i+1}: {type(part)}")

            if hasattr(part, 'inline_data') and part.inline_data:
                print(f"  - Bilddata hittad!")
                print(f"  - MIME-typ: {part.inline_data.mime_type}")
                print(f"  - Storlek: {len(part.inline_data.data)} bytes")

                # Spara bilden
                with open(output_path, 'wb') as f:
                    f.write(part.inline_data.data)

                bild_hittad = True
                print()
                print("=" * 70)
                print(f"SUCCE! Bild sparad: {output_path}")
                print("=" * 70)
                break

            elif hasattr(part, 'text') and part.text:
                print(f"  - Text (visar första 200 tecken):")
                print(f"    {part.text[:200]}")

    if not bild_hittad:
        print()
        print("Ingen bilddata hittades.")
        print()
        print("Modellen svarade med:")
        if hasattr(response, 'text'):
            print(response.text[:500])
        print()
        print("=" * 70)
        print("SLUTSATS: gemini-2.5-flash-image genererar inte bilder ännu")
        print("=" * 70)
        print()
        print("Din API-nyckel från Google AI Studio stödjer INTE bildgenerering.")
        print()
        print("Alternativ:")
        print("1. Använd CSS/SVG för grafiska element (rekommenderas!)")
        print("2. Hitta fria bilder från Unsplash/Pexels")
        print("3. Skapa ett Google Cloud-projekt för Imagen via Vertex AI")
        print("4. Använd andra AI-verktyg: DALL-E, Midjourney, Stable Diffusion")

except Exception as e:
    print(f"FEL: {e}")
    import traceback
    traceback.print_exc()

print()
