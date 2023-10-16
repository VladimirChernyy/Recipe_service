from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True, max_length=150)

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
        constraints = (
            models.UniqueConstraint(
                fields=('username', 'author'),
                name='unique_follow',
            ),
        )

    def __str__(self):
        return f'{self.username} follows {self.author}'
