from flask import Flask

# for getting environment variables
import os

###########################################################
# Setup App
###########################################################

def create_app():
    app = Flask(
        __name__,
        static_url_path="/static",
        instance_relative_config=True
    )

    # load configuration
    configMode = os.environ.get("app_configuration", "Config")
    app.config.from_object("config." + str(configMode))

    with app.app_context():
        # default app related views
        from bot.views.controller import views

        # Register controller blueprints
        app.register_blueprint(views)

    return app

