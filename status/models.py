from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from users.models import User

MOOD_CHOICES = [(1, 'amazing'), (2, 'happy'), (3, 'good'), (4, 'sad'), (5, 'terrible')]


class Status(models.Model):
    """
    Model to hold Member Status, is an extension of User through one 2 one relationship
    """
    mood = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], choices=MOOD_CHOICES,
                                       null=True, blank=True)
    plans = models.TextField(max_length=250, default="Nothing")
    help = models.TextField(max_length=250, default="Nothing")
    owner = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{0} by {1}".format(self.mood, self.owner)


class StatusInput(models.Model):
    """
    Model to help validate/serialize User Mood Object when user posts new mood
      Should never actually create a DB instance of this object
      Initiated from Update button In How you Doing section of Family Wall
    """
    mood = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=True, blank=True)
    plans = models.TextField(max_length=250, default="Nothing")
    help = models.TextField(max_length=250, default="Nothing")
    user_id = models.PositiveIntegerField()
    family_id = models.PositiveIntegerField()

    def __str__(self):
        return str(self.mood)


class AllStatusInput(models.Model):
    """
    Model to serialize/validate get_status incoming request
     Should never actually create a DB instance of this object
     Initiated from timer on wall page
    """
    user_id = models.PositiveIntegerField()
    family_id = models.PositiveIntegerField()

    def __str__(self):
        user = User.objects.get(id=self.user_id)
        return "{0} - {1}".format(self.family_id, user)
