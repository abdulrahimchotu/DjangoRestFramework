from django.urls import path
from .views.movie_views import create_movie, movie_detail
from .views.user_views import get_users, delete_all_users
from .views.booking_views import get_bookings

urlpatterns = [
    # Movie routes
    path('movies/create/', create_movie, name='admin_create_movie'),
    path('movies/<int:pk>/', movie_detail, name='admin_movie_detail'),
    
    # User routes
    path('users/', get_users, name='admin_get_users'),
    path('users/delete-all/', delete_all_users, name='admin_delete_all_users'),
    
    # Booking routes
    path('bookings/', get_bookings, name='admin_get_bookings'),
]