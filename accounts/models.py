from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='account_profile',
        verbose_name='Пользователь'  # Уникальное имя
    )
    def __str__(self):
        return f"{self.user.username} Profile"
