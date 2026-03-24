from django.conf import settings

import requests


def get_movie_by_imdb_title_id(imdb_title_id: str):
    return requests.get(f"http://www.omdbapi.com/?apikey={settings.OMDB_API_KEY}&i={imdb_title_id}")
