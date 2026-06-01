# Vota 🗳️

A full-featured polling and voting web application built with Django. Create multi-question MCQ polls, share them with other users, and view real-time vote breakdowns with percentage stats.

---

## Features

- **Poll creation** — multi-question MCQ polls with dynamic formsets (add/remove questions and options on the fly)
- **Voting** — one vote per user per poll, enforced at both the application and database level
- **Results dashboard** — live vote counts and percentage breakdowns per option, per question
- **Auth** — standard username/password login + Google OAuth via `django-allauth`
- **User poll management** — view and delete your own polls
- **Access control** — login required to vote or create; only the poll creator can delete

---

## Tech Stack

- **Backend** — Django 4.x, Django REST Framework (planned)
- **Database** — PostgreSQL
- **Auth** — `django-allauth` (Google OAuth)
- **Frontend** — Django templates (server-side rendered, monolith phase)
- **Deployment** — Render

---

## Project Structure

```
votingapp/
├── poll/                        # Core app — polls, questions, voting logic
├── users/                       # User profiles
├── tests/
├── static/
│   └── account/
│       └── login.css
├── templates/
│   ├── account/                 # allauth overrides
│   │   ├── base.html
│   │   └── login.html
│   └── socialaccount/           # Google OAuth templates
├── Voting/                      # Django project config
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── .env
├── .gitignore
├── client.json
├── manage.py
├── notes.txt
└── README.md
```

---

## Data Models

```
Poll ──< Question ──< Options
  |           |
  └──< Answer ──> Options (selected)
         └──> User (voter)
```

- `Poll` — created by a user, has a title and optional expiry
- `Question` — belongs to a poll, supports MCQ or open-ended types
- `Options` — belongs to a question, tracks `vote_count`
- `Answer` — records each vote; `unique_together` on `(voter, poll, question)` prevents double voting

---

## Getting Started

### Prerequisites

- Python 3.10+
- PostgreSQL
- A Google Cloud project with OAuth credentials (for social login)

### Setup

```bash
# Clone the repo
git clone https://github.com/AcexDev/vota.git
cd vota

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Fill in DB credentials, SECRET_KEY, Google OAuth keys

# Apply migrations
python manage.py migrate

# Create a superuser
python manage.py createsuperuser

# Run the dev server
python manage.py runserver
```

### Environment Variables

```env
SECRET_KEY=your-django-secret-key
DEBUG=True

# Production only (Postgres on Render)
# Leave these unset locally to fall back to SQLite
DB_NAME=your-db-name
DB_USER=your-db-user
DB_PASSWORD=your-db-password
DB_HOST=your-db-host
DB_PORT=5432

GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
```

> **Local dev** uses SQLite (`db.sqlite3`) by default — no DB setup needed.
> **Production** (Render) uses PostgreSQL. Set the `DB_*` vars in your Render environment.

---

## URL Routes

| Method | URL | View | Description |
|--------|-----|------|-------------|
| GET | `/` | `homepage` | All polls |
| GET | `/poll/<pk>/` | `PollDetailView` | Poll detail + results |
| GET/POST | `/poll/new/` | `poll_type_select` | Select poll type |
| GET/POST | `/poll/new/mcq` | `PollCreateView` | Create MCQ poll |
| POST | `/poll/<pk>/addvote/` | `add_vote` | Submit a vote |
| POST | `/poll/<pk>/delete/` | `PollDeleteView` | Delete poll (creator only) |
| GET | `/user_poll/` | `user_polls` | Current user's polls |

---

## Roadmap

This project is currently in **Phase 1 (monolith)**. Planned work:

- [ ] Migrate to Django REST Framework (DRF) — full REST API
- [ ] Decouple frontend to React/Next.js
- [ ] Open-ended (text) poll type
- [ ] Poll expiry enforcement
- [ ] Public/private poll visibility toggle
- [ ] Shareable poll links

---

## License

Apache 2.0