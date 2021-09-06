from django.db import models
from django.urls import reverse

from django_extensions.db.fields import AutoSlugField

from users.models import AdvUser


class StocksETFsBonds(models.Model):
    name = models.CharField(max_length=50, unique=True)
    # slug = models.SlugField(unique=True)
    slug = AutoSlugField(populate_from='name', allow_unicode=True, unique=True)
    icon = models.ImageField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тип ценной бумаги'
        verbose_name_plural = 'Типы ценных бумаг'


class StockETFBond(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Название')
    slug = AutoSlugField(populate_from='ticker', unique=True)
    stocketforbond = models.ForeignKey(StocksETFsBonds, on_delete=models.PROTECT, blank=True, verbose_name='Тип')
    ticker = models.CharField(max_length=10, blank=True, unique=True, verbose_name='Тикер')
    icon = models.ImageField(blank=True, verbose_name='Логотип')
    description = models.TextField(max_length=500, blank=True, verbose_name='Описание')
    watchlist = models.ManyToManyField(AdvUser, blank=True, verbose_name='Список наблюдения')

    def __str__(self):
        return self.ticker


    class Meta:
        verbose_name = 'Ценная бумага'
        verbose_name_plural = 'Ценные бумаги'

    # You don’t even need to provide a success_url
    # for CreateView or UpdateView - they will use get_absolute_url() on the model object if available.
    def get_absolute_url(self):
        return reverse('securities:security_detail', kwargs={'slug': self.slug})
