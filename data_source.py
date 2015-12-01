# coding=utf-8
import os
import fcntl


class FileSource:
    DATABASE_DIR = 'data'
    USER_FILENAME = 'users.txt'
    USER_PASSWORD_SEPARATOR = ':'

    def __init__(self):
        if not os.path.isdir(self.DATABASE_DIR):
            os.makedirs(self.DATABASE_DIR)
        os.chdir(self.DATABASE_DIR)

    def get_user_credentials(self, name):
        try:
            with open(self.USER_FILENAME, 'r') as user_file:
                for line in user_file:
                    username, password = line[:-1].split(
                        self.USER_PASSWORD_SEPARATOR
                    )
                    if username == name:
                        return username, password
                raise ValueError
        except (FileNotFoundError, ValueError):
            raise

    def add_user(self, name, password):
        self._append_to_file(
            self.USER_FILENAME,
            self.USER_PASSWORD_SEPARATOR.join(
                [name, password]
            )
        )

    def _append_to_file(self, filename, message):
        with open(filename, 'a') as file_for_append:
            fcntl.flock(file_for_append, fcntl.LOCK_EX)
            file_for_append.write(message + '\n')
