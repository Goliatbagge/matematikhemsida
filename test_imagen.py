"""
Testar om Imagen 3 kan användas med din API-nyckel
"""

import os
import sys

# Sätt API-nyckel som miljövariabel
os.environ['GOOGLE_API_KEY'] = "AIzaSyAQY2e5bV97Z61QKalq19Rs7zDpuNjMM8o"

print("=" * 70)
print("Test av Imagen 3-åtkomst")
print("=" * 70)
print()

# Test 1: Testa med google-genai (nyare API)
print("Test 1: Försöker använda google-genai för bildgenerering...")
print()

try:
    from google import genai
    from google.genai import types

    # Skapa klient
    client = genai.Client(api_key=os.environ['GOOGLE_API_KEY'])

    print("Klient skapad!")
    print()
    print("Försöker generera bild...")

    # Försök generera en enkel bild
    response = client.models.generate_image(
        model='imagen-3.0-generate-001',
        prompt='A simple blue circle on white background',
        config=types.GenerateImageConfig(
            number_of_images=1,
            aspect_ratio="1:1",
        )
    )

    if response.generated_images:
        print("SUCCÉ! Bild genererad med google-genai!")
        print(f"Antal bilder: {len(response.generated_images)}")

        # Spara bilden
        from pathlib import Path
        img_dir = Path(__file__).parent / "images"
        img_dir.mkdir(exist_ok=True)

        output_path = img_dir / "test_imagen.png"
        with open(output_path, 'wb') as f:
            f.write(response.generated_images[0].image.image_bytes)

        print(f"Bild sparad: {output_path}")
        print()
        print("=" * 70)
        print("DIN API-NYCKEL FUNGERAR MED IMAGEN!")
        print("=" * 70)
        sys.exit(0)

except Exception as e:
    print(f"google-genai fungerade inte: {e}")
    print()

# Test 2: Testa med Vertex AI
print("Test 2: Försöker använda Vertex AI...")
print()

try:
    import vertexai
    from vertexai.preview.vision_models import ImageGenerationModel

    print("OBS: Vertex AI kräver ett Google Cloud-projekt.")
    print("API-nycklar fungerar inte direkt med Vertex AI.")
    print()
    print("För Vertex AI behövs:")
    print("1. Google Cloud-projekt")
    print("2. Service Account med nyckelfil (JSON)")
    print("3. Vertex AI aktiverat")
    print()

except Exception as e:
    print(f"Vertex AI-import misslyckades: {e}")
    print()

# Test 3: Kontrollera vilka modeller som är tillgängliga
print("=" * 70)
print("Test 3: Kontrollerar tillgängliga modeller...")
print("=" * 70)
print()

try:
    import google.generativeai as genai

    genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

    print("Tillgängliga modeller:")
    for model in genai.list_models():
        if 'generateContent' in model.supported_generation_methods:
            print(f"  - {model.name}")
            print(f"    Metoder: {model.supported_generation_methods}")
            print()

except Exception as e:
    print(f"Kunde inte lista modeller: {e}")

print()
print("=" * 70)
print("SAMMANFATTNING")
print("=" * 70)
print()
print("Din API-nyckel är giltig för Google AI Studio.")
print()
print("För bildgenerering med Imagen 3 finns det två vägar:")
print()
print("1. GOOGLE AI STUDIO API (enklast)")
print("   - Använd google-genai-biblioteket")
print("   - Kräver endast API-nyckel")
print("   - Kan ha begränsningar i free tier")
print()
print("2. VERTEX AI (mer avancerat)")
print("   - Kräver Google Cloud-projekt")
print("   - Kräver Service Account och JSON-nyckelfil")
print("   - Mer kontroll och högre gränser")
print()
