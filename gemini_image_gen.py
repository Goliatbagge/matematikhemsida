"""
Bildgenerator med Gemini 2.5 Flash Image
Använder din befintliga API-nyckel!
"""

import google.generativeai as genai
from pathlib import Path
import sys

# API-nyckel
API_KEY = "AIzaSyAQY2e5bV97Z61QKalq19Rs7zDpuNjMM8o"

# Konfigurera API
genai.configure(api_key=API_KEY)

def generate_image(prompt, output_filename="generated_image.png"):
    """
    Genererar en bild med Gemini 2.5 Flash Image

    Args:
        prompt: Beskrivning av bilden
        output_filename: Filnamn för sparad bild
    """

    # Skapa bildkatalog
    script_dir = Path(__file__).parent
    img_dir = script_dir / "images"
    img_dir.mkdir(exist_ok=True)
    output_path = img_dir / output_filename

    print("=" * 70)
    print("Gemini 2.5 Flash Image - Bildgenerator")
    print("=" * 70)
    print()
    print(f"Prompt: {prompt}")
    print()

    try:
        # Använd Gemini 2.5 Flash Image
        model = genai.GenerativeModel('gemini-2.5-flash-image')

        print("Genererar bild...")
        print()

        # Generera bild med prompt
        response = model.generate_content([
            prompt,
            "Generate this as an image."
        ])

        print("Svar mottaget!")
        print(f"Response type: {type(response)}")
        print()

        # Försök extrahera bilden
        if hasattr(response, 'parts'):
            for part in response.parts:
                print(f"Part type: {type(part)}")
                if hasattr(part, 'inline_data'):
                    # Detta är bilddatan
                    image_data = part.inline_data.data
                    mime_type = part.inline_data.mime_type

                    print(f"Bilddata hittad! MIME-typ: {mime_type}")
                    print(f"Datastorlek: {len(image_data)} bytes")

                    # Spara bilden
                    with open(output_path, 'wb') as f:
                        f.write(image_data)

                    print()
                    print("=" * 70)
                    print(f"SUCCE! Bild sparad: {output_path}")
                    print("=" * 70)
                    return str(output_path)

        # Om ingen bild hittades, visa vad vi fick
        print("Ingen bilddata hittades i svaret.")
        print()
        print("Svar från modellen:")
        if hasattr(response, 'text'):
            print(response.text)
        print()
        print("Modellen kanske inte stödjer bildgenerering ännu.")
        return None

    except Exception as e:
        print(f"FEL: {e}")
        import traceback
        traceback.print_exc()
        return None


# Prompter för matematikhemsidan
PROMPTS = {
    "hero": """A modern, inspiring educational hero image for a mathematics website.
Abstract mathematical patterns, geometric shapes (circles, triangles, hexagons) and
subtle calculus curves in the background. Color scheme: deep blue (#2c3e50) and
vibrant orange (#e67e22) gradients. Clean, minimalist style with plenty of negative
space. Professional and inviting atmosphere. 16:9 widescreen format. No text or
numbers visible. High quality, modern digital art style.""",

    "derivative": """Educational illustration of a tangent line touching a smooth curve.
Simple, clean design. A blue curved line (parabola) with an orange straight line
(tangent) touching it at one point. White background. Minimalist mathematical diagram
style. Clear, high contrast. Professional educational illustration.""",

    "integral": """Educational illustration showing integration concept. A smooth blue
curve with light blue shaded area underneath representing the integral. The area is
divided into thin rectangles. White background. Clean, minimalist educational style.
Professional mathematical diagram.""",

    "background": """Very subtle mathematical pattern for website background. Extremely
faint and light geometric shapes, barely visible mathematical symbols (∫, ∂, Σ) in
very light blue and light orange. Should not distract from content. Soft, professional,
minimalist. Suitable as repeating background texture."""
}


if __name__ == "__main__":
    print()
    print("Välkommen till Gemini Image Generator!")
    print()
    print("Tillgängliga prompter:")
    for i, (name, prompt) in enumerate(PROMPTS.items(), 1):
        print(f"{i}. {name}")
    print()

    choice = input("Välj prompt (1-4) eller tryck Enter för egen: ").strip()

    if choice.isdigit() and 1 <= int(choice) <= len(PROMPTS):
        prompt_name = list(PROMPTS.keys())[int(choice) - 1]
        prompt = PROMPTS[prompt_name]
        default_filename = f"{prompt_name}_matematik.png"
    else:
        prompt = input("Ange din prompt: ").strip()
        default_filename = "custom_image.png"

    filename = input(f"Filnamn [{default_filename}]: ").strip() or default_filename

    print()
    result = generate_image(prompt, filename)

    if not result:
        print()
        print("=" * 70)
        print("INFO: Gemini 2.5 Flash Image är experimentell")
        print("=" * 70)
        print()
        print("Om bildgenerering inte fungerar:")
        print("1. Modellen kanske inte är tillgänglig i alla regioner")
        print("2. Vissa API-nycklar kanske inte har åtkomst ännu")
        print("3. Gemini kan ge textbeskrivningar istället för bilder")
        print()
        print("Alternativ:")
        print("- Skapa bilder med CSS/SVG istället")
        print("- Använd gratis bildbanker (Unsplash, Pexels)")
        print("- Testa andra AI-verktyg som DALL-E eller Midjourney")
