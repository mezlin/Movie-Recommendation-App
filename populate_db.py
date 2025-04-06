# THIS SCRIPT IT FOR POPULATING THE MOVIE DATABASE
# This script fetches movie data from TMDB and populates a MySQL database with the information.
# It retrieves movie details such as title, genre, director, actors and overview.

import requests
import mysql.connector
import time

# Your TMDB API key
API_KEY = "your_api_key_here"

# Function to get movie data from TMDB
def get_movie_data(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    response = requests.get(url)
    data = response.json()

    title = data.get("title")
    genre = ", ".join([g['name'] for g in data.get('genres', [])])  # Extract genres
    director = "Unknown"  # We will fetch the director separately
    actors = "Unknown"  # We will fetch the actors separately
    overview = data.get("overview", "No overview available.")

    return title, genre, director, actors, overview

# Function to get the director (since it's in the crew data)
def get_movie_director(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={API_KEY}"
    response = requests.get(url)
    data = response.json()

    for crew_member in data.get('crew', []):
        if crew_member['job'] == 'Director':
            return crew_member['name']
    
    return "Unknown Director"

# Function to get the actors
def get_movie_actors(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={API_KEY}"
    response = requests.get(url)
    data = response.json()

    actors = []
    for cast_member in data.get('cast', []):
        actors.append(cast_member['name'])
    
    return ", ".join(actors)

# Function to insert data into the database
def insert_movie_into_db(movie_id):
    title, genre, director, actors, overview= get_movie_data(movie_id)
    director = get_movie_director(movie_id)
    actors = get_movie_actors(movie_id)

    # Connect to MySQL
    conn = mysql.connector.connect(
        host="localhost",
        user="your username",
        password="your password",
        database="your database name"
    )
    cursor = conn.cursor()

    # Get the latest ID from the database (to increment)
    cursor.execute("SELECT MAX(id) FROM movies")
    last_id = cursor.fetchone()[0]
    new_id = last_id + 1 if last_id is not None else 1  # If no rows exist, start from 1

    # Insert the movie data into the movies table
    cursor.execute("""
        INSERT INTO movies (id, title, genre, director, actors, overview)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (new_id, title, genre, director, actors, overview))

    conn.commit()
    cursor.close()
    conn.close()
    print(f"Inserted {title} into the database")

# Function to get the total number of pages
def get_total_pages():
    url = f"https://api.themoviedb.org/3/movie/popular?api_key={API_KEY}&language=en-US&page=1"
    response = requests.get(url)
    data = response.json()
    return data['total_pages']

# Function to populate the database with all movies
def populate_database():
    total_pages = 50  # Set a limit for the number of pages to fetch
    # total_pages = get_total_pages()  # Uncomment this line to fetch the actual number of pages 
    # BE AWARE THAT THERE IS MORE THAN 49000 PAGES!!!!

    # Loop through all the pages
    for page in range(1, total_pages + 1):
        print(f"Fetching page {page}/{total_pages}...")
        
        url = f"https://api.themoviedb.org/3/movie/popular?api_key={API_KEY}&language=en-US&page={page}"
        response = requests.get(url)
        data = response.json()

        for movie in data['results']:
            movie_id = movie['id']
            insert_movie_into_db(movie_id)
        
        # Sleep to avoid hitting the rate limit
        time.sleep(1)

if __name__ == "__main__":
    populate_database()