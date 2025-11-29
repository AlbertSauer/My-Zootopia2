# data_fetcher.py
import requests

# --------------------- CONFIGURATION ---------------------
API_URL = "https://api.api-ninjas.com/v1/animals"
API_KEY = 'NkGoA6SmFd8K9/R8j0Vo4g==2tS6KSZmV9oiagM5'
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