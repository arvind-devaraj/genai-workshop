
from typing import Dict

class User:
    def __init__(self, username: str, password: str, age: int):
        self.username = username
        self.password = password
        self.age = age

def user_func(user: User) -> None:
    if user.username == "john" and user.password == "password" and user.age == 30:
        print("User authenticated")
    else:
        print("Authentication failed")

def user_func_nested(user: User) -> None:
    if user.username == "john" and user.password == "password" and user.age == 30:
        print("User authenticated")
    else:
        print("Authentication failed")
