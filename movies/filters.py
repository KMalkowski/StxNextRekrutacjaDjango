import django_filters
from django_filters import CharFilter

from .models import *

class MovieFilter(django_filters.FilterSet):
    genres = CharFilter(field_name='genres', lookup_expr='icontains')
    tags = CharFilter(field_name='tags', lookup_expr='icontains')
    title = CharFilter(field_name='title', lookup_expr='icontains')
    class Meta:
        model = Movie
        fields = '__all__'
        exclude = ['ratings', 'movieId']
