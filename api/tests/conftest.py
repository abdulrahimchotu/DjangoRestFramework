import pytest
from rest_framework.test import APIClient
from api.models import User, Movie, Booking
from django.urls import reverse

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def admin_user():
    # Create user without using the manager to avoid password hashing
    user = User(username="admin1", password="admin123", is_admin=True)
    user.save()
    return user

@pytest.fixture
def regular_user():
    # Create user without using the manager to avoid password hashing
    user = User(username="testuser", password="testpass123", is_admin=False)
    user.save()
    return user

@pytest.fixture
def authenticated_client(api_client, regular_user):
    # Login to get cookies set
    url = reverse('login')
    data = {
        'username': 'testuser',
        'password': 'testpass123'
    }
    response = api_client.post(url, data)
    return api_client

@pytest.fixture
def admin_client(api_client, admin_user):
    # Login to get cookies set
    url = reverse('login')
    data = {
        'username': 'admin1',
        'password': 'admin123'
    }
    response = api_client.post(url, data)
    return api_client

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
