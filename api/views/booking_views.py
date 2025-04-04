from rest_framework.decorators import api_view
from rest_framework.response import Response 
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.utils import timezone
from ..models import Movie, Booking
from ..serializers import BookingSerializer
from ..decorators import require_auth

@api_view(['POST'])
@require_auth
def book_movie_tickets(request, pk):
    try:
        movie = get_object_or_404(Movie, pk=pk)
        seats = int(request.data.get('seats', 1))
        
        if seats <= 0:
            return Response({
                'status': 'error',
                'message': 'Invalid number of seats'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if seats > movie.available_seats:
            return Response({
                'status': 'error',
                'message': 'Not enough available seats'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        total_amount = movie.price * seats
        
        booking = Booking.objects.create(
            user_id=request.user_id,
            movie=movie,
            seats=seats,
            total_amount=total_amount,
            booking_date=timezone.now()
        )
        
        movie.available_seats -= seats
        movie.save()
        
        serializer = BookingSerializer(booking)
        return Response({
            'status': 'success',
            'message': 'Booking successful',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@require_auth
def cancel_booking(request, pk):
    try:
        booking = Booking.objects.filter(
            movie_id=pk,
            user_id=request.user_id
        ).order_by('-booking_date').first()

        if not booking:
            return Response({
                'status': 'error',
                'message': 'No booking found for this movie'
            }, status=status.HTTP_404_NOT_FOUND)

        movie = booking.movie
        movie.available_seats += booking.seats
        movie.save()

        booking.delete()

        return Response({
            'status': 'success',
            'message': 'Booking cancelled successfully',
            'data': {
                'refund_amount': booking.total_amount,
                'seats_returned': booking.seats
            }
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@require_auth
def get_user_bookings(request):
    bookings = Booking.objects.filter(user_id=request.user_id)
    serializer = BookingSerializer(bookings, many=True)
    return Response({
        'status': 'success',
        'data': serializer.data
    }, status=status.HTTP_200_OK)