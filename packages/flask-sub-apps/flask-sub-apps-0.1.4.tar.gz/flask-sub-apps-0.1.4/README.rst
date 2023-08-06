Flask Sub-Apps
========

    Flask sub-apps are modules that can be installed to a Flask application.
    Each sub-app can have its own routes, commands, models, etc. Installing
    a sub-app is as simple as passing a string containing a module. The module
    will be automatically imported and the appropriate attributes will be installed in the
    application.

    Here is an example of installing a sub-app::

        from flask import Flask
        from flask.ext.app import FlaskApp
        from myapp import myapp

        app = Flask(__name__)
        sub_apps = FlaskSubApps(
            app,
            installed_sub_apps=["path.to.myapp"],
        )
        app.run()

    The above example will install the `myapp` module to the application.
    The `myapp` module can then be used as a regular Flask application.

    The `installed_sub_apps` parameter is used to specify where to find sub-apps.
    It's a list of strings, each string being a path to a sub-app.


By default, files within sub-app will be search by below code::

    MODELS_FILE = env.get("FLASK_SUB_APPS_MODELS_FILE", ["models", "sqla_models"])
    COMMANDS_FILE = env.get("FLASK_SUB_APPS_COMMANDS_FILE", ["commands", "flask_commands"])
    ROUTERS_FILE = env.get(
        "FLASK_SUB_APPS_ROUTERS_FILE",
        ["routers", "views", "api_views", "urls", "blueprints"],
    )
    # Specify name of the module the application should look for.
    # String and array of strings are accepted.
    # You can use a module path, relative to root of the sub-app.
