# TMDb Movie Visualization

This project uses the [TMDb API](https://www.themoviedb.org/documentation/api) to extract data about movies released in 2024, focusing on details like popularity, genres, revenue, and more. The extracted data is then saved as a JSON file for later use in visualizations.

## Project Structure

The project is organized into the following directories and files:

- **`src/`**: Contains Python scripts for extracting data.
  - **`extract_2024_movies.py`**: Authenticates and extracts movie data from TMDb for 2024.
  - **`check_total_movies.py`**: A utility to check the total number of movies available in the TMDb API (limited to 500 pages).
- **`visualization/`**: Contains Python files for visualizing the data (e.g., with Streamlit).
  - **`app.py`**: Placeholder for later interactive visualizations.
- **`data/`**: Stores the JSON file containing the extracted movie data.
- **`.env`**: Contains the API key and bearer token for secure access to the TMDb API.
- **`requirements.txt`**: Lists all required Python libraries for running the project.

## How It Works

1. **Data Extraction**:  
   The `extract_2024_movies.py` script authenticates with the TMDb API, retrieves movie data for 2024, and saves it in the `data` folder as `all_2024_movies.json`. The script fetches up to 500 pages of movie data, respecting TMDb's rate limits (50 requests per second).

2. **Data Visualization**:  
   The `app.py` file in the `visualization` folder will be used to create interactive visualizations from the extracted movie data. This file can be further developed using libraries like Streamlit, Plotly, or Matplotlib to generate charts and insights.

## Rate Limiting

The script is designed to respect TMDb's rate limit of 50 requests per second. A small delay is introduced between requests to ensure the API rate limits are not exceeded.

## License

This project is licensed under the Apache-2.0 License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- The Movie Database (TMDb) API for providing the movie data.
