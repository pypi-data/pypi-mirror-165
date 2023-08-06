import os

from .log import log

babel = """{
    "presets": [
        "@babel/preset-react",
        "@babel/preset-env"
    ],
    "plugins": [
        "@babel/plugin-proposal-class-properties",
        "@babel/plugin-transform-react-jsx"
    ]
}
"""


def install_react_project():
    log(f"Initializing yarn project.")
    os.system(f"yarn init -y >/dev/null 2>&1")

    log(f"Installing packages.")
    os.system(
        f"yarn add webpack webpack-cli react react-dom babel-loader @babel/core @babel/preset-env @babel/preset-react @babel/preset-env @babel/plugin-proposal-class-properties @babel/plugin-transform-react-jsx >/dev/null 2>&1"
    )

    os.system(f"""echo '{babel}' > .babelrc""")

    log(f"Installation done.")


def update_packages():
    log(f"Updating packages.")
    os.system(f"yarn install >/dev/null 2>&1")
    log(f"Update done.")
