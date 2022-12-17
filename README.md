## Django-DRF

A backend API to manage employee reviews and feedbacks. Authenticated users may add employees, reviews and assign employees to give feedbacks to other employees' reviews. Employees may give feedbacks to reviews.

This app is built with [Django](https://www.djangoproject.com/), [Django Rest Framework](https://www.django-rest-framework.org/) and [Postgres](https://www.postgresql.org/). This README file contains information about:
- [Setup](#setup)
- [Design](#design)
- [Tests](#tests)
- [Deploy](#deploy)
- [Documentation](#documentation)


## Setup

You may easily setup this app using [Docker](https://www.docker.com/) _(recommended)_ or a local environment. 

#### Docker    
```bash
# Build the docker image and run containers. 
# A PGAdmin4 service will be available at  http://localhost:5050/. 
# It is not necessary to use PGAdmin4 and it is included as a convenience.
docker compose up -d --build

# Run migrations
docker compose exec django python manage.py makemigrations
docker compose exec django python manage.py migrate

# Seed database
docker compose exec django python manage.py loaddata data.json

# Create superuser
docker compose exec django python manage.py createsuperuser
```
#### Local

```bash
# 1 . Databases: Make sure you have postgres and redis 
# servers running on ports 5432 and 6379 respectively
# Configure your databases users and passwords following the
# information in the docker-compose.yml/settings.py files

# 2 . Python: Make sure you have python 3.10 installed

# 3 . Clone the repository

# 4 . Install dependencies
# # Create virtual environment to isolate python dependencies
python -m venv ./venv

# # Activate virtual environment
source ./venv/bin/activate #(linux/mac users)
./venv/Scripts/activate #(windows users)

# # Install dependencies
pip install -r requirements.txt

# 5 . Prepare and run the app
# # Run migrations
python manage.py makemigrations
python manage.py migrate

# # Create superuser
python manage.py createsuperuser

# # Seed database
python manage.py loaddata data.json

# # Run the app
python manage.py runserver
```

## Design

There are three core entities in this app: ```Employee```, ```Review``` and ```Feedback```.  All entities have a primary key and timestamps.
- The ```Employee``` model is the most simple one and has only a __unique__ ```name```
- The ```Review``` model has a ```title```, ```review``` and ```employee``` field. The ```employee``` field represent which employee is being __reviewed__ and is constrained to ```Employee``` entries. It is modelled to be deleted on cascade if the employee is deleted.
- The ```Feedback``` model has a ```feedback```, ```review```, ```employee``` and ```pending``` field. The ```review``` field represent which review is __receiving a feedback__ is constrained to ```Review``` entries. The ```employee``` field represent which employee is __giving feedback__ and is constrained to ```Employee``` entries. These two foreign keys are configured to cascade on DELETE. The ```pending``` field is a boolean that indicates if the feedback is pending or not. It is set to ```true``` when the feedback is created and set to ```false``` when the feedback is patched. 

Admins and Users from Django's built-in authentication system are used to manage the app. Authenticated users may use the ```/api/admin``` endpoints. These endpoints are:
- Add, edit, delete and view employees (```/api/admin/employees```)
- Add, edit and view reviews. Reviews __cannot__ be deleted. (```/api/admin/reviews```)
- Assign employees to give feedbacks to reviews. This is done by creating a feedback entry. Feedbacks __cannot__ be deleted or edited via ```/api/admin``` admin routes. (```/api/admin/feedbacks```)

Unauthenticated users may use all other endpoints under ```/api/``` endpoints. These endpoints are:
- View employees (```/api/employees```). It is possible to access all pending feedbacks for an employee by accessing ```/api/employees/{id}/pending-feedbacks```
- View reviews (```/api/reviews```)
- Give feedback to reviews. This is done by consulting and __patching__ existent feedback entries. (```/api/feedbacks```)

For further information about the API endpoints, please refer to the [documentation](#documentation).

## Tests

The app is tested using Django's built-in test framework.

#### Docker
```bash
# Run tests
docker compose exec django python manage.py test
```
#### Local
```bash
# Run tests
python manage.py test
```

## Deploy

This app is configured for development. Please note:
- All credentials are configured directly in the settings.py file. For production, it is recommended to use environment variables to store sensitive information. 
- Change the ```SECRET_KEY```
- Set ```DEBUG = False```.
- Consider using a specific and secure list on ```ALLOWED_HOSTS``` and, if CORS is necessary, on ```CORS_ALLOWED_ORIGINS``` as well.
- No throttling nor caching are configured. For production, it is recommended to use a throttling system and a caching system.
- __i18n__ and __l10n__ are not configured. For production, it is recommended to configure these settings if your API will be used by users from different countries.

## Documentation

#### Swagger

The API documentation is automatically built with [drf-yasg](https://github.com/axnsan12/drf-yasg/) and made available at:
- Swagger-UI: http://localhost:8000/swagger/
- Redoc: http://localhost:8000/redoc/ 

There are some unaddressed issues with the automatic documentation of the ```PATCH /api/feedbacks/{id}``` endpoint:
- The only field required and processed is ```feedback```. The other fields (```review```, ```employee```, ```pending```) are ignored. 
- The patching can only be done once. Subsequent patching will result in a 400 error. When ```feedback``` is patched, the ```pending``` field is set to ```false```. This is done to prevent the employee from giving feedback to the same review more than once.
- Employees are not associated with any authentication system. Thus, the ```PATCH /api/feedbacks/{id}``` endpoint is public available and any feedback can be patched by anyone. Further development would require an authentication system to be implemented for employees.

Additionally, all ```/api/admin/**``` endpoints are protected by Django's built-in authentication system. As a proof of concept, only Basic Authentication is used. Don't forget to create a superuser to access the admin endpoints.
