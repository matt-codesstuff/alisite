# Generated by Django 4.2 on 2023-05-08 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_alter_recipe_ingredients'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='media/images')),
            ],
        ),
        migrations.AlterField(
            model_name='recipe',
            name='ingredients',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
