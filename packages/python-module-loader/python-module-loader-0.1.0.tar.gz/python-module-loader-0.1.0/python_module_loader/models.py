import importlib
import os
from dataclasses import dataclass
from types import ModuleType
from typing import Callable, Any

from python_module_loader import helpers


@dataclass
class PythonModule:
    """Wrapper for a python's module."""

    name: str
    module: ModuleType

    @property
    def directory(self):
        """Returns the directory of the module."""
        return os.path.dirname(self.module.__file__)

    def __str__(self):
        return f"<{self.name}>"

    @classmethod
    def from_module_name(
        cls,
        module_name: str,
        package: str = __package__,
    ) -> "PythonModule":
        """
        Create PythonModule from module name.

        :param module_name: Module name.
        :param package: Package name to allow relative imports. Defaults to the current package.
        :return: PythonModule.
        """
        module = importlib.import_module(module_name, package=package)
        name = helpers.remove_suffix(module.__name__, ".__init__")
        return cls(name=name, module=module)

    def is_valid_file(self):
        """Returns True if the module is a valid file."""
        return bool(self.module.__file__)

    def is__init__(self):
        """Returns True if the module is __init__.py file."""
        return self.module.__file__.endswith("__init__.py")


ValidateFunction = Callable[[Any], bool]
