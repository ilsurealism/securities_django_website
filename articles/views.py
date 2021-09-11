from django.core.exceptions import PermissionDenied
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Count, Q, F
from itertools import chain
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

from taggit.models import Tag
from dal import autocomplete

from .models import Article
from .forms import ArticleForm
from stocksetfsbonds.models import StocksETFsBonds
from stocksetfsbonds.models import StockETFBond
from users.models import AdvUser


def BookmarkArticleView(request, slug):
    article = get_object_or_404(Article, id=request.POST.get('article_id'))
    bookmarked = False
    if article.bookmark.filter(id=request.user.id).exists():
        article.bookmark.remove(request.user)
        bookmarked = False
    else:
        article.bookmark.add(request.user)
        bookmarked = True
    # return HttpResponseRedirect(reverse('articles:detail_view', args=[str(slug)]))
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


class TagAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        qs = Tag.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


class SecurityAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        qs = StockETFBond.objects.all()

        if self.q:
            qs = qs.filter(ticker__istartswith=self.q) | qs.filter(name__istartswith=self.q)

        return qs



class ArticlesList(ListView):
    model = Article
    template_name = 'articles/list_view.html'
    context_object_name = 'articles_list'
    articles_quantiy = Tag.objects.annotate(Count('taggit_taggeditem_items'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 5 тегов с наиболшим количством публикаций
        context['tags_list'] = Tag.objects.annotate(articles_quantiy=Count('taggit_taggeditem_items')).order_by(
            '-articles_quantiy')[:10]
        context['securities_types_list'] = StocksETFsBonds.objects.all()
        context['articles_list'] = Article.objects.filter(published=True)[:20]
        return context


class ArticleDetail(DetailView):
    model = Article
    template_name = 'articles/detail_view.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super(ArticleDetail, self).get_context_data(**kwargs)

        stuff = get_object_or_404(Article, slug=self.kwargs['slug'])
        bookmarked = False
        if stuff.bookmark.filter(id=self.request.user.id).exists():
            bookmarked = True
        context["bookmarked"] = bookmarked

        self.object.views = F('views') + 1
        self.object.save()
        self.object.refresh_from_db()

        # необходимы для показа списка тэгов и типов бумаг в хедере
        # context['tags_list'] = Tag.objects.all()
        context['securities_types_list'] = StocksETFsBonds.objects.all()
        # 5 тегов с наиболшим количством публикаций
        context['tags_list'] = Tag.objects.annotate(articles_quantiy=Count('taggit_taggeditem_items')).order_by(
            '-articles_quantiy')[:10]
        return context


class ArticleCreate(LoginRequiredMixin, CreateView):
    model = Article
    template_name = 'articles/create_view.html'
    # fields = ['title', 'description', 'body', 'tags', 'stocks_etfs_or_bonds']
    form_class = ArticleForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # необходимы для показа списка тэгов и типов бумаг в хедере
        # context['tags_list'] = Tag.objects.all()
        context['securities_types_list'] = StocksETFsBonds.objects.all()
        # 5 тегов с наиболшим количством публикаций
        context['tags_list'] = Tag.objects.annotate(articles_quantiy=Count('taggit_taggeditem_items')).order_by(
            '-articles_quantiy')[:10]
        return context

    def get_initial(self):
        initial = super(ArticleCreate, self).get_initial()
        initial = initial.copy()
        initial['author'] = self.request.user.pk
        return initial


class ArticleUpdate(LoginRequiredMixin, UpdateView):
    model = Article
    template_name = 'articles/update_view.html'
    # fields = ['title', 'description', 'body', 'tags']
    context_object_name = 'article_update'
    form_class = ArticleForm

    def setup(self, request, *args, **kwargs):
        self.author = request.user.pk
        return super().setup(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # необходимы для показа списка тэгов и типов бумаг в хедере
        # context['tags_list'] = Tag.objects.all()
        context['securities_types_list'] = StocksETFsBonds.objects.all()
        # 5 тегов с наиболшим количством публикаций
        context['tags_list'] = Tag.objects.annotate(articles_quantiy=Count('taggit_taggeditem_items')).order_by(
            '-articles_quantiy')[:10]
        return context

    def get_queryset(self):
        author = super(ArticleUpdate, self).get_queryset()
        return author.filter(author=self.request.user)


class ArticleDelete(LoginRequiredMixin, DeleteView):
    model = Article
    template_name = 'articles/delete_view.html'
    success_url = reverse_lazy('articles:list_view')
    context_object_name = 'article_delete'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # необходимы для показа списка тэгов и типов бумаг в хедере
        # context['tags_list'] = Tag.objects.all()
        # 5 тегов с наиболшим количством публикаций
        context['tags_list'] = Tag.objects.annotate(articles_quantiy=Count('taggit_taggeditem_items')).order_by(
            '-articles_quantiy')[:10]
        context['securities_types_list'] = StocksETFsBonds.objects.all()
        return context

    def get_queryset(self):
        author = super(ArticleDelete, self).get_queryset()
        return author.filter(author=self.request.user)


class ArticlesByTagsList(ListView):

    template_name = 'articles/articles_by_tags.html'
    context_object_name = 'articles_list'


    # работает
    # def get_queryset(self):
    #     return TaggedItem.objects.filter(tag_id=self.kwargs['tag_id'])


    # def get_queryset(self):
    #     return TaggedItem.objects.filter(tag=self.kwargs['tag'])

    def get_queryset(self):
        return Article.objects.filter(published=True, tags__name=self.kwargs['tag'])

    # def get_queryset(self):
    #     self.slug = get_object_or_404(Tag, name=self.kwargs['slug'])
    #     return Article.objects.filter(slug=self.slug)
    #
    # рабочий вариант (почти)
    # def get_queryset(self):
    #     self.tag = get_object_or_404(Tag, name=self.kwargs['tag'])
    #     return Article.objects.filter(slug=self.tag)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # необходимы для показа списка тэгов и типов бумаг в хедере
        # context['tags_list'] = Tag.objects.all()
        context['securities_types_list'] = StocksETFsBonds.objects.all()
        # 5 тегов с наиболшим количством публикаций
        context['tags_list'] = Tag.objects.annotate(articles_quantiy=Count('taggit_taggeditem_items')).order_by(
            '-articles_quantiy')[:10]

        # заголовок списка по тегу
        context['current_tag'] = Tag.objects.get(name=self.kwargs['tag'])
        return context

class SearchView(ListView):
    template_name = 'articles/search_view.html'

    def get_queryset(self):
        query = self.request.GET.get('q')

        object_list = Article.objects.filter(Q(title__icontains=query) | Q(description__icontains=query)|
                                             Q(body__icontains=query) |
                                             Q(stocks_etfs_or_bonds__ticker__icontains=query) |
                                             Q(stocks_etfs_or_bonds__description__icontains=query) |
                                             Q(stocks_etfs_or_bonds__name__icontains=query) |
                                             Q(tags__name__icontains=query), published=True)
        # securities_list = StockETFBond.objects.filter(Q(name__icontains=query))
        # search_result = list(chain(object_list, securities_list))
        # return list(chain(object_list, securities_list))
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q')

        # 5 тегов с наиболшим количством публикаций
        context['tags_list'] = Tag.objects.annotate(articles_quantiy=Count('taggit_taggeditem_items')).order_by(
            '-articles_quantiy')[:10]
        context['securities_types_list'] = StocksETFsBonds.objects.all()

        query = self.request.GET.get('q')
        context['securities_list'] = StockETFBond.objects.filter(Q(name__icontains=query) |
                                                                 Q(ticker__icontains=query) |
                                                                 Q(description__icontains=query))
        context['users_list'] = AdvUser.objects.filter(Q(username__icontains=query) |
                                                                 Q(first_name__icontains=query) |
                                                                 Q(last_name__icontains=query))
        # context['articles_list'] = Article.objects.all()[:10]
        return context


# class BookmarkedArticlesView(TemplateView):
#     template_name = 'articles/bookmarked_articles.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#
#         # необходимы для показа списка тэгов и типов бумаг в хедере
#         context['securities_types_list'] = StocksETFsBonds.objects.all()
#         # 5 тегов с наиболшим количством публикаций
#         context['tags_list'] = Tag.objects.annotate(articles_quantiy=Count('taggit_taggeditem_items')).order_by(
#             '-articles_quantiy')[:10]
#         return context

@login_required
def bookmarked_articles(request):
    bookemarked_articles = Article.objects.filter(bookmark=request.user.pk)
    context = {'bookemarked_articles': bookemarked_articles}
    return render(request, 'articles/bookmarked_articles.html', context)


@login_required
def bookmarked_articles(request):
    bookemarked_articles = Article.objects.filter(bookmark=request.user.pk)
    tags_list = Tag.objects.annotate(articles_quantiy=Count('taggit_taggeditem_items')).order_by(
        '-articles_quantiy')[:10]
    securities_types_list = StocksETFsBonds.objects.all()
    context = {'bookemarked_articles': bookemarked_articles, 'tags_list': tags_list, 'securities_types_list': securities_types_list,}
    return render(request, 'articles/bookmarked_articles.html', context)