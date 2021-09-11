from django.contrib import admin

from .models import StocksETFsBonds, StockETFBond


class StocksETFsBondsAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')


class StockETFBondAdmin(admin.ModelAdmin):
    list_display = ('ticker', 'name', 'stocketforbond')
    list_display_links = ('ticker', 'name')
    list_filter = ('stocketforbond',)
    fields = (('name', 'icon'), ('ticker', 'slug'), 'stocketforbond',  'description', 'watchlist')
    readonly_fields = ('watchlist', 'slug')
    search_fields = ('name', 'ticker', 'description')



admin.site.register(StocksETFsBonds, StocksETFsBondsAdmin)
admin.site.register(StockETFBond, StockETFBondAdmin)
