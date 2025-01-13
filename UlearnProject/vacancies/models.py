from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User


class PageElement(models.Model):
    title = models.CharField(max_length=200)  # Заголовок элемента
    image = models.ImageField(upload_to='uploads/')  # Графики или изображения
    content = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(
        upload_to='avatars/', blank=True, null=True)  # Аватарка
    first_name = models.CharField(max_length=100, blank=True)  # Имя

    def __str__(self):
        return self.user.username
