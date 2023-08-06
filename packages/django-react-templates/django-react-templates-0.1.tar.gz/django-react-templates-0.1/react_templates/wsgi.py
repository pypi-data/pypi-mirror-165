from .core.check import (
    check_react_templates_folder,
)

from .core.install import install_react_project, update_packages


def get_web_application():
    if not check_react_templates_folder():
        install_react_project()

    update_packages()
