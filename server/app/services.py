from django.conf import settings

import requests

from app import models


def log(message: str):
    if settings.DEBUG is False:
        with open("movie_dinghy.log", "a") as log_file:
            log_file.write(f"{message}\n")
    else:
        print("=========================")
        print("DEBUG MODE - Log message:")
        print(message)
        print("=========================")


def get_movie_by_imdb_title_id(imdb_title_id: str):
    try:
        movie = models.Movie.objects.get(imdb_title_id=imdb_title_id)

        create_movie_query_history(movie.id)

        return {
            "Title": movie.title,
            "Year": movie.year,
            "imdbID": movie.imdb_title_id,
        }

    except models.Movie.DoesNotExist:
        params = {"apikey": settings.OMDB_API_KEY, "i": imdb_title_id}
        movie_data = requests.get("http://www.omdbapi.com/", params=params).json()

        new_movie = models.Movie(
            title=movie_data.get("Title"),
            year=movie_data.get("Year"),
            imdb_title_id=imdb_title_id,
        )
        new_movie.save()

        create_movie_query_history(new_movie.id)

        return movie_data

    except Exception as error:
        log(f"Error fetching movie data for {imdb_title_id}: {error}")

        params = {"apikey": settings.OMDB_API_KEY, "i": imdb_title_id}
        return requests.get("http://www.omdbapi.com/", params=params).json()


def create_movie_query_history(movie_id: int):
    history_entry = models.MovieQueryHistory(movie_id=movie_id)
    history_entry.save()
