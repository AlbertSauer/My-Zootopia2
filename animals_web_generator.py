import os
from pathlib import Path
import requests
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# --------------------- CONFIGURATION ---------------------
API_URL = "https://api.api-ninjas.com/v1/animals"
API_KEY = os.getenv("API_KEY")  # Loaded from .env
TEMPLATE_FILE = Path("animals_template.html")
OUTPUT_FILE = Path("animals.html")
PLACEHOLDER = "__REPLACE_ANIMALS_INFO__"
TIMEOUT = 10  # seconds for API requests
# ---------------------------------------------------------

def fetch_animals(animal_name):
    """Call the API and return a list of animals matching the name."""
    if not API_KEY:
        print("[Error] API_KEY is not set. Please add it to your .env file.")
        return []

    headers = {"X-Api-Key": API_KEY}
    params = {"name": animal_name.strip()}

    try:
        response = requests.get(API_URL, headers=headers, params=params, timeout=TIMEOUT)
        response.raise_for_status()
        data = response.json()
        if isinstance(data, list):
            return data
        else:
            print(f"[Warning] Unexpected API response format: {data}")
            return []
    except requests.exceptions.RequestException as e:
        print(f"[Error] API request failed: {e}")
        return []


def generate_cards(animals):
    """Create HTML <li> cards for a list of animals."""
    cards = []

    for animal in animals:
        name = animal.get("name", "Unknown Animal")
        chars = animal.get("characteristics", {})

        diet = chars.get("diet", "Unknown")
        locations = animal.get("locations", [])
        location = locations[0] if locations else "Worldwide"

        animal_type = chars.get("class") or animal.get("taxonomy", {}).get("class") or "Unknown"

        # Simple HTML escaping
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
    cards_html = generate_cards(animals)

    if not TEMPLATE_FILE.exists():
        print(f"Template file '{TEMPLATE_FILE}' not found!")
        return

    template = TEMPLATE_FILE.read_text(encoding="utf-8")

    if PLACEHOLDER not in template:
        print(f"Template does not contain the placeholder '{PLACEHOLDER}'")
        return

    final_html = template.replace(PLACEHOLDER, cards_html)
    OUTPUT_FILE.write_text(final_html, encoding="utf-8")

    print(f"Website successfully generated → {OUTPUT_FILE}")
    print("Open animals.html in your browser and enjoy!")


if __name__ == "__main__":
    if not API_KEY:
        print("Warning: API_KEY not found in .env. Please add your API key.")
    main()
