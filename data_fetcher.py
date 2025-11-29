import os
from dotenv import load_dotenv
import requests


load_dotenv()  # loads .env into environment variables

API_KEY = os.getenv("API_KEY")
# --------------------- CONFIGURATION ---------------------
API_URL = "https://api.api-ninjas.com/v1/animals"
# ---------------------------------------------------------

def fetch_data(animal_name: str):
    """
    Fetches animal data from the API-Ninjas Animals API.

    Args:
        animal_name (str): The name of the animal to search for (e.g., "Fox", "Tiger")

    Returns:
        list[dict]: List of animal dictionaries exactly as returned by the API.
                    Each animal has keys: 'name', 'taxonomy', 'locations', 'characteristics', etc.
                    Returns empty list on error or no results.
    """
    if not animal_name:
        return []

    headers = {"X-Api-Key": API_KEY}
    params = {"name": animal_name.strip()}

    try:
        response = requests.get(API_URL, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"[data_fetcher] API request failed: {e}")
        return []