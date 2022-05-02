# convert json file to csv

import csv
import json

with open('scraped_data/patrick_second_movie_project.json', 'r') as file:
    movie_data = json.load(file)

header =['Title', 'Release Year', 'Parent Rating', 'genre', 'Summary', 'Writers', 'Stars', 'Direcctor']

csv_rows = []
for movie in movie_data:
    movie_row = [
        movie['title'],
        movie['release_year'],
        movie['parent_rating'],
        movie['genres'],
        movie['summary'],
        movie['writers'],
        movie['stars'],
        movie['director'],
    ]
    
    csv_rows.append(movie_row)

print('reading file..')    

with open('scraped_data/patrick_second_movie_project.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(csv_rows)

    