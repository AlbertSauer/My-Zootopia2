import requests
from pathlib import Path

# --------------------- CONFIGURATION ---------------------
API_URL = "https://api.api-ninjas.com/v1/animals"
API_KEY = "NkGoA6SmFd8K9/R8j0Vo4g==2tS6KSZmV9oiagM5"          # ← Replace with your free key from https://api-ninjas.com
TEMPLATE_FILE = Path("animals_template.html")
OUTPUT_FILE = Path("animals.html")
PLACEHOLDER = "__REPLACE_ANIMALS_INFO__"
# ---------------------------------------------------------

def fetch_animals(animal_name: str):
    """Call the API and return a list of animals matching the name."""
    headers = {"X-Api-Key": API_KEY}
    params = {"name": animal_name.strip()}

    try:
        response = requests.get(API_URL, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error contacting the API: {e}")
        return []


def generate_cards(animals):
    """Create HTML <li> cards for a list of animals."""
    cards = []

    for animal in animals:
        name = animal.get("name", "Unknown Animal")

        chars = animal.get("characteristics", {})

        # Diet
        diet = chars.get("diet", "Unknown")

        # First location (if any)
        locations = animal.get("locations", [])
        location = locations[0] if locations else "Worldwide"

        # Type / Class – the API puts the taxonomic class in two possible places
        animal_type = (
            chars.get("class") or
            animal.get("taxonomy", {}).get("class") or
            "Unknown"
        )

        # Simple HTML escaping for safety
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


def main():
    print("Animal Web Generator")
    print("This tool creates a beautiful HTML page with animal cards using live API data.\n")

    # Ask the user
    animal_name = input("Enter the name of an animal (e.g. Fox, Monkey, Lion): ").strip()
    if not animal_name:
        print("No animal entered – exiting.")
        return

    print(f"\nFetching data for '{animal_name}' from the API...")
    animals = fetch_animals(animal_name)

    if not animals:
        print("No animals found or API error. Check your internet connection and API key.")
        return

    print(f"Found {len(animals)} matching animal(s). Generating cards...")

    # Generate the HTML cards
    cards_html = generate_cards(animals)

    # Load template
    if not TEMPLATE_FILE.exists():
        print(f"Template file '{TEMPLATE_FILE}' not found!")
        return

    template = TEMPLATE_FILE.read_text(encoding="utf-8")

    if PLACEHOLDER not in template:
        print(f"Template does not contain the placeholder '{PLACEHOLDER}'")
        return

    # Inject cards and save
    final_html = template.replace(PLACEHOLDER, cards_html)
    OUTPUT_FILE.write_text(final_html, encoding="utf-8")

    print(f"Website successfully generated → {OUTPUT_FILE}")
    print("Open animals.html in your browser and enjoy!")


if __name__ == "__main__":
    # Quick check for the API key
    if "YOUR_API_KEY_HERE" in API_KEY:
        print("Warning: Please replace 'YOUR_API_KEY_HERE' with a real API key from https://api-ninjas.com")
    main()