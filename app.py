import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    api_key='8265bd1679663a7ea12ac168da84d2e8'
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US'.format(movie_id))
    result = response.json()
    return 'https://image.tmdb.org/t/p/w500'+result['poster_path']


movie_dict = pickle.load(open('movie_dict.pkl','rb'))
movie = pd.DataFrame(movie_dict)
similarity = pickle.load(open('similarity.pkl','rb'))

def recommendor_system(movie_name) :
    # index of the movie in df
    movie_index = movie[movie['title']==movie_name].index[0]
    distances = similarity[movie_index]
    #we will sort the distances and to get the correct index we use enumerate
    movies_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    recommended_movie=[]
    recommended_movies_poster=[]
    for i in movies_list :
        movie_id= movie.iloc[i[0]].movie_id
        recommended_movie.append(movie.iloc[i[0]].title)
        #fetch poster from api
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movie,recommended_movies_poster

st.title('Movie-Recommender-System')

selected_movie_name = st.selectbox('write your movie name',movie['title'].values)

if st.button('recommend'):
    recommended_movies,poster=recommendor_system(selected_movie_name)
    col1,col2,col3,col4,col5 = st.columns(5)
    with col1:
        st.text(recommended_movies[0])
        st.image(poster[0])
    with col2:
        st.text(recommended_movies[1])
        st.image(poster[1])
    with col3:
        st.text(recommended_movies[2])
        st.image(poster[2])
    with col4:
        st.text(recommended_movies[3])
        st.image(poster[3])
    with col5:
        st.text(recommended_movies[4])
        st.image(poster[4])

