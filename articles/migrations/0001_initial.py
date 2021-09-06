# Generated by Django 3.2.6 on 2021-09-06 21:25

import articles.utilities
from django.db import migrations, models
import django_extensions.db.fields
import froala_editor.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250, verbose_name='Заголовок')),
                ('slug', django_extensions.db.fields.AutoSlugField(allow_unicode=True, blank=True, editable=False, help_text='То, как будет выглядеть URL адрес статьи. Можно не указывать', populate_from='title', verbose_name='Слаг')),
                ('title_image', models.ImageField(blank=True, upload_to=articles.utilities.user_img_directory_path, verbose_name='Титульное изображение')),
                ('description', models.TextField(verbose_name='Краткое описание')),
                ('body', froala_editor.fields.FroalaField(verbose_name='Текст')),
                ('post_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')),
                ('update_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата обновления публикации')),
                ('views', models.IntegerField(default=0, verbose_name='Просмотры')),
            ],
            options={
                'verbose_name': 'Публикация',
                'verbose_name_plural': 'Публикации',
                'ordering': ['-post_date'],
            },
        ),
    ]