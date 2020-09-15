## BASIC API DOCUMENTATION

### USAGE

- ##### Installation
```sh
$ pip install poetry
$ poetry install
$ poetry run python manage.py test
```

- ##### Usage
To run the server, use the following command:
```sh
$ poetry run python manage.py runserver
```
To run the bot, use the following command:
```sh
$ poetry run python bot.py
```
Edit `bot.env` to change bot configuration.


### ENDPOINTS

#### Authentication

- `/auth/users/` `POST`

Register a user with provided credentials.
Body:
```json
{
    "username": "username",
    "password: "password"
}
```
Response:
```json
{
    "id": "fafb3f06-5a7b-4fbe-9705-9cf3fba1fc79",
    "username": "user"
}

```
- `/auth/jwt/create/` `POST`

Log in using provided credentials.
Body:
```json
{
    "username": "username",
    "password: "password"
}
```
Response
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjAwNzI1NjQ0LCJqdGkiOiIzNmRhMjVmMjQ1ZTA0NDAzODUxZGNiOGFmMmNjMTU1NSIsInVzZXJfaWQiOiJlOWU5MjE4OC1kNDhkLTQ2MWItYjNlNS1kY2Q3Y2ZhNWYyNzgifQ._JWfsqQGFrlytKryq1PsH__iRA0nC_l-IPGgtqYA9P4",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYwMjcxMjg0NCwianRpIjoiNTIzNDhiYjhmMzlkNGVjZTgyZDk1OTljMmQ2MjQxMzEiLCJ1c2VyX2lkIjoiZTllOTIxODgtZDQ4ZC00NjFiLWIzZTUtZGNkN2NmYTVmMjc4In0.aWnHt2Qvn_1g5lsMhActkPwXXyR-ZyGGaXiS_HDFwSM"
}
```

#### User activity

- `/api/me/activity/` `GET`

Retrieve activity for currently authenticated user.
Response:
```json
{
    "last_login": "2020-09-15",
    "last_action": "2020-09-15T08:57:21.286757Z"
}
```

#### Posts and likes

- `/api/posts/create/` `POST`

Add a post.
Body:
```json
{
    "title": "Post Title",
    "body": "Post Body"
}
```
Response:
```json
{
    "id": 1,
    "likes": [],
    "title": "Post Title",
    "body": "Post Body",
    "created_at": "2020-09-15T08:52:02.905860Z",
    "created_by": "b7352c67-de31-4adc-aff7-3daf86d7d57c"
}
```

- `/api/like/<id>` `POST`

Either add or remove like on a post
Response (added like):
```json
{
    "id": 1,
    "likes": [
        {
            "created_at": "2020-09-15T08:57:21.249327Z",
            "created_by": "b7352c67-de31-4adc-aff7-3daf86d7d57c"
        }
    ],
    "title": "Post Title",
    "body": "Post Body",
    "created_at": "2020-09-15T00:46:50.425079Z",
    "created_by": "b7352c67-de31-4adc-aff7-3daf86d7d57c"
}
```

- `/api/posts/posts/?date_from=2020-09-15` `GET`

Filter post by `date_from` and `date_to` creation date.

- `/api/posts/likes/?date_from=2020-09-15` `GET`

Filter likes by `date_from` and `date_to` creation date.