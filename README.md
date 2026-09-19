# Job Application Tracker — Backend

A multi-user REST API for tracking job applications, built with Django REST
Framework and PostgreSQL. Each user manages their own applications with full
status-change history, contact tracking, and JWT-based authentication.

## Features

- **JWT authentication** — signup, login, and token refresh via `djangorestframework-simplejwt`
- **Per-user data isolation** — every endpoint enforces object-level ownership, not just authentication
- **Automatic status history logging** — every status transition (e.g. `applied` → `interview`) is recorded with a timestamp, not just overwritten
- **Contact tracking** — attach recruiter/referral contacts to individual applications
- **Filtering** — query applications by status
- **PostgreSQL**, containerized with Podman for local development

## Tech Stack

| Layer              | Technology                            |
| ------------------ | ------------------------------------- |
| Framework          | Django + Django REST Framework        |
| Auth               | JWT (`djangorestframework-simplejwt`) |
| Database           | PostgreSQL 16                         |
| Containerization   | Podman + podman-compose               |
| Package management | [uv](https://github.com/astral-sh/uv) |

## Architecture

```
React Frontend → Django REST API (Auth + Business Logic) → PostgreSQL
```

The API enforces authentication and per-object ownership at the view layer,
so a request is only ever able to read or modify data belonging to the
authenticated user.

## Data Model

```
User
 └── Application (company, role_title, status, applied_date)
      ├── StatusHistory (old_status, new_status, changed_at)
      └── Contact (name, email, role)
```

Every application status change — including its initial creation — writes a
`StatusHistory` row, giving a full timeline rather than a single mutable
status field.

## API Endpoints

| Method | Endpoint                             | Description                                | Auth Required |
| ------ | ------------------------------------ | ------------------------------------------ | ------------- |
| POST   | `/api/auth/register/`                | Create a new user account                  | No            |
| POST   | `/api/auth/login/`                   | Obtain access + refresh JWT                | No            |
| POST   | `/api/auth/refresh/`                 | Refresh an access token                    | No            |
| GET    | `/api/applications/`                 | List the authenticated user's applications | Yes           |
| POST   | `/api/applications/`                 | Create a new application                   | Yes           |
| GET    | `/api/applications/{id}/`            | Retrieve a single application              | Yes           |
| PATCH  | `/api/applications/{id}/`            | Update an application (e.g. status)        | Yes           |
| DELETE | `/api/applications/{id}/`            | Delete an application                      | Yes           |
| GET    | `/api/applications/{id}/history/`    | Get an application's status change history | Yes           |
| GET    | `/api/applications/{id}/contacts/`   | List contacts for an application           | Yes           |
| POST   | `/api/applications/{id}/contacts/`   | Add a contact to an application            | Yes           |
| GET    | `/api/applications/?status={status}` | Filter applications by status              | Yes           |

## Getting Started

### Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv)
- Podman + podman-compose **or** Docker + Docker Compose (the included `compose.yaml` works with either)

### Setup

1. Clone the repository

   ```bash
   git clone https://github.com/yashG0/job-application-tracker.git
   cd job-application-tracker/backend
   ```

2. Install dependencies

   ```bash
   uv sync
   ```

3. Create a `.env` file

   ```
   DB_NAME=jobtracker
   DB_USER=jobtracker
   DB_PASSWORD=your_password_here
   DB_HOST=localhost
   DB_PORT=5432
   DJANGO_SECRET_KEY=your_secret_key_here
   ```

4. Start PostgreSQL

   ```bash
   podman-compose up -d
   # or, if using Docker instead of Podman:
   docker compose up -d
   ```

5. Run migrations

   ```bash
   uv run manage.py migrate
   ```

6. Start the development server
   ```bash
   uv run manage.py runserver 0.0.0.0:8000
   ```

The API is now available at `http://localhost:8000/api/`.

## Authentication Flow

1. `POST /api/auth/register/` to create an account
2. `POST /api/auth/login/` with username/password to receive an `access` and `refresh` token
3. Include the access token on all subsequent requests:
   ```
   Authorization: Bearer <access_token>
   ```
4. When the access token expires, use `POST /api/auth/refresh/` with the refresh token to obtain a new one

## Security Notes

- Passwords are hashed via Django's built-in `create_user`, never stored in plaintext
- Every application/contact endpoint checks both authentication _and_ object-level ownership — a user cannot read or modify another user's data, even by guessing IDs
- The `user` field is never accepted as client input; it's always derived from the authenticated request

## License

MIT
