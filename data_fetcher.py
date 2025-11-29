import os
from dotenv import load_dotenv
import requests

# Load environment variables from .env
load_dotenv()

# Access the API key
API_KEY = os.getenv("API_KEY")

# --------------------- CONFIGURATION ---------------------
API_URL = "https://api.api-ninjas.com/v1/animals"
TIMEOUT = 10  # seconds
# ---------------------------------------------------------

def fetch_data(animal_name):
    """
    Fetches animal data from the API-Ninjas Animals API.

    Args:
        animal_name (str): The name of the animal to search for (e.g., "Fox", "Tiger").

    Returns:
        list: List of animal dictionaries as returned by the API.
              Returns empty list on error or if no results.
    """
    if not animal_name:
        return []

    if not API_KEY:
        print("[data_fetcher] Warning: API_KEY is not set. Please set it in your .env file.")
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
            print(f"[data_fetcher] Unexpected response format: {data}")
            return []
    except requests.exceptions.RequestException as e:
        print(f"[data_fetcher] API request failed: {e}")
        return []
