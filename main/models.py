from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Url(models.Model):
    link = models.CharField(max_length=10000)
    short_link = models.CharField(max_length=10)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
