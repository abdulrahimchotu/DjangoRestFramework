import pytest
from django.urls import reverse
from rest_framework import status
from api.models import User

@pytest.mark.django_db
class TestAuthEndpoints:
    def test_signup_success(self, api_client):
        url = reverse('signup')
        data = {
            'username': 'newuser',
            'password': 'newpass123'
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.filter(username='newuser').exists()

    def test_signup_duplicate_username(self, api_client, regular_user):
        url = reverse('signup')
        data = {
            'username': 'testuser',  # Same as regular_user
            'password': 'newpass123'
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_login_success(self, api_client, regular_user):
        url = reverse('login')
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert 'status' in response.data
        assert response.data['status'] == 'success'
        assert 'user_id' in response.data
        
        # Check that cookies are set
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

    def test_logout(self, authenticated_client):
        url = reverse('logout')
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert 'status' in response.data
        assert response.data['status'] == 'success'
        
        # Check that cookies are cleared
        assert 'refresh_token' in response.cookies
        assert response.cookies['refresh_token']['max-age'] == 0
        assert 'access_token' in response.cookies
        assert response.cookies['access_token']['max-age'] == 0

    def test_check_auth_status_authenticated(self, authenticated_client):
        url = reverse('check_auth_status')
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert 'is_authenticated' in response.data
        assert response.data['is_authenticated'] is True
        assert 'user_id' in response.data
        assert response.data['user_id'] is not None

    def test_check_auth_status_unauthenticated(self, api_client):
        url = reverse('check_auth_status')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert 'is_authenticated' in response.data
        assert response.data['is_authenticated'] is False
        assert 'user_id' in response.data
        assert response.data['user_id'] is None
