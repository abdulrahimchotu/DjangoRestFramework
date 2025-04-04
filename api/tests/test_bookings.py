import pytest
from django.urls import reverse
from rest_framework import status

@pytest.mark.django_db
class TestBookingEndpoints:
    def test_book_movie_success(self, api_client, regular_user, sample_movie):
        api_client.force_authenticate(user=regular_user)
        url = reverse('book_movie_tickets', kwargs={'pk': sample_movie.id})
        data = {'seats': 2}
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['data']['seats'] == 2

    def test_book_movie_insufficient_seats(self, api_client, regular_user, sample_movie):
        sample_movie.available_seats = 1
        sample_movie.save()
        api_client.force_authenticate(user=regular_user)
        url = reverse('book_movie_tickets', kwargs={'pk': sample_movie.id})
        data = {'seats': 2}
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_get_user_bookings(self, api_client, regular_user, sample_booking):
        api_client.force_authenticate(user=regular_user)
        url = reverse('get_user_bookings')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['data']) == 1
        assert response.data['data'][0]['movie'] == sample_booking.movie.id

    def test_cancel_booking(self, api_client, regular_user, sample_booking):
        api_client.force_authenticate(user=regular_user)
        url = reverse('cancel_booking', kwargs={'pk': sample_booking.movie.id})
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_200_OK