from django.shortcuts import redirect

from ninja import NinjaAPI
from ninja.responses import Response

from app import services

api = NinjaAPI()


@api.get("title/{title_id}")
def imdb_title(request, title_id: str):
    if not title_id.startswith("tt"):
        return Response(
            status_code=400,
            content={"error": "Invalid title_id format. It should start with 'tt'."},
        )

    movie_data = services.get_movie_by_imdb_title_id(title_id)

    if movie_data["title"]:
        movie_title = movie_data["title"].replace(" ", "+")
        search_query = movie_title
    else:
        return Response(
            status_code=404,
            content={"error": "Movie not found for the given title_id."},
        )
    if movie_data["year"]:
        search_query += f"+{movie_data['year']}"

    return redirect(f"ext.to/browse/?q={search_query}")
