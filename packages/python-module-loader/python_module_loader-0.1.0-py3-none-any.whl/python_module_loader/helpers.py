import logging


def get_logger() -> logging.Logger:
    """Get logger for PythonModuleLoader."""
    return logging.getLogger("PythonModuleLoader")


def is_python_file(file_name: str) -> bool:
    """Check if file_name is a python file by checking its extension."""
    return file_name.endswith(".py") if file_name else False


def remove_suffix(string: str, suffix: str) -> str:
    """Remove suffix from string."""
    return string[: -len(suffix)] if string.endswith(suffix) else string
