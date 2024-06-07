import pickle
import streamlit as st
import pandas as pd
import requests
from requests.exceptions import ConnectionError
from tenacity import retry, wait_fixed, stop_after_attempt
from requests.exceptions import ConnectionError, Timeout


def fetch_poster(movie_id):
   response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=192f4bef78fa7c1020f0116eb99c0398&language=en-US'.format(movie_id))
   data = response.json()
   return "https://image.tmdb.org/t/p/w500/"+data['poster_path']

    
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse=True,key = lambda x: x[1])[1:6]
    
    recommend_movies = []
    recommended_movie_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommend_movies.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))
    return recommend_movies,recommended_movie_posters



movies_dict = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl','rb'))

st.title("Movie Recommendation System")

selected_movie_name=option = st.selectbox(
    'How would you like to be contacted?',
    (movies['title'].values)
)


if st.button('Recommend'):
    names,poster = recommend(selected_movie_name)
    cols = st.columns(5)

    for i, col in enumerate(cols):
        with col:
            st.text(names[i])
            st.image(poster[i])
