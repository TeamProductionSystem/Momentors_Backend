# Team Production System

Team Production System is an app for mentees to schedule one-on-one sessions with mentors. 

## Contributing

Contributions are always welcome!

See `contributing.md` for ways to get started.

Please adhere to this project's [code of conduct](https://github.com/TeamProductionSystem/Team_Production_System_BE/blob/main/CODE_OF_CONDUCT.md).


## Features

- Users can setup profiles as a mentor or mentee.
- Mentors can set their skill set and avalibilty.
- Mentees can schedule sessions with the menots, filtered by skills and avalibilty
- Menotrs can confirm sessions
- Both mentor and mentee can cancel a session prior to session start time. 


# API Reference

API https://team-production-system.onrender.com

## User Create

- Create a new user entry 

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
