import os
from typing import List

from python_module_loader import helpers
from python_module_loader.models import PythonModule

logger = helpers.get_logger()


class ModuleLoader:
    def __init__(self):
        self.modules: List[PythonModule] = []
        self._visited_dirs: List[str] = []

    @classmethod
    def from_module_name(
        cls, module_name: str, recursive: bool = False
    ) -> "ModuleLoader":
        """
        Creates a new ModuleLoader instance from a module name.
        """
        self = cls()
        self.load(module_name, recursive)
        return self

    def load(self, module_name: str, recursive: bool = False) -> List[PythonModule]:
        """
        Finds and loads all python modules within the same directory as the module.

        :param module_name: name of the module. e.g. 'backend.users'
        :param recursive: if True, will load all modules from subdirectories.
        :return: list of loaded modules.
        """
        python_module = PythonModule.from_module_name(module_name)
        if not python_module.is_valid_file():
            return

        directory_tree = next(os.walk(python_module.directory))
        directory, subdirectories, files = directory_tree
        logger.debug(
            f"Visiting {directory}",
            f"{len(subdirectories)} directories, {len(files)} files",
        )
        self._visit(base_module_name=module_name, directory=directory, files=files)
        if recursive:
            for subdirectory in subdirectories:
                self.load(
                    module_name=f"{module_name}.{subdirectory}",
                    recursive=True,
                )

        return self.modules

    def _visit(self, base_module_name: str, directory: str, files: List[str] = None):
        """
        Visits a directory, finds and loads all python modules within it.
        Each visited directory is added to _visited_dirs to avoid visiting it again.

        :param base_module_name: name of the module. e.g. 'backend.users'
        :param directory: directory to visit.
        :param files: files in the directory (optional).
        """
        if directory in self._visited_dirs:
            return

        files = files or os.listdir(directory)

        for file in filter(helpers.is_python_file, files):
            module_name = f"{base_module_name}.{file[:-3]}"
            module = PythonModule.from_module_name(module_name)
            self.modules.append(module)

        self._visited_dirs.append(directory)
