from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from users.models import User


class Status(models.Model):
    """
    Model to hold Member Status, is an extension of User through one 2 one relationship
    """
    mood = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=True, blank=True)
    plans = models.TextField(max_length=250, default="Nothing")
    help = models.TextField(max_length=250, default="Nothing")
    owner = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{0} by {1}".format(self.mood, self.owner)


class StatusInput(models.Model):
    """
    Model to help serialize User Mood Object when user posts new mood, should never actually create a DB instance of this object
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
    Model to help serialize User Mood Objects when updating family wall on timer, should never actually create a DB instance of this object
    """
    mood = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=True, blank=True)
    plans = models.TextField(max_length=250)
    help = models.TextField(max_length=250)
    user_id = models.PositiveIntegerField()
    updated_date = models.DateTimeField()
    family_id = models.PositiveIntegerField()

    def __str__(self):
        return str(self.mood)
