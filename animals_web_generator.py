import json
import requests

# API Configuration
API_URL = 'https://api.api-ninjas.com/v1/animals'
API_KEY = 'NkGoA6SmFd8K9/R8j0Vo4g==2tS6KSZmV9oiagM5'  #API KEY!!!
SEARCH_TERM = 'fox'


# 1. Fetch animal data from API
def fetch_animals():
    headers = {'X-Api-Key': API_KEY}
    params = {'name': SEARCH_TERM}

    try:
        response = requests.get(API_URL, headers=headers, params=params)
        response.raise_for_status()  # Raises error for bad status
        data = response.json()
        print(f"Fetched {len(data)} fox-related animals from API.")
        return data
    except requests.exceptions.RequestException as e:
        print(f"API error: {e}")
        return []


data = fetch_animals()

# 2. Generate beautiful HTML cards
output = ''

for animal in data:
    # --- Safely extract data (API structure matches closely) ---
    name = animal.get('name', 'Unknown Animal')

    chars = animal.get('characteristics', {})
    diet = chars.get('diet', 'Unknown')

    # Location: take the first one if available
    location = 'Unknown'
    if animal.get('locations') and len(animal['locations']) > 0:
        location = animal['locations'][0]

    # Type: prefer 'class' from characteristics (API uses taxonomy.class too, but this is simpler)
    animal_type = 'Unknown'
    if chars.get('class'):
        animal_type = chars['class']
    elif animal.get('taxonomy', {}).get('class'):
        animal_type = animal['taxonomy']['class']

    # --- Build the professional card ---
    output += '<li class="cards__item">\n'
    output += f'  <div class="card__title">{name}</div>\n'
    output += '  <p class="card__text">\n'
    output += f'      <strong>Diet:</strong> {diet}<br/>\n'
    output += f'      <strong>Location:</strong> {location}<br/>\n'
    output += f'      <strong>Type:</strong> {animal_type}<br/>\n'
    output += '  </p>\n'
    output += '</li>\n\n'

# 3. Load the template
with open('animals_template.html', 'r', encoding='utf-8') as f:
    template = f.read()

# 4. Inject our beautiful cards
final_html = template.replace('__REPLACE_ANIMALS_INFO__', output)

# 5. Save the final masterpiece
with open('animals.html', 'w', encoding='utf-8') as f:
    f.write(final_html)

print("Open animals.html")