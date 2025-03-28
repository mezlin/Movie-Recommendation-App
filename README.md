# Movie Recommendation API

This is a simple Flask-based API that provides movie recommendations based on user preferences or a given movie title. The API uses TF-IDF and cosine similarity to find similar movies from a dataset.

## Features
- Get movie recommendations based on a given title.
- Get movie recommendations based on favorite genres, actors, and directors.
- Search for movies by genre, actor, or director.

## Requirements
Ensure you have Python installed and install the required dependencies:

```sh
pip install -r requirements.txt
```

### Dependencies
- Flask
- Pandas
- Scikit-learn
- RapidFuzz
- Requests

## Running the API
Start the Flask server by running:

```sh
python app.py
```

By default, the API runs on `http://127.0.0.1:5000/`.

## API Endpoints

### 1. Get Movie Recommendations by Title
**Endpoint:** `/recommend`

**Method:** `GET`

**Query Parameter:**
- `title`: The name of the movie.

**Example Request:**
```sh
curl "http://127.0.0.1:5000/recommend?title=Inception"
```

**Example Response:**
```json
{
    "message": "Best match found: Inception",
    "recommendations": ["Interstellar", "The Dark Knight", "Tenet", ...]
}
```

### 2. Get Recommendations by Preferences
**Endpoint:** `/recommend/preferences`

**Method:** `POST`

**Body (JSON):**
```json
{
    "genres": ["Action", "Sci-Fi"],
    "actors": ["Leonardo DiCaprio"],
    "directors": ["Christopher Nolan"]
}
```

**Example Request:**
```sh
curl -X POST "http://127.0.0.1:5000/recommend/preferences" \
     -H "Content-Type: application/json" \
     -d '{"genres": ["Action"], "actors": ["Leonardo DiCaprio"], "directors": ["Christopher Nolan"]}'
```

**Example Response:**
```json
{
    "message": "Movies based on your preferences",
    "recommendations": ["Inception", "Interstellar", "The Dark Knight"]
}
```

### 3. Search Movies by Category
**Endpoint:** `/search`

**Method:** `GET`

**Query Parameters:**
- `category`: "Genre", "Actors", or "Director".
- `keyword`: The search keyword.

**Example Request:**
```sh
curl "http://127.0.0.1:5000/search?category=Genre&keyword=Action"
```

**Example Response:**
```json
{
    "message": "Movies found for Genre - Action",
    "recommendations": ["Mad Max: Fury Road", "The Dark Knight"]
}
```

## Dataset
The API uses a `movies.csv` dataset containing the following columns:
- `Title`
- `Genre`
- `Director`
- `Actors`
- `Overview`

Ensure `movies.csv` is placed in the project directory before running the API.
To do so simply run the **Loading the dataset from TMDB** section in the **model.ipynb** file.

## Notes
- The API uses **RapidFuzz** to handle slight variations in movie titles.
- It uses **TF-IDF Vectorization** and **Cosine Similarity** to recommend movies.
- It is recommended to use Postman to test the queries for a better experience.


