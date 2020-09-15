import json
import os
import random
from os.path import dirname, join
from urllib.parse import urljoin

import requests
from dotenv import load_dotenv
from faker import Faker

dotenv_path = join(dirname(__file__), "bot.env")

load_dotenv(dotenv_path)


class Bot(object):
    urls = {
        "create": "auth/users/",
        "login": "auth/jwt/create/",
        "posts": "api/posts/create/",
        "like": "api/posts/like/{0}/",
    }

    def __init__(self):
        self.fake = Faker()
        self.url = "http://127.0.0.1:8000/"
        self.max_number_of_users = int(os.environ.get("MAX_NUMBER_OF_USERS"))
        self.max_posts_per_user = int(os.getenv("MAX_NUMBER_OF_USERS"))
        self.max_likes_per_user = int(os.getenv("MAX_NUMBER_OF_USERS"))
        self.users = []
        self.posts_to_like = []

    def __enter__(self):
        return self

    def run(self):
        for x in range(random.randint(1, self.max_number_of_users)):
            self.create_user()
        self.like_posts()

    def create_user(self):
        # initialize user
        user = self.fake.profile(fields=("username",))
        user["password"] = self.fake.password()

        # register and login
        self.__post(urljoin(self.url, self.urls.get("create")), data=user)

        login_response = self.__post(
            urljoin(self.url, self.urls.get("login")), data=user
        )

        user["token"] = login_response.json().get("access")

        self.users.append(user)
        self.create_posts(user)
        return user

    def create_posts(self, user):
        posts_url = urljoin(self.url, self.urls.get("posts"))
        for x in range(random.randint(1, self.max_posts_per_user)):
            response = self.__post(posts_url, self.__create_post(), user.get("token"))
            self.posts_to_like.append(response.json().get("id"))

    def like_posts(self):
        for user in self.users:
            for post_id in random.choices(
                self.posts_to_like, k=self.max_likes_per_user
            ):
                self.__post(
                    urljoin(self.url, self.urls.get("like").format(post_id)),
                    {},
                    user.get("token"),
                )

    def __post(self, url, data, token=None):
        headers = None
        if token:
            headers = {"Authorization": f"Token {token}"}
        return requests.post(url=url, json=data, headers=headers)

    def __create_post(self):
        return {
            "title": " ".join(self.fake.words()).capitalize(),
            "body": " ".join(self.fake.text(max_nb_chars=2000)),
        }

    def __exit__(self, exc_type, exc_value, traceback):
        """Save users to json on exit"""
        with open("users.json", "w+") as f:
            f.write(json.dumps(self.users, indent=2))


if __name__ == "__main__":
    with Bot() as bot:
        bot.run()
        print("Finished.")
