import pytest
from django.urls import reverse
from rest_framework import status
from api.models import Booking

@pytest.mark.django_db
class TestBookingEndpoints:
    def test_book_movie_success(self, authenticated_client, sample_movie):
        url = reverse('book_movie_tickets', kwargs={'pk': sample_movie.id})
        data = {
            'seats': 2
        }
        response = authenticated_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert 'data' in response.data
        assert response.data['data']['seats'] == 2
        
        # Check that available seats were reduced
        sample_movie.refresh_from_db()
        assert sample_movie.available_seats == 98  # 100 - 2

    def test_book_movie_insufficient_seats(self, authenticated_client, sample_movie):
        url = reverse('book_movie_tickets', kwargs={'pk': sample_movie.id})
        data = {
            'seats': 101  # More than available seats
        }
        response = authenticated_client.post(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'status' in response.data
        assert response.data['status'] == 'error'

    def test_get_user_bookings(self, authenticated_client, sample_booking):
        url = reverse('get_user_bookings')
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert 'data' in response.data
        assert len(response.data['data']) == 1
        assert response.data['data'][0]['id'] == sample_booking.id

    def test_cancel_booking(self, authenticated_client, sample_booking):
        url = reverse('cancel_booking', kwargs={'pk': sample_booking.movie.id})
        response = authenticated_client.delete(url)
        assert response.status_code == status.HTTP_200_OK
        assert 'status' in response.data
        assert response.data['status'] == 'success'
        assert 'data' in response.data
        assert 'refund_amount' in response.data['data']
        assert 'seats_returned' in response.data['data']
        
        # Check that booking was deleted
        assert not Booking.objects.filter(id=sample_booking.id).exists()
        
        # Check that available seats were increased
        sample_booking.movie.refresh_from_db()
        assert sample_booking.movie.available_seats == 102  # 100 + 2

    def test_cancel_nonexistent_booking(self, authenticated_client):
        url = reverse('cancel_booking', kwargs={'pk': 999})
        response = authenticated_client.delete(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
