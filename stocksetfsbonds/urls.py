from django.urls import path

from .views import SecuritiesList, SecurityDetail, SecurityCreate, Watchlist, WatchlistView, SecurityUpdate

app_name = 'securities'

urlpatterns = [
    path('create/', SecurityCreate.as_view(), name='security_create'),
    path('update/<slug:slug>', SecurityUpdate.as_view(), name='security_update'),
    path('<slug:slug>/', SecuritiesList.as_view(), name='securities_list'),
    path('<slug:slug>', SecurityDetail.as_view(), name='security_detail'),
    path('watchlist/<slug:slug>', Watchlist, name='in_watchlist'),
    path('watchlist/securities/', WatchlistView, name='watchlist'),
]