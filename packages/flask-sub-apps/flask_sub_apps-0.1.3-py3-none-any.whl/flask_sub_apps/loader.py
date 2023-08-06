import importlib
import inspect
from functools import partial
from types import ModuleType
from typing import Union, Any, Callable, List

from flask_sub_apps import helpers, config, type_validation
from flask_sub_apps.models import SubApp

ValidateFunction = Callable[[Any], bool]


class ModuleLoader:
    """Loader of Flask sub-apps."""

    def __init__(
        self,
        is_valid_model: ValidateFunction = None,
        is_valid_command: ValidateFunction = None,
        is_valid_router: ValidateFunction = None,
    ):
        """
        Initialize loader with validators for models, commands and routers.
        Those functions will be used to filter out invalid items when loading modules.

        :param is_valid_model: function returning if obj is valid model class.
        :param is_valid_command: function returning if obj is valid command object.
        :param is_valid_router: function returning if obj is valid router object.
        """

        self.is_valid_model = is_valid_model or type_validation.is_valid_model
        self.is_valid_command = is_valid_command or type_validation.is_valid_command
        self.is_valid_router = is_valid_router or type_validation.is_valid_router

    def load_sub_app(self, module_name: str) -> SubApp:
        """
        Find and load a Flask sub-app by its module name.
        Method will try to load sub-app items from user defined keys in config.

        :param module_name: name of the module. e.g. 'backend.users'
        :return: initialized sub-app
        """
        module = self._import_module(module_name)
        if not module:
            raise ModuleNotFoundError(f"Module {module_name} not found")

        get_submodule_items = partial(self._get_submodule_items, module)
        models = set(
            filter(
                self.is_valid_model,
                get_submodule_items(submodule_name=config.MODELS_FILE),
            )
        )
        commands = set(
            filter(
                self.is_valid_command,
                get_submodule_items(submodule_name=config.COMMANDS_FILE),
            )
        )
        routers = set(
            filter(
                self.is_valid_router,
                get_submodule_items(submodule_name=config.ROUTERS_FILE),
            )
        )
        app_module = SubApp(
            name=self._get_short_module_name(module_name),
            module=module,
            models=models,
            commands=commands,
            routers=routers,
        )
        return app_module

    def _get_submodule_items(
        self,
        module: ModuleType,
        submodule_name: Union[str, List[str]],
    ) -> List[Any]:
        """
        Get all items from submodule of specified name.

        :param module: module to get submodule from.
        :param submodule_name: name of submodule to get items from. Can be a list of names.
        :return: list of items from submodule.
        """

        # If submodule_name is a list, then we need to iterate over submodules
        # and get all items from each of them and merge them into a single list.
        if isinstance(submodule_name, list):
            return helpers.merge_lists(
                self._get_submodule_items(module, name) for name in submodule_name
            )

        # Because file might not be imported we need to assemble
        # the name of the submodule and try to import it.
        submodule_name = f"{module.__name__}.{submodule_name}"
        submodule = self._import_module(submodule_name)
        if not submodule:
            return []

        return self._get_members_of_module(submodule)

    @staticmethod
    def _get_short_module_name(module: ModuleType) -> str:
        """
        Get short version of name of a module.
        It is used to generate name of the sub-app.

        :param module: module to get short name of.
        :return: short name of the module.
        """
        return module.split(".")[-1]

    @staticmethod
    def _import_module(module_name: str) -> ModuleType:
        """
        Import module by its name.

        :param module_name: name of the module.
        :return: imported module.
        """
        try:
            return importlib.import_module(module_name)
        except (ModuleNotFoundError, ImportError):
            return None

    @staticmethod
    def _get_members_of_module(module: ModuleType) -> List[Any]:
        """
        Get all members of a module.
        :param module: module to get members of.
        :return: list of members of the module.
        """
        return [self for name, self in inspect.getmembers(module)]
