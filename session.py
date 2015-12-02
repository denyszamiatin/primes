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
    def _validate_name(name):
        if len(name) < Session.USERNAME_LENGTH or '.' in name:
            raise PrimesError(_('Invalid name'))
        try:
            Session.data_source.get_user_credentials(name)
        except (FileNotFoundError, ValueError):
            return
        raise PrimesError(_('Existing name'))

    @staticmethod
    def _validate_password(password):
        if not password:
            raise PrimesError(_('Empty password'))

    @staticmethod
    def _validate_receiver(receiver):
        if len(receiver) < Session.USERNAME_LENGTH:
            raise PrimesError('Invalid receiver')

    @staticmethod
    def _validate_message(message):
        if not 0 < len(message) <= Session.MESSAGE_LENGTH:
            raise PrimesError(_('Invalid message'))

    @staticmethod
    def register(name, password):
        Session._validate_name(name) and Session._validate_password(password)
        Session.data_source.add_user(name, Session.encrypt(password))

    def __init__(self, name, password):
        try:
            username, encrypted_password = \
                self.data_source.get_user_credentials(name)
        except ValueError:
            raise PrimesError(_('Invalid username'))
        except FileNotFoundError:
            raise PrimesError(_('User file access error'))
        if encrypted_password != Session.encrypt(password):
            raise PrimesError(_('Invalid password'))
        self.name = name

    def __str__(self):
        return self.name

    def send_message(self, receiver, message):
        Session._validate_receiver(receiver)
        Session._validate_message(message)
        self.data_source.add_message(self.name, receiver, message)
