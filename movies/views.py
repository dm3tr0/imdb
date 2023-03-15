import random

from django.http import HttpResponse

from movies.forms import PersonEditForm
from movies.forms import PersonForm
from movies.forms import PersonMovieForm
from movies.forms import MovieForm
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from movies.models import Movie, Comment, PersonMovie, Person, RateMovie, PersonPerson
from movies.forms import CommentModelForm, StarRatingForm
from django.utils import timezone
from authentication.models import User


def index(request):
    return render(request, 'movies/home.html')


class ListMovie(ListView):
    model = Movie
    paginate_by = 4
    template_name = 'movie_list.html'
    context_object_name = 'movie'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            object_list = self.model.objects.filter(name__icontains=query) #type: ignore
        else:
            object_list = self.model.objects.all() #type: ignore
        return object_list

class ListPerson(ListView):
    model = Person
    paginate_by = 4
    template_name = 'person_list.html'
    context_object_name = 'person'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            object_list = self.model.objects.filter(name__icontains=query) #type: ignore
        else:
            object_list = self.model.objects.all() #type: ignore
        return object_list
    

def movie_detail(request, id):
    movie = get_object_or_404(Movie, imdb_id=id)
    form = CommentModelForm(request.POST)
    comments = Comment.objects.filter(movie=movie, parent=None)
    actors = PersonMovie.objects.filter(mid=movie.imdb_id)
    for actor in actors:
        try:
            if not PersonPerson.objects.filter(person=Person.objects.get(imdb_id=actor.pid), personmovie=actor).exists():
                personperson = PersonPerson(person=Person.objects.get(imdb_id=actor.pid), personmovie=actor, movie=id)
                personperson.save()
        except:
            pass
        
    
    persons = PersonPerson.objects.filter(movie=id)
    

    try:
        user_rate = RateMovie.objects.get(user_id=request.user.id, movie=movie.pk)
    except:
        user_rate = None


    context = {
        'movie': movie,
        'form': form,
        'comments': comments,
        'actors': actors,
        'persons': persons,
        'user_rate': user_rate,
    }

    if request.method == "POST":
        form = CommentModelForm(request.POST)
        if form.is_valid():
            parent_obj = None
            try:
                parent_id = request.POST.get('parent_id')
            except:
                parent_id = None
            if parent_id:
                parent_qs = Comment.objects.filter(id=parent_id)
                if parent_qs.exists() and parent_qs.count() == 1:
                    parent_obj = parent_qs.first()

            comment = Comment(
                author=form.cleaned_data.get('author'),
                timestamp=timezone.now(), 
                email=form.cleaned_data.get('email'), 
                text=form.cleaned_data.get('text'), 
                movie_id=movie.pk,
                parent=parent_obj
                )

            comment.save()
            return redirect('/movie/'+movie.imdb_id)
    else:   
        form = CommentModelForm()
    return render(request, 'movies/movie_detail.html', context)


def person_detail(request, id):
    person = get_object_or_404(Person, imdb_id=id)
    movies = PersonMovie.objects.filter(pid=id)
    
    if person.rates == 0:

        for pm in movies:
            movie = get_object_or_404(Movie, imdb_id=pm.mid)
            person.rating += movie.literal_rating #type: ignore
            person.rates += 1
            person.literal_rating = round(person.rating / person.rates, 2)
            person.save()

    form = CommentModelForm(request.POST)
    comments = Comment.objects.filter(person=person, parent=None)
    actors = PersonMovie.objects.filter(mid=person.imdb_id)
    persons = Person.objects.all()
    context = {
        'person': person,
        'form': form,
        'comments': comments,
        'actors': actors,
        'persons': persons,
    }

    if request.method == "POST":
        form = CommentModelForm(request.POST)
        if form.is_valid():
            parent_obj = None
            try:
                parent_id = request.POST.get('parent_id')
            except:
                parent_id = None
            if parent_id:
                parent_qs = Comment.objects.filter(id=parent_id)
                if parent_qs.exists() and parent_qs.count() == 1:
                    parent_obj = parent_qs.first()

            comment = Comment(
                author=form.cleaned_data.get('author'),
                timestamp=timezone.now(), 
                email=form.cleaned_data.get('email'), 
                text=form.cleaned_data.get('text'), 
                person_id=person.pk,
                parent=parent_obj
                )

            comment.save()
            return redirect('/person/'+person.imdb_id)
    else:   
        form = CommentModelForm()
    return render(request, 'movies/person_detail.html', context)

def person_edit(request, id):
    person = get_object_or_404(Person, imdb_id=id)
    person_form = PersonEditForm(request.POST)
    context = {
        'form': person_form,
        'person': person
    }

    if request.method == "POST":
        form = PersonEditForm(request.POST)
        if form.is_valid() and int(form.cleaned_data.get('birthday')) < int(form.cleaned_data.get('deathday')):
            person.birthday = form.cleaned_data.get('birthday')
            person.deathday = form.cleaned_data.get('deathday')
            person.save()
            return redirect('/person/'+person.imdb_id)
        elif form.is_valid and not int(form.cleaned_data.get('birthday')) < int(form.cleaned_data.get('deathday')):
            print('nope')
    else:   
        form = PersonEditForm(request.POST)

    return render(request, 'movies/person_edit.html', context)

def movie_edit(request, id):
    movie = get_object_or_404(Movie, imdb_id=id)
    movie_form = MovieForm(request.POST)
    person_form = PersonForm(request.POST)
    personmovie_form = PersonMovieForm(request.POST)
    comments = Comment.objects.filter(movie=movie, parent=None)
    actors = PersonMovie.objects.filter(mid=movie.imdb_id)
    for actor in actors:
        try:
            if not PersonPerson.objects.filter(person=Person.objects.get(imdb_id=actor.pid), personmovie=actor).exists():
                personperson = PersonPerson(person=Person.objects.get(imdb_id=actor.pid), personmovie=actor, movie=id)
                personperson.save()
        except:
            pass
        
    
    persons = PersonPerson.objects.filter(movie=id)
    

    try:
        user_rate = RateMovie.objects.get(user_id=request.user.id, movie=movie.pk)
    except:
        user_rate = None


    context = {
        'movie': movie,
        'comments': comments,
        'actors': actors,
        'persons': persons,
        'user_rate': user_rate,
        'movie_form': movie_form,
        'person_form': person_form,
        'personmovie_form': personmovie_form
    }

    if request.method == "POST":
        movie_form = MovieForm(request.POST)
        person_form = PersonForm(request.POST)
        personmovie_form = PersonMovieForm(request.POST)

        if movie_form.is_valid():
            movie.name = movie_form.cleaned_data.get('name')
            movie.year = movie_form.cleaned_data.get('year')
            movie.genre = movie_form.cleaned_data.get('genre')
            movie.save()

            return redirect('/movie/'+movie.imdb_id)

        if person_form.is_valid() and personmovie_form.is_valid():

            person = Person()
            person.name = person_form.cleaned_data.get('name')
            person.birthday = person_form.cleaned_data.get('birthday')
            person.deathday = person_form.cleaned_data.get('deathday')
            person.imdb_id = 'nn'+str(random.randint(1, 9999999))
            person.save()


            person_movie = PersonMovie()
            person_movie.category = personmovie_form.cleaned_data.get('category')
            person_movie.job = personmovie_form.cleaned_data.get('job')
            person_movie.chars = personmovie_form.cleaned_data.get('chars')
            person_movie.order = random.randint(1, 10)
            person_movie.pid = person.pk
            person_movie.mid = movie.imdb_id
            person_movie.save()


            person_person = PersonPerson()
            person_person.person = get_object_or_404(Person, imdb_id=person.pk)
            person_person.movie = movie.imdb_id
            person_person.personmovie = get_object_or_404(PersonMovie, pk=person_movie.pk) 
            print(person_person.personmovie)
            person_person.save()

            return redirect('/movie/'+movie.imdb_id)
    else:   
        movie_form = MovieForm(request.POST)
        person_form = PersonForm(request.POST)
        personmovie_form = PersonMovieForm(request.POST)
            
    return render(request, 'movies/movie_edit.html', context)


def review_movie(request, id):
    movie = get_object_or_404(Movie, imdb_id=id)
    form = CommentModelForm(request.POST)
    comments = Comment.objects.filter(movie=movie)

    try:
        user_rate = RateMovie.objects.get(user_id=request.user.id, movie=movie.pk)
    except:
        user_rate = None

    context = {
        'movie': movie,
        'form': form,
        'comments': comments
    }
    if request.method == "POST":
        stars = StarRatingForm(request.POST)

        if stars.is_valid() and user_rate is None:
            user_rate = RateMovie()
            user_rate.movie = Movie(id=movie.pk)
            user = User.objects.get(id=request.user.id)
            user_rate.user = user
            user_rate.rating = stars.cleaned_data.get('rating')
            movie.rates += 1
            movie.rating += stars.cleaned_data.get('rating')
            movie.literal_rating = round(movie.rating / movie.rates, 2)
            movie.save()
            user_rate.save()

        elif stars.is_valid() and user_rate is not None:
            movie.rating -= user_rate.rating
            movie.rating += stars.cleaned_data.get('rating')
            movie.literal_rating = round(movie.rating / movie.rates, 2)
            movie.save()
            user_rate.rating = stars.cleaned_data.get('rating')
            user_rate.save()

        return redirect('/movie/'+movie.imdb_id)
    return render(request, 'movies/movie_detail.html', context)


def person_delete(request, mid, pid):
    person = get_object_or_404(PersonMovie, pid=pid, mid=mid)
    person.delete()
    return redirect(f'/movie/{mid}')

def home(request):
    return render(request, 'movies/home.html', {})