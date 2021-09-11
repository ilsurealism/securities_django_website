from datetime import datetime
from django.utils.text import slugify
from unidecode import unidecode
from django.template.defaultfilters import slugify as slug
import re

def user_photo_directory_path(instance, filename):
    return 'images/{0}/{1}'.format(instance.username, filename)