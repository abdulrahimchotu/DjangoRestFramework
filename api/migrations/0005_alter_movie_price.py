# Generated by Django 5.2 on 2025-04-04 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_movie_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='price',
            field=models.IntegerField(default=10.0),
        ),
    ]
