from rest_framework import generics
from django.db import models

from .models import Movie, Actor
from .serializers import (
    MovieSerializer,
    MovieDetailsSerializer,
    ReviewCreateSerializer,
    CreateRatingSerializer,
    ActorsListSerializer,
    ActorsDetailSerializer,
)
from .service import get_client_ip


class MovieListView(generics.ListAPIView):
    '''Вывод списка фильмов'''
    serializer_class = MovieSerializer

    def get_queryset(self):
        movies = Movie.objects.filter(draft=False).annotate(
            rating_user=models.Count('ratings', filter=models.Q(ratings__ip=get_client_ip(self.request)))
        ).annotate(
            middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
        )
        return movies


class MovieDetailView(generics.RetrieveAPIView):
    '''Вывод фильма'''
    queryset = Movie.objects.filter(draft=False)
    serializer_class = MovieDetailsSerializer


class ReviewCreateView(generics.CreateAPIView):
    '''Добавление отзыва к фильму'''
    serializer_class = ReviewCreateSerializer


class AddStarRatingView(generics.CreateAPIView):
    '''Добавление рейтинга фильму'''
    serializer_class = CreateRatingSerializer

    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))


class ActorsListView(generics.ListAPIView):
    '''Вывод списка актеров'''
    queryset = Actor.objects.all()
    serializer_class = ActorsListSerializer


class ActorsDetailView(generics.RetrieveAPIView):
    '''Вывод списка актеров'''
    queryset = Actor.objects.all()
    serializer_class = ActorsDetailSerializer
