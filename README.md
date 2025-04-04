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
git clone https://github.com/abdulrahimchotu/DjangoRestFramework.git
cd myproj
```

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
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

5. Run the development server:
```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000`

## Default Admin Credentials

Use these credentials to access the admin features:
- Username: `admin1`
- Password: `admin`

You can login at:
- API Login: `http://localhost:8000/api/login/`

## API Endpoints

### Authentication Endpoints

#### Sign Up
- URL: `/api/signup/`
- Method: `POST`
- Request Body:
```json
{
    "username": "string",
    "password": "string"
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
- URL: `/api/me/`
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

## Testing

### Test Files Structure

The project includes comprehensive test suites for both the API and admin functionality:

#### API Tests

- `api/tests/test_auth.py`: Tests for authentication endpoints (signup, login, logout)
- `api/tests/test_movies.py`: Tests for movie listing and detail endpoints
- `api/tests/test_bookings.py`: Tests for booking creation, cancellation, and listing

#### Admin API Tests

- `admin_api/tests/test_admin.py`: Tests for admin-only functionality

### Running Tests

```bash
python -m pytest
```

To run specific test files:

```bash
python -m pytest api/tests/test_auth.py
python -m pytest api/tests/test_movies.py
python -m pytest api/tests/test_bookings.py
python -m pytest admin_api/tests/test_admin.py
```

To run tests with verbose output:

```bash
python -m pytest -v
```

### Test Coverage

The test suite covers the following functionality:

1. **Authentication**
   - User signup
   - User login with token generation
   - User logout and token invalidation
   - Authentication status checking

2. **Movie Management**
   - Listing movies (authenticated and unauthenticated access)
   - Retrieving movie details
   - Error handling for non-existent movies

3. **Booking System**
   - Creating bookings
   - Handling insufficient seats
   - Retrieving user bookings
   - Cancelling bookings

4. **Admin Functionality**
   - Creating new movies (admin only)
   - Access control for non-admin users
   - Listing all users (admin only)
   - Listing all bookings (admin only)

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

