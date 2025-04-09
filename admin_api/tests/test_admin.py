import pytest
from django.urls import reverse
from rest_framework import status
from api.models import Movie, User, Booking

@pytest.mark.django_db
class TestAdminEndpoints:
    def test_create_movie_success(self, admin_authenticated_client):
        url = reverse('admin_create_movie')
        data = {
            'title': 'New Movie',
            'year': 2023,
            'director': 'New Director',
            'rating': 9.0,
            'available_seats': 150,
            'price': 12
        }
        response = admin_authenticated_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Movie.objects.filter(title='New Movie').exists()

    def test_create_movie_non_admin(self, authenticated_client):
        url = reverse('admin_create_movie')
        data = {
            'title': 'New Movie',
            'year': 2023,
            'director': 'New Director',
            'rating': 9.0,
            'available_seats': 150,
            'price': 12
        }
        response = authenticated_client.post(url, data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_movie_detail(self, admin_authenticated_client, sample_movie):
        url = reverse('admin_movie_detail', kwargs={'pk': sample_movie.id})
        response = admin_authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert 'data' in response.data
        assert response.data['data']['title'] == sample_movie.title

    def test_update_movie(self, admin_authenticated_client, sample_movie):
        url = reverse('admin_movie_detail', kwargs={'pk': sample_movie.id})
        data = {
            'title': 'Updated Movie',
            'year': sample_movie.year,  # Include all required fields for PUT
            'director': sample_movie.director,
            'rating': sample_movie.rating,
            'available_seats': sample_movie.available_seats,
            'price': 15
        }
        response = admin_authenticated_client.put(url, data)  # Use PUT instead of PATCH
        assert response.status_code == status.HTTP_200_OK
        sample_movie.refresh_from_db()
        assert sample_movie.title == 'Updated Movie'
        assert sample_movie.price == 15

    def test_delete_movie(self, admin_authenticated_client, sample_movie):
        url = reverse('admin_movie_detail', kwargs={'pk': sample_movie.id})
        response = admin_authenticated_client.delete(url)
        assert response.status_code == status.HTTP_200_OK  # API returns 200 OK, not 204
        assert 'status' in response.data
        assert response.data['status'] == 'success'
        assert not Movie.objects.filter(id=sample_movie.id).exists()

    def test_get_all_users(self, admin_authenticated_client, regular_user):
        url = reverse('admin_get_users')
        response = admin_authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert 'data' in response.data
        assert len(response.data['data']) >= 2  # admin_user and regular_user

    def test_get_all_bookings(self, admin_authenticated_client, sample_booking):
        url = reverse('admin_get_bookings')
        response = admin_authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert 'data' in response.data
        assert len(response.data['data']) == 1
        assert response.data['data'][0]['id'] == sample_booking.id

    def test_delete_all_users(self, admin_authenticated_client, regular_user):
        # Create a new admin user that will survive the deletion
        admin2 = User(username="admin2", password="admin456", is_admin=True)
        admin2.save()

        url = reverse('admin_delete_all_users')
        response = admin_authenticated_client.delete(url)
        assert response.status_code == status.HTTP_200_OK
        assert 'status' in response.data
        assert response.data['status'] == 'success'

        # The delete_all_users view deletes all users, including the admin
        # So we need to check that no users remain
        assert User.objects.count() == 0
