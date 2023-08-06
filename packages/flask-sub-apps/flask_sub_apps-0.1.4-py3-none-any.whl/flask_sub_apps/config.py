import os

from click import Command
from flask import Blueprint
from flask_sqlalchemy import DefaultMeta

env = os.environ

DBModel = DefaultMeta
Router = Blueprint
AppCommand = Command
