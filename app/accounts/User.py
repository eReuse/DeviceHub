from werkzeug.http import parse_authorization_header


__author__ = 'busta'


class ClassProperty(property):
    def __get__(self, cls, owner):
        return self.fget.__get__(None, owner)()

class User:
    _actual = None

    @ClassProperty
    @classmethod
    def actual(cls):
        if cls._actual is None:
            from flask import request
            try:
                x = request.headers.environ['HTTP_AUTHORIZATION']
                token = parse_authorization_header(x)['username']
            except KeyError:
                from app.exceptions import UserIsAnonymous
                raise UserIsAnonymous("You need to be logged in.")
            from app.app import app
            cls._actual = app.data.driver.db['accounts'].find_one({'token': token})
        return cls._actual
