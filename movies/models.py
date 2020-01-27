from django.db import models
import datetime


class Movie(models.Model):
    title                   = models.CharField(max_length=60, null=False, blank=False)
    movieId                 = models.IntegerField(unique=True)
    genres                  = models.TextField(max_length=200, null=False, blank=False)
    date                    = models.CharField(max_length=10, null=False, blank=False)
    tags                    = models.TextField(max_length=200, null=False, blank=False, default="")
    ratings                 = models.TextField(max_length=200, null=False, blank=False, default="")

    def __str__(self):
        return self.title
