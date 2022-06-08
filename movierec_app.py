import streamlit as st
import json
from data_classifier import KNearestNeighbours
from operator import itemgetter
from PIL import Image

# Load data and movies list from corresponding JSON files
with open(r'data.json', 'r+', encoding='utf-8') as f:
    data = json.load(f)
with open(r'titles.json', 'r+', encoding='utf-8') as f:
    movie_titles = json.load(f)

def knn(test_point, k):
    # Create dummy target variable for the KNN Classifier
    target = [0 for item in movie_titles]
    # Instantiate object for the Classifier
    model = KNearestNeighbours(data, target, test_point, k=k)
    # Run the algorithm
    model.fit()
    # Distances to most distant movie
    max_dist = sorted(model.distances, key=itemgetter(0))[-1]
    # Print list of 10 recommendations < Change value of k for a different number >
    table = list()
    for i in model.indices:
        # Returns back movie title and imdb link
        table.append([movie_titles[i][0], movie_titles[i][2]])
    return table

if __name__ == '__main__':
    genres = ['Action', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Family',
              'Fantasy', 'Film-Noir', 'Game-Show', 'History', 'Horror', 'Music', 'Musical', 'Mystery', 'News',
              'Reality-TV', 'Romance', 'Sci-Fi', 'Short', 'Sport', 'Thriller', 'War', 'Western']

    movies = [title[0] for title in movie_titles]
    st.markdown("<h1 style='text-align: center;'>RECLINER LOUNGE</h1>", unsafe_allow_html=True)
    
    st.markdown("<h2 style='text-align: center;'>Which Movie to Watch Today?</h2>", unsafe_allow_html=True)
    #st.header('Which Movie To Watch Today?')
    st.markdown("<h3 style='text-align: center;'>One solution for all movie cravings!</h3>", unsafe_allow_html=True)
    #st.subheader('One solution for all movie cravings!')
    #loading image from system
    img = Image.open('yo.png') 
    st.image(img, use_column_width=True)
    
    name = st.text_input("Enter Your Name", "Type Here")
    if(st.button('Submit')):
       result = name.title()
    
    st.write("This is a simple Movie Recommendation Application. \nIt consists of redirecting IMDB links to particular movies in order to give the viewers a review of selected movies."
                        "\nYou can select the genres and change the IMDb score. \nClick on the Movie and you'll be redirected to its IMDB page and watch its trailer.\n\n")
    
    apps = ['--Select--', 'Movie based', 'Genres based']   
    app_options = st.selectbox('Select application:', apps)
    st.write("Select on which basis you'd like movie recommendations.")
    
    if app_options == 'Movie based':
        movie_select = st.selectbox('Select movie:', ['--Select--'] + movies)
        if movie_select == '--Select--':
            st.write('Select a movie')
        else:
            n = st.number_input('Number of movie recommendations:', min_value=5, max_value=20, step=1)
            genres = data[movies.index(movie_select)]
            test_point = genres
            table = knn(test_point, n)
            for movie, link in table:
                # Displays movie title with link to imdb
                st.markdown(f"[{movie}]({link})")
    elif app_options == apps[2]:
        st.write("Select your favourite genres")
        options = st.multiselect('Select genres:', genres)
        if options:
            imdb_score = st.slider('IMDb score:', 1, 10, 8)
            st.write("You can customize IMDB score")
            n = st.number_input('Number of movie recommendations:', min_value=5, max_value=20, step=1)
            test_point = [1 if genre in options else 0 for genre in genres]
            test_point.append(imdb_score)
            table = knn(test_point, n)
            for movie, link in table:
                # Displays movie title with link to imdb
                st.markdown(f"[{movie}]({link})")

        else:
                st.write("This is a simple Movie Recommendation Application. \nIt consists of redirecting IMDB links to particular movies in order to give the viewers a review of selected movies."
                        "\nYou can select the genres and change the IMDb score. \nClick on the Movie and you'll be redirected to its IMDB page and watch its trailer.")

    else:
        st.write('Select option')
  
#loading audio from system
    st.write("Play this button to accompany your vibe while you look for your movie!!")
    audio1 = open("song.mp3", "rb")
    st.audio(audio1)
    
    img = Image.open('yo1.png') 
    st.image(img, use_column_width=True)
