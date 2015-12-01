# coding: utf-8
import hashlib
import fcntl
import os
from gettext import gettext as _


class PrimesError(Exception):
    pass

DATABASE_DIR = 'data'
if not os.path.isdir(DATABASE_DIR):
    os.makedirs(DATABASE_DIR)
os.chdir(DATABASE_DIR)


class Session:
    USERNAME_LENGTH = 3
    USER_FILENAME = 'users.txt'
    USER_PASSWORD_SEPARATOR = ':'

    @staticmethod
    def get_user_credentials(name):
        try:
            with open(Session.USER_FILENAME, 'r') as user_file:
                for line in user_file:
                    if line.split(Session.USER_PASSWORD_SEPARATOR)[0] == name:
                        return line[:-1]
        except FileNotFoundError:
            pass
        return False

    @staticmethod
    def encrypt(password):
        return hashlib.sha1(bytes(password, 'utf8')).hexdigest()

    @staticmethod
    def register(name, password):
        Session.validate_name(name) and Session.validate_password(password)
        with open(Session.USER_FILENAME, 'a') as user_file:
            fcntl.flock(user_file, fcntl.LOCK_EX)
            user_file.write(
                Session.USER_PASSWORD_SEPARATOR.join(
                    [name, Session.encrypt(password)]
                ) + '\n'
            )

    @staticmethod
    def validate_name(name):
        if len(name) < Session.USERNAME_LENGTH or '.' in name:
            raise PrimesError(_('Invalid name'))
        if Session.get_user_credentials(name):
            raise PrimesError(_('Existing name'))

    @staticmethod
    def validate_password(password):
        if not password:
            raise PrimesError(_('Empty password'))

    def __init__(self, name, password):
        user = Session.get_user_credentials(name)
        if not user:
            raise PrimesError(_('Invalid username'))
        name, encrypted_password = user.split(Session.USER_PASSWORD_SEPARATOR)
        if encrypted_password != Session.encrypt(password):
            raise PrimesError(_('Invalid password'))
        self.name = name

    def __str__(self):
        return self.name
