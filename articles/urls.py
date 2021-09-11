from django.urls import path, re_path

from .views import ArticlesList, ArticleDetail, ArticleCreate, ArticleUpdate, ArticleDelete, ArticlesByTagsList, SearchView
from .views import TagAutocomplete, SecurityAutocomplete, BookmarkArticleView, bookmarked_articles
from stocksetfsbonds.models import StockETFBond

app_name = 'articles'

urlpatterns = [
    path('tag-autocomplete/', TagAutocomplete.as_view(), name='tag-autocomplete'),
    path('security-autocomplete/', SecurityAutocomplete.as_view(), name='security-autocomplete'),
    path('', ArticlesList.as_view(), name='list_view'),
    path('search/', SearchView.as_view(), name='search_view'),
    path('<tag>/', ArticlesByTagsList.as_view(), name='articles_by_tags'),
    path('articles/create/', ArticleCreate.as_view(), name='create_view'),
    re_path(r'^articles/(?P<slug>[\w-]+)/$', ArticleDetail.as_view(), name='detail_view'),
    # path('articles/<slug:slug>', ArticleDetail.as_view(), name='detail_view'),

    # path('articles/<slug:slug>/', ArticleUpdate.as_view(), name='update_view'),
    re_path(r'^articles/(?P<slug>[\w-]+)/update/$', ArticleUpdate.as_view(), name='update_view'),
    # path('articles/<slug:slug>/delete/', ArticleDelete.as_view(), name='delete_view'),
    re_path(r'^articles/(?P<slug>[\w-]+)/delete/$', ArticleDelete.as_view(), name='delete_view'),
    re_path(r'^bookmark/(?P<slug>[\w-]+)/$', BookmarkArticleView, name='bookmark_article'),
    # path('bookmark/<slug:slug>', BookmarkArticleView, name='bookmark_article'),
    path('bookmarked/articles/', bookmarked_articles, name='bookmarked_articles'),
]
