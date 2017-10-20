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

    blueprints = [
      iot_api_core.common_routes_blueprint
    ]

    def behavior_factory(instance_id):
      namespace = None
      if hasattr(g, 'namespace'):
        namespace = g.namespace

      return behavior.InstanceVersion.InstanceVersionBehavior(namespace, instance_id)

    iot_api_core.common_routes_blueprint.behavior_factory = behavior_factory

    @app.route('/discover/icons/<string:icon>')
    def return_icon(icon):
      return send_from_directory('icons', icon)

    app.register_blueprint(default_blueprint)
    for b in blueprints:
      app.register_blueprint(b, url_prefix="/api")

    return app
