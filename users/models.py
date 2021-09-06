from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class AdvUser(AbstractUser):
    photo = models.ImageField(blank=True, verbose_name='Фотография')
    description = models.TextField(blank=True, verbose_name='Обо мне')


