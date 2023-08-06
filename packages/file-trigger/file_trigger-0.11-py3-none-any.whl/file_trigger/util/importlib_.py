from importlib import import_module


def import_module_class(name: str):
    *mods, classname = name.split(".")
    return getattr(import_module(".".join(mods)), classname)
