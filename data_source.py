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
        self.file_size = self._get_user_file_size()

    def _get_user_file_size(self):
        return os.path.getsize(self.username)

    def add_message(self, receiver, message):
        self._append_to_file(
            receiver,
            self.username,
            datetime.datetime.now().strftime(FileSource.TIME_FORMAT),
            message
        )

    def get_unread_messages(self):
        unread_messages = []
        try:
            for message in self._reader(self.username):
                if not message[0]:
                    unread_messages = []
                else:
                    unread_messages.append(message)
            if unread_messages:
                self._append_to_file(self.username, '')
                self.file_size = self._get_user_file_size()
        finally:
            return unread_messages

    def is_new_messages(self):
        return self.file_size != self._get_user_file_size()
