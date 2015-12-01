# coding: utf-8
from gettext import gettext as _
import getpass

from file_source import PrimesError, User


def ask_username(prompt):
    username = input(prompt)
    return username if username else getpass.getuser()


def ask_password():
    return getpass.getpass(_("Password"))


def create_username_prompt(message=''):
    return _("Username ({} is default{})".format(getpass.getuser(), message))


def ask_register_user():
    while True:
        username = ask_username(create_username_prompt())
        password = ask_password()
        try:
            User.register(username, password)
            break
        except PrimesError as error:
            print(error)


def login_user():
    while True:
        username = ask_username(
            create_username_prompt(_("'.' for registration"))
        )
        if username == '.':
            ask_register_user()
            continue
        password = ask_password()
        try:
            user = User(username, password)
            break
        except PrimesError as error:
            print(error)
    return user


user = login_user()
while True:
    action = input(_("{}> ".format(user)))
    if action and action in "Qq":
        break
