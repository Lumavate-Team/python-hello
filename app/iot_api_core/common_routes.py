from flask import Blueprint, request, g, current_app
import iot_api_core

common_routes_blueprint = Blueprint("common_routes_blueprint", __name__)

def behavior_factory(instance_id):
  raise Exception ('Not Implemented')

common_routes_blueprint.behavior_factory = behavior_factory

@common_routes_blueprint.route("/instances/<int:instance_id>/versions", methods=["POST"])
@iot_api_core.lumavate_protected
@iot_api_core.api_response
@iot_api_core.log_time
def rest_versions(instance_id):
  handler = common_routes_blueprint.behavior_factory(instance_id)
  return handler.rest_create()

@common_routes_blueprint.route("/instances/<int:instance_id>/versions/<string:version>/publish", methods=["POST"])
@iot_api_core.lumavate_protected
@iot_api_core.api_response
def publish_version(instance_id, version):
  handler = common_routes_blueprint.behavior_factory(instance_id)
  return handler.publish(version)

@common_routes_blueprint.route("/instances/<int:instance_id>/background", methods=["POST"])
@iot_api_core.lumavate_protected
@iot_api_core.api_response
def publish_version_background(instance_id):
  handler = common_routes_blueprint.behavior_factory(instance_id)
  return handler.run_background()

@common_routes_blueprint.route("/instances/<int:instance_id>/data", methods=["GET"])
@iot_api_core.microsite_protected
@iot_api_core.api_response
def get_company_info(instance_id):
  handler = common_routes_blueprint.behavior_factory(instance_id)
  return handler.get_config_data()

@common_routes_blueprint.route("/instances/<int:instance_id>/discover/properties", methods=["GET"])
@iot_api_core.lumavate_protected
@iot_api_core.api_response
def get_properties(instance_id):
  handler = common_routes_blueprint.behavior_factory(instance_id)
  return handler.get_widget_properties()

@common_routes_blueprint.route("/instances/<int:instance_id>/discover/components", methods=["GET"])
@iot_api_core.lumavate_protected
@iot_api_core.api_response
def get_components(instance_id):
  handler = common_routes_blueprint.behavior_factory(instance_id)
  return handler.get_all_components()

@common_routes_blueprint.route("/instances/<int:instance_id>/discover/components/<string:type>/properties", methods=["GET"])
@iot_api_core.lumavate_protected
@iot_api_core.api_response
def get_component_properties(instance_id, type):
  handler = common_routes_blueprint.behavior_factory(instance_id)
  return handler.get_component_properties(type)

@common_routes_blueprint.route("/precache", methods=["GET"])
@iot_api_core.api_response
def precache():
  pwa = iot_api_core.PwaBehavior()

  try:
    files = pwa.load_precache_files()
  except:
    files = []

  return {
    'files': [{"file": filename, "versioned": pwa.is_versioned(filename)} for filename in files],
    'revision': pwa.get_revision()
  }
