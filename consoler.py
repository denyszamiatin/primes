# coding=utf-8
from gettext import gettext as _
import getpass
import threading

from session import PrimesError, Session


def ask_username(prompt):
    username = input(prompt)
    return username if username else getpass.getuser()


def ask_password():
    return getpass.getpass(_("Password"))


def ask_message():
    return input(_("Message? "))


def start_session():
    while True:
        username = ask_username(
            _("Username ({} is default)".format(getpass.getuser()))
        )
        password = ask_password()
        try:
            return Session(username, password)
        except PrimesError as error:
            print(error)


def ask_send_message(session):
    receiver = ask_username(_('Receiver? '))
    message = ask_message()
    try:
        session.send_message(receiver, message)
    except PrimesError as error:
        print(error)


def print_messages(session):
    messages = session.read_messages()
    if messages:
        print_formatted_messages(messages)
    else:
        print(_('There are no unread messages'))


def print_formatted_messages(messages):
    for sender, time, message in messages:
        print(_('From {} at {}: {}').format(sender, time, message))


def default(*args):
    print(_("Invalid action"))

session = start_session()

actions = {
    's': ask_send_message,
}

print_messages(session)
while True:
    action = input(_("{}> ".format(session)))
    if action and action in "Qq":
        break
    actions.get(action, default)(session)
