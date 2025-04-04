from django.urls import path
from .views import (
    signup, login, logout, check_auth_status,
    get_movies, movie_detail, 
    book_movie_tickets, cancel_booking,
    get_user_bookings
)

urlpatterns = [
    # Authentication routes
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('me/', check_auth_status, name='check_auth_status'),
    
    # Movie routes
    path('movies/', get_movies, name='get_movies'),
    path('movies/<int:pk>/', movie_detail, name='movie_detail'),
    
    # Booking routes
    path('movies/<int:pk>/book/', book_movie_tickets, name='book_movie_tickets'),
    path('movies/<int:pk>/cancel/', cancel_booking, name='cancel_booking'),
    path('bookings/', get_user_bookings, name='get_user_bookings'),
]
