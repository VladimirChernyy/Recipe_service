from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from foodgram.constants import CustomUserLimit


class CustomUser(AbstractUser):
    username = models.CharField(
        verbose_name='Никнейм',
        max_length=CustomUserLimit.MAX_LEN_USERNAME.value,
        unique=True,
        validators=[UnicodeUsernameValidator()]
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=CustomUserLimit.MAX_LEN_FIRST_NAME.value
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=CustomUserLimit.MAX_LEN_LAST_NAME.value
    )
    email = models.EmailField(
        unique=True,
        max_length=CustomUserLimit.MAX_LEN_EMAIL_FIELD.value
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        ordering = ('username',)
        verbose_name = ('Пользователь',)
        verbose_name_plural = ('Пользователи',)

    def __str__(self):
        return self.username


class Follow(models.Model):
    username = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE,
        related_name='follower',
    )
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE,
        related_name='following',
    )

    class Meta:
        verbose_name = ('Подписчик',)
        verbose_name_plural = ('Подписчики',)
        constraints = (
            models.UniqueConstraint(
                fields=('username', 'author'),
                name='unique_follow',
            ),
            models.CheckConstraint(
                check=~models.Q(username=models.F('author')),
                name='cannot_follow_self'
            ),
        )

    def __str__(self):
        return f'{self.username} follows {self.author}'
