# Generated by Django 4.2 on 2023-04-26 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_alter_recipe_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='ingredients',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
