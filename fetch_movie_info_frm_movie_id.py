import pandas as pd
import requests
from time import sleep
from bs4 import BeautifulSoup
import json

def fetch_page_html(movie_id):
    url = f'https://www.imdb.com/title/{movie_id}/'
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"}
    page = requests.get(url, headers = headers)
    return page.content
    

def get_top_section_object(html):
    soup = BeautifulSoup(html, "html.parser")

    top_section = soup.find('section', attrs={'class': [
        "ipc-page-background", 
        "ipc-page-background--baseAlt", 
        "sc-1cdfe45a-0 iWJZJA"]})
    return top_section

def get_title(top_section):
    return top_section.find('h1').text

#   I use top section because that it where the movie data I need are placed
def get_release_year_and_parent_rating(top_section):
    ul = top_section.find('ul', attrs={"data-testid":"hero-title-block__metadata"})

    list_items = ul.find_all('li')
    
    if len(list_items) < 2: # Any movie with < 2 items on this sect. is lacking release yr and parent.
        return None, None
    first_item, second_item  = list_items[0:2] # just need the yr and parental rating info

    year_anchor = first_item.find('a')
    parental_rating = None        # most movies lacks parental rating info
    if year_anchor:
        year = year_anchor.text
        parental_rating = second_item.find('a')
        if parental_rating:
            parental_rating = parental_rating.text
    else:
        year = second_item.find('a').text # this is for TV series that have realese yr as 2nd item
    
        
    return year, parental_rating

def get_movie_genre(top_section):
    genre_parent = top_section.find('div', attrs={"data-testid":"genres"})
    
    if genre_parent is None: # Most TV series do not have genre
        return None
    movie_genres = []

    for anchor in genre_parent.find_all('a'):
        movie_genres.append(anchor.text)

    return ', '.join(movie_genres)

def get_movie_summary(top_section):
    summary = top_section.find('span', attrs={"data-testid":"plot-xl"})
    if not summary:    # Most TV series and some movies do not have genre
        return None
    return summary.text

def get_movie_crew(top_section):
    info_parent = top_section.find('div', attrs={'class': ["sc-10602b09-10"]})

    ul = info_parent.find('ul', attrs={'class': [
        "ipc-metadata-list", 
        "ipc-metadata-list--dividers-all", 
        "title-pc-list", 
        "ipc-metadata-list--baseAlt"]})
    
    if ul is None:           # for movies and TV series do not have crew info
        return None, None, None


    movie_crew = ul.find_all('ul')
    director = writers = None   # In case the movie or TV series is lacking this info
                                # movies has director while TV series has writer
    stars_ul = movie_crew[-1]   # Because stars info is always the last detail on this list

    stars = []
    stars_ul.find('a').text

    for star in stars_ul.find_all('a'): # To get all stars in the list of stars
          stars.append(star.text)

    stars = ', '.join(stars) # Join all stars in a row
    
    if len(movie_crew) == 3:
        director_ul, writer_ul, stars_ul = movie_crew
        director = director_ul.find('a').text
        writers = []

        writer_ul.find('a').text

        for writer in writer_ul.find_all('a'):
              writers.append(writer.text)

        writers = ', '.join(writers)


    return writers, stars, director
    
def get_movie_data(movie_id):     # Function combining all the other functions
    imdb_html = fetch_page_html(movie_id)
    top_section = get_top_section_object(imdb_html)
    if not top_section:       # In case the page has no movie detail at all
        return None
    
    title = get_title(top_section)
    release_year, parent_rating = get_release_year_and_parent_rating(top_section)
    genres = get_movie_genre(top_section)
    summary = get_movie_summary(top_section)
    writers, stars, director = get_movie_crew(top_section)
    return {
       'title': title,
        'release_year': release_year,
        'parent_rating': parent_rating,
        'genres': genres,
        'summary': summary,
        'writers': writers,
        'stars': stars,
        'director': director
        
    }
    
    
def extract_movies_data(movie_id_list): # Extracting all movie data from my movie id list.
    movies = []
    
    for movie_id in movie_id_list:
        print(f'Getting movie data for {movie_id}...')
        movie_data= get_movie_data(movie_id)
        if movie_data:
            movies.append(movie_data)
    return movies


df = pd.read_csv('clean\clean_movie_hunt.csv')

imdb_ids_from_csv  = df['Imdb_id'].unique()

# Extracting the 1st 200 movie data from my movie id list. 
first_200 = extract_movies_data(imdb_ids_from_csv[:200]) 

sleep(120)
print('Extracted the first 200, now we are going to sleep')


# Extracting the 2nd 200 movie data from my movie id list.
second_200 = extract_movies_data(imdb_ids_from_csv[200:400])

sleep(120)
print('Extracted the second 200, now we are going to sleep')


# Extracting the 3rd 200 movie data from my movie id list.
third_200 = extract_movies_data(imdb_ids_from_csv[400:600])

sleep(120)
print('Extracted the third 200, now we are going to sleep')


# Extracting the remaining movie data from my movie id list.
fourth_200 = extract_movies_data(imdb_ids_from_csv[600:])

movie_data_list = first_200 + second_200 + third_200 + fourth_200

# combining all the extracted movies to a single list and convert to json file
dumped_json_str = json.dumps(movie_data_list)

with open('scraped_data/patrick_second_movie_project.json', 'w') as file:
    file.write(dumped_json_str)
