from django.utils import timezone 
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.conf import settings

class CommentManager(models.Manager):
    def all(self):
        qs = super(CommentManager, self).filter(parent=None)
        return qs

    def filter_by_instance(self, instance):
        content_type = ContentType.objects.get_for_model(instance.__class__)
        obj_id = instance.id
        sq = super(CommentManager, self).filter(content_type=content_type, object_id=obj_id).filter(parent=None)

class Movie(models.Model):
    imdb_id = models.CharField(max_length=256)
    title_type = models.CharField(max_length=256)
    name = models.CharField(max_length=256, blank=True)
    adult = models.BooleanField()
    year = models.CharField(max_length=10, blank=True)
    genre = models.CharField(max_length=256, blank=True)
    literal_rating = models.FloatField(default=0)
    rating = models.IntegerField(default=0)
    rates = models.IntegerField(default=0)
    pic = models.CharField(max_length=512)

    def __str__(self):
        return self.name

class Person(models.Model):
    imdb_id = models.CharField(max_length=256, primary_key=True)
    name = models.CharField(max_length=256, blank=True)
    birthday = models.CharField(max_length=10, blank=True)
    deathday = models.CharField(max_length=10, blank=True)

    literal_rating = models.FloatField(default=0)
    rating = models.IntegerField(default=0)
    rates = models.IntegerField(default=0)
    rating = models.FloatField(default=0)

class PersonMovie(models.Model):
    mid = models.CharField(max_length=256)
    pid = models.CharField(max_length=256)
    order = models.IntegerField()
    category = models.CharField(max_length=256, blank=True)
    job = models.CharField(max_length=256, blank=True)
    chars = models.CharField(max_length=256, blank=True)


class PersonPerson(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, db_constraint=False)
    movie = models.CharField(max_length=256)
    personmovie = models.ForeignKey(PersonMovie, on_delete=models.CASCADE, db_constraint=False)


class Comment(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, null=True)
    person = models.ForeignKey(Person, on_delete=models.CASCADE, null=True)
    author = models.CharField(max_length=256, blank=True)
    text = models.CharField(max_length=512, blank=True)
    email = models.EmailField(max_length=256, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

    def children(self):
        return Comment.objects.filter(parent=self)

    @property
    def is_parent(self):
        return not self.parent

    def __str__(self):
        return self.text
    
    class Meta:
        db_table = 'movies_comment'
        ordering = ['-timestamp']

class RateMovie(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.IntegerField()