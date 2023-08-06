from typing import Optional, Type, Dict, List

from flask import Flask

from flask_sub_apps import helpers, config
from flask_sub_apps.loader import ModuleLoader, ValidateFunction
from flask_sub_apps.models import SubApp

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
        self._loader = ModuleLoader(is_valid_model, is_valid_command, is_valid_router)

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
            sub_app = self._loader.load_sub_app(module_name)

            self.sub_apps[sub_app.module_name] = sub_app
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
        return [view for sub_app in self.get_sub_apps() for view in sub_app.routers]

    def get_commands(self) -> List[config.Command]:
        """Get all registered commands."""
        return [
            command for sub_app in self.get_sub_apps() for command in sub_app.commands
        ]

    def get_models(self) -> List[Type[config.DBModel]]:
        """Get all registered models."""
        return [model for sub_app in self.get_sub_apps() for model in sub_app.models]

    def get_model(self, model_name: str) -> Optional[Type[config.DBModel]]:
        """
        Get model by its name.

        :param model_name: Name of the model to find.
        :return: Model class if exists, None otherwise.
        """
        return next(
            (model for model in self.get_models() if model.__name__ == model_name), None
        )
