# Task Application API

Backend API built with Django, Django REST Framework, Simple JWT, django-filter, and drf-spectacular.

## Project Setup

Clone the repository first:

```bash
git clone https://github.com/Abduqodir7007/job_task.git
cd job_task
```

Downloads the project from GitHub and moves into the project directory.

Then run these commands from the project root.

```bash
uv sync
```

Installs the Python dependencies from `pyproject.toml` and `uv.lock` into the local virtual environment.

```bash
cp .env.example .env
```

Creates a local environment file. Fill in the values for `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, `DATABASE_URL`, and optionally `VERCEL_URL`.

Example:

```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=
VERCEL_URL=
```

```bash
uv run python manage.py migrate
```
Creates the default roles used by the API.

```bash
python manage.py createsuperuser
```

Creates an admin user for Django admin and admin-only API actions.

```bash
python manage.py runserver
```

Starts the local development server at `http://127.0.0.1:8000/`.

## Authentication

The API uses JWT authentication.

Send the access token in protected requests:

```http
Authorization: Bearer <access_token>
```

Register and login endpoints return both `refresh` and `access` tokens.

## Test Users

You can use these test users for login:

| Email | Password |
| --- | --- |
| `admin@test.com` | `AdminUser123!` |
| `payment@test.com` | `PaymentUser123!` |
| `reports@test.com` | `ReportsUser123!` |
| `user@test.com` | `RegularUser123!` |

## Pagination

List endpoints use DRF page-number pagination.

Use the `page` query parameter:

```http
GET /api/users/?page=2
GET /api/payments/?page=2
```

Paginated responses include `count`, `next`, `previous`, and `results`.

## Users API

### Register

`POST /api/register/`

Creates a new user and returns JWT tokens.

Request body:

```json
{
  "email": "user@example.com",
  "password": "StrongPassword123!",
  "first_name": "Ali",
  "last_name": "Valiyev",
  "roles": [1]
}
```

Notes:

- `email` must be unique.
- `first_name` and `last_name` must contain only letters.
- `roles` is required and must contain existing role IDs.
- The admin role cannot be assigned during public registration.

### Login

`POST /api/login/`

Authenticates a user and returns JWT tokens.

Request body:

```json
{
  "email": "user@example.com",
  "password": "StrongPassword123!"
}
```

### Current User

`GET /api/auth/me/`

Returns the authenticated user's profile.

Requires JWT authentication.

### Roles List

`GET /api/roles/`

Returns available roles.

Response fields:

- `id`
- `name`
- `display`

### Users List and Management

`GET /api/users/`

Returns a paginated list of users.

Requires an admin role.

Filters:

| Query parameter | Description |
| --- | --- |
| `email__iexact` | Exact email match, case-insensitive |
| `email__icontains` | Email contains text, case-insensitive |
| `first_name__iexact` | Exact first name match, case-insensitive |
| `first_name__icontains` | First name contains text, case-insensitive |
| `last_name__iexact` | Exact last name match, case-insensitive |
| `roles__name__iexact` | Exact role name match, case-insensitive |
| `page` | Pagination page number |

Examples:

```http
GET /api/users/?email__icontains=gmail.com
GET /api/users/?first_name__icontains=ali
GET /api/users/?roles__name__iexact=user&page=1
```

Other user management endpoints:

| Method | Endpoint | Description |
| --- | --- | --- |
| `POST` | `/api/users/` | Create a user |
| `GET` | `/api/users/{id}/` | Retrieve one user |
| `PUT` | `/api/users/{id}/` | Fully update a user |
| `PATCH` | `/api/users/{id}/` | Partially update a user |
| `DELETE` | `/api/users/{id}/` | Delete a user |

### Dashboard

`GET /api/users/dashboard/`

Returns user counts for the admin dashboard.

Requires JWT authentication and admin role.

Response body:

```json
{
  "total_users": 100,
  "active_users": 92,
  "admin_users": 3,
  "payment_users": 12,
  "report_users": 8
}
```

Status codes:

| Code | Meaning |
| --- | --- |
| `200 OK` | Dashboard data returned successfully |
| `401 Unauthorized` | Missing or invalid JWT token |
| `403 Forbidden` | Authenticated user does not have the admin role |

## Payments API

### Payments List

`GET /api/payments/`

Returns a paginated list of payments with user details.

Requires JWT authentication and payment/admin permission.

Filters:

| Query parameter | Description |
| --- | --- |
| `status` | Exact payment status |
| `status__iexact` | Exact payment status, case-insensitive |
| `method` | Exact payment method |
| `method__iexact` | Exact payment method, case-insensitive |
| `amount__gte` | Amount greater than or equal to value |
| `amount__lte` | Amount less than or equal to value |
| `user__first_name` | Exact user first name |
| `user__first_name__iexact` | Exact user first name, case-insensitive |
| `user__last_name` | Exact user last name |
| `user__last_name__iexact` | Exact user last name, case-insensitive |
| `page` | Pagination page number |

Supported payment methods:

- `payme`
- `click`
- `uzum`

Supported statuses:

- `pending`
- `completed`
- `failed`

Examples:

```http
GET /api/payments/?method=payme
GET /api/payments/?status__iexact=completed
GET /api/payments/?amount__gte=10000&amount__lte=50000
GET /api/payments/?user__first_name__iexact=Ali&page=1
```

### Create Payment

`POST /api/payments/`

Creates a payment for the authenticated user.

Requires JWT authentication and payment/admin permission.

Request body:

```json
{
  "amount": "25000.00",
  "method": "payme"
}
```

Notes:

- `amount` must be greater than zero.
- `method` can be `payme`, `click`, or `uzum`.
- The API currently saves created payments with `completed` status.

### Payment Report

`GET /api/reports/`

Returns total sales and totals grouped by payment method.

Requires JWT authentication and report/admin permission.

Filters:

| Query parameter | Description |
| --- | --- |
| `start_date` | Include payments created on or after this date. Format: `YYYY-MM-DD` |
| `end_date` | Include payments created on or before this date. Format: `YYYY-MM-DD` |

Example:

```http
GET /api/reports/?start_date=2026-05-01&end_date=2026-05-31
```

Response body:

```json
{
  "payments_by_method": {
    "click": "100000.00",
    "payme": "250000.00",
    "uzum": "75000.00"
  },
  "total_sales": "425000.00"
}
```

## Swagger

Swagger API documentation is available here:

[https://job-task-7ns2llutu-jobtask1.vercel.app/api/docs/](https://job-task-7ns2llutu-jobtask1.vercel.app/api/docs/)
