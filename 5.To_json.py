# декоратор to_json, который можно применить к различным функциям,
# чтобы преобразовывать их возвращаемое значение в JSON-формат

import json
import functools


def to_json(filename):
    @functools.wraps(filename)
    def wrapped(*args, **kwargs):
        return json.dumps(filename(*args, **kwargs))
    return wrapped

@to_json
def get_data():
    return {
        'data': 42
    }

get_data() # вернёт '{"data": 42}'
