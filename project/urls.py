from django.urls import include, path
from movies.views import (
    ListMovie, ListPerson, movie_detail, review_movie,
    person_detail, movie_edit, person_delete, person_edit, home
)
from django.contrib import admin
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', home, name='home'),
    path('movies/', ListMovie.as_view(), name='list_movies'),
    path('movie/<str:id>/', movie_detail, name='movie_detail'),
    path('movie/<str:id>/review', review_movie, name='movie_review'),
    path('movie/<str:id>/edit', movie_edit, name='movie_edit'),
    path('person_delete/<str:mid>/<str:pid>', person_delete, name='person_delete'),

    path('persons/', ListPerson.as_view(), name='list_person'),
    path('person/<str:id>/', person_detail, name='person_detail'),
    path('person/<str:id>/edit', person_edit, name='person_edit'),

    path('admin/', admin.site.urls),
    path('auth/', include('authentication.urls', namespace='auth')),
    path('social-auth/', include('social_django.urls', namespace='social')),

    path('captcha/', include('captcha.urls')),
    path('reset_password', auth_views.PasswordResetView.as_view(), name="reset_password"),
    path('reset_password_sent', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('reset_password_complete', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
]
