from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Listing(models.Model):
    title = models.CharField(max_length=35)
    description = models.CharField(max_length=500)
    imageUrl = models.CharField(max_length=1500)
    price = models.FloatField()
    active = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="category")
    def __str__(self):
        return self.title