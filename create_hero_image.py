"""
Skapar en hero-bild för matematikhemsidan med Gemini
"""

import google.generativeai as genai
import os
import sys
from pathlib import Path

# API-nyckel
GEMINI_API_KEY = "AIzaSyAQY2e5bV97Z61QKalq19Rs7zDpuNjMM8o"

# Konfigurera Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Skapa bildkatalog
script_dir = Path(__file__).parent
img_dir = script_dir / "images"
img_dir.mkdir(exist_ok=True)

# Hero-bild prompt
prompt = """A modern, inspiring educational hero image for a mathematics website.
Features abstract mathematical patterns, geometric shapes, and subtle calculus curves
in the background. Color scheme: deep blue (#2c3e50) and orange (#e67e22) gradients.
Clean, minimalist style with plenty of negative space. Professional and inviting
atmosphere. 16:9 aspect ratio, suitable for website header. No text or numbers.
High quality, photorealistic rendering."""

output_path = img_dir / "hero_matematik.png"

print("=" * 60)
print("Skapar hero-bild för matematikhemsidan...")
print("=" * 60)
print()
print(f"Prompt: {prompt[:100]}...")
print()

try:
    # Skapa modell för bildgenerering
    model = genai.GenerativeModel('gemini-2.0-flash-exp')

    print("Genererar bild med Gemini...")

    # Generera innehåll med bildprompt
    response = model.generate_content([prompt])

    print(f"Response type: {type(response)}")
    print(f"Response attributes: {dir(response)}")

    # Försök spara bild om den finns
    if hasattr(response, '_result'):
        print(f"Result: {response._result}")

    print()
    print("OBS: Gemini 2.0 Flash kanske inte stödjer bildgenerering direkt.")
    print("Vi kan behöva använda en annan modell eller metod.")
    print()
    print("Testar alternativ metod med Imagen...")

    # Testa med imagen istället
    try:
        imagen_model = genai.ImageGenerationModel('imagen-3.0-generate-001')
        result = imagen_model.generate_images(
            prompt=prompt,
            number_of_images=1,
        )

        if result.images:
            result.images[0].save(str(output_path))
            print(f"✓ Bild sparad med Imagen: {output_path}")
        else:
            print("✗ Ingen bild genererades med Imagen")

    except Exception as e:
        print(f"✗ Imagen fungerade inte heller: {e}")
        print()
        print("INFORMATION:")
        print("- Gemini API kanske inte har bildgenerering aktiverat för din nyckel")
        print("- Kontrollera på Google AI Studio vilka funktioner som är tillgängliga")
        print("- Bildgenerering kan kräva särskild åtkomst eller betalplan")

except Exception as e:
    print(f"✗ Fel: {e}")
    import traceback
    traceback.print_exc()

print()
print("=" * 60)
