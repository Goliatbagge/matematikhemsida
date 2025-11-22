"""
Bildgenererare för Matematik 3c-hemsidan
Använder Google Gemini för att skapa bilder
"""

import google.generativeai as genai
import os
import sys
from pathlib import Path

# Importera API-nyckel
sys.path.insert(0, str(Path(__file__).parent.parent / '.claude'))
from gemini_config import GEMINI_API_KEY

# Konfigurera Gemini
genai.configure(api_key=GEMINI_API_KEY)

def generate_image(prompt, output_filename, image_dir="images"):
    """
    Genererar en bild med Gemini baserat på en prompt.

    Args:
        prompt (str): Beskrivning av bilden som ska genereras
        output_filename (str): Filnamn för den genererade bilden
        image_dir (str): Katalog där bilden ska sparas (default: images)

    Returns:
        str: Sökväg till den sparade bilden
    """

    # Skapa bildkatalog om den inte finns
    script_dir = Path(__file__).parent
    img_path = script_dir / image_dir
    img_path.mkdir(exist_ok=True)

    # Fullständig sökväg för bildfil
    output_path = img_path / output_filename

    print(f"Genererar bild med Gemini...")
    print(f"Prompt: {prompt}")

    try:
        # Skapa modell
        model = genai.GenerativeModel('gemini-2.0-flash-exp')

        # Generera bild
        response = model.generate_content([
            prompt,
            "Generate an image based on this description."
        ])

        # Kontrollera om bilden genererades
        if hasattr(response, 'images') and response.images:
            # Spara första bilden
            image = response.images[0]
            image.save(str(output_path))
            print(f"✓ Bild sparad: {output_path}")
            return str(output_path)
        else:
            print("⚠ Ingen bild genererades. Försöker alternativ metod...")

            # Alternativ: Använd imagen om tillgängligt
            imagen = genai.ImageGenerationModel('imagen-3.0-generate-001')
            result = imagen.generate_images(
                prompt=prompt,
                number_of_images=1,
                aspect_ratio="16:9"
            )

            if result.images:
                result.images[0].save(str(output_path))
                print(f"✓ Bild sparad: {output_path}")
                return str(output_path)
            else:
                print("✗ Kunde inte generera bild")
                return None

    except Exception as e:
        print(f"✗ Fel vid bildgenerering: {e}")
        print("\nFelsökning:")
        print("- Kontrollera att API-nyckeln är korrekt")
        print("- Verifiera att du har tillgång till bildgenerering i Gemini")
        print("- Testa med Google AI Studio först")
        return None


# Exempel-prompter för matematikhemsidan
EXAMPLE_PROMPTS = {
    "hero_main": """A modern, inspiring educational hero image for a mathematics website.
    Features abstract mathematical patterns, geometric shapes, and subtle calculus curves
    in the background. Color scheme: deep blue (#2c3e50) and orange (#e67e22) gradients.
    Clean, minimalist style with plenty of negative space. Professional and inviting
    atmosphere. 16:9 aspect ratio, suitable for website header. No text or numbers.""",

    "derivative_concept": """Educational illustration showing the concept of a tangent
    line to a curve. Simple, clean geometric design with a smooth blue curve and an
    orange tangent line touching it at one point. Minimalist style on white background.
    Suitable for educational mathematics website. High contrast, clear lines.""",

    "integral_concept": """Educational illustration showing the concept of integration
    as area under a curve. A smooth curve with shaded area underneath, divided into
    rectangles. Colors: blue curve, light blue shaded area. Clean, minimalist educational
    style on white background.""",

    "background_pattern": """Subtle abstract mathematical pattern background. Very light
    pastel colors (light blue and light orange), barely visible geometric shapes and
    mathematical symbols. Very subtle, suitable as a website background texture. Should
    not distract from content. Seamless tileable pattern. Soft, professional appearance.""",

    "study_inspiration": """Inspiring image of mathematics study materials. Open textbook
    with graphs and equations, notebook with handwritten calculations, calculator, and
    coffee cup on a clean desk. Natural lighting, modern aesthetic. Professional photo
    style. Warm, inviting atmosphere for learning."""
}


if __name__ == "__main__":
    print("=" * 60)
    print("Bildgenerator för Matematik 3c-hemsidan")
    print("=" * 60)
    print()

    # Visa tillgängliga exempel
    print("Tillgängliga exempel-prompts:")
    for i, (name, prompt) in enumerate(EXAMPLE_PROMPTS.items(), 1):
        print(f"{i}. {name}")
    print()

    # Låt användaren välja
    choice = input("Välj exempel (1-5) eller tryck Enter för egen prompt: ").strip()

    if choice.isdigit() and 1 <= int(choice) <= len(EXAMPLE_PROMPTS):
        # Använd exempel-prompt
        prompt_name = list(EXAMPLE_PROMPTS.keys())[int(choice) - 1]
        prompt = EXAMPLE_PROMPTS[prompt_name]
        default_filename = f"{prompt_name}.png"
    else:
        # Egen prompt
        prompt = input("Ange din prompt: ").strip()
        default_filename = "generated_image.png"

    # Filnamn
    filename = input(f"Filnamn [{default_filename}]: ").strip() or default_filename

    # Generera bild
    print()
    result = generate_image(prompt, filename)

    if result:
        print()
        print("=" * 60)
        print("✓ Klart! Bilden är redo att användas på hemsidan.")
        print("=" * 60)
    else:
        print()
        print("=" * 60)
        print("✗ Bildgenerering misslyckades. Se felsökningsinformation ovan.")
        print("=" * 60)
