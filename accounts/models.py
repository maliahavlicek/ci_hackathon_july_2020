from django.conf import settings
from django.db import models
from django.contrib.auth.models import User


class UserExtended(models.Model):
    """
    The user extended model to create a
    new user and extend it with some extra field options.
    A extended user can only have 1 user & user only 1 extended user
    """
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    profile_picture = models.ImageField(
        upload_to='profile',
        null=True,
        blank=True
    )


class Family(models.Model):
    """
    A model for the family
    Users can be added to more then one family and visa versa.
    """
    family_name = models.CharField(max_length=25)
    members = models.ManyToManyField(User)
    hero_image = models.ImageField(
        upload_to='banners',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.family_name

    def get_members(self):
        try:
            members = list(self.members.all())
        except:
            members = []
        return members
