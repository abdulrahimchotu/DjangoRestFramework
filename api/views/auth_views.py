from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import User
from ..serializers import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken

@api_view(['POST'])
def signup(request):
    try:
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'status': 'success',
                'message': 'User created successfully',
                'data': serializer.data,
            }, status=status.HTTP_201_CREATED)
        return Response({
            'status': 'error',
            'message': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    try:
        username = request.data.get('username')
        password = request.data.get('password')

        user = User.objects.get(username=username, password=password)

        refresh = RefreshToken()
        refresh['user_id'] = user.id
        refresh['is_admin'] = user.is_admin
        refresh['username'] = user.username

        response = Response({
            'status': 'success',
            'user_id': user.id,
        }, status=status.HTTP_200_OK)

        response.set_cookie(
            'refresh_token',
            str(refresh),
            httponly=True,
            secure=True,
            samesite='Lax',
            max_age=24 * 60 * 60  
        )

        response.set_cookie(
            'access_token',
            str(refresh.access_token),
            httponly=True,
            secure=True,
            samesite='Lax',
            max_age=60 * 60  
        )

        return response
    except User.DoesNotExist:
        return Response({
            'status': 'error',
            'message': 'Invalid credentials'
        }, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def logout(request):
    try:
        refresh_token = request.COOKIES.get('refresh_token')
        token = RefreshToken(refresh_token)
        token.blacklist()

        response = Response({
            'status': 'success',
            'message': 'Successfully logged out'
        }, status=status.HTTP_200_OK)

        response.set_cookie('refresh_token', '', max_age=0)
        response.set_cookie('access_token', '', max_age=0)

        return response
    except Exception:
        return Response({
            'status': 'error',
            'message': 'Invalid token'
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def check_auth_status(request):
    refresh_token = request.COOKIES.get('refresh_token')

    if not refresh_token:
        return Response({
            'is_authenticated': False,
            'is_admin': False,
            'user_id': None
        })

    try:
        token = RefreshToken(refresh_token)
        return Response({
            'is_authenticated': True,
            'is_admin': token['is_admin'],
            'user_id': token['user_id']
        })
    except Exception:
        return Response({
            'is_authenticated': False,
            'is_admin': False,
            'user_id': None
        })