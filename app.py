import streamlit as st
import pickle
import pandas as pd
import requests
import os

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
similarity = pickle.load(open('similarity.pkl', 'rb'))



def fetch_poster(movie_id):
    #response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key={TMDB_API_KEY}&language=en-US'.format(movie_id))
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US')
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/"+ data['poster_path']

movies_df = pickle.load(open('movies.pkl', 'rb'))
movies_list = movies_df['title'].tolist()
similarity = pickle.load(open('similarity.pkl', 'rb'))

def recommend(movie):
    if movie not in movies_list:
        return ["Movie not found!"], []

    movie_index = movies_df[movies_df['title'] == movie].index[0]
    distance = similarity[movie_index]
    m_list = sorted(enumerate(distance), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_poster = []
    for i in m_list:
        movie_id = movies_df.iloc[i[0]].id
        recommended_movies.append(movies_df.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_poster  

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'Select a movie', movies_list
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    if names == ["Movie not found!"]:
        st.error("Movie not found!")
    else:
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.text(names[0])
            st.image(posters[0])
        with col2:
            st.text(names[1])
            st.image(posters[1])
        with col3:
            st.text(names[2])
            st.image(posters[2])
        with col4:
            st.text(names[3])
            st.image(posters[3])
        with col5:
            st.text(names[4])
            st.image(posters[4])

import os
print("Current working directory:", os.getcwd())
print("Files in the directory:", os.listdir())
