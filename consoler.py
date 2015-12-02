# coding=utf-8
from gettext import gettext as _
import getpass
import threading
import time

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
    with console_lock:
        receiver = ask_username(_('Receiver? '))
        message = ask_message()
        try:
            session.send_message(receiver, message)
        except PrimesError as error:
            print(error)


def print_messages(session):
    for sender, time, message in session.read_messages():
        print(_('From {} at {}: {}').format(sender, time, message))


def check_new_messages(session):
    while True:
        if canceled:
            break
        if session.new_messages():
            with console_lock:
                print()
                print_messages(session)
        time.sleep(1)


def default(*args):
    print(_("Invalid action"))

session = start_session()
canceled = False
console_lock = threading.Lock()
message_checker = threading.Thread(target=check_new_messages, args=(session, ))
message_checker.daemon = True
message_checker.start()

actions = {
    's': ask_send_message,
}

print_messages(session)
while True:
    action = input(_("{}> ".format(session)))
    if action and action in "Qq":
        canceled = True
        break
    actions.get(action, default)(session)
