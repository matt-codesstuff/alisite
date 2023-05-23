from django.db import models
from ckeditor.fields import RichTextField
from django.core.validators import RegexValidator


class Category(models.Model):
    name = models.CharField(max_length=50)
    image = models.URLField(blank=True, null=True,)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=50)
    body = models.TextField()
    ingredients = models.CharField(max_length=1000, blank=True, null=True)
    servings = models.IntegerField(blank=True, null=True)
    site = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.title
