from functools import wraps
from pathlib import Path
from os import path
from beam import load_config


def with_config(callback):
    @wraps(callback)
    def wrapper(*args, **kwargs):
        load_config()
        return callback(*args, **kwargs)

    return wrapper


def requires_credentials(callback, *outer_args, **outer_kwargs):
    def wrapper(*args, **kwargs):
        profile_name = outer_kwargs.get("profile", "default")
        return callback(*args, **kwargs)

    return wrapper
