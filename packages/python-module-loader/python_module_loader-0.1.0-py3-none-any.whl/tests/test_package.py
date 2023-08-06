import inspect

from python_module_loader import PythonModuleLoader


def test_module_autoloader():
    loader = PythonModuleLoader().load("tests.example")
    assert len(loader.modules) == 3

    classes = (
        PythonModuleLoader()
        .load("tests.example")
        .find_objects(validators=[inspect.isclass])
    )
    assert len(classes) == 2

    classes = (
        PythonModuleLoader()
        .load("tests.example", recursive=True)
        .find_objects(validators=[inspect.isclass])
    )
    assert len(classes) == 4
    assert {c.__name__ for c in classes} == {"A", "B", "C", "D"}
