# Importing necessary libraries
import requests
import json
import time
import csv
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import random
from rapidfuzz import process, fuzz
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Jojol2014",
        database="movie_reco"
    )

# Load the dataset from the database
conn = get_db_connection()
ds = pd.read_sql("SELECT * FROM movies", conn)
conn.close()

# Fill the missing values with empty string
ds.fillna("", inplace=True)

# Combine relevant features into a single string
ds["combined_features"] = ds["genre"] + " " + ds["director"] + " " + ds["actors"] + " " + ds["overview"]

# Convert the text to a matrix of TF-IDF features
vectorizer = TfidfVectorizer(stop_words="english")
tfidf_matrix = vectorizer.fit_transform(ds["combined_features"].values.astype('U'))

# Compute the cosine similarity matrix
cosine_sim = cosine_similarity(tfidf_matrix)

# Function to get the movie recommendations
def get_recommendations(movie_title, cosine_sim=cosine_sim, ds=ds):
    movie_title = movie_title.lower()  # Convert to lowercase for case-insensitive matching

    # Convert all dataset titles to lowercase and find matching index
    ds["lower_title"] = ds["title"].str.lower()
    
    # Use RapidFuzz to find the best match
    best_match, score, _ = process.extractOne(movie_title, 
                                              ds["lower_title"], 
                                              scorer=fuzz.WRatio) # Using WRatio for typos and different spellings

    if score < 75:  # If the best match is not good enough
        print("No close match found.")
        return {"message": "No close match found.", "recommendations": []}
    
    # Get the index of the movie that matches the title
    matched_idx = ds[ds["lower_title"] == best_match].index[0]
    matched_title = ds.iloc[matched_idx]["title"]
    print(f"Best match found: {matched_title} with score {score}")
    idx = matched_idx

    # Get similarity scores for all movies
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the movies based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    # Get the scores of the 10 most similar movies
    top_movies = [ds.iloc[i[0]]["title"] for i in sim_scores[0:10]]

    return {"message": f"Best match found: {matched_title}", "recommendations": top_movies}

def get_reco_on_pref(fav_genres, fav_actors, fav_directors, ds=ds):
    filtered_movies = ds.copy()
    
    # Filter by genres
    if fav_genres:
        filtered_movies = filtered_movies[filtered_movies["genre"].str.contains('|'.join(fav_genres), case=False, na=False)]

    # Filter by actors
    if fav_actors:
        filtered_movies = filtered_movies[filtered_movies["actors"].str.contains('|'.join(fav_actors), case=False, na=False)]

    # Filter by directors
    if fav_directors:
        filtered_movies = filtered_movies[filtered_movies["director"].str.contains('|'.join(fav_directors), case=False, na=False)]

    # If no movies match, return a random movie
    if filtered_movies.empty:
       return {"message": "No movies found matching your preferences.", "recommendations": []}
    
    # Handle the case where the filtered movies are less than 5
    if len(filtered_movies) < 5:
        return {"message": "Movies based on your preferences", "recommendations": filtered_movies.sample()["title"].tolist()}
    
    return {"message": "Movies based on your preferences", "recommendations": filtered_movies.sample(5)["title"].tolist()}

def search_movies_by(category, keyword, ds=ds):
    if category not in ["genre", "actors", "director"]:
        return {"message": "Invalid category. Choose 'Genre', 'Actors', or 'Director'.", "results": []}
    
    results = ds[ds[category].str.contains(keyword, case=False, na=False)]["title"].tolist()
    results = random.sample(results, len(results))

    if results:
        return {"message": f"Movies found for {category} - {keyword}", "recommendations":results[:10]}
    return {"message": "No movies found.", "results": []}

# Route to the home page
@app.route("/")
def home():
    return render_template("index.html")

# Route to get movie recommendations based on title
@app.route("/recommend", methods=["GET"])
def recommend():
    movie_title = request.args.get("title")
    if not movie_title:
        return jsonify({"error": "No title provided."}), 400
    return jsonify(get_recommendations(movie_title)), 200

# Route to get movie recommendations based on user preferences
@app.route("/recommend/preferences", methods=["POST"])
def recommend_preferences():
    data = request.get_json()
    fav_genres = data.get("genres", ["action"])
    fav_actors = data.get("actors", [])
    fav_directors = data.get("directors", [])

    if not fav_genres and not fav_actors and not fav_directors:
        return jsonify({"error": "No preferences provided."}), 400
    return jsonify(get_reco_on_pref(fav_genres, fav_actors, fav_directors)), 200

# Route to search movies by category
@app.route("/search", methods=["GET"])
def search():
    category = request.args.get("category")
    keyword = request.args.get("keyword")

    if not category or not keyword:
        return jsonify({"error": "Missing 'category' or 'keyword' parameter"}), 400

    return jsonify(search_movies_by(category, keyword)), 200

if __name__ == "__main__":
    app.run(debug=True) # By default, Flask runs on port 5000