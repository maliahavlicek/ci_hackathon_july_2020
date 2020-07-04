from django.conf import settings
from django.db import models
from users.models import User


class Reaction(models.Model):
    """
    A model for the reaction icons.
    """
    name = models.CharField(max_length=10)
    icon = models.ImageField(
        upload_to='icons',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name


class Post(models.Model):
    """
    User createdable posts.
    """
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    status = models.TextField(max_length=250)
    react = models.ForeignKey(
        Reaction,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    placed = models.BooleanField(default=False)
    datetime = models.DateTimeField(auto_now_add=True)
    photo = models.ImageField(
        upload_to='posts',
        null=True,
        blank=True
    )
