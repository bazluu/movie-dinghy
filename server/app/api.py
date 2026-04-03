from django.http import JsonResponse
from django.shortcuts import redirect

from ninja import NinjaAPI

from app import services

api = NinjaAPI()


@api.get("title/{title_id}/")
def imdb_title(request, title_id: str):
    if not title_id.startswith("tt"):
        return JsonResponse(
            status=400,
            data={"error": "Invalid title_id format. It should start with 'tt'."},
        )

    movie_data = services.get_movie_by_imdb_title_id(title_id)

    if movie_data.get("Title"):
        movie_title = movie_data["Title"].replace(" ", "+")
        search_query = movie_title
    else:
        return JsonResponse(
            status=404,
            data={"error": "Movie not found for the given title_id."},
        )
    if movie_data.get("Year"):
        search_query += f"+{movie_data['Year']}"

    return redirect(f"https://ext.to/browse/?q={search_query}")
