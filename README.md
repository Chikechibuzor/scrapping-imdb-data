# Scrapping IMDB movie information

- This project extracts Movie and TV Series information from IMDB site.
- It starts with extraction of movie id when Movie Title is passed It then goes for specific information(Movie title, Release Year, Parental Rating, Genre, Summary, Director and Stars) of the movie.
-  It then saves this information as a JSON file

## What does this project achieve
### Setup 
In other to run this application we need to install [Python 3](https://www.python.org/downloads/)


After installing Python we need to install [Pipenv](https://pypi.org/project/pipenv/) using:

```
 pip install pipenv
 ```

After installing pipenv we need to install all the packages required for the project using:

```
pipenv install
```


### Steps to scraping Movies
-	Get movie ids of movies in text file “scrape_movie_ids_from_txt.py”:

```
pipenv run python  scrape_movie_ids_from_txt.py
```
	
-	Get movie information (Movie title, Release Year, Parental Rating, Genre, Summary, Director and Stars) “fetch_movie_info_frm_movie_id.py”

```
pipenv run python  fetch_movie_info_frm_movie_id.py
```
	
-	Convert Json file of “fetch_movie info_frm_movie_id.py”  to csv file “convert _imdbjson_to_csv.py”

```
pipenv run python  convert _imdbjson_to_csv.py
```



