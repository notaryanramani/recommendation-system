from flask import render_template, request, redirect, url_for, flash, session
from web_app import app
import html

import pandas as pd
import numpy as np
import pickle

movies_encoded_data = pd.read_csv('data/source/movies_encoded_data.csv')
movies_info_data = pd.read_csv('data/source/movies_info_data.csv')

movies_nn_model = pickle.load(open('models/nn_model_movies.pkl', 'rb'))
movies_ratings_scaler = pickle.load(open('models/movies_rating_scaler.pkl', 'rb'))

books_data = pd.read_csv('data/source/books_encoded_data.csv', index_col=0)
books_nn_model = pickle.load(open('models/nn_model_book.pkl', 'rb'))

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
    movies_list = movies_info_data['title'].sort_values(ascending=True)
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
    return render_template('movies.html', recs = recs, movies_list = movies_list)


@app.route('/movies_name', methods=['POST', 'GET'])
def movies_name():
    movies_list = movies_info_data['title'].sort_values(ascending=True)
    recs = None
    if request.method == 'POST':
        option = request.form.get('opt')
        movie_name = html.unescape(request.form.get('user_input'))
        movie_index = movies_info_data.loc[movies_info_data['title'] == movie_name].index[0]
        sample = np.array(movies_encoded_data.iloc[movie_index]).reshape(1, -1)
        if option == 'top5':
            distances, indices = movies_nn_model.kneighbors(sample, n_neighbors = 6)
            recs = []
            for i in range(0, len(indices.flatten())):
                rec = movies_info_data.iloc[indices.flatten()[i]]['title']
                if rec != movie_name:
                    recs.append(rec)
        elif option == 'random5':
            random_nums = np.random.randint(0, 100, 5)
            distances, indices = movies_nn_model.kneighbors(sample, n_neighbors = 100)
            recs = []
            for i in random_nums:
                rec = movies_info_data.iloc[indices.flatten()[i]]['title']
                if rec != movie_name:
                    recs.append(rec)
        else:
            flash('Choose Option')
    return render_template('movies.html', recs = recs, movies_list = movies_list)


@app.route('/books', methods=['POST', 'GET'])
def books():
    books_titles = list(books_data.index)
    recs = None
    if request.method == 'POST':
        option = request.form.get('opt')
        book_name = html.unescape(request.form.get('user_input'))
        sample = np.array(books_data.loc[books_data.index == book_name]).reshape(1, -1)
        if option == 'top5':
            distances, indices = books_nn_model.kneighbors(sample, n_neighbors = 6)
            recs = []
            for i in range(0, len(indices.flatten())):
                rec = books_data.iloc[indices.flatten()[i]].name
                if rec != book_name:
                    recs.append(rec)
        elif option == 'random5':
            random_nums = np.random.randint(0, 100, 5)
            distances, indices = books_nn_model.kneighbors(sample, n_neighbors = 100)
            recs = []
            for i in random_nums:
                rec = books_data.iloc[indices.flatten()[i]].name
                if rec != book_name:
                    recs.append(rec)
        else:
            flash('Choose Option')
    return render_template('books.html', recs=recs, books_titles=books_titles)