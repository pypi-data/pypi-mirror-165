import os


def check_react_templates_folder() -> bool:
    return os.path.isfile("package.json")
