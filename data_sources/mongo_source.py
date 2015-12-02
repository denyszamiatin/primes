# coding=utf-8
import datetime
import pymongo

from .abstract_source import AbstractSource


class MongoSource(AbstractSource):
    db = pymongo.MongoClient().primes

    def is_new_messages(self):
        return self._get_unread_messages().count()

    def _get_unread_messages(self):
        return self.db.messages.find({
                'receiver': self.username,
                'time': {'$gte': self._get_user(self.username)['last_read']}
        })

    @staticmethod
    def add_user(name, password):
        MongoSource.db.users.insert_one({
            'name': name,
            'password': password,
            'last_read': datetime.datetime(1000, 1, 1)
        })

    @staticmethod
    def get_user_credentials(name):
        user = MongoSource._get_user(name)
        if user:
            return user['name'], user['password']
        raise ValueError

    @staticmethod
    def _get_user(name):
        return MongoSource.db.users.find_one({'name': name})

    def add_message(self, receiver, message):
        self.db.messages.insert_one({
            'sender': self.username,
            'receiver': receiver,
            'message': message,
            'time': datetime.datetime.now()
        })

    def get_unread_messages(self):
        messages = [(
                message['sender'],
                message['time'].strftime(self.TIME_FORMAT),
                message['message']
        ) for message in self._get_unread_messages()]
        self.db.users.update_one(
            {'name': self.username},
            {'$set': {'last_read': datetime.datetime.now()}}
        )
        return messages
