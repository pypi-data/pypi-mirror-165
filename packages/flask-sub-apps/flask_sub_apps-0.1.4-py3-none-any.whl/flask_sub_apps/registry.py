from typing import Optional, Type, Dict, List

from flask import Flask
from python_module_loader import PythonModuleLoader

import type_validation
from flask_sub_apps import helpers, config
from flask_sub_apps.models import SubApp, ValidateFunction

logger = helpers.get_logger()


class AppRegistry:
    """Registry of Flask sub-apps."""

    sub_apps: Dict[str, SubApp] = dict()

    def __init__(
        self,
        is_valid_model: ValidateFunction = None,
        is_valid_command: ValidateFunction = None,
        is_valid_router: ValidateFunction = None,
    ):
        self.is_valid_model = is_valid_model or type_validation.is_valid_model
        self.is_valid_command = is_valid_command or type_validation.is_valid_command
        self.is_valid_router = is_valid_router or type_validation.is_valid_router
        self._loader = PythonModuleLoader()

    def get_sub_apps(self) -> List[SubApp]:
        """
        Get all registered sub-apps.
        :return: List of registered sub-apps.
        """
        return list(self.sub_apps.values())

    def register(self, module_name: str, app: Flask) -> Optional[SubApp]:
        """
        Register module as a Flask sub-app.

        :param module_name: module name.
        :param app: Flask app.
        :return: Sub-app with modules or None if failed to register.
        """
        try:
            self._loader.load(module_name)
            sub_app = SubApp(
                name=module_name,
                models=list(self._loader.find_objects(self.is_valid_model)),
                commands=list(self._loader.find_objects(self.is_valid_command)),
                routers=list(self._loader.find_objects(self.is_valid_router)),
            )
            self.sub_apps[module_name] = sub_app
            self.register_routers(app)
            self.register_commands(app)
            return sub_app
        except ModuleNotFoundError as e:
            logger.error(f"Failed to register module {module_name!r}", e)

    def register_routers(self, app: Flask):
        """Register Flask routers of all registered modules."""
        for router in self.get_routers():
            if app.blueprints.get(router.name):
                logger.debug(f"Router {router.name} already registered.")
                continue

            app.register_blueprint(router)
            logger.debug(f"Registered {router.name!r} blueprint")

    def register_commands(self, app: Flask):
        """Register Flask commands of all registered modules."""
        for command in self.get_commands():
            if app.cli.commands.get(command.name):
                logger.debug(f"Command {command.name} already registered.")
                continue

            app.cli.add_command(command, name=command.name)
            logger.debug(f"Registered {command.name!r} command")

    def get_routers(self) -> List[config.Router]:
        """Get all registered routers."""
        return [router for router in self._loader.find_objects([self.is_valid_router])]

    def get_commands(self) -> List[config.Command]:
        """Get all registered commands."""
        return [
            command for command in self._loader.find_objects([self.is_valid_command])
        ]

    def get_models(self) -> List[Type[config.DBModel]]:
        """Get all registered models."""
        return [model for model in self._loader.find_objects([self.is_valid_model])]

    def get_model(self, model_name: str) -> Optional[Type[config.DBModel]]:
        """
        Get model by its name.

        :param model_name: Name of the model to find.
        :return: Model class if exists, None otherwise.
        """
        return next(
            (model for model in self.get_models() if model.__name__ == model_name), None
        )
