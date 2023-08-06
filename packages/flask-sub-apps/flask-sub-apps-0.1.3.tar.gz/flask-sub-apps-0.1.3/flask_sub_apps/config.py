import os

from click import Command
from flask import Blueprint
from flask_sqlalchemy import DefaultMeta

env = os.environ

DBModel = DefaultMeta
Router = Blueprint
AppCommand = Command

# Specify name of the module the application should look for.
# String and array of strings are accepted.
# You can use a module path, relative to root of the sub-app.
# Example: "models", "sub_app.models" or ["sub_app.sqla_models", "sub_app.models.sqla_models"]
MODELS_FILE = env.get("FLASK_SUB_APPS_MODELS_FILE", ["models", "sqla_models"])
COMMANDS_FILE = env.get("FLASK_SUB_APPS_COMMANDS_FILE", ["commands", "flask_commands"])
ROUTERS_FILE = env.get(
    "FLASK_SUB_APPS_ROUTERS_FILE",
    ["routers", "views", "api_views", "urls", "blueprints"],
)
