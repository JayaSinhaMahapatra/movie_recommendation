from flask import Flask, render_template, request
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Load data
movies = pd.read_csv('tmdb_5000_movies.csv')
credits = pd.read_csv('tmdb_5000_credits.csv')
movies = movies.merge(credits, on='title')
movies = movies[['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]
movies.dropna(inplace=True)

# Preprocess data
vectorizer = CountVectorizer()
vectors = vectorizer.fit_transform(movies['overview'])

# Recommendation logic
def recommend(movie_title):
    # Find movie index
    movie_index = movies[movies['title'] == movie_title].index
    if len(movie_index) == 0:
        return []

    movie_index = movie_index[0]  # Get the first index if multiple matches found

    # Calculate similarity scores
    similarity_scores = cosine_similarity(vectors, vectors[movie_index].reshape(1, -1))

    # Get top 5 similar movies
    similar_movies_indices = similarity_scores.argsort()[0][-6:-1][::-1]

    # Return movie titles of top 5 similar movies
    recommended_movies = [movies.iloc[index]['title'] for index in similar_movies_indices if index != movie_index]
    return recommended_movies

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        movie_title = request.form['movie_title']
        recommendations = recommend(movie_title)
        return render_template('index.html', recommendations=recommendations)
    return render_template('index.html', recommendations=[])
@app.route('/static/<path:path>')
def static_file(path):
    return app.send_static_file(path)


if __name__ == '__main__':
    app.run(debug=True)
