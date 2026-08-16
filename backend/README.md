# Cloud Job Portal

A Django-based job portal where users can browse job listings, apply with a resume and cover letter, and track their applications.

## Features
- User registration and login (Django auth)
- Browse and search job listings
- View detailed job descriptions
- Apply to jobs with resume upload and cover letter
- Track your submitted applications
- Duplicate application prevention

## Tech Stack
- Python 3.14
- Django 6.1
- SQLite (default database)

## Setup Instructions

1. Clone the repository
   git clone <repo-url>
   cd cloud-job-portal/backend

2. Create and activate a virtual environment
   python -m venv venv
   source venv/bin/activate

3. Install dependencies
   pip install -r requirements.txt

4. Apply migrations
   python manage.py migrate

5. Create a superuser (for admin access)
   python manage.py createsuperuser

6. Run the development server
   python manage.py runserver

7. Visit http://127.0.0.1:8000/ in your browser

## Admin Panel
Visit http://127.0.0.1:8000/admin/ and log in with your superuser account to add or edit job listings.

## Project Structure
- accounts/ - user authentication (login, register)
- jobs/ - job listings, applications, and related views
- config/ - Django project settings and root URL configuration
