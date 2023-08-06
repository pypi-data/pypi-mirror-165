from python_module_loader import helpers


def test_helpers():
    assert helpers.is_python_file("python_module_loader/helpers.py") is True
    assert helpers.is_python_file("python_module_loader/__init__.py") is True
    assert helpers.is_python_file("python_module_loader/loader.py") is True
    assert helpers.is_python_file("models.py") is True
    assert helpers.is_python_file("file") is False
    assert helpers.is_python_file("script.sh") is False
    assert helpers.is_python_file("file.pyc") is False
    assert helpers.is_python_file("") is False
    assert helpers.is_python_file(None) is False

