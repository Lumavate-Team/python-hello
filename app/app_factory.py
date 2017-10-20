from flask import Flask, jsonify, send_from_directory, g
from routes import *
import iot_api_core
import behavior
import rollbar

def create_app(options=None):
    app = Flask(__name__)
    app.config.from_envvar('APP_SETTINGS')

    # apply any configuration override options
    if options is not None:
      for key, value in options.items():
        app.config[key] = value

    @app.route('/<string:integration_cloud>/<string:widget_type>/discover/icons/<string:icon>')
    def return_icon(integration_cloud, widget_type, icon):
      return send_from_directory('icons', icon)

    app.register_blueprint(default_blueprint)

    return app
