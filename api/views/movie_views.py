from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from ..models import Movie
from ..serializers import MovieSerializer
from ..decorators import require_auth

@api_view(['GET'])
@require_auth
def get_movies(request):
    movies = Movie.objects.all()
    serializer = MovieSerializer(movies, many=True)
    return Response({
        'status': 'success',
        'data': serializer.data
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
@require_auth
def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    serializer = MovieSerializer(movie)
    return Response({
        'status': 'success',
        'data': serializer.data
    }, status=status.HTTP_200_OK)