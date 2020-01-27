from django.urls import path
from movies.views import home, movie_detail, create, update_movies_view

app_name = 'movies'

urlpatterns = [
    path('', home, name="movies-home"),
    path('create/', create, name="create"),
    path('update/', update_movies_view, name="update"),
    path('<movieId>/', movie_detail, name="movie-detail"),
]
