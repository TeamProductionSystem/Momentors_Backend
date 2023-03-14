# Team Production System

Team Production System is an app for mentees to schedule one-on-one sessions with mentors.

## Contributing

Contributions are always welcome!

See [contributing.md](https://github.com/TeamProductionSystem/Team_Production_System_BE/blob/main/CONTRIBUTING.md) for ways to get started.

Please adhere to this project's [code of conduct](https://github.com/TeamProductionSystem/Team_Production_System_BE/blob/main/CODE_OF_CONDUCT.md).

## Features

- Users can setup profiles as a mentor or mentee.
- Mentors can set their skill set and avalibilty.
- Mentees can schedule sessions with the menots, filtered by skills and avalibilty
- Menotrs can confirm sessions
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

## Environment Variables

1. Create a file named .env in the root directory of your project. This file will contain your environment variables.
2. Open the .env file in a text editor and set your environment variables in the following format:
'VARIABLE_NAME=value'

	For example:
```DATABASE_URL=postgres://username:password@localhost/mydatabase
SECRET_KEY=my_secret_key
DEBUG=True
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_PASSWORD=admin_password
DJANGO_SUPERUSER_EMAIL=admin@example.com
```

- DATABASE_URL: This should be set to the URL of your database. Depending on your database type, this may include a username, password, host, and port.

- SECRET_KEY: This should be set to a secret key that is used for cryptographic signing in Django. It is important that this value is kept secret and is not shared publicly.

- DEBUG: This should be set to a boolean value (True or False) and is used to enable or disable debugging in Django. It is recommended to set this to False in production environments.

- DJANGO_SUPERUSER_USERNAME: This should be set to the username you want to use for the Django superuser account.

- DJANGO_SUPERUSER_PASSWORD: This should be set to the password you want to use for the Django superuser account.

- DJANGO_SUPERUSER_EMAIL: This should be set to the email address you want to use for the Django superuser account.


3. Save the .env file.

---

# API Reference

API https://team-production-system.onrender.com

## User Create

- Create a new user

```http
  POST https://team-production-system.onrender.com/auth/users/
```

| Body       | Type     | Description             |
| :--------- | :------- | :---------------------- |
| `username` | `string` | New Username            |
| `password` | `string` | User generated password |
| `email`    | `string` | User generated email    |

#### Request Sample:

```
POST /auth/users/
Content-Type: json
Authorization: N/A
Host: https://team-production-system.onrender.com
{
	"username": "TestUserLogin" ,
	"password": "TestUserPassword",
	"email": "testemail@fake.com"
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

| Body            | Type        | Description                 |
| :-------------- | :---------- | :-------------------------- |
| `username`      | `string`    | Username                    |
| `first_name`    | `string`    | User generated first name   |
| `last_name`     | `string`    | User generated last name    |
| `email`         | `string`    | User generated email        |
| `phone_number`  | `string`    | User generated phone number |
| `profile_photo` | `form-data` | User submitted phone number |
| `is_mentor`     | `boolean`   | Is mentor flag              |
| `is_mentee`     | `boolean`   | Is mentee flag              |
| `is_active`     | `boolean`   | Is active flag              |

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

```http
PATCH - https://team-production-system.onrender.com/myprofile/
```

| Body            | Type        | Description                 |
| :-------------- | :---------- | :-------------------------- |
| `username`      | `string`    | Username                    |
| `first_name`    | `string`    | User generated first name   |
| `last_name`     | `string`    | User generated last name    |
| `email`         | `string`    | User generated email        |
| `phone_number`  | `string`    | User generated phone number |
| `profile_photo` | `form-data` | User submitted phone number |
| `is_mentor`     | `boolean`   | Is mentor flag              |
| `is_mentee`     | `boolean`   | Is mentee flag              |
| `is_active`     | `boolean`   | Is active flag              |

#### Request Sample:

```
PATCH /myprofile/
Content-Type: json
Authorization: Required
Host: https://team-production-system.onrender.com

{
	"first_name": "testuserfirstname",
	"last_name": "testuserlastname",
	"phone_number": "+12345678987",
	"is_mentor": true,
	"is_active": true
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
	"profile_photo": null,
	"is_mentor": true,
	"is_mentee": false,
	"is_active": true
}

```

---

## View Mentors (User Authentication **Required**)

- View a list of all user with the mentors flag

```http
GET - https://team-production-system.onrender.com/mentor/
```

| Body            | Type        | Description                 |
| :-------------- | :---------- | :-------------------------- |
| `pk`            | `int`       | The user pk                 |
| `username`      | `string`    | Username                    |
| `first_name`    | `string`    | User generated first name   |
| `last_name`     | `string`    | User generated last name    |
| `is_mentor`     | `boolean`   | Is mentor flag              |
| `profile_photo` | `form-data` | User submitted phone number |

Nested Information:

| Body       | Type     | Description                |
| :--------- | :------- | :------------------------- |
| `about_me` | `string` | Information about the user |
| `skills`   | `string` | Skills the user has        |

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
		}
	}
]

```

---
