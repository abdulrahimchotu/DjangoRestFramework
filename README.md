# Movie Booking System API

A Django REST API for a movie booking system that allows users to browse movies, make bookings, and manage their reservations. The system also includes an admin interface for managing movies, users, and bookings.

## Features

- User authentication with JWT tokens
- Movie listing and details
- Ticket booking system
- Admin dashboard for system management
- Secure cookie-based token storage

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd myproj
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Apply database migrations:
```bash
python manage.py migrate
```

5. Create a superuser (admin):
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Authentication Endpoints

#### Sign Up
- URL: `/api/signup/`
- Method: `POST`
- Request Body:
```json
{
    "username": "string",
    "password": "string",
    "is_admin": false
}
```

#### Login
- URL: `/api/login/`
- Method: `POST`
- Request Body:
```json
{
    "username": "string",
    "password": "string"
}
```
- Response: Sets HTTP-only cookies for access and refresh tokens

#### Logout
- URL: `/api/logout/`
- Method: `GET`
- Response: Clears authentication cookies

#### Check Auth Status
- URL: `/api/check_auth/`
- Method: `GET`
- Response: Returns authentication status and user info

### Movie Endpoints

#### List Movies
- URL: `/api/movies/`
- Method: `GET`
- Authentication: Required
- Response: List of all movies

#### Movie Detail
- URL: `/api/movies/<id>/`
- Method: `GET`
- Authentication: Required
- Response: Detailed movie information

### Booking Endpoints

#### Book Movie Tickets
- URL: `/api/movies/<id>/book/`
- Method: `POST`
- Authentication: Required
- Request Body:
```json
{
    "seats": 2
}
```

#### Cancel Booking
- URL: `/api/movies/<id>/cancel/`
- Method: `DELETE`
- Authentication: Required

#### Get User Bookings
- URL: `/api/bookings/`
- Method: `GET`
- Authentication: Required

### Admin Endpoints

#### Create Movie
- URL: `/api/admin/movies/create/`
- Method: `POST`
- Authentication: Admin only
- Request Body:
```json
{
    "title": "string",
    "year": 2023,
    "director": "string",
    "rating": 8.5,
    "available_seats": 100,
    "price": 10
}
```

#### Get All Users
- URL: `/api/admin/users/`
- Method: `GET`
- Authentication: Admin only

#### Get All Bookings
- URL: `/api/admin/bookings/`
- Method: `GET`
- Authentication: Admin only

## Database Schema

### User Model
```python
{
    "id": "integer (auto)",
    "username": "string (unique)",
    "password": "string",
    "is_admin": "boolean"
}
```

### Movie Model
```python
{
    "id": "integer (auto)",
    "title": "string",
    "year": "integer",
    "director": "string",
    "rating": "float",
    "available_seats": "integer",
    "price": "integer"
}
```

### Booking Model
```python
{
    "id": "integer (auto)",
    "user": "foreign key (User)",
    "movie": "foreign key (Movie)",
    "seats": "integer",
    "total_amount": "integer",
    "booking_date": "datetime"
}
```

## Authentication

The system uses JWT (JSON Web Tokens) for authentication. Tokens are stored in HTTP-only cookies for security.
- Access tokens expire after 1 hour
- Refresh tokens expire after 1 day

## Error Handling

All endpoints return standardized error responses:
```json
{
    "status": "error",
    "message": "Error description"
}
```

Common HTTP status codes:
- 200: Success
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found

## Development

1. Make sure DEBUG is set to False in production:
```python
# settings.py
DEBUG = False
```

2. Update ALLOWED_HOSTS in settings.py for production:
```python
ALLOWED_HOSTS = ['your-domain.com']
```

3. Use a proper database in production (e.g., PostgreSQL)

## Security Notes

1. Store sensitive information in environment variables
2. Use HTTPS in production
3. Keep Django and all dependencies updated
4. Never expose DEBUG=True in production
5. Change the Django SECRET_KEY in production

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

[Add your license here]