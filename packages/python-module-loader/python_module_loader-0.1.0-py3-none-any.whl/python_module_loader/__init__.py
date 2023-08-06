import inspect
from types import ModuleType
from typing import List, Any, Set

from python_module_loader.loader import ModuleLoader
from python_module_loader.models import ValidateFunction


class PythonModuleLoader:
    """Loads a module and all python modules in same directory as the module."""

    def __init__(self):
        self._loader = ModuleLoader()

    @property
    def modules(self) -> List[ModuleType]:
        """Returns a list of loaded modules."""
        return [python_module.module for python_module in self._loader.modules]

    @property
    def objects(self) -> List[Any]:
        """Returns a list of all loaded objects found in modules."""
        return [
            obj for module in self.modules for name, obj in inspect.getmembers(module)
        ]

    def load(self, module_name: str, recursive: bool = False) -> "PythonModuleLoader":
        """
        Loads a module and all python modules in same directory as the module.

        :param module_name: name of the module. e.g. 'backend.users'
        :param recursive: if True, will load all modules from subdirectories.
        :return: PythonModuleLoader.
        """
        self._loader.load(module_name, recursive)
        return self

    def find_objects(self, validators: List[ValidateFunction]) -> Set[Any]:
        """
        Finds all modules objects that pass the validation.

        :param validators: list of validators functions that return True if module object is valid.
        :return: list of valid objects.
        """
        return set(
            obj for obj in self.objects if self._validate_object(obj, validators)
        )

    @staticmethod
    def _validate_object(obj: Any, validators: List[ValidateFunction]) -> bool:
        """
        Validates an object against a list of validators.

        :param obj: object to validate.
        :param validators: list of validators functions that return True if object is valid.
        :return: True if object passed all validators and is valid.
        """
        if not validators:
            return True
        try:
            return all(validator(obj) for validator in validators)
        except Exception:
            return False


def autoload(
    module_name: str,
    validators: List[ValidateFunction] = None,
    recursive: bool = True,
) -> Any:
    """
    Loads a module and all python modules in same directory as the module.

    :param module_name: name of the module. e.g. 'backend.users'
    :param validators: list of validators functions that return True if module object is valid.
    :param recursive: if True, will load all modules from subdirectories.
    :return: set of modules objects.
    """
    return (
        PythonModuleLoader()
        .load(module_name, recursive=recursive)
        .find_objects(validators=validators)
    )
