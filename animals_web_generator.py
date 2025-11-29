import json

# 1. Load the animal data
with open('animals_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 2. Generate beautiful HTML cards
output = ''

for animal in data:
    # --- Safely extract data (some animals miss fields) ---
    name = animal.get('name', 'Unknown Animal')

    chars = animal.get('characteristics', {})
    diet = chars.get('diet', 'Unknown')

    # Location: take the first one if available
    location = 'Unknown'
    if animal.get('locations') and len(animal['locations']) > 0:
        location = animal['locations'][0]

    # Type: prefer 'type', fallback to 'class' or other fields
    animal_type = 'Unknown'
    if chars.get('type'):
        animal_type = chars['type']
    elif chars.get('class'):
        animal_type = chars['class']

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