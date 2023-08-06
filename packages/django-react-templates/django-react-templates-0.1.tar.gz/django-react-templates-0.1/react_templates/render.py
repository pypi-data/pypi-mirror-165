import os
from django.shortcuts import render
from django.http import HttpRequest

from .core.log import log
from .core.regex import export_regex

webpack = """
const path = require("path");

module.exports = {
  entry: "./.react_templates_build/result.js",
  mode: "development",
  output: {
    path: path.resolve(__dirname, "./.react_templates_build"),
    filename: "bundle.js",
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: ["babel-loader"],
      },
    ],
  },
};

"""

result = """
import React from "react";
import { createRoot } from 'react-dom/client';
import {{entrypoint}} from "../{{path}}";

document.addEventListener("DOMContentLoaded", () => {
    const container = document.getElementById('root');
    const root = createRoot(container);
    root.render(<{{entrypoint}}/>);
});
"""


def render_react(request: HttpRequest, template_name: str):
    bundle: str
    entrypoint: str
    template_split = template_name.split("/")
    template_path = os.path.join(template_split[0], *["web", *template_split[1:]])

    os.system("mkdir .react_templates_build 2>&1")

    log(f"Rendering {template_path}.")

    with open(template_path, "r+") as f:
        entrypoint = export_regex.search(f.read()).group(1)

    with open("webpack.config.js", "w+") as f:
        f.write(webpack.replace("{{file}}", template_path))

    with open(os.path.join(".react_templates_build", "result.js"), "w+") as f:
        f.write(
            result.replace("{{entrypoint}}", entrypoint).replace(
                "{{path}}", template_path
            )
        )

    log(f"Created webpack config file.")

    os.system("npx webpack 2>&1")

    log(f"Created bundle.")

    os.system("rm webpack.config.js")

    with open(os.path.join(".react_templates_build", "bundle.js"), "r") as f:
        bundle = f.read()

    return render(
        request,
        "_django_react_templates/base.html",
        {"code": bundle, "entrypoint": "Home"},
    )
