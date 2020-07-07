from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import UserManager
from . import constants as user_constants


class User(AbstractUser):
    # remove username field, we will use email as unique identifier
    username = None
    email = models.EmailField(unique=True, null=True, db_index=True)
    user_type = models.PositiveSmallIntegerField(
        choices=user_constants.USER_TYPE_CHOICES, default=2)

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    objects = UserManager()


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="user_profile"
    )
    profile_picture = models.ImageField(
        upload_to='profile',
        null=True,
        blank=True,
        default="profile1.png",
    )

    def __str__(self):
        return self.user.email
