import streamlit as st
import pandas as pd
import requests
import pickle

# ---------------- Load Data ----------------
movies_dict = pickle.load(open('movies.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

API_KEY = 'affc3c3b904f873cf46f6e1be0098533'

# ---------------- Functions ----------------
def fetch_poster(movie_id):
    try:
        url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}'
        response = requests.get(url, timeout=5)
        data = response.json()
        return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    except:
        return "https://via.placeholder.com/500x750.png?text=No+Image"

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    recommended_movies_ids = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
        recommended_movies_ids.append(movie_id)

    return recommended_movies, recommended_movies_posters, recommended_movies_ids

# ---------------- Streamlit Config ----------------
st.set_page_config(page_title="Movie Magic", layout="wide", page_icon="🎬")

# ---------------- Sidebar ----------------
page = st.sidebar.selectbox("Navigate", ["Home", "Recommend", "About"])

# ---------------- Home Page ----------------
if page == "Home":
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@700&display=swap');

    .hero {
        height: 100vh;
        background-image: url('https://images.unsplash.com/photo-1524985069026-dd778a71c7b4?auto=format&fit=crop&w=1950&q=80');
        background-size: cover;
        background-position: center;
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
        text-align: center;
        color: white;
        font-family: 'Roboto', sans-serif;
        position: relative;
    }

    .overlay {
        position: absolute;
        top:0; left:0; right:0; bottom:0;
        background: rgba(0,0,0,0.5);
        z-index:1;
    }

    .hero-content {
        position: relative;
        z-index:2;
    }

    .hero-title {
        font-size: 80px;
        font-weight: bold;
        animation: floatText 3s ease-in-out infinite;
        text-shadow: 0 0 20px #ff4b4b, 0 0 40px #ff8c42, 0 0 60px #ffc107;
    }

    .hero-subtitle {
        font-size: 28px;
        margin-top:20px;
        background: rgba(255,255,255,0.1);
        padding: 15px 30px;
        border-radius: 15px;
        display: inline-block;
        animation: fadeIn 3s ease-in-out;
    }

    @keyframes floatText {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-20px); }
        100% { transform: translateY(0px); }
    }

    @keyframes fadeIn {
        0% {opacity:0;}
        100% {opacity:1;}
    }

    .cta-btn {
        margin-top:30px;
        padding:15px 40px;
        background: linear-gradient(90deg,#FF4B4B,#FF8C42);
        color:white;
        font-size:20px;
        border-radius:50px;
        text-decoration:none;
        transition:0.3s all;
    }

    .cta-btn:hover {
        transform: scale(1.1);
        box-shadow:0 0 20px #FF4B4B;
    }
    </style>

    <div class="hero">
        <div class="overlay"></div>
        <div class="hero-content">
            <h1 class="hero-title">Movie Magic</h1>
            <a class="cta-btn" href="#recommend">Get Recommendations</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ---------------- Recommend Page ----------------
elif page == "Recommend":
    st.markdown("<h2 style='color:#FF4B4B;'>Pick a movie you like:</h2>", unsafe_allow_html=True)
    selected_movie_name = st.selectbox("", movies['title'].values, key='movie_select')

    if st.button('Recommend'):
        names, posters, ids = recommend(selected_movie_name)
        st.markdown("<h3 style='color:#4B6CB7;'>Recommended Movies:</h3>", unsafe_allow_html=True)
        
        # Show cards
        cols = st.columns(len(names))
        for i, col in enumerate(cols):
            with col:
                st.image(posters[i], use_container_width=True)
                st.markdown(f"**{names[i]}**")
                
                # Expandable details
                details_url = f"https://api.themoviedb.org/3/movie/{ids[i]}?api_key={API_KEY}"
                response = requests.get(details_url)
                data = response.json()
                with st.expander("See Details"):
                    st.markdown(f"**Title:** {data.get('title','N/A')}")
                    st.markdown(f"**Overview:** {data.get('overview','N/A')}")
                    st.markdown(f"**Rating:** {data.get('vote_average','N/A')}")
                    st.markdown(f"**Release Date:** {data.get('release_date','N/A')}")

# ---------------- About Page ----------------
elif page == "About":
    st.markdown("<h2 style='color:#FF4B4B;'>About Movie Magic</h2>", unsafe_allow_html=True)
    st.markdown("""
    **Movie Magic** is a professional movie recommendation platform built for movie lovers.  

    **💡 Features:**
    - Personalized recommendations based on your favorite movies
    - Stunning movie posters from TMDB
    - Modern UI with animations
    - Full responsive design

    **🛠 Tech Stack:**
    - Python & Streamlit
    - Pandas & Pickle
    - TMDB API

    **📬 Contact:**
    - Email: nadafethi766@gmail.com  
    - Phone: 0633356195

    **🔗 Credits:**
    - Poster data & info from [TMDB](https://www.themoviedb.org/)
    """)
    st.image("https://images.unsplash.com/photo-1581091012184-d2d3f2e6f0f3?auto=format&fit=crop&w=1950&q=80", use_container_width=True)
