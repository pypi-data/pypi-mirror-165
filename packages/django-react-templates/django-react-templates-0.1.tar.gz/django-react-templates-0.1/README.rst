======================
Django React Templates
======================

React Templates is a Django app made to integrate React into Django Templates.

Installation
____________

``pip install django-react-templates``

Update your `wsgi.py` file with:

.. code-block:: python3

    import os

    from django.core.wsgi import get_wsgi_application
    from react_templates.wsgi import get_web_application

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings")

    application = get_wsgi_application()
    web_application = get_web_application() # Make sure this is after the application


Once `runserver` command is called, React Templates will setup it's necessary files and packages.

Important Files
_______________

React Templates creates several files inside your root:

- `package.json` - For managing the React packages, you can also install your own packages inside.
- `yarn.lock` - Lockfile for your packages.
- `.babelrc` - Configuration file for Babel compiler.

*Removing any of these files (or altering .babelrc) will result in unpredicted results or failure.*

Quick Start
___________

Inside any app in your project, create a `web` folder and a `.js` file.

.. code-block:: js

    // File inside /my-app/web/HelloWorld.js

    import React from "react";

    function HelloWorld() {
      const [number, setNumber] = React.useState(0);
      return (
        <div>
          <h1>Hello World! {number} times!</h1>
          <button onClick={() => setNumber(number + 1)}>Click me!</button>
        </div>
      );
    }

    export default HelloWorld; // Defines which component will be rendered as an entrypoint.


Once you have your React Component, create a view that renders that template:

.. code-block:: python3

    # File inside /my-app/views.py
    from react_templates.render import render_react

    def hello_world_page(request):
        return render_react(request, "my-app/HelloWorld.js") # Notice you must not mention the web folder!


Now you can path it to some url and it will render a html page!

Importing
_________

Importing components from your own project must be done using the relative path from it. For example, if we have a component in a different app:

.. code-block:: js

    // File inside /my-app/web/Home.js

    import { OtherComponent } from "../../../new-app/web/components/OtherComponent.js";

    ...
