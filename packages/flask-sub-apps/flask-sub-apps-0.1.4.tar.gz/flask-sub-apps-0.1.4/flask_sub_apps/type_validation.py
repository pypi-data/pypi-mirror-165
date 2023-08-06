from abc import ABC

from flask_sub_apps import config


def is_abstract_class(obj):
    """Check if it's abstract class by looking for ABC is in the object's __bases__ attribute."""
    try:
        return ABC in obj.__bases__
    except AttributeError:
        return False


def is_valid_model(obj):
    """Check if the object is a valid SQLAlchemy model class."""
    return isinstance(obj, config.DBModel)


def is_valid_command(obj):
    """
    Check if the object is a valid Flask command class.
    Click commands are also accepted.
    """
    return isinstance(obj, config.AppCommand)


def is_valid_router(obj):
    """Check if the object is a valid APIFlask blueprint class."""
    try:
        return isinstance(obj, config.Router)
    except TypeError:
        return False
