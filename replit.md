# IFRIMentorLink

A web-based mentorship platform for students at the Institut de Formation et de Recherche en Informatique (IFRI) in Benin. It connects student mentees with experienced peer mentors using an intelligent matching algorithm.

## Tech Stack

- **Backend:** Python 3.12 + Django 6 + Django REST Framework
- **Auth:** JWT via `djangorestframework-simplejwt`
- **Database:** SQLite (development)
- **Frontend:** Vanilla HTML5, CSS3, JavaScript (root-level static files)
- **CORS:** `django-cors-headers`

## Project Structure

- `config/` — Django project config (settings, URLs, WSGI/ASGI)
- `config/users/` — Custom user model (`Utilisateur`) with mentor/mentee roles
- `matching/` — Mentor matching algorithm, profiles, availability, and session logic
- `messaging/` — Conversation and message models
- `notifications/` — Signal-based notification system
- `*.html`, `*.css`, `*.js` — Frontend pages served from project root

## Running the App

```bash
python manage.py runserver 0.0.0.0:5000
```

## Key URLs

- `/` — Landing page
- `/connexion/` — Login page
- `/inscription/` — Registration page
- `/dashboard/mentor/` — Mentor dashboard
- `/dashboard/mentee/` — Mentee dashboard
- `/api/users/register/` — User registration API
- `/api/users/me/` — User profile API
- `/api/login/` — Login (returns JWT tokens)
- `/api/token/` — JWT token endpoint
- `/api/matching/` — Mentor recommendations
- `/api/messaging/` — Conversations and messages
- `/api/notifications/` — Notifications
- `/admin/` — Django admin

## User Preferences

(none set yet)
