from django.db import models
from datetime import date
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    '''Категории'''
    name = models.CharField("Категория", max_length=150)
    description = models.TextField("Описание")
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "categories"
        verbose_name = _("Категория")
        verbose_name_plural = _("Категории")


class Actor(models.Model):
    '''Актеры и режисеры'''
    name = models.CharField("Имя", max_length=100)
    age = models.PositiveIntegerField("Возраст", default=0)
    description = models.TextField("Описание")
    image = models.ImageField("Изображение", upload_to="actors/")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('actor_detail', kwargs={'slug': self.name})

    class Meta:
        db_table = "actors"
        verbose_name = _("Актеры и режисеры")
        verbose_name_plural = _("Актеры и режисеры")


class Genre(models.Model):
    '''Жанры'''
    name = models.CharField("Название", max_length=150)
    description = models.TextField("Описание")
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "genres"
        verbose_name = _("Жанр")
        verbose_name_plural = _("Жанры")


class Movie(models.Model):
    '''Фильм'''
    title = models.CharField("Название", max_length=100)
    tagline = models.CharField("Слоган", max_length=100, default='')
    description = models.TextField("Описание")
    poster = models.ImageField("Постер", upload_to="movies/")
    year = models.PositiveIntegerField("Дата выхода", default=2019)
    country = models.CharField("Старана", max_length=30)
    directors = models.ManyToManyField(Actor, verbose_name="Режисер", related_name="film_director")
    actors = models.ManyToManyField(Actor, verbose_name="Актер", related_name="film_actor")
    genres = models.ManyToManyField(Genre, verbose_name="Жанры")
    world_premiere = models.DateField("Премера в мире", default=date.today)
    budget = models.PositiveIntegerField("Бюджет", default=0, help_text="указывать сумму в долларах")
    fees_in_usa = models.PositiveIntegerField("Собры в США", default=0, help_text="указывать сумму в долларах")
    fees_in_world = models.PositiveIntegerField("Собры в мире", default=0, help_text="указывать сумму в долларах")
    category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.SET_NULL, null=True)
    url = models.SlugField(max_length=160, unique=True)
    draft = models.BooleanField("Черновик", default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("movie_detail", kwargs={"slug": self.url})

    def get_review(self):
        return self.reviews_set.filter(parent__isnull=True)

    class Meta:
        db_table = "movies"
        verbose_name = _("Фильм")
        verbose_name_plural = _("Фильмы")


class MovieShots(models.Model):
    '''Кадры из фильма'''
    title = models.CharField("Заголовок", max_length=100)
    description = models.TextField("Описание")
    image = models.ImageField("Изображение", upload_to="movie_shots/")
    movie = models.ForeignKey(Movie, verbose_name="Фильм", on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "movie_shots"
        verbose_name = _("Кадр из фильма")
        verbose_name_plural = _("Кадры из фильма")


class RatingStar(models.Model):
    '''Звезды рейтинга'''
    value = models.SmallIntegerField("Значение", default=0)

    def __str__(self):
        return str(self.value)

    class Meta:
        db_table = "rating_stars"
        verbose_name = _("Звезда рейтинга")
        verbose_name_plural = _("Звезды рейтинга")
        ordering = ['-value']


class Rating(models.Model):
    '''Рейтинг'''
    ip = models.CharField("IP адрес", max_length=15)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name="Звезда")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name="Фильм", related_name="ratings")

    def __str__(self):
        return f"{self.star} - {self.movie}"

    class Meta:
        db_table = "ratings"
        verbose_name = _("Рейтинг")
        verbose_name_plural = _("Рейтинги")


class Review(models.Model):
    '''Отзывы'''
    email = models.EmailField()
    name = models.CharField("Имя", max_length=100)
    text = models.TextField("Сообщение", max_length=5000)
    parent = models.ForeignKey('self', verbose_name="Родитель", on_delete=models.SET_NULL, blank=True, null=True,
                               related_name='children')
    movie = models.ForeignKey(Movie, verbose_name="Фильм", on_delete=models.CASCADE, related_name='reviews')

    def __str__(self):
        return f"{self.name} - {self.movie}"

    class Meta:
        db_table = "reviews"
        verbose_name = _("Отзыв")
        verbose_name_plural = _("Отзывы")
