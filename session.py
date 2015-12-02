# coding=utf-8
import hashlib
import fcntl
import os
from gettext import gettext as _

from data_source import FileSource


class PrimesError(Exception):
    pass


class Session:
    USERNAME_LENGTH = 3
    MESSAGE_LENGTH = 200
    data_source = FileSource()

    @staticmethod
    def encrypt(password):
        return hashlib.sha1(bytes(password, 'utf8')).hexdigest()

    @staticmethod
    def _validate_username_len(username):
        if len(username) < Session.USERNAME_LENGTH:
            raise PrimesError(_('Invalid name'))

    @staticmethod
    def _validate_username(username):
        Session._validate_username_len(username)
        if '.' in username:
            raise PrimesError(_('Invalid name'))

    @staticmethod
    def _validate_password(password):
        if not password:
            raise PrimesError(_('Empty password'))

    @staticmethod
    def _validate_message(message):
        if not 0 < len(message) <= Session.MESSAGE_LENGTH:
            raise PrimesError(_('Invalid message'))

    @staticmethod
    def register(name, password):
        Session.data_source.add_user(name, Session.encrypt(password))

    def __init__(self, username, password):
        try:
            self._validate_username(username)
            self._validate_password(password)
            username, encrypted_password = \
                self.data_source.get_user_credentials(username)
        except (FileNotFoundError, ValueError):
            self.register(username, password)
        except PrimesError:
            raise
        else:
            if encrypted_password != Session.encrypt(password):
                raise PrimesError(_('Invalid password'))
        self.username = username

    def __str__(self):
        return self.username

    def send_message(self, receiver, message):
        Session._validate_username_len(receiver)
        Session._validate_message(message)
        self.data_source.add_message(self.username, receiver, message)
