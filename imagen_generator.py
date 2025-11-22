"""
Bildgenerator med Google Imagen 3 via Vertex AI
För Matematik 3c-hemsidan
"""

import vertexai
from vertexai.preview.vision_models import ImageGenerationModel
import base64
from pathlib import Path
import sys

# API-nyckel (används för autentisering)
API_KEY = "AIzaSyAQY2e5bV97Z61QKalq19Rs7zDpuNjMM8o"

def generate_image_with_imagen(prompt, output_filename, project_id=None, location="us-central1"):
    """
    Genererar en bild med Imagen 3

    Args:
        prompt: Beskrivning av bilden
        output_filename: Filnamn att spara bilden som
        project_id: Google Cloud projekt-ID (krävs för Vertex AI)
        location: Region för Vertex AI
    """

    # Skapa bildkatalog
    script_dir = Path(__file__).parent
    img_dir = script_dir / "images"
    img_dir.mkdir(exist_ok=True)
    output_path = img_dir / output_filename

    print("=" * 70)
    print("Imagen 3 Bildgenerator")
    print("=" * 70)
    print()

    # Kontrollera projekt-ID
    if not project_id:
        print("ERROR: Projekt-ID saknas!")
        print()
        print("For att anvanda Imagen 3 behovs:")
        print("1. Ett Google Cloud-projekt")
        print("2. Vertex AI aktiverat i projektet")
        print("3. Projekt-ID angivet")
        print()
        print("Skapa ett projekt pa: https://console.cloud.google.com/")
        print()
        return None

    try:
        print(f"Initierar Vertex AI...")
        print(f"- Projekt: {project_id}")
        print(f"- Region: {location}")
        print()

        # Initiera Vertex AI
        vertexai.init(project=project_id, location=location)

        # Ladda Imagen-modellen
        print("Laddar Imagen 3-modellen...")
        model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-001")

        print()
        print("Genererar bild...")
        print(f"Prompt: {prompt[:100]}...")
        print()

        # Generera bilder
        images = model.generate_images(
            prompt=prompt,
            number_of_images=1,
            aspect_ratio="16:9",
            safety_filter_level="block_some",
            person_generation="allow_adult",
        )

        if images.images:
            # Spara första bilden
            image = images.images[0]
            image.save(location=str(output_path))

            print("=" * 70)
            print(f"SUCCE! Bild sparad: {output_path}")
            print("=" * 70)
            return str(output_path)
        else:
            print("Ingen bild genererades.")
            return None

    except Exception as e:
        print(f"FEL vid bildgenerering: {e}")
        print()
        print("Felsokning:")
        print("- Kontrollera att Vertex AI ar aktiverat i ditt projekt")
        print("- Verifiera att du har rattigheter att anvanda Imagen")
        print("- Kontrollera att projekt-ID ar korrekt")
        print()
        print("Mer info: https://cloud.google.com/vertex-ai/docs/generative-ai/image/generate-images")
        import traceback
        traceback.print_exc()
        return None


# Exempel-prompter
HERO_PROMPT = """A modern, inspiring educational hero image for a mathematics website.
Features abstract mathematical patterns, geometric shapes, and subtle calculus curves
in the background. Color scheme: deep blue (#2c3e50) and orange (#e67e22) gradients.
Clean, minimalist style with plenty of negative space. Professional and inviting
atmosphere. 16:9 aspect ratio, suitable for website header. No text or numbers.
High quality, photorealistic rendering."""


if __name__ == "__main__":
    print()
    print("VIKTIGT: Imagen 3 kraver Google Cloud Vertex AI")
    print()

    # Fråga efter projekt-ID
    project_id = input("Ange ditt Google Cloud projekt-ID (eller tryck Enter for att avbryta): ").strip()

    if not project_id:
        print()
        print("Ingen projekt-ID angavs. Avslutar.")
        print()
        print("For att anvanda Imagen 3:")
        print("1. Ga till https://console.cloud.google.com/")
        print("2. Skapa ett nytt projekt eller valj ett befintligt")
        print("3. Aktivera Vertex AI API")
        print("4. Kor detta script igen och ange projekt-ID")
        sys.exit(0)

    print()
    filename = input("Filnamn [hero_matematik.png]: ").strip() or "hero_matematik.png"

    print()
    generate_image_with_imagen(
        prompt=HERO_PROMPT,
        output_filename=filename,
        project_id=project_id
    )
