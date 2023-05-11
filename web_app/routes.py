from flask import render_template, request, redirect, url_for, session
from web_app import app

import pandas as pd
import numpy as np
import pickle

movies_encoded_data = pd.read_csv('data/source/movies_encoded_data.csv')
movies_info_data = pd.read_csv('data/source/movies_info_data.csv')

movies_nn_model = pickle.load(open('models/nn_model_movies.pkl', 'rb'))
movies_ratings_scaler = pickle.load(open('models/movies_rating_scaler.pkl', 'rb'))

movies_input_dict = {}
for col in movies_encoded_data.columns:
    movies_input_dict[col.upper()] = 0

m = 9
C = 3.26
# determined from data used


@app.route('/')
def home(): 
    return render_template('home.html')


@app.route('/movies', methods=['POST', 'GET'])
def movies():
    recs = None
    if request.method == 'POST':
        v = int(request.form.get('ratings_count'))
        R = int(request.form.get('ratings_average'))
        weighted_avg = ((R * v) + (C * m)) / (v + m) 
        movies_input_dict['RATING_COUNT'] = movies_ratings_scaler.transform(np.array(v).reshape(1,-1))[0][0]
        movies_input_dict['RATING_AVG'] = R
        movies_input_dict['WEIGHTED_AVG'] = weighted_avg
        genres = request.form.get('genres').split(',')
        for genre in genres:
            temp_genre = genre.lstrip().rstrip().upper()
            if temp_genre in movies_input_dict.keys():
                movies_input_dict[temp_genre] = 1
        # print(movies_input_dict)
        sample = np.array(list(movies_input_dict.values())).reshape(1, -1)
        distances, indices = movies_nn_model.kneighbors(sample, n_neighbors = 5)
        recs = []
        for i in indices.flatten():
            recs.append(movies_info_data.iloc[i]['title'])
    return render_template('movies.html', recs = recs)


@app.route('/books')
def books():
    return render_template('books.html')