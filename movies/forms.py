from django import forms

class CreateNewMovie(forms.Form):
    movieId = forms.IntegerField()
    title = forms.CharField(max_length=60)
    genres = forms.CharField(max_length=200)
    date = forms.CharField()

class UpdateDb(forms.Form):
    source = forms.CharField(max_length=60)
