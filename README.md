# Playto – Community Feed Prototype

This project is a prototype implementation of a community feed with threaded discussions and a dynamic leaderboard, built as part of the Playto Engineering Challenge.

The focus of this project is **backend correctness, performance, and data integrity**, with a minimal frontend to demonstrate real user interactions.

---

## Tech Stack

- **Backend:** Django, Django REST Framework
- **Frontend:** React
- **Database:** SQLite (compatible with PostgreSQL)
- **Styling:** Minimal inline styles (UI kept intentionally simple)

---

## Features

- Feed showing posts with author and like count
- Threaded (nested) comments similar to Reddit
- Like system with concurrency safety
- Karma system:
  - Like on a post → **5 karma**
  - Like on a comment → **1 karma**
- Leaderboard showing **Top 5 users by karma in the last 24 hours only**
- All karma is derived dynamically (no cached counters)

---

## Project Structure
playto-challenge/
├── backend/ # Django project
├── feed/ # Django app (models, views, serializers)
├── frontend/ # React app
├── manage.py
└── README.md



---

## Running the Project Locally

### Backend (Django)

```bash
# activate virtual environment
venv\Scripts\activate   # Windows
# or
source venv/bin/activate

# install dependencies
pip install -r requirements.txt

# run migrations
python manage.py migrate

# create admin user
python manage.py createsuperuser

# start server
python manage.py runserver



###FrontEnd (React)
cd frontend
npm install
npm start

Frontend runs at:
http://localhost:3000
