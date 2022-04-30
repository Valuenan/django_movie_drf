from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
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


class MovieListView(APIView):
    '''Вывод списка фильмов'''

    def get(self, requset):
        movies = Movie.objects.filter(draft=False).annotate(
            rating_user=models.Count('ratings', filter=models.Q(ratings__ip=get_client_ip(requset)))
        ).annotate(
            middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
        )
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)


class MovieDetailView(APIView):
    '''Вывод фильма'''

    def get(self, requset, pk):
        movie = Movie.objects.get(id=pk, draft=False)
        serializer = MovieDetailsSerializer(movie)
        return Response(serializer.data)


class ReviewCreateView(APIView):
    '''Добавление отзыва к фильму'''

    def post(self, request):
        review = ReviewCreateSerializer(data=request.data)
        if review.is_valid():
            review.save()
        return Response(status=201)


class AddStarRatingView(APIView):
    '''Добавление рейтинга фильму'''

    def post(self, request):
        serializer = CreateRatingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(ip=get_client_ip(request))
            return Response(status=200)
        else:
            return Response(status=400)


class ActorsListView(generics.ListAPIView):
    '''Вывод списка актеров'''
    queryset = Actor.objects.all()
    serializer_class = ActorsListSerializer


class ActorsDetailView(generics.RetrieveAPIView):
    '''Вывод списка актеров'''
    queryset = Actor.objects.all()
    serializer_class = ActorsDetailSerializer
