from django.db import models
from users.models import User


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
