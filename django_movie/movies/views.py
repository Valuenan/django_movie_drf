from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Movie
from .serializers import MovieSerializer, MovieDetailsSerializer, ReviewCreateSerializer


class MovieListView(APIView):
    '''Вывод списка фильмов'''

    def get(self, requset):
        movies = Movie.objects.filter(draft=False)
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
