from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class MatchForm(models.Model):
    juego = models.CharField(max_length=100)
    tags = models.TextField(max_length=100)
    descripcion = models.TextField(max_length=200)
    user = models.CharField(max_length=150, default='')
    time = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    def __str__(self):
        return self.juego  # name to be shown when called


class PersonalGames(models.Model):
    lol = models.BooleanField(default=False)
    minecraft = models.BooleanField(default=False)
    smash = models.BooleanField(default=False)
    valorant = models.BooleanField(default=False)
    overwatch = models.BooleanField(default=False)
    otros = models.BooleanField(default=False)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    objects = models.Manager()

    def __str__(self):
        return self.user.name + " favorite games"


class PersonalTags(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.TextField(max_length=1000, default='')
    # slug = models.SlugField(unique=True, max_length=100)
    time = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    def __str__(self):
        return self.user.name + " tags"
