# Team Production System

Team Production System is an app for mentees to schedule one-on-one sessions with mentors.

## Quick links:

- [Features](#features)
- [Run Locally](#run-locally)
- [Running Celery and Redis Locally](#run-celery-and-redis-locally)
- [Environment Variables](#environment-variables)
- [Testing](#testing)
- [Submitting Code](#submitting-code)
- [API Reference](#api-reference)

## Contributing

Contributions are always welcome!

See [contributing.md](https://github.com/TeamProductionSystem/Team_Production_System_BE/blob/main/CONTRIBUTING.md) for ways to get started.

Please adhere to this project's [code of conduct](https://github.com/TeamProductionSystem/Team_Production_System_BE/blob/main/CODE_OF_CONDUCT.md).

## Features

- Users can setup profiles as a mentor or mentee.
- Mentors can set their skill set and avalibilty.
- Mentees can schedule sessions with the menots, filtered by skills and avalibilty
- Mentors can confirm sessions
- Both mentor and mentee can cancel a session prior to session start time.

# Run Locally

Clone the project:

```bash
git clone https://github.com/TeamProductionSystem/Team_Production_System_BE.git
```

Navigate to the project directory:

```bash
cd Team_Production_System_BE
```

Set up a virtual environment for the project using pipenv. If you don't have pipenv installed, you can install it using pip:

```bash
pip install pipenv
```

Then, activate the virtual environment by running:

```bash
pipenv shell
```

Install the project dependencies:

```bash
pipenv install
```

Set up the database by running the migrations:

```bash
python manage.py migrate
```

Start the development server:

```bash
python manage.py runserver
```

The app should now be running at http://localhost:8000/

## Run Celery and Redis locally

Only needed if you want 15/60 minute reminders of scheduled sessions.

Start the Redis server:

```bash
redis-server
```

Start the Celery server:

```bash
celery -A config.celery worker --loglevel=info
```

Start the Celery Beat server:

```bash
celery -A config.celery beat -l debug
```

## Environment Variables

1.  Create a file named .env in the root directory of your project. This file will contain your environment variables.
2.  Open the .env file in a text editor and set your environment variables in the following format:
    'VARIABLE_NAME=value'

    For example:

```
DATABASE_PASSWORD=mentors
DATABASE_NAME=mentors
DATABASE_USER=mentors
DATABASE_HOST=localhost
DATABASE_PORT=5432
SECRET_KEY=my_secret_key
DEBUG=True
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_PASSWORD=admin_password
DJANGO_SUPERUSER_EMAIL=admin@example.com
CELERY_BROKER_URL = local_redis_url
CELERY_RESULT_BACKEND = local_redis_url
```

- DATABASE_URL: This should be set to the URL of your database. Depending on your database type, this may include a username, password, host, and port.

- SECRET_KEY: This should be set to a secret key that is used for cryptographic signing in Django. It is important that this value is kept secret and is not shared publicly.

- DEBUG: This should be set to a boolean value (True or False) and is used to enable or disable debugging in Django. It is recommended to set this to False in production environments.

- DJANGO_SUPERUSER_USERNAME: This should be set to the username you want to use for the Django superuser account.

- DJANGO_SUPERUSER_PASSWORD: This should be set to the password you want to use for the Django superuser account.

- DJANGO_SUPERUSER_EMAIL: This should be set to the email address you want to use for the Django superuser account.

- CELERY_BROKER_URL: This should be set to your local redis url.

- CELERY_RESULT_BACKEND: This should be set to your local redis url.

3. Save the .env file.

# Testing

For testing this app, we are using [Django Test Case](https://docs.djangoproject.com/en/4.2/topics/testing/overview/) and [Django REST Framework API Test Case](https://www.django-rest-framework.org/api-guide/testing/#api-test-cases) along with [coverage.py](https://coverage.readthedocs.io/en/7.2.7/index.html) for test coverage reporting.

To run tests:
`python manage.py test`

To skip a test that isn't finished, add the following before the test class:
`@unittest.skip("Test file is not ready yet")`

To run coverage for test:
`coverage run manage.py test`

After you run tests you can get the report in command-line by running:
`coverage report`

For an interactive html report, run:
`coverage html`

Then in the `htmlcov` folder of the project, open the file `index.html` in a browser. Here you can see an indepth analysis of coverage and what lines need testing. Click available links to view specific file coverage data.

Here is some helpful information on testing in Django and Django REST Framework: https://www.rootstrap.com/blog/testing-in-django-django-rest-basics-useful-tools-good-practices

# Submitting Code

We use a pre-commit to check branch names and commit messages. Please follow the the following schema for branch names and commit messages:

## Branch Names

Branch names should be in the following format:

`<type>/<issue-number>/<description>`

**Type:** The type of branch. This should be one of the following:

- feat - Adding a new feature
- bugfix - Fixing bugs in the code
- hotfix - For emergency fixes
- test - Experimental changes for testing purposes
- chore - Changes to the build process or auxiliary tools and libraries such as documentation generation

**Issue Number:** The issue number associated with the branch. This should be the number of the issue in the GitHub repository or the trello board.

**Description:** A short description of the branch. This should be in lowercase and use dashes instead of spaces.

## Commit Messages

Commit messages should be in the following format:

`<type>(<scope>): <description>`

**Type:** Represents the type of change that was made. This should be one of the following:

- feat - Adding a new feature
- fix - Fixing bugs in the code
- docs - Changes to documentation
- style - Changes to code style
- refactor - Changes to code that neither fixes a bug nor adds a feature
- perf - Changes to code that improves performance
- test - Adding or updating tests
- build - Changes to the build process or dependencies
- ci - Changes to CI configuration files and scripts
- chore - Miscellaneous changes, such as updating packages or bumping a version number
- revert - Reverting a previous commit

**Scope:** This is optional but can provide additional contextual information. It describes the section or aspect of the codebase affected by the change. For example, auth for authentication-related changes or header for changes to a website's header component.

**Description:** A concise description of the changes. Start with a lowercase verb indicating what was done (e.g., add, update, remove, fix).

# API Reference

API URL - https://team-production-system.onrender.com

## Quck Links:

- [User Endpoints](#user-create)
- [Mentor Endpoints](#view-mentors-list-user-authentication-required)
- [Mentee Endpoints](#view-mentee-list-user-authentication-required)
- [Availability Endpoints](#mentors-availabilty-user-authentication-required)
- [Session Endpoints](#sessions-user-authentication-required)
- [Notification Endpoints](#update-notification-settings-user-authentication-required)

## User Create

- Create a new user

```http
  POST https://team-production-system.onrender.com/auth/users/
```

| Body          | Type     | Description             |
| :------------ | :------- | :---------------------- |
| `username`    | `string` | New Username            |
| `password`    | `string` | User generated password |
| `re_password` | `string` | User generated password |
| `email`       | `string` | User generated email    |

#### Request Sample:

```
POST /auth/users/
Content-Type: json
Authorization: N/A
Host: https://team-production-system.onrender.com
{
	"username": "TestUserLogin" ,
	"email": "testemail@fake.com"
	"password": "TestUserPassword",
	"re_password": "TestUserPassword",
}

```

#### Response Example (201 Created)

```
{
	"email": "testemail@fake.com",
	"username": "TestUserLogin",
	"id": 5
}

```

---

## Token Authentication / User Login

- Create a user token.

```http
POST - https://team-production-system.onrender.com/auth/token/login/
```

| Body       | Type     | Description             |
| :--------- | :------- | :---------------------- |
| `username` | `string` | Username                |
| `password` | `string` | User generated password |

#### Request Sample:

```
POST /auth/token/login/
Content-Type: json
Authorization: N/A
Host: https://team-production-system.onrender.com

{
	"username": "TestUserLogin" ,
	"password": "TestUserPassword"
}

```

#### Response Example (200 OK)

```
{
	"auth_token": "****************************************"
}

```

---

## User Logout (User Authentication **Required**)

- Log the current user out.

```http
POST - https://team-production-system.onrender.com/auth/token/logout/
```

| Body       | Type     | Description             |
| :--------- | :------- | :---------------------- |
| `username` | `string` | Username                |
| `password` | `string` | User generated password |

#### Request Sample:

```
POST /auth/token/logout/
Content-Type: json
Authorization: Required
Host: https://team-production-system.onrender.com

{
	"username": "TestUserLogin" ,
	"password": "TestUserPassword",
}

```

#### Response Example (204 No Content)

```
No body returned for response

```

---

## View Logged in Users Profile (User Authentication **Required**)

- View the current logged in users information

```http
GET - https://team-production-system.onrender.com/myprofile/
```

| Body            | Type        | Description                  |
| :-------------- | :---------- | :--------------------------- |
| `username`      | `string`    | Username                     |
| `first_name`    | `string`    | User generated first name    |
| `last_name`     | `string`    | User generated last name     |
| `email`         | `string`    | User generated email         |
| `phone_number`  | `string`    | User generated phone number  |
| `profile_photo` | `form-data` | User submitted profile photo |
| `is_mentor`     | `boolean`   | Is mentor flag               |
| `is_mentee`     | `boolean`   | Is mentee flag               |
| `is_active`     | `boolean`   | Is active flag               |

#### Request Sample:

```
GET /myprofile/
Content-Type: json
Authorization: Required
Host: https://team-production-system.onrender.com

{
	""
}

```

#### Response Example (200 OK)

```
{
	"pk": 6,
	"username": "testusername",
	"first_name": "",
	"last_name": "",
	"email": "testuser@testemail.com",
	"phone_number": null,
	"profile_photo": null,
	"is_mentor": false,
	"is_mentee": false,
	"is_active": true
}

```

---

## Edit User Profile (User Authentication **Required**)

- Update the users profile information.
- **Note: This endpoint has multipart/form-data content type.**

```http
PATCH - https://team-production-system.onrender.com/myprofile/
```

| Body            | Type        | Description                  |
| :-------------- | :---------- | :--------------------------- |
| `username`      | `string`    | Username                     |
| `first_name`    | `string`    | User generated first name    |
| `last_name`     | `string`    | User generated last name     |
| `email`         | `string`    | User generated email         |
| `phone_number`  | `string`    | User generated phone number  |
| `profile_photo` | `form-data` | User submitted profile photo |
| `is_mentor`     | `boolean`   | Is mentor flag               |
| `is_mentee`     | `boolean`   | Is mentee flag               |
| `is_active`     | `boolean`   | Is active flag               |

#### Request Sample:

```
PATCH /myprofile/
Content-Type: Multipart/form-data
Authorization: Required
Host: https://team-production-system.onrender.com

	body: MultiPartFormData,
	Example:

	{
		"username": "testusername",
		"first_name": "testuserfirstname",
		"last_name": "testuserlastname",
		"email": "testuser@testemail.com",
		"phone_number": "+12345678987",
		"profile_photo": ".../testuser.jpg",
		"is_mentor": true
	}


```

#### Response Example (200 OK)

```
{
	"pk": 6,
	"username": "testusername",
	"first_name": "testuserfirstname",
	"last_name": "testuserlastname",
	"email": "testuser@testemail.com",
	"phone_number": "+12345678987",
	"profile_photo": ".../testuser.jpg",
	"is_mentor": true,
	"is_mentee": false,
	"is_active": true
}

```

---

## View Mentors List (User Authentication **Required**)

- View a list of all user with the mentors flag (Expired availabilties are filtered out)

```http
GET - https://team-production-system.onrender.com/mentor/
```

| Body            | Type        | Description                  |
| :-------------- | :---------- | :--------------------------- |
| `pk`            | `int`       | The user pk                  |
| `username`      | `string`    | Username                     |
| `first_name`    | `string`    | User generated first name    |
| `last_name`     | `string`    | User generated last name     |
| `is_mentor`     | `boolean`   | Is mentor flag               |
| `profile_photo` | `form-data` | User submitted profile photo |

**Nested Information:**

| Body             | Type     | Description                   |
| :--------------- | :------- | :---------------------------- |
| `about_me`       | `string` | Information about the user    |
| `skills`         | `string` | Skills the user has           |
| `availabilities` | `array`  | Availabilities the mentor has |

#### Request Sample:

```
GET /mentor/
Content-Type: json
Authorization: Required
Host: https://team-production-system.onrender.com

{
	""
}

```

#### Response Example (200 OK)

```
[
	{
		"pk": 6,
		"username": "testusername",
		"first_name": "Test",
		"last_name": "User",
		"is_mentor": true,
		"mentor_profile": {
			"about_me": "I am test user",
			"skills": [
				"CSS",
				"JavaScript",
				"Django"
			]
			"availabilities": [
				{
					"pk": 2,
					"mentor": 6,
					"start_time": "2023-04-12T05:30:00Z",
					"end_time": "2023-04-12T15:30:00Z"
				},
			]
		}
	}
]

```

---

## Create Mentors Information (User Authentication **Required**)

- Create information about the current logged-in mentor.

```http
POST - https://team-production-system.onrender.com/mentorinfo/
```

| Body       | Type     | Description                |
| :--------- | :------- | :------------------------- |
| `about_me` | `string` | Information about the user |
| `skills`   | `string` | Skills the user has        |

#### Request Sample:

```
POST /mentorinfo/
Content-Type: json
Authorization: Required
Host: https://team-production-system.onrender.com

{
	"about_me": "Hi, I am so and so and do such and such",
	"skills": "CSS"
}

```

#### Response Example (201 Created)

```
{
	"about_me": "Hi, I am so and so and do such and such",
	"skills": "CSS"
}

```

---

## View Mentors Information (User Authentication **Required**)

- Retrieve information about the current logged-in mentor.

```http
GET - https://team-production-system.onrender.com/mentorinfo/
```

| Body       | Type     | Description                |
| :--------- | :------- | :------------------------- |
| `about_me` | `string` | Information about the user |
| `skills`   | `string` | Skills the user has        |

**Nested Information:**

| Body             | Type    | Description                   |
| :--------------- | :------ | :---------------------------- |
| `availabilities` | `array` | Availabilities the mentor has |

#### Request Sample:

```
GET /mentorinfo/
Content-Type: json
Authorization: Required
Host: https://team-production-system.onrender.com

{
	""
}

```

#### Response Example (200 OK)

```
{
	"about_me": "Hi, I am so and so and do such and such",
	"skills": "CSS"
	"availabilities": [
			{
				"pk": 1,
				"mentor": 2,
				"start_time": "2023-04-12T14:30:00Z",
				"end_time": "2023-04-12T15:30:00Z"
			}
		]

}

```

---

## Update Mentors Information (User Authentication **Required**)

- Update information about the current logged-in mentor.

```http
PATCH - https://team-production-system.onrender.com/mentorinfoupdate/
```

| Body       | Type     | Description                |
| :--------- | :------- | :------------------------- |
| `about_me` | `string` | Information about the user |
| `skills`   | `string` | Skills the user has        |

#### Request Sample:

```
PATCH /mentorinfoupdate/
Content-Type: json
Authorization: Required
Host: https://team-production-system.onrender.com

{
	"skills": "Python"
}

```

#### Response Example (200 OK)

```
{
	"about_me": "Hi, I am so and so and do such and such",
	"skills": "Python"
}

```

---

## Delete Mentors Information (User Authentication **Required**)

- Delete information about the current logged-in mentor.

```http
DELETE - https://team-production-system.onrender.com/mentorinfoupdate/
```

| Body       | Type     | Description                |
| :--------- | :------- | :------------------------- |
| `about_me` | `string` | Information about the user |
| `skills`   | `string` | Skills the user has        |

#### Request Sample:

```
DELETE /mentorinfoupdate/
Content-Type: json
Authorization: Required
Host: https://team-production-system.onrender.com

{
	""
}

```

#### Response Example (204 No Content)

```

No body returned to response

```

---

## View a List of mentors by skill (User Authentication **Required**)

- View a list of mentors filtered by their skill.

```http
GET - https://team-production-system.onrender.com/mentor/<str:skills>/
```

| Body       | Type     | Description                |
| :--------- | :------- | :------------------------- |
| `about_me` | `string` | Information about the user |
| `skills`   | `string` | Skills the user has        |

#### Request Sample:

```
GET mentor/<str:skills>/
Content-Type: json
Authorization: Required
Host: https://team-production-system.onrender.com

{
	""
}

```

#### Response Example (200 Ok)

```
[
	{
		"pk": 2,
		"about_me": "Hi i'm testuser, I like to code.",
		"skills": [
			"HTML",
		]
	},
	{
		"pk": 5,
		"about_me": "Coding is so fun",
		"skills": [
			"HTML",
			"CSS",
			"Django"
		]
	},
	{
		"pk": 6,
		"about_me": "Hi, I'm testuser",
		"skills": "HTML"
	}
]

```

---

## View Mentee List (User Authentication **Required**)

- View a list of all user with the mentee flag set to true

```http
GET - https://team-production-system.onrender.com/mentee/
```

| Body            | Type        | Description                  |
| :-------------- | :---------- | :--------------------------- |
| `pk`            | `int`       | The user pk                  |
| `username`      | `string`    | Username                     |
| `first_name`    | `string`    | User generated first name    |
| `last_name`     | `string`    | User generated last name     |
| `is_mentee`     | `boolean`   | Is mentee flag               |
| `profile_photo` | `form-data` | User submitted profile photo |

Nested Information:

| Body          | Type  | Description                          |
| :------------ | :---- | :----------------------------------- |
| `team_number` | `int` | Team number associated with the user |

#### Request Sample:

```
GET /mentee/
Content-Type: json
Authorization: Required
Host: https://team-production-system.onrender.com

{
	""
}

```

#### Response Example (200 OK)

```
[
	{
		"pk": 4,
		"username": "testusername",
		"first_name": "Test",
		"last_name": "User",
		"is_mentee": true,
		"mentee_profile": {
			"team_number": 4
		}
	}
]

```

---

## Create Mentees Information (User Authentication **Required**)

- Create information about the current logged-in mentee.

```http
POST - https://team-production-system.onrender.com/menteeinfo/
```

| Body          | Type  | Description                          |
| :------------ | :---- | :----------------------------------- |
| `team_number` | `int` | Team number associated with the user |

#### Request Sample:

```
POST /menteeinfo/
Content-Type: json
Authorization: Required
Host: https://team-production-system.onrender.com

{
	"team_number": "4"
}

```

#### Response Example (201 Created)

```
[
	{
		"team_number": 4
	}
]

```

---

## View Mentees Information (User Authentication **Required**)

- Retrieve information about the current logged-in mentee.

```http
GET - https://team-production-system.onrender.com/menteeinfo/
```

| Body          | Type  | Description                          |
| :------------ | :---- | :----------------------------------- |
| `team_number` | `int` | Team number associated with the user |

#### Request Sample:

```
GET /menteeinfo/
Content-Type: json
Authorization: Required
Host: https://team-production-system.onrender.com

{
	""
}

```

#### Response Example (200 OK)

```
[
	{
		"team_number": 4
	}
]

```

---

## Update Mentees Information (User Authentication **Required**)

- Update information about the current logged-in mentee.

```http
PATCH - https://team-production-system.onrender.com/menteeinfoupdate/
```

| Body          | Type  | Description                          |
| :------------ | :---- | :----------------------------------- |
| `team_number` | `int` | Team number associated with the user |

#### Request Sample:

```
PATCH /menteeinfoupdate/
Content-Type: json
Authorization: Required
Host: https://team-production-system.onrender.com

[
	{
		"team_number": "5"
	}
]

```

#### Response Example (200 OK)

```
{
	"team_number": 5
}

```

---

## Delete Mentees Information (User Authentication **Required**)

- Delete information about the current logged-in mentee.

```http
DELETE - https://team-production-system.onrender.com/menteeinfoupdate/
```

| Body          | Type  | Description                          |
| :------------ | :---- | :----------------------------------- |
| `team_number` | `int` | Team number associated with the user |

#### Request Sample:

```
DELETE /menteeinfoupdate/
Content-Type: json
Authorization: Required
Host: https://team-production-system.onrender.com

{
	""
}

```

#### Response Example (204 No Content)

```

No body returned to response

```

---

## Mentors Availabilty (User Authentication **Required**)

- Get mentor availabilty
- This endpoint filters out any expired availabilty. Only shows availabilty that is in the future.

```http
GET - https://team-production-system.onrender.com/availabilty/
```

| Body         | Type        | Description                                      |
| :----------- | :---------- | :----------------------------------------------- |
| `pk`         | `int`       | The pk of the availabilty                        |
| `mentor`     | `int`       | The pk of the mentor attached to the availabilty |
| `start_time` | `date-time` | Start time of the availabilty                    |
| `end_time`   | `date-time` | Start time of the availabilty                    |

#### Request Sample:

```
GET /availabilty/
Content-Type: json
Authorization: Required
Host: https://team-production-system.onrender.com

{
	""
}

```

#### Response Example (200 OK)

```
[
	{
		"pk": 19,
		"mentor": 4,
		"start_time": "1999-12-31T14:30:00Z",
		"end_time": "1999-12-31T15:30:00Z"
	},
	{
		"pk": 20,
		"mentor": 5,
		"start_time": "1999-12-31T14:30:00Z",
		"end_time": "1999-12-31T15:30:00Z"
	},
	{
		"pk": 21,
		"mentor": 4,
		"start_time": "1999-12-31T14:30:00Z",
		"end_time": "1999-12-31T15:30:00Z"
	},
	{
		"pk": 22,
		"mentor": 7,
		"start_time": "1999-12-31T14:30:00Z",
		"end_time": "1999-12-31T15:30:00Z"
	}
]
```

---

## Add Mentor Availabilty (User Authentication **Required**)

- Add mentor availabilty (This endpoint filters out any expired availabilty. Only shows availabilty that is in the future.)

```http
POST - https://team-production-system.onrender.com/availabilty/
```

| Body         | Type        | Description                                      |
| :----------- | :---------- | :----------------------------------------------- |
| `pk`         | `int`       | The pk of the availabilty                        |
| `mentor`     | `int`       | The pk of the mentor attached to the availabilty |
| `start_time` | `date-time` | Start time of the availabilty                    |
| `end_time`   | `date-time` | Start time of the availabilty                    |

#### Request Sample:

```
POST /availabilty/
Content-Type: json
Authorization: Required
Host: https://team-production-system.onrender.com

{
	"start_time": "1999-12-31T14:30:00Z",
	"end_time": "1999-12-31T15:30:00Z"
}

```

#### Response Example (201 Created)

```
{
	"pk": 23,
	"mentor": 4,
	"start_time": "1999-12-31T14:30:00Z",
	"end_time": "1999-12-31T14:30:00Z"
}
```

---

## Delete Mentor Availabilty (User Authentication **Required**)

- Delete a mentor availabilty

```
DELETE - https://team-production-system.onrender.com/availabilty/<int:pk>/
```

| Body | Type  | Description               |
| :--- | :---- | :------------------------ |
| `pk` | `int` | The pk of the availabilty |

#### Request Sample:

```
DELETE /availabilty/<int:pk>/
Content-Type: json
Authorization: Required
Host: https://team-production-system.onrender.com

{
	""
}

```

#### Response Example (204 No Content)

```
No body returned to response
```

---

````http

## Sessions (User Authentication **Required**)

- Get a list of all sessions

```http
GET - https://team-production-system.onrender.com/session/
````

| Body                 | Type        | Description                                      |
| :------------------- | :---------- | :----------------------------------------------- |
| `pk`                 | `int`       | The pk of the session                            |
| `mentor_firstname`   | `string`    | The first name of the mentor attached to session |
| `mentor_lastname`    | `string`    | The last name of the mentor attached to session  |
| `mentor_avaliabilty` | `int`       | The avalibility pk attached to mentor            |
| `mentor`             | `int`       | The pk of the mentor attached to the availabilty |
| `mentee`             | `int`       | The pk of the mentee attached to the session     |
| `start_time`         | `date-time` | Start time of the availabilty                    |
| `end_time`           | `date-time` | Start time of the availabilty                    |
| `status`             | `string`    | Status of the session                            |
| `session_length`     | `int`       | Length of the session                            |

#### Request Sample:

```
GET /session/
Content-Type: json
Authorization: Required
Host: https://team-production-system.onrender.com

{
	""
}

```

#### Response Example (200 OK)

```
[
	{
		"pk": 5,
		"mentor_first_name": "Test User",
		"mentor_last_name": "Test User",
		"mentor_availability": 2,
		"mentee": 3,
		"start_time": "2023-04-12T15:30:00Z",
		"end_time": "2023-04-12T16:00:00Z",
		"status": "Pending",
		"session_length": 60
	},
	{
		"pk": 2,
		"mentor_first_name": "Test User",
		"mentor_last_name": "Test User",
		"mentor_availability": 2,
		"mentee": 3,
		"start_time": "2023-04-12T15:30:00Z",
		"end_time": "2023-04-12T16:00:00Z",
		"status": "Confirmed",
		"session_length": 30
	},
	{
		"pk": 6,
		"mentor_first_name": "Test User",
		"mentor_last_name": "Test User",
		"mentor_availability": 2,
		"mentee": 3,
		"start_time": "2023-04-12T15:30:00Z",
		"end_time": "2023-04-12T16:00:00Z",
		"status": "Confirmed",
		"session_length": 30
	},
	{
		"pk": 7,
		"mentor_first_name": "Test User",
		"mentor_last_name": "Test User",
		"mentor_availability": 2,
		"mentee": 3,
		"start_time": "2023-04-12T15:30:00Z",
		"end_time": "2023-04-12T16:00:00Z",
		"status": "Canceled",
		"session_length": 30
	}
]
```

---

## Archived Sessions (User Authentication **Required**)

- Get a list of all archived sessions (start time earlier than 24 hrs before time of request)

```http
GET - https://team-production-system.onrender.com/archivesession/
```

| Body                 | Type        | Description                                      |
| :------------------- | :---------- | :----------------------------------------------- |
| `pk`                 | `int`       | The pk of the session                            |
| `mentor_firstname`   | `string`    | The first name of the mentor attached to session |
| `mentor_lastname`    | `string`    | The last name of the mentor attached to session  |
| `mentor_avaliabilty` | `int`       | The avalibility pk attached to mentor            |
| `mentor`             | `int`       | The pk of the mentor attached to the availabilty |
| `mentee`             | `int`       | The pk of the mentee attached to the session     |
| `start_time`         | `date-time` | Start time of the availabilty                    |
| `end_time`           | `date-time` | Start time of the availabilty                    |
| `status`             | `string`    | Status of the session                            |
| `session_length`     | `int`       | Length of the session                            |

#### Request Sample:

```
GET /archivesession/
Content-Type: json
Authorization: Required
Host: https://team-production-system.onrender.com

{
	""
}

```

#### Response Example (200 OK)

```
[
	{
		"pk": 1,
		"mentor_first_name": "Test-mentor",
		"mentor_last_name": "Test-mentor",
		"mentor_availability": 1,
		"mentee": 3,
		"mentee_first_name": "Test-mentee",
		"mentee_last_name": "Test-mentee",
		"start_time": "2023-05-22T12:00:00Z",
		"end_time": "2023-05-22T12:30:00Z",
		"status": "Confirmed",
		"session_length": 30
	}
]

```

---

## Create a Session (User Authentication **Required**)

- Create a session with a mentor

```http
POST - https://team-production-system.onrender.com/sessionrequest/
```

| Body                 | Type        | Description                                      |
| :------------------- | :---------- | :----------------------------------------------- |
| `pk`                 | `int`       | The pk of the session                            |
| `mentor_firstname`   | `string`    | The first name of the mentor attached to session |
| `mentor_lastname`    | `string`    | The last name of the mentor attached to session  |
| `mentor_avaliabilty` | `int`       | The avalibility pk attached to mentor            |
| `mentor`             | `int`       | The pk of the mentor attached to the availabilty |
| `mentee`             | `int`       | The pk of the mentee attached to the session     |
| `start_time`         | `date-time` | Start time of the availabilty                    |
| `end_time`           | `date-time` | Start time of the availabilty                    |
| `status`             | `string`    | Status of the session                            |
| `session_length`     | `int`       | Length of the session                            |

#### Request Sample:

```
POST /sessionrequest/
Content-Type: json
Authorization: Required
Host: https://team-production-system.onrender.com

{
	"mentor_availability": 8,
	"start_time": "2020-06-23T21:30:00.000Z",
	"session_length": 60
}

```

#### Response Example (201 Created)

```
{
	"pk": 8,
	"mentor_first_name": "testuser",
	"mentor_last_name": "testuser",
	"mentor_availability": 8,
	"mentee": 3,
	"mentee_first_name": "Test",
	"mentee_last_name": "Mentee",
	"start_time": "2020-04-26T21:00:00Z",
	"end_time": "2020-04-26T22:00:00Z",
	"status": "Pending",
	"session_length": 60
}

```

---

## Update a Session (User Authentication **Required**)

- Update a session status

```http
PATCH - https://team-production-system.onrender.com/sessionrequest/<int:pk>
```

| Body                 | Type        | Description                                      |
| :------------------- | :---------- | :----------------------------------------------- |
| `pk`                 | `int`       | The pk of the session                            |
| `mentor_firstname`   | `string`    | The first name of the mentor attached to session |
| `mentor_lastname`    | `string`    | The last name of the mentor attached to session  |
| `mentor_avaliabilty` | `int`       | The avalibility pk attached to mentor            |
| `mentor`             | `int`       | The pk of the mentor attached to the availabilty |
| `mentee`             | `int`       | The pk of the mentee attached to the session     |
| `start_time`         | `date-time` | Start time of the availabilty                    |
| `end_time`           | `date-time` | Start time of the availabilty                    |
| `status`             | `string`    | Status of the session                            |
| `session_length`     | `int`       | Length of the session                            |

#### Request Sample:

```
PATCH /sessionrequest/<int:pk>
Content-Type: json
Authorization: Required
Host: https://team-production-system.onrender.com

{
	"status": "Confirmed"
}

```

#### Response Example (201 Created)

```
{
	"pk": 8,
	"mentor_first_name": "testuser",
	"mentor_last_name": "testuser",
	"mentor_availability": 8,
	"mentee": 3,
	"start_time": "2020-04-26T21:00:00Z",
	"end_time": "2020-04-26T22:00:00Z",
	"status": "Confirmed",
	"session_length": 60
}

```

---

## Update Notification Settings (User Authentication **Required**)

- Update user's notification settings

```http
PATCH - https://team-production-system.onrender.com/notificationsettings/<int:pk>
```

| Body                   | Type      | Description                            |
| :--------------------- | :-------- | :------------------------------------- |
| `pk`                   | `int`     | The pk of the notification             |
| `session_requested`    | `boolean` | Session requested notification flag    |
| `session_confirmed`    | `boolean` | Session confirmation notification flag |
| `session_canceled`     | `boolean` | Session cancellation notification flag |
| `fifteen_minute_alert` | `boolean` | 15-minute alert notification flag      |
| `sixty_minute_alert`   | `int`     | 60-minute alert notification flag      |

#### Request Sample:

```
PATCH /notificationsettings/<int:pk>
Content-Type: json
Authorization: Required
Host: https://team-production-system.onrender.com

{
	"sixty_minute_alert": "True"
}

```

#### Response Example (200 OK)

```
{
	"pk": 4,
	"user": 3,
	"session_requested": false,
	"session_confirmed": false,
	"session_canceled": true,
	"fifteen_minute_alert": false,
	"sixty_minute_alert": true
}

```

---
