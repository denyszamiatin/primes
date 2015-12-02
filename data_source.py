# coding=utf-8
import os
import fcntl
import datetime


class FileSource:
    TIME_FORMAT = "%d.%m.%Y %H:%M"
    DATABASE_DIR = 'data'
    USER_FILENAME = 'users.txt'
    SEPARATOR = '|'

    if not os.path.isdir(DATABASE_DIR):
        os.makedirs(DATABASE_DIR)
    os.chdir(DATABASE_DIR)

    @staticmethod
    def get_user_credentials(name):
        for username, password in FileSource._reader(
                FileSource.USER_FILENAME):
            if username == name:
                return username, password
        raise ValueError

    @staticmethod
    def add_user(name, password):
        FileSource._append_to_file(FileSource.USER_FILENAME, name, password)

    @staticmethod
    def _reader(filename):
        with open(filename, 'r') as file_for_read:
            fcntl.flock(file_for_read, fcntl.LOCK_SH)
            for line in file_for_read:
                yield line[:-1].split(FileSource.SEPARATOR)

    @staticmethod
    def _append_to_file(filename, *args):
        with open(filename, 'a') as file_for_append:
            fcntl.flock(file_for_append, fcntl.LOCK_EX)
            file_for_append.write(FileSource.SEPARATOR.join(args) + '\n')

    def __init__(self, username):
        self.username = username

    @staticmethod
    def add_message(sender, receiver, message):
        FileSource._append_to_file(
            receiver,
            sender,
            datetime.datetime.now().strftime(FileSource.TIME_FORMAT),
            message
        )

    @staticmethod
    def get_unread_messages(receiver):
        unread_messages = []
        try:
            for message in FileSource._reader(receiver):
                if not message[0]:
                    unread_messages = []
                else:
                    unread_messages.append(message)
            if unread_messages:
                FileSource._append_to_file(receiver, '')
        finally:
            return unread_messages
