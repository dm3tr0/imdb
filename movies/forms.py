from django import forms
from captcha.fields import CaptchaField
from movies.models import Comment, Movie, Person, PersonMovie

class CommentForm(forms.Form):
    author = forms.CharField(label='Name', max_length=256)
    email = forms.CharField(label='Email adress', max_length=256)
    text = forms.CharField(label='Text', max_length=512)
    
    def clean_text(self):
        cleaned_data = self.cleaned_data
        return cleaned_data.get('title')

class CommentModelForm(forms.ModelForm):
    captcha = CaptchaField()
    class Meta:
        model = Comment
        fields = ['author', 'email', 'text']

        
class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['name', 'year', 'genre']

class PersonMovieForm(forms.ModelForm):
    class Meta:
        model = PersonMovie
        fields = ['category', 'job', 'chars']

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['name', 'birthday', 'deathday']

class PersonEditForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['birthday', 'deathday']

class StarRatingForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['rating']
        
    