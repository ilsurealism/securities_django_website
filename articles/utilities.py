from datetime import datetime
from django.utils.text import slugify
from unidecode import unidecode
from django.template.defaultfilters import slugify as slug
import re

def article_img_directory_path(instance, filename):
    date = datetime.now().date()
    # if instance.author.user.is_superuser:
    #     return 'images/{0}/{1}'.format(instance.slug, filename)
    # else:
    #     return 'images/{0}/{1}/{2}'.format(instance.author.username, date, filename)
    # article_title = instance.title.replace(" ", "_").lower()
    article_title = slugify(instance.title, allow_unicode=True)
    return 'images/{0}/{1}'.format(article_title, filename)

def article_slugify_function(content):
    # return slugify(unidecode(content), allow_unicode=True)
    return slugify(content, allow_unicode=True)
    # return slugify(slug(content), allow_unicode=True)
    # return unidecode(article_slug)


# def my_slugify_function(title):
#     slugified_title = slugify(title, allow_unicode=True)
#     slugified_title = slugified_title.replace(" ", "-").lower
#     return slugified_title