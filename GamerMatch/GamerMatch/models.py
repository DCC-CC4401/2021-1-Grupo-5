from django.db import models


# Create your models here.
class MatchForm(models.Model):
    juego = models.CharField(max_length=100)
    tags = models.TextField(max_length=100)
    descripcion = models.TextField(max_length=200)
    user = models.CharField(max_length=150, default='')
    time = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.juego  # name to be shown when called