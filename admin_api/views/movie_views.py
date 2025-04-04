from rest_framework.decorators import api_view
from rest_framework.response import Response 
from rest_framework import status
from api.models import Movie
from api.serializers import MovieSerializer
from api.decorators import require_auth

@api_view(['GET', 'POST'])
@require_auth
def create_movie(request):
    if not request.is_admin:
        return Response({
            'status': 'error',
            'message': 'Admin privileges required'
        }, status=status.HTTP_403_FORBIDDEN)
    serializer = MovieSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            'status': 'success',
            'message': 'Movie created successfully',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)
    return Response({
        'status': 'error',
        'message': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@require_auth
def movie_detail(request, pk):
    if not request.is_admin:
        return Response({
            'status': 'error',
            'message': 'Admin privileges required'
        }, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        movie = Movie.objects.get(pk=pk)
        serializer = MovieSerializer(movie)
        return Response({
            'status': 'success',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    try:
        movie = Movie.objects.get(pk=pk)
    except Movie.DoesNotExist:
        return Response({
            'status': 'error',
            'message': 'Movie not found'
        }, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = MovieSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'success',
                'message': 'Movie updated successfully',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            'status': 'error',
            'message': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        movie.delete()
        return Response({
            'status': 'success',
            'message': 'Movie deleted successfully'
        }, status=status.HTTP_200_OK)