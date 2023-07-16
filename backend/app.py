import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from fuzzywuzzy import fuzz
from flask import Flask, jsonify, request
from flask_cors import CORS 
movies = pd.read_csv('./data/movies.csv')

def extract_title(title):
  year = title[len(title) - 5 : len(title) - 1]

  if year.isnumeric():
    title_no_year = title[:len(title)-7]
    return title_no_year
  else:
    return title

def extract_year(title):
  year = title[len(title)-5:len(title)-1]
  if year.isnumeric():
    return int(year)
  else:
    return np.nan

# change the column name from title to title_year
movies.rename(columns={'title':'title_year'}, inplace=True) 
# remove leading and ending whitespaces in title_year
movies['title_year'] = movies['title_year'].apply(lambda x: x.strip()) 
# create the columns for title and year
movies['title'] = movies['title_year'].apply(extract_title) 
movies['year'] = movies['title_year'].apply(extract_year) 

r,c = movies[movies['genres']=='(no genres listed)'].shape

# remove the movies without genre information and reset the index
movies = movies[~(movies['genres']=='(no genres listed)')].reset_index(drop=True)

# remove '|' in the genres column
movies['genres'] = movies['genres'].str.replace('|',' ')
# count the number of occurences for each genre in the data set
counts = dict()
for i in movies.index:
  for g in movies.loc[i,'genres'].split(' '):
    if g not in counts:
      counts[g] = 1
    else:
      counts[g] = counts[g] + 1

# change 'Sci-Fi' to 'SciFi' and 'Film-Noir' to 'Noir'
movies['genres'] = movies['genres'].str.replace('Sci-Fi','SciFi')
movies['genres'] = movies['genres'].str.replace('Film-Noir','Noir')

# create an object for TfidfVectorizer
tfidf_vector = TfidfVectorizer(stop_words='english')
# apply the object to the genres column
tfidf_matrix = tfidf_vector.fit_transform(movies['genres'])

sim_matrix = linear_kernel(tfidf_matrix,tfidf_matrix)

# create a function to find the closest title
def matching_score(a,b):
  return fuzz.ratio(a,b)

# a function to convert index to title_year
def get_title_year_from_index(index):
  return movies[movies.index == index]['title_year'].values[0]
# a function to convert index to title
def get_title_from_index(index):
  return movies[movies.index == index]['title'].values[0]
# a function to convert title to index
def get_index_from_title(title):
  return movies[movies.title == title].index.values[0]
# a function to return the most similar title to the words a user type
def find_closest_title(title):
  leven_scores = list(enumerate(movies['title'].apply(matching_score, b=title)))
  sorted_leven_scores = sorted(leven_scores, key=lambda x: x[1], reverse=True)
  closest_title = get_title_from_index(sorted_leven_scores[0][0])
  distance_score = sorted_leven_scores[0][1]
  return closest_title, distance_score

def contents_based_recommender(movie_user_likes, how_many):
  closest_title, distance_score = find_closest_title(movie_user_likes)
  recommendations = []
  # When a user does not make misspellings
  if distance_score == 100:
    movie_index = get_index_from_title(closest_title)
    movie_list = list(enumerate(sim_matrix[int(movie_index)]))
    # remove the typed movie itself
    similar_movies = list(filter(lambda x:x[0] != int(movie_index), sorted(movie_list,key=lambda x:x[1], reverse=True))) 
    
    print('Here\'s the list of movies similar to '+'\033[1m'+str(closest_title)+'\033[0m'+'.\n')
    for i,s in similar_movies[:how_many]:
      recommendations.append(get_title_year_from_index(i))
  # When a user makes misspellings    
  else:
    movie_index = get_index_from_title(closest_title)
    movie_list = list(enumerate(sim_matrix[int(movie_index)]))
    similar_movies = list(filter(lambda x:x[0] != int(movie_index), sorted(movie_list,key=lambda x:x[1], reverse=True)))
    print('Here\'s the list of movies similar to '+'\033[1m'+str(closest_title)+'\033[0m'+'.\n')
    for i, s in similar_movies[:how_many]:
      recommendations.append(get_title_year_from_index(i))
  return closest_title, recommendations

app = Flask(__name__)
CORS(app)

@app.route('/recommender', methods=['POST'])
def recommend():
  if 'movie' not in request.args:
    return 'A movie name is required'

  movie = request.args.get("movie")
  size = int(request.args.get("size")) if 'size' in request.args else 20

  if not movie:
    return
  
  return jsonify(movies=contents_based_recommender(movie, size))

@app.route('/', methods=['GET'])
def index():
  return 'Movies content based recommender.'

if __name__ == '__main__':
  app.run()
  print('App Running')