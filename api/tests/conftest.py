import pytest
from rest_framework.test import APIClient
from api.models import User, Movie, Booking

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def admin_user():
    return User.objects.create(
        username="admin1",
        password="admin",
        is_admin=True
    )

@pytest.fixture
def regular_user():
    return User.objects.create(
        username="testuser",
        password="testpass",
        is_admin=False
    )

@pytest.fixture
def sample_movie():
    return Movie.objects.create(
        title="Test Movie",
        year=2023,
        director="Test Director",
        rating=8.5,
        available_seats=100,
        price=10
    )

@pytest.fixture
def sample_booking(regular_user, sample_movie):
    return Booking.objects.create(
        user=regular_user,
        movie=sample_movie,
        seats=2,
        total_amount=20
    )