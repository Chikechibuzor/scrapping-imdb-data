import csv 
import requests


def read_raw_txt_file():
    movie_list= []
    with open('raw/movie-list.txt', 'r', encoding='UTF8') as f:
        movie_list = f.read()
        movie_list = movie_list.split('\n')
    return movie_list 

def get_movie_json_from_imdb(movie_name):
    movie_name = movie_name.lower()
    movie_search_url = "https://v2.sg.media-imdb.com/suggestion/{initial}/{name}.json"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"}
    movie_url = movie_search_url.format(initial=movie_name[0], name=movie_name)
    page = requests.get(movie_url, headers = headers)

    return page.json()


def parse_search_result(movie_we_are_looking_for, search_result):
    movie_and_id = []
    for single_result in search_result.get('d', []):
        movie_name = single_result['l']
        if movie_name.lower() == movie_we_are_looking_for.lower():
            row = movie_name, single_result['id']
            movie_and_id.append(row)
    return movie_and_id

def write_movie_hunt(movies, file_name='movie_hunt.csv'):
    with open(file_name, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(movies)


# Main proogram

movie_list = read_raw_txt_file()
found_items = []
not_found_movies = []
for movie_name in movie_list[:603]:
    print('Reading... ' + movie_name)
    search_result = get_movie_json_from_imdb(movie_name)
    data = parse_search_result(movie_name, search_result)
    if len(data) > 0:
        found_items.extend(data)
    else:
        not_found_movies.append((movie_name,))


write_movie_hunt(found_items, 'scraped_data/movie_ids/movie_hunt.csv')
write_movie_hunt(not_found_movies, 'scraped_data/movie_ids/hunt_not_found.csv')
