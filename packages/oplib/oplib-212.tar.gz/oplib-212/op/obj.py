# This file is placed in the Public Domain.
# pylint: disable=W0613


"big Object"


import datetime
import os
import uuid


def __dir__():
    return (
            'Object',
            'edit',
            'find',
            'get',
            'items',
            'keys',
            'register',
            'search',
            'update',
            'values'
           )


class Object:

    "big Object"

    __slots__ = (
        '__dict__',
        '__stp__'
    )

    @staticmethod
    def __new__(cls, *args, **kwargs):
        "create new object."
        obj = object.__new__(cls)
        otype = str(type(obj)).split()[-1][1:-2]
        obj.__stp__ = os.path.join(
                                 otype,
                                 str(uuid.uuid4()),
                                 os.sep.join(str(datetime.datetime.now()).split())
                                )
        return obj

    def __iter__(self):
        return iter(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __str__(self):
        return str(self. __dict__)


def delete(obj, key):
    "delete key from object."
    delattr(obj, key)


def edit(obj, setter):
    "edit object using a setter."
    for key, value in items(setter):
        register(obj, key, value)


def get(obj, key, default=None):
    "return value by key."
    try:
        return obj.__dict__.get(key, default)
    except AttributeError:
        return obj.get(key)


def items(obj):
    "return items (key/value)."
    try:
        return obj.__dict__.items()
    except AttributeError:
        return obj.items()


def keys(obj):
    "return keys."
    try:
        return obj.__dict__.keys()
    except (AttributeError, TypeError):
        return obj.keys()


def register(obj, key, value):
    "set a key/value."
    setattr(obj, key, value)


def update(obj, data):
    "update an object."
    try:
        obj.__dict__.update(vars(data))
    except TypeError:
        obj.__dict__.update(data)
    return obj


def values(obj):
    "return values."
    try:
        return obj.__dict__.values()
    except TypeError:
        return obj.values()
