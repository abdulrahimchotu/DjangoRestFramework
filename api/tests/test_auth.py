import pytest
from django.urls import reverse
from rest_framework import status

@pytest.mark.django_db
class TestAuthEndpoints:
    def test_signup_success(self, api_client):
        url = reverse('signup')
        data = {
            'username': 'newuser',
            'password': 'newpass'
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert 'user_id' in response.data

    def test_signup_duplicate_username(self, api_client, regular_user):
        url = reverse('signup')
        data = {
            'username': regular_user.username,
            'password': 'newpass'
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_login_success(self, api_client, regular_user):
        url = reverse('login')
        data = {
            'username': regular_user.username,
            'password': regular_user.password
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert 'refresh_token' in response.cookies
        assert 'access_token' in response.cookies

    def test_login_invalid_credentials(self, api_client):
        url = reverse('login')
        data = {
            'username': 'wronguser',
            'password': 'wrongpass'
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_logout(self, api_client):
        url = reverse('logout')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.cookies['refresh_token'].value == ''
        assert response.cookies['access_token'].value == ''