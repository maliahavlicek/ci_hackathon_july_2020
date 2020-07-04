from django.conf import settings
from django.db import models


class Post(models.Model):
    """
    User createdable posts.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    status = models.TextField(max_length=250)
    placed = models.BooleanField(default=False)
    reations = models.CharField(max_length=25)
    datetime = models.DateTimeField(auto_now_add=True)
    photo = models.ImageField(
        upload_to='posts',
        null=True,
        blank=True
    )
