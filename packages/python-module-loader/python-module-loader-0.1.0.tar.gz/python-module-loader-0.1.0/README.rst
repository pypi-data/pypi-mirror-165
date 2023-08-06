Python Autoloader
========

    This package provides a way to automatically load specified modules with all of its submodules.
    It is useful if we want to get all of the submodules without explicitly importing them.

For example, if we want to get all command classes in the package `commands`, we can do the following:
::

    commands = (
        PythonModuleLoader()
        .load("app.commands", recursive=True)
        .find_objects(validators=[lambda obj: issubclass(obj, Command)])
    )

The above code will load all modules in the package `app.commands` and find all subclasses of `Command` in it.