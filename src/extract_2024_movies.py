import os
import requests
import json
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

# Load environment variables
load_dotenv()

# API Key and Bearer Token from .env
BEARER_TOKEN = os.getenv("TMDB_BEARER_TOKEN")

# Base URL for the TMDb API
BASE_URL = "https://api.themoviedb.org/3/discover/movie"

# Headers for the TMDb API request
HEADERS = {
    "accept": "application/json",
    "Authorization": f"Bearer {BEARER_TOKEN}"
}

# Parameters for the API request
params = {
    "include_adult": "false",  # Don't include adult content
    "include_video": "false",  # Don't include video content
    "language": "en-US",  # Use English language
    "year": 2024,  # Focus on 2024 movies
    "sort_by": "popularity.desc"  # Sort by popularity
}

def get_total_pages():
    """Fetch the total number of pages from the TMDb API"""
    response = requests.get(BASE_URL, headers=HEADERS, params=params)
    if response.status_code == 200:
        return response.json()['total_pages']
    else:
        print("Error fetching total pages")
        return 0

def fetch_page(page):
    """Fetches a single page of movie data"""
    params["page"] = page
    try:
        response = requests.get(BASE_URL, headers=HEADERS, params=params)
        if response.status_code == 200:
            return response.json()["results"]
        else:
            print(f"Error fetching data for page {page}: {response.status_code}")
            return []
    except requests.exceptions.RequestException as e:
        print(f"Request failed for page {page}: {e}")
        return []

def get_all_movies():
    """Fetch all movies from all pages using ThreadPoolExecutor and rate limiting"""
    total_pages = get_total_pages()
    # Limit the number of pages to 500
    total_pages = min(total_pages, 500)

    print(f"Total pages available (limited to 500): {total_pages}")

    all_movies = []

    # To stay within the limit of 50 requests per second, we can adjust the sleep time
    requests_per_second = 50  # Max requests per second allowed by the API
    sleep_time = 1 / requests_per_second  # Sleep time between each request

    # Use ThreadPoolExecutor to fetch data concurrently
    with ThreadPoolExecutor(max_workers=10) as executor:  # Limiting to 10 concurrent workers
        future_to_page = {executor.submit(fetch_page, page): page for page in range(1, total_pages + 1)}
        
        for future in as_completed(future_to_page):
            page = future_to_page[future]
            movies = future.result()
            if movies:
                all_movies.extend(movies)
            print(f"Processed {len(all_movies)} out of {total_pages * 20} movies", end="\r")

            # Rate limiting: Add a sleep time between requests to avoid exceeding 50 requests per second
            time.sleep(sleep_time)  # Delay to ensure we don't exceed the rate limit

    # Save the aggregated data to a JSON file
    with open(os.path.join("..", "data", "all_2024_movies.json"), "w", encoding="utf-8") as f:
        json.dump(all_movies, f, ensure_ascii=False, indent=4)

    print(f"\nSuccessfully saved {len(all_movies)} movies to all_2024_movies.json")

if __name__ == "__main__":
    start_time = time.time()
    get_all_movies()
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Total time taken: {elapsed_time:.2f} seconds")
