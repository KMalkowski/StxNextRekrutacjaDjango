from django.shortcuts import render, redirect
from movies.models import Movie
from movies.forms import CreateNewMovie, UpdateDb
from .filters import MovieFilter
import csv, io, requests, zipfile, shutil, os

import io, csv
from django.core.paginator import Paginator

def home(request):
     year = request.GET.get('year')
     if(year):
        movie_items = Movie.objects.filter(date=year)
     else:
        movie_items = Movie.objects.all()

     myFilter = MovieFilter(request.GET, queryset=movie_items)
     movie_items = myFilter.qs

     sort = 'id'
     sort = request.GET.get('sort')
     if sort != None:
         movie_items = Movie.objects.order_by(sort)

     paginator = Paginator(movie_items, 20)
     page = request.GET.get('page')
     movie_items = paginator.get_page(page)

     context = {
            'movie_items': movie_items,
            'myFilter': myFilter,
        }
     return render(request, 'movies/home.html', context)


#SHOW SPECIFIC OBJECT
def movie_detail(request, movieId):
    movie_items = Movie.objects.filter(movieId=movieId)
    for movie_item in movie_items:
        list = movie_item.ratings.split(',')
        list_length = len(list)
        sum = 0.0
        for item in list:
            if item != "":
                sum += float(item)
        rating = round(sum/list_length, 2)
    context = {
        'movie_items': movie_items,
        'rating': rating,
    }
    return render(request, 'movies/detail.html', context)

#USE FORM TO CREATE NEW MOVIE OBJECT
def create(request):
    if request.method == "POST":
        form = CreateNewMovie(request.POST)

        if form.is_valid():
            i = form.cleaned_data['movieId']
            t = form.cleaned_data['title']
            g = form.cleaned_data['genres']
            d = form.cleaned_data['date']

            m = Movie(movieId=i, title=t, genres=g, date=d)
            m.save()
        return redirect("/movies/" + str(m.movieId))
    else:
        form = CreateNewMovie()
    context = {
        'form': form
    }
    return render(request, 'movies/create.html', context)

def update_movies_view(request):
    if request.method == "POST":
        form = UpdateDb(request.POST)
        if form.is_valid():
            s = form.cleaned_data['source']
            #DELETES CSV FOLDER
            if(s == 'ml-latest-small' and os.path.isdir('ml-latest-small')):
                shutil.rmtree('ml-latest-small')
                #DELETE MOVIE OBJECTS FROM DB
                to_delete = Movie.objects.all()
                to_delete.delete()

            #OPEN & EXTRACT ZIP MOVIES
            r = requests.get('http://files.grouplens.org/datasets/movielens/ml-latest-small.zip')
            z = zipfile.ZipFile(io.BytesIO(r.content))
            z.extractall()

            #OPEN CSV MOVIES AND WRITE IT DO DB
            csv_name = open('ml-latest-small/movies.csv', "r")
            with open('ml-latest-small/movies.csv', 'r', encoding="utf8") as csv_file:
                csv_reader = csv.reader(csv_file)
                header = next(csv_reader)
                for line in csv_reader:
                    year = line[1]
                    year = year[-5:-1]
                    if year.isdigit():
                        year = int(year)
                    instance = Movie(movieId=line[0], title =line[1], genres=line[2], date=year)
                    instance.save()

            with open('ml-latest-small/tags.csv', 'r', encoding="utf8") as csv_file:
                csv_reader = csv.reader(csv_file)
                header = next(csv_reader)
                for line in csv_reader:
                    movieId = line[1]
                    tag = line[2]
                    item = Movie.objects.get(movieId=movieId)
                    item.tags += (tag + '|')
                    item.save()

            with open('ml-latest-small/ratings.csv', 'r', encoding="utf8") as csv_file:
                csv_reader = csv.reader(csv_file)
                header = next(csv_reader)
                for line in csv_reader:
                    movieId = line[1]
                    rating = line[2]
                    item = Movie.objects.get(movieId=movieId)
                    item.ratings += (rating + ',')
                    item.save()


    else:
        form = UpdateDb()

    context = {
        'form': form
        }
    return render(request, 'movies/update.html', context)
