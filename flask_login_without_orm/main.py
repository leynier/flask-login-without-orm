from json import load
from os import getenv
from typing import Dict, Optional

from flask import Flask, redirect, url_for
from flask_login import (
    LoginManager,
    UserMixin,
    current_user,
    login_required,
    login_user,
    logout_user,
)

app = Flask(__name__)
app.config["SECRET_KEY"] = getenv("SECRET_KEY", default="secret_key_example")

login_manager = LoginManager(app)

users: Dict[str, "User"] = {}


class User(UserMixin):
    def __init__(self, id: str, username: str, email: str, password: str):
        self.id = id
        self.username = username
        self.email = email
        self.password = password

    @staticmethod
    def get(user_id) -> Optional["User"]:
        return users.get(user_id)

    def __str__(self) -> str:
        return f"<Id: {self.id}, Username: {self.username}, Email: {self.email}>"

    def __repr__(self) -> str:
        return self.__str__()


with open("users.json") as file:
    data = load(file)
    for key in data:
        users[key] = User(
            id=key,
            username=data[key]["username"],
            email=data[key]["email"],
            password=data[key]["password"],
        )


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route("/")
def index():
    username = current_user.username if current_user.is_authenticated else "anonymous"
    return f"""
        <h1>Hi {username}</h1>
        <h3>Welcome to Flask Login without ORM!</h3>
    """


@app.route("/login/<id>/<password>")
def login(id, password):
    user = User.get(id)
    print(user)
    if user and user.password == password:
        login_user(user)
        return redirect(url_for("index"))
    return "<h1>Invalid user id or password</h1>"


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/settings")
@login_required
def settings():
    return "<h1>Route protected</h1>"
