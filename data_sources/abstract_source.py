from abc import abstractmethod, ABCMeta


class AbstractSource(metaclass=ABCMeta):
    TIME_FORMAT = "%d.%m.%Y %H:%M"

    def __init__(self, username):
        self.username = username

    @staticmethod
    @abstractmethod
    def get_user_credentials(name):
        pass

    @staticmethod
    @abstractmethod
    def add_user(name, password):
        pass

    @abstractmethod
    def add_message(self, receiver, message):
        pass

    @abstractmethod
    def get_unread_messages(self):
        pass

    @abstractmethod
    def is_new_messages(self):
        pass
