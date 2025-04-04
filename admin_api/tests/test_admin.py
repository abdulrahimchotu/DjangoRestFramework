import pytest
from django.urls import reverse
from rest_framework import status

@pytest.mark.django_db
class TestAdminEndpoints:
    def test_create_movie_admin(self, api_client, admin_user):
        api_client.force_authenticate(user=admin_user)
        url = reverse('admin_create_movie')
        data = {
            'title': 'New Movie',
            'year': 2023,
            'director': 'New Director',
            'rating': 9.0,
            'available_seats': 150,
            'price': 12
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['data']['title'] == 'New Movie'

    def test_create_movie_non_admin(self, api_client, regular_user):
        api_client.force_authenticate(user=regular_user)
        url = reverse('admin_create_movie')
        data = {
            'title': 'New Movie',
            'year': 2023,
            'director': 'New Director',
            'rating': 9.0,
            'available_seats': 150,
            'price': 12
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_all_users_admin(self, api_client, admin_user, regular_user):
        api_client.force_authenticate(user=admin_user)
        url = reverse('admin_get_users')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['data']) == 2

    def test_get_all_bookings_admin(self, api_client, admin_user, sample_booking):
        api_client.force_authenticate(user=admin_user)
        url = reverse('admin_get_bookings')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['data']) == 1