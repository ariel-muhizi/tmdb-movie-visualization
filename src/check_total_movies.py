import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BEARER_TOKEN = os.getenv("TMDB_BEARER_TOKEN")
BASE_URL = "https://api.themoviedb.org/3/discover/movie"
HEADERS = {
    "accept": "application/json",
    "Authorization": f"Bearer {BEARER_TOKEN}"
}

def get_total_movies():
    """
    Fetches the total number of 2024 English movies from TMDb API.
    :return: Total number of movies
    """
    params = {
        "include_adult": "false",
        "include_video": "false",
        "language": "en-US",
        "page": 1,
        "sort_by": "popularity.desc",
        "year": 2024
    }
    try:
        response = requests.get(BASE_URL, headers=HEADERS, params=params)
        response.raise_for_status()
        data = response.json()
        total_movies = data.get("total_results", 0)
        print(f"Total number of 2024 English movies: {total_movies}")
        return total_movies
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return 0

if __name__ == "__main__":
    get_total_movies()
