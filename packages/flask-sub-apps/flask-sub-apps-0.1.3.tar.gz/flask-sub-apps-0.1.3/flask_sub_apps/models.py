from dataclasses import dataclass
from types import ModuleType
from typing import Set

from flask_sub_apps import config


@dataclass(frozen=True)
class SubApp:
    name: str
    module: ModuleType

    models: Set[config.DBModel]
    commands: Set[config.Command]
    routers: Set[config.Router]

    api_prefix: str = ""

    @property
    def module_name(self):
        return self.module.__name__

    def __str__(self):
        return self.module_name
