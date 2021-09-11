from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

from .utilities import user_photo_directory_path


class AdvUser(AbstractUser):
    photo = models.ImageField(blank=True, verbose_name='Фотография', upload_to=user_photo_directory_path)
    description = models.TextField(blank=True, verbose_name='Обо мне')


