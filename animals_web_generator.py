# animals_web_generator.py
import data_fetcher
from pathlib import Path

# --------------------- CONFIGURATION ---------------------
TEMPLATE_FILE = Path("animals_template.html")
OUTPUT_FILE = Path("animals.html")
PLACEHOLDER = "__REPLACE_ANIMALS_INFO__"
# ---------------------------------------------------------

def generate_cards(animals):
    """Generate HTML cards from a list of animal dictionaries."""
    cards = []
    for animal in animals:
        name = animal.get("name", "Unknown Animal")
        chars = animal.get("characteristics", {})
        diet = chars.get("diet", "Unknown")
        locations = animal.get("locations", [])
        location = locations[0] if locations else "Worldwide"
        animal_type = (
            chars.get("class") or
            animal.get("taxonomy", {}).get("class") or
            "Unknown"
        )
        name_safe = name.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

        card = f"""    <li class="cards__item">
      <div class="card__title">{name_safe}</div>
      <p class="card__text">
        <strong>Diet:</strong> {diet}<br/>
        <strong>Location:</strong> {location}<br/>
        <strong>Type:</strong> {animal_type}<br/>
      </p>
    </li>"""
        cards.append(card)
    return "\n".join(cards)


def generate_no_results_message(animal_name: str) -> str:
    """fallback when no animals are found."""
    safe_name = animal_name.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return f"""    <div class="no-results">
      <h2>Oops! No animal found for "<strong>{safe_name}</strong>"</h2>
      <p>Try a different spelling or a more common name like "Lion", "Eagle", or "Shark"</p>
      <div style="font-size: 5rem; margin: 30px 0;">Question Mark</div>
    </div>"""


def main():
    print("Animal Web Generator (Modular Edition)")
    print("Uses live data from API-Ninjas\n")

    animal_name = input("Enter the name of an animal: ").strip()
    if not animal_name:
        print("No input provided. Exiting.")
        return

    print(f"\nFetching data for '{animal_name}'...")
    animals = data_fetcher.fetch_data(animal_name)

    # Decide what to show
    if not animals:
        print("No results found – showing friendly message.")
        content = generate_no_results_message(animal_name)
    else:
        print(f"Found {len(animals)} animal(s)! Generating cards...")
        content = generate_cards(animals)

    # Load template
    if not TEMPLATE_FILE.exists():
        print(f"Error: Template file '{TEMPLATE_FILE}' not found!")
        return

    template = TEMPLATE_FILE.read_text(encoding="utf-8")
    if PLACEHOLDER not in template:
        print(f"Error: Template missing placeholder '{PLACEHOLDER}'")
        return

    # Generate final HTML
    final_html = template.replace(PLACEHOLDER, content)
    OUTPUT_FILE.write_text(final_html, encoding="utf-8")

    print(f"\nWebsite generated successfully → {OUTPUT_FILE}")
    print("Open animals.html in your browser!")


if __name__ == "__main__":
    if "YOUR_API_KEY_HERE" in data_fetcher.API_KEY:
        print("Warning: Please set a real API key in data_fetcher.py")
    main()