# coding=utf-8
import os
import fcntl
import datetime


class FileSource:
    TIME_FORMAT = "%d.%m.%Y %H:%M"
    DATABASE_DIR = 'data'
    USER_FILENAME = 'users.txt'
    SEPARATOR = '|'

    def __init__(self):
        if not os.path.isdir(self.DATABASE_DIR):
            os.makedirs(self.DATABASE_DIR)
        os.chdir(self.DATABASE_DIR)

    def get_user_credentials(self, name):
        with open(self.USER_FILENAME, 'r') as user_file:
            fcntl.flock(user_file, fcntl.LOCK_SH)
            for line in user_file:
                username, password = line[:-1].split(
                    self.SEPARATOR
                )
                if username == name:
                    return username, password
            raise ValueError

    def add_user(self, name, password):
        self._append_to_file(
            self.USER_FILENAME,
            self.SEPARATOR.join(
                [name, password]
            )
        )

    def _append_to_file(self, filename, message):
        with open(filename, 'a') as file_for_append:
            fcntl.flock(file_for_append, fcntl.LOCK_EX)
            file_for_append.write(message + '\n')

    def add_message(self, sender, receiver, message):
        self._append_to_file(
            receiver,
            self.SEPARATOR.join([
                sender,
                datetime.datetime.now().strftime(self.TIME_FORMAT),
                message
            ])
        )
