from rest_framework.decorators import api_view
from rest_framework.response import Response 
from rest_framework import status
from api.models import Booking
from api.serializers import BookingSerializer
from api.decorators import require_auth

@api_view(['GET'])
@require_auth
def get_bookings(request):
    if not request.is_admin:
        return Response({
            'status': 'error',
            'message': 'Admin privileges required'
        }, status=status.HTTP_403_FORBIDDEN)
    serializer = BookingSerializer(Booking.objects.all(), many=True)
    return Response({
        'status': 'success',
        'data': serializer.data
    }, status=status.HTTP_200_OK)