import uuid

from django.db import models
from django.contrib.auth.models import User




class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    image = models.URLField(blank=True, null=True,)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=200, blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    ingredients = models.CharField(max_length=2000, blank=True, null=True)
    servings = models.IntegerField(blank=True, null=True)
    site = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.title
