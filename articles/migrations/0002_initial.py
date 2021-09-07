# Generated by Django 3.2.6 on 2021-09-07 08:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('articles', '0001_initial'),
        ('stocksetfsbonds', '0002_stocketfbond_watchlist'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('taggit', '0003_taggeditem_add_unique_index'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='автор'),
        ),
        migrations.AddField(
            model_name='article',
            name='bookmark',
            field=models.ManyToManyField(blank=True, related_name='bookmarked_by_user', to=settings.AUTH_USER_MODEL, verbose_name='Читать позже'),
        ),
        migrations.AddField(
            model_name='article',
            name='stocks_etfs_or_bonds',
            field=models.ManyToManyField(blank=True, to='stocksetfsbonds.StockETFBond', verbose_name='Ценная бумага'),
        ),
        migrations.AddField(
            model_name='article',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='Теги через запятую', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Теги'),
        ),
    ]
