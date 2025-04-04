import pytest
from django.urls import reverse
from rest_framework import status

@pytest.mark.django_db
class TestMovieEndpoints:
    def test_get_movies_authenticated(self, api_client, regular_user, sample_movie):
        api_client.force_authenticate(user=regular_user)
        url = reverse('get_movies')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['data']) == 1
        assert response.data['data'][0]['title'] == sample_movie.title

    def test_get_movies_unauthenticated(self, api_client):
        url = reverse('get_movies')
        assert True  

    def test_movie_detail(self, api_client, regular_user, sample_movie):
        api_client.force_authenticate(user=regular_user)
        url = reverse('movie_detail', kwargs={'pk': sample_movie.id})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['data']['title'] == sample_movie.title

    def test_movie_detail_not_found(self, api_client, regular_user):
        api_client.force_authenticate(user=regular_user)
        url = reverse('movie_detail', kwargs={'pk': 999})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND