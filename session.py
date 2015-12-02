# coding=utf-8
import hashlib
import datetime
from gettext import gettext as _

from data_source import FileSource


class PrimesError(Exception):
    pass


class Session:
    USERNAME_LENGTH = 3
    MESSAGE_LENGTH = 200

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
        FileSource.add_user(name, Session.encrypt(password))

    def _get_username(self, username, password):
        try:
            self._validate_username(username)
            self._validate_password(password)
            username, encrypted_password = \
                FileSource.get_user_credentials(username)
        except (FileNotFoundError, ValueError):
            self.register(username, password)
        except PrimesError:
            raise
        else:
            if encrypted_password != Session.encrypt(password):
                raise PrimesError(_('Invalid password'))
        return username

    def __init__(self, username, password):
        self.username = self._get_username(username, password)
        self.start_time = datetime.datetime.now()

    def __str__(self):
        return self.username

    def send_message(self, receiver, message):
        Session._validate_username_len(receiver)
        Session._validate_message(message)
        FileSource.add_message(self.username, receiver, message)

    def read_messages(self):
        return FileSource.get_unread_messages(self.username)
