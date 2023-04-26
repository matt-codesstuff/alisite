from django.db import models
from ckeditor.fields import RichTextField


class Category(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='media/images', blank=True, null=True)
    description = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name
    

class Recipe(models.Model):
     category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
     title = models.CharField(max_length=50)
     body = RichTextField()
     ingredients = models.CharField(max_length=500, blank=True, null=True)

     def __str__(self):
         return self.title




