from django.contrib import admin
from django.utils.safestring import mark_safe
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget


from .models import Category, Genre, Movie, MovieShots, Actor, Rating, RatingStar, Review


class MovieAdminForm(forms.ModelForm):
    '''Форма с виджитом ckeditor'''

    description = forms.CharField(label='Описание', widget=CKEditorUploadingWidget())

    class Meta:
        model = Movie
        fields = '__all__'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "url")
    list_display_links = ("name",)


class ReviewInLine(admin.TabularInline):
    model = Review
    extra = 1
    readonly_fields = ("name", "email")


class MovieShotsInLine(admin.TabularInline):
    model = MovieShots
    extra = 1
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} with="70" height="80"')

    get_image.short_description = "Изображение"


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "url", "get_image", "draft")
    list_filter = ("category", "year")
    readonly_fields = ("get_image",)
    search_fields = ("title", "category__name")
    inlines = [MovieShotsInLine, ReviewInLine]
    save_on_top = True
    save_as = True
    list_editable = ("draft",)
    actions = ['publish', 'unpublish']
    form = MovieAdminForm
    fieldsets = (
        (None, {
            "fields": (("title", "tagline"),)
        }),
        (None, {
            "fields": (("description", "poster", "get_image"),)
        }),
        (None, {
            "fields": (("year", "world_premiere", "country"),)
        }),
        ("Actors", {
            "classes": ("collapse",),
            "fields": (("actors", "directors", "genres"),)
        }),
        (None, {
            "fields": (("budget", "fees_in_usa", "fees_in_world"),)
        }),
        (None, {
            "fields": (("category", "url", "draft"),)
        })
    )

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.poster.url} with="100" height="110"')

    def unpublish(self, request, queryset):
        '''Снять с публикации'''

        row_update = queryset.update(draft=True)
        if row_update == 1:
            message_bit = "1 запись была обнавлена"
        else:
            message_bit = f"{row_update} записи(ей) были обнавлены"
        self.message_user(request, f"{message_bit}")

    def publish(self, request, queryset):
        '''Опубликовать'''

        row_update = queryset.update(draft=False)
        if row_update == 1:
            message_bit = "1 запись была обнавлена"
        else:
            message_bit = f"{row_update} записи(ей) были обнавлены"
        self.message_user(request, f"{message_bit}")

    publish.short_description = "Опубликовать"
    publish.allowed_permissions = ('change',)

    unpublish.short_description = "Снять с публикации"
    unpublish.allowed_permissions = ('change',)

    get_image.short_description = "Постер"


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "parent", "movie", "id")
    readonly_fields = ("name", "email")


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name", "url")


@admin.register(MovieShots)
class MovieShotsAdmin(admin.ModelAdmin):
    list_display = ("title", "movie")


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ("name", "age", "get_image")
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} with="50" height="60"')

    get_image.short_description = "Изображение"


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("star", "movie", "ip")


admin.site.register(RatingStar)

admin.site.site_title = "Django Movies"
admin.site.site_header = "Django Movies"
