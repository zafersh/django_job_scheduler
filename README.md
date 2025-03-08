# Django Job Scheduler

A simple Django-based web application that allows users to submit "jobs" to be processed by a background system.

## Installation

Make sure the following libraries are installed:
`pip install django djangorestframework psycopg2-binary`

1. Clone the repository.
2. Init the database. `python manage.py migrate`
3. Create a super user. `python manage.py createsuperuser`
4. Run the server. `python manage.py runserver`
5. login with created super user.


### REST APIs
`/api/jobs/`
Exposes REST APIs for:
- Submitting new jobs. `/api/submit-job/`
- Fetching the status of a specific job. `/api/jobs/<int:job_id>/status/`
- Listing all jobs for a user. `/user/jobs/`

## Technology Stack
Used tools are limited to:
- **Backend**: Django + Django REST Framework (DRF)
- **Database**: SQLite (PostgreSQL sample config is commented in settings.py)
- **Frontend**: HTML, CSS, JavaScript, Bootstrap, DataTables

