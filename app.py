import os
import pickle
import pandas as pd
import streamlit as st
import requests
import logging
import warnings
import zipfile
import urllib.request
st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide"
)

# Setup logging and suppress warnings
logging.basicConfig(level=logging.ERROR)
st.set_option('client.showErrorDetails', False)
warnings.filterwarnings("ignore")



# ✅ Download similarity.zip if not exists
if not os.path.exists("similarity.pkl"):
    zip_url = "https://drive.google.com/file/d/14qQt-2ctu1dhTOtjY7zCBWKkLLopP_Yv/view?usp=drivesdk"  # direct download link
    urllib.request.urlretrieve(zip_url, "similarity.zip")

    # ✅ Unzip it
    with zipfile.ZipFile("similarity.zip", "r") as zip_ref:
        zip_ref.extractall()  # extract to current directory

# ✅ Load data
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))






# Setup requests session
session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0',
    'Accept': 'application/json'
})

# Poster fetch function
def fetch_poster(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=e44a3f3a67c827f9403cf85f5ce37fac&language=en-US'
    for attempt in range(3):
        try:
            response = session.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                poster_path = data.get('poster_path')
                return f"https://image.tmdb.org/t/p/w500/{poster_path}" if poster_path else "https://via.placeholder.com/500x750?text=No+Image"
            else:
                logging.error(f"Poster fetch failed. Status code: {response.status_code}")
                return "https://via.placeholder.com/500x750?text=No+Image"
        except Exception as e:
            logging.error(f"Retrying poster fetch ({attempt + 1}/3) due to: {e}")
    logging.error("Failed to fetch poster after 3 attempts.")
    return "https://via.placeholder.com/500x750?text=Error"

# Description fetch function
def fetch_description(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=e44a3f3a67c827f9403cf85f5ce37fac&language=en-US'
    for attempt in range(3):
        try:
            response = session.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                return data.get('overview', 'No description available.')
            else:
                logging.error(f"Description fetch failed. Status code: {response.status_code}")
                return "No description available."
        except Exception as e:
            logging.error(f"Retrying description fetch ({attempt + 1}/3) due to: {e}")
    logging.error("Failed to fetch description after 3 attempts.")
    return "Error retrieving description."

# Recommendation logic
def recommend(query):
    query = query.lower()
    matched_title = movies[movies['title'].str.lower() == query]

    recommended_indices = set()

    if not matched_title.empty:
        index = matched_title.index[0]
        recommended_indices.add(index)
        distances = similarity[index]
        recs = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
        for rec in recs:
            recommended_indices.add(rec[0])
    else:
        genre_matches = movies[movies['tags'].str.lower().str.contains(query)]
        if genre_matches.empty:
            return [], [], []

        top_n = min(3, len(genre_matches))
        indices = genre_matches.index[:top_n]

        for index in indices:
            recommended_indices.add(index)
            distances = similarity[index]
            recs = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:4]
            for rec in recs:
                recommended_indices.add(rec[0])

    recommended_movies = []
    recommended_movies_posters = []
    recommended_movies_descriptions = []

    for index in list(recommended_indices)[:10]:
        movie_id = movies.iloc[index]['movie_id']
        recommended_movies.append(movies.iloc[index]['title'])
        recommended_movies_posters.append(fetch_poster(movie_id))
        recommended_movies_descriptions.append(fetch_description(movie_id))

    return recommended_movies, recommended_movies_posters, recommended_movies_descriptions



# Background image and styling
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1524985069026-dd778a71c7b4?fit=crop&w=1500&q=80");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }

    .stTitle, .stSubheader {
        color: white !important;
    }

    .stTextInput input {
        color: white;
        background-color: rgba(0, 0, 0, 0.5);
    }

    .stButton button {
        color: white;
        background-color: grey;
    }

    p {
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# App title and input
st.markdown('<h1 style="color: white;">🎬 Movie Recommendation System</h1>', unsafe_allow_html=True)
selected_movie_name = st.text_input("Enter a movie title or genre:")

if st.button('🎥 Get Recommendations'):
    if selected_movie_name:
        names, posters, descriptions = recommend(selected_movie_name)
        if names:
            st.markdown('<h3 style="color: white;">📽️ Recommended Movies for You:</h3>', unsafe_allow_html=True)
            movies_per_row = 5
            for i in range(0, len(names), movies_per_row):
                cols = st.columns(movies_per_row)
                for j in range(movies_per_row):
                    if i + j < len(names):
                        with cols[j]:
                            st.markdown(
                                f"""
                                <div style="display: flex; flex-direction: column; align-items: center;
                                            border: 1px solid #eee; border-radius: 10px; padding: 10px;
                                            height: 550px; overflow: hidden; text-align: center;
                                            background-color: rgba(255, 255, 255, 0.8);">
                                    <img src="{posters[i + j]}" style="height: 250px; object-fit: cover; border-radius: 8px;" />
                                    <h4 style="margin: 10px 0 5px 0;">{names[i + j]}</h4>
                                    <p style="font-size: 14px; color: #555; overflow: hidden;
                                              text-overflow: ellipsis; display: -webkit-box;
                                              -webkit-line-clamp: 5; -webkit-box-orient: vertical;
                                              text-align: justify;">
                                        {descriptions[i + j]}
                                    </p>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
        else:
            st.error("⚠️ No recommendations found for that input.")
    else:
        st.error("⚠️ Please enter a movie name or genre.")
