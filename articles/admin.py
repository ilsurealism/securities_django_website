from django.contrib import admin

from .models import Article


class ArticlesAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'post_date', 'update_date', 'published', 'views')
    list_filter = ('post_date', 'update_date', 'published')
    fields = ('title', 'slug', 'author', 'post_date', 'update_date',  'title_image', 'description', 'body', 'tags', 'stocks_etfs_or_bonds', 'published', 'bookmark', 'views')
    readonly_fields = ('author', 'post_date', 'update_date', 'views', 'bookmark')
    search_fields = ('title', 'author', 'description', 'body', 'tags', 'stocks_etfs_or_bonds')


admin.site.register(Article, ArticlesAdmin)
