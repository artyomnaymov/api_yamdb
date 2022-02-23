from django.contrib import admin

from reviews.models import Category, Comment, Genre, Review, Title, User


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'pub_date', 'get_author', 'get_title',
                    'score')
    search_fields = ('title',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'

    def get_author(self, obj):
        return obj.author
    get_author.short_description = 'Автор'

    def get_title(self, obj):
        return obj.title
    get_title.short_description = 'Произведение'


class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'pub_date', 'get_author', 'get_review')
    search_fields = ('review',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'

    def get_author(self, obj):
        return obj.author
    get_author.short_description = 'Автор'

    def get_review(self, obj):
        return obj.review
    get_review.short_description = 'Отзыв'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    search_fields = ('name', )
    empty_value_display = '-пусто-'


class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    search_fields = ('name', )
    empty_value_display = '-пусто-'


class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'year', 'description', 'category')
    search_fields = ('name',)
    list_filter = ('year', 'genre', 'category')
    empty_value_display = '-пусто-'


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', "role", 'bio')


admin.site.register(Comment, CommentAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(User, UserAdmin)
