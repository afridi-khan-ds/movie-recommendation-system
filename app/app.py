import streamlit as st
import pandas as pd
import pickle

# Page config
st.set_page_config(page_title="Movie Recommender", page_icon="🎬")

# Load data
movies = pd.read_csv('data/movies.csv')

# Load model
with open('models/item_similarity.pkl', 'rb') as f:
    item_similarity_df = pickle.load(f)

# Title
st.title("🎬 Movie Recommendation System")
st.write("Get movie recommendations based on similarity")

# Input
movie_name = st.text_input("Enter a movie name")

# Recommendation function
def recommend_movies(movie_title):
    
    movie_title = movie_title.lower().strip()
    
    matches = [m for m in item_similarity_df.columns if movie_title in m.lower()]
    
    if not matches:
        return []
    
    matched_movie = matches[0]
    
    similar_movies = item_similarity_df[matched_movie].sort_values(ascending=False)
    similar_movies = similar_movies.drop(matched_movie)
    
    return similar_movies.head(10).index.tolist()

# Button
if st.button("Recommend"):
    
    if movie_name == "":
        st.warning("Please enter a movie name")
    
    else:
        results = recommend_movies(movie_name)
        
        if not results:
            st.error("Movie not found")
        else:
            st.success("Here are some recommendations:")
            
            for i, movie in enumerate(results, 1):
                st.write(f"{i}. {movie}")
                
st.markdown("---")
st.markdown("### About")
st.write("This app recommends movies using collaborative filtering based on user ratings.")