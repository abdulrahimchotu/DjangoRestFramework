# Generated by Django 5.2 on 2025-04-04 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_movie_rename_name_user_username_remove_user_age_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='price',
            field=models.DecimalField(decimal_places=2, default=10.0, max_digits=6),
        ),
    ]
