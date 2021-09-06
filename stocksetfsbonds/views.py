from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.db.models import Count
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone

from .models import StockETFBond, StocksETFsBonds
from articles.models import Article

from .tiingo import get_meta_data, get_price, get_daily_data, get_additional_data


from taggit.models import Tag

class SecuritiesList(ListView):

    template_name = 'stocksetfsbonds/securities_list.html'
    context_object_name = 'securities_list'

    # список бумаг по категории
    def get_queryset(self):
        return StockETFBond.objects.filter(stocketforbond__slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # необходимы для показа списка тэгов и типов бумаг в хедере
        # context['tags_list'] = Tag.objects.all()
        context['securities_types_list'] = StocksETFsBonds.objects.all()
        # 5 тегов с наиболшим количством публикаций
        context['tags_list'] = Tag.objects.annotate(articles_quantiy=Count('taggit_taggeditem_items')).order_by(
            '-articles_quantiy')[:10]

        # заголовок с названием типа ценной бумаги
        context['current_type'] = StocksETFsBonds.objects.get(slug=self.kwargs['slug'])
        return context


class SecurityDetail(DetailView):
    model = StockETFBond
    template_name = 'stocksetfsbonds/security_detail.html'
    context_object_name = 'security'

    # def get_queryset(self):
    #     return Article.objects.filter(stocks_etfs_or_bonds__name=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # необходимы для показа списка тэгов и типов бумаг в хедере
        # context['tags_list'] = Tag.objects.all()
        context['securities_types_list'] = StocksETFsBonds.objects.all()
        # 5 тегов с наиболшим количством публикаций
        context['tags_list'] = Tag.objects.annotate(articles_quantiy=Count('taggit_taggeditem_items')).order_by(
            '-articles_quantiy')[:10]

        # for tiingo
        context['ticker'] = StockETFBond.objects.get(ticker=self.object.ticker)
        context['meta'] = get_meta_data(StockETFBond.objects.get(ticker=self.object.ticker))
        context['price'] = get_price(StockETFBond.objects.get(ticker=self.object.ticker))
        security_daily_data = get_daily_data(StockETFBond.objects.get(ticker=self.object.ticker))
        context['daily_data'] = security_daily_data

        # context['additional_data'] = get_additional_data()

        stuff = get_object_or_404(StockETFBond, slug=self.kwargs['slug'])
        in_watchlist = False
        if stuff.watchlist.filter(id=self.request.user.id).exists():
            in_watchlist = True
        context["watchlist"] = in_watchlist


        # вывод связанных статей
        context['articles_list'] = Article.objects.filter(stocks_etfs_or_bonds__slug=self.kwargs['slug'])
        return context


class SecurityCreate(LoginRequiredMixin, CreateView):
    model = StockETFBond
    template_name = 'stocksetfsbonds/security_create.html'
    context_object_name = 'security'
    fields = ('name', 'stocketforbond', 'ticker', 'icon', 'description')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # необходимы для показа списка тэгов и типов бумаг в хедере
        # context['tags_list'] = Tag.objects.all()
        context['securities_types_list'] = StocksETFsBonds.objects.all()
        # 5 тегов с наиболшим количством публикаций
        context['tags_list'] = Tag.objects.annotate(articles_quantiy=Count('taggit_taggeditem_items')).order_by(
            '-articles_quantiy')[:10]
        return context


def Watchlist(request, slug):
    secuirity = get_object_or_404(StockETFBond, id=request.POST.get('stocketfbond_id'))
    in_watchlist = False
    if secuirity.watchlist.filter(id=request.user.id).exists():
        secuirity.watchlist.remove(request.user)
        in_watchlist = False
    else:
        secuirity.watchlist.add(request.user)
        in_watchlist = True
    # return HttpResponseRedirect(reverse('articles:detail_view', args=[str(slug)]))
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


@login_required
def WatchlistView(request):
    in_watchlist = StockETFBond.objects.filter(watchlist=request.user.pk)
    tags_list = Tag.objects.annotate(articles_quantiy=Count('taggit_taggeditem_items')).order_by(
        '-articles_quantiy')[:10]
    securities_types_list = StocksETFsBonds.objects.all()
    context = {'in_watchlist': in_watchlist, 'tags_list': tags_list, 'securities_types_list': securities_types_list,}

    return render(request, 'stocksetfsbonds/watchlist_view.html', context)