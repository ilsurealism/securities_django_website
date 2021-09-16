from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from django_extensions.db.fields import AutoSlugField
from taggit.managers import TaggableManager
# from autoslug import AutoSlugField
from ckeditor_uploader.fields import RichTextUploadingField

from stocksetfsbonds.models import StockETFBond
from users.models import AdvUser
from .utilities import article_img_directory_path, article_slugify_function



class Article(models.Model):
    title = models.CharField(max_length=250, verbose_name='Заголовок')
    slug = AutoSlugField(populate_from='title', editable=True, verbose_name='Слаг',
                         help_text='То, как будет выглядеть URL адрес статьи. Можно не указывать',
                         slugify_function=article_slugify_function, allow_unicode=True)
    author = models.ForeignKey(AdvUser, verbose_name='автор', on_delete=models.CASCADE)
    title_image = models.ImageField(verbose_name='Титульное изображение', blank=True, upload_to=article_img_directory_path)
    description = models.TextField(verbose_name='Краткое описание')
    body = models.TextField(verbose_name='Текст')
    post_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    update_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата обновления публикации')
    tags = TaggableManager(verbose_name='Теги', help_text='Теги через запятую', blank=True)
    stocks_etfs_or_bonds = models.ManyToManyField(StockETFBond, blank=True, verbose_name='Ценная бумага')
    published = models.BooleanField(verbose_name='Опубликовано', default=True, db_index=True)
    bookmark = models.ManyToManyField(AdvUser, related_name='bookmarked_by_user', blank=True,
                                      verbose_name='Читать позже')
    views = models.IntegerField(default=0, verbose_name='Просмотры')

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'
        ordering = ['-post_date']

    def __str__(self):
        return self.title

    # You don’t even need to provide a success_url
    # for CreateView or UpdateView - they will use get_absolute_url() on the model object if available.
    def get_absolute_url(self):
        return reverse('articles:detail_view', kwargs={'slug': self.slug})

    def total_bookmark(self):
        return self.bookmark.count()