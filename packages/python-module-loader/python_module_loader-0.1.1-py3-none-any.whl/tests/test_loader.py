import pytest

from python_module_loader import ModuleLoader


def test_module_loader():
    loader = ModuleLoader.from_module_name("tests.example")
    assert len(loader.modules) == 3
    assert len(loader._visited_dirs) == 1

    loader = ModuleLoader.from_module_name("tests.example", recursive=True)
    assert len(loader.modules) == 6
    assert len(loader._visited_dirs) == 2

    loaded_module_names = {module.name for module in loader.modules}
    assert "tests.example" in loaded_module_names
    assert "tests.example.module1" in loaded_module_names
    assert "tests.example.submodule" in loaded_module_names
    assert "tests.example.submodule.submodule2" in loaded_module_names

    with pytest.raises(ModuleNotFoundError):
        ModuleLoader.from_module_name("tests.not_existing")

    with pytest.raises(ModuleNotFoundError):
        ModuleLoader.from_module_name("tests.example.not_existing")
