import streamlit as st
import pandas as pd
import requests, pickle, gzip
st.title('Movie Recommender System')

@st.cache_data
def load_movies():
    return pickle.load(open('movies.pkl', 'rb'))

@st.cache_data
def load_similarity():
    with gzip.open('similarities.pkl.gz', 'rb') as f:
        similarities = pickle.load(f)
    return similarities
movies = load_movies()
similarity = load_similarity()

def get_image(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/images"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI5ZGJhYTljMzIzYzc3YTIyZDVkODFlNGNhNTE0ZmJjMyIsIm5iZiI6MTcyNTcwMDM3Ny40NjQ0MTQsInN1YiI6IjY2ZGMxNzQxZDAxZTUwOTkzMDk2NWJhNCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.jgEc3IGu9byHPh3QlNUmnJ8BGp2ZOkJnec8CsifyoVA"
    }
    data = requests.get(url, headers=headers).json()
    if 'backdrops' in data and len(data['backdrops']) > 0:
        file_path = data['backdrops'][0]['file_path']
        image_url = f"https://image.tmdb.org/t/p/w500{file_path}"
        return image_url
@st.cache_data
def recommend(name):
    idx = movies[movies['title'] == name].index[0]
    cs_value = sorted(list(enumerate(similarity[idx])), reverse=True, key = lambda x: x[1])[0:6]
    return cs_value
# @st.cache_data
# def movies_df():
#     return pd.read_csv("merged_movies.csv")
# movies = movies_df()

def search_movies(movie):
    recommendations = recommend(movie)
    movie_name, posters = [], []
    for i in recommendations[0:]:
        mov_fetched = movies.iloc[i[0]]
        movie_name.append(mov_fetched.title)
        posters.append(get_image(mov_fetched.id))
    return movie_name, posters

movie = st.selectbox('Seach a Movie', movies['title'])
if st.button('Search'):
    names, posters = search_movies(movie)
    col1, col2, col3 = st.columns(3)
    col4, col5, col6 = st.columns(3)
    columns = [col1,col2,col3,col4,col5,col6]
    for i in range(6):
        if posters[i]:
            with columns[i]:
                # st.header(names[i])
                st.image(posters[i],caption=names[i])