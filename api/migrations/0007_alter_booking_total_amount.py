# Generated by Django 5.2 on 2025-04-04 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_alter_movie_options_booking_booking_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='total_amount',
            field=models.IntegerField(default=1),
        ),
    ]
