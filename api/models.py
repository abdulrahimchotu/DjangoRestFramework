from django.db import models 
from django.utils import timezone
from .managers import UserManager

class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'users'

    def check_password(self, raw_password):
        from django.contrib.auth.hashers import check_password
        return check_password(raw_password, self.password)


class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    year = models.IntegerField()
    director = models.CharField(max_length=100)
    rating = models.FloatField(default=0.0)
    available_seats = models.IntegerField(default=100)
    price = models.IntegerField(default=10)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'movies'
        ordering = ['id']


class Booking(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    seats = models.IntegerField(default=1)
    total_amount = models.IntegerField(default=1)
    booking_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.movie.title}"

    class Meta:
        db_table = 'bookings'
