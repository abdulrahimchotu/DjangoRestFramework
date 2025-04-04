from rest_framework.decorators import api_view
from rest_framework.response import Response 
from rest_framework import status
from api.models import User
from api.serializers import UserSerializer
from api.decorators import require_auth

@api_view(['GET'])
@require_auth
def get_users(request):
    if not request.is_admin:
        return Response({
            'status': 'error',
            'message': 'Admin privileges required'
        }, status=status.HTTP_403_FORBIDDEN)
    serializer = UserSerializer(User.objects.all(), many=True)
    return Response({
        'status': 'success',
        'data': serializer.data
    }, status=status.HTTP_200_OK)

@api_view(['DELETE'])
@require_auth
def delete_all_users(request):
    if not request.is_admin:
        return Response({
            'status': 'error',
            'message': 'Admin privileges required'
        }, status=status.HTTP_403_FORBIDDEN)
    User.objects.all().delete()
    return Response({
        'status': 'success',
        'message': 'All users deleted successfully'
    }, status=status.HTTP_200_OK)