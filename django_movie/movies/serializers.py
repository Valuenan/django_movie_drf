from rest_framework import serializers

from .models import Movie, Review, Rating, Actor


class MovieSerializer(serializers.ModelSerializer):
    '''Список фильмов'''
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    rating_user = serializers.BooleanField()
    middle_star = serializers.FloatField()

    class Meta:
        model = Movie
        fields = ('id', 'title', 'tagline', 'category', 'rating_user', 'middle_star')


class RecursiveSerializer(serializers.Serializer):
    '''Вывод рекурсивно children'''

    def to_representation(self, instance):
        serializer = ReviewSerializer(instance, context=self.context)
        return serializer.data


class ActorsListSerializer(serializers.ModelSerializer):
    '''Вывод актеров и режисеров'''

    class Meta:
        model = Actor
        fields = ('id', 'name', 'image')


class ActorsDetailSerializer(serializers.ModelSerializer):
    '''Вывод информации об актере или режисере'''

    class Meta:
        model = Actor
        fields = '__all__'


class ReviewCreateSerializer(serializers.ModelSerializer):
    '''Добавление отзыва'''

    class Meta:
        model = Review
        fields = '__all__'


class FilterReviewSerializer(serializers.ListSerializer):
    '''Фильтр комментраиев, только parents'''

    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class ReviewSerializer(serializers.ModelSerializer):
    '''Вывод отзыва'''
    children = RecursiveSerializer(many=True)

    class Meta:
        list_serializer_class = FilterReviewSerializer
        model = Review
        fields = ('name', 'text', 'children')


class MovieDetailsSerializer(serializers.ModelSerializer):
    '''Список фильмов'''
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    directors = ActorsListSerializer(read_only=True, many=True)
    actors = ActorsListSerializer(read_only=True, many=True)
    genres = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    reviews = ReviewSerializer(many=True)

    class Meta:
        model = Movie
        exclude = ('draft',)


class CreateRatingSerializer(serializers.ModelSerializer):
    '''Добавление рейтинга пользователем'''

    class Meta:
        model = Rating
        fields = ('star', 'movie')

    def create(self, validated_data):
        reating, _ = Rating.objects.update_or_create(
            ip=validated_data.get('ip', None),
            movie=validated_data.get('movie', None),
            defaults={'star': validated_data.get('star')}
        )
        return reating
