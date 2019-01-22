from flask import Blueprint, jsonify, request, make_response, redirect, render_template, g
from lumavate_signer import Signer
import requests
import json
import os

default_blueprint = Blueprint('default_blueprint', __name__)

def make_payload(data):
  payload = {
    'payload': {
      'data': data
    }
  }

  return payload

@default_blueprint.route('/<string:integration_cloud>/<string:widget_type>/discover/properties', methods=['GET'])
def get_properties(integration_cloud, widget_type):
  properties = [
    {
      'classification': 'Hello World Tab',
      'section': 'Hello World Section',
      'label': 'Message',
      'name': 'message',
      'options': {
        'readonly': False,
        'rows': 0
      },
      'type': 'text'
    },
    {
      "classification": "Hello World Tab",
      "section": "Hello World Section",
      "label": "Color",
      "name": "helloColor",
      "type": "color"
    },
    {
      "classification": "Hello World Tab",
      "section": "Hello World Section",
      "label": "Hello Icon",
      "name": "helloIcon",
      "type": "image-upload"
    },
    {
      "classification": "Hello World Tab",
      "section": "Hello World Section",
      "label": "Hello Checkbox",
      "name": "helloCheckbox",
      "type": "checkbox"
    },
    {
      "classification": "Hello World Tab",
      "section": "Hello World Section",
      "label": "Hello Toggle",
      "name": "helloToggle",
      "type": "toggle"
    },
    {
      "classification": "Hello World Tab",
      "section": "Hello World Section",
      "label": "Hello Translated Text",
      "name": "helloTranslatedText",
      "type": "translated-text"
    },
    {
      "classification": "Hello World Tab",
      "section": "Hello World Section",
      "label": "Hello Numeric",
      "name": "helloNumeric",
      "type": "numeric",
      "default": 3,
      "options": {
        "min": 1,
        "max": 10
      }
    },
    {
      "classification": "Hello World Tab",
      "section": "Hello World Section",
      "label": "Hello Dropdown",
      "name": "helloDropdown",
      "type": "dropdown",
      "options": {
        "1": "option 1",
        "2": "option 2",
        "3": "option 3"
      },
      "default": "1"
    },
    {
      "classification": "Hello World Tab",
      "section": "Hello World Section",
      "label": "Hello Multiselect",
      "name": "helloMultiselect",
      "type": "multiselect",
      "options": [
        { "value": "1", "displayValue": "option 1" },
        { "value": "2", "displayValue": "option 2" },
        { "value": "3", "displayValue": "option 3" }
      ],
      "default": [1, 3]
    },
    {
      "classification": "Hello World Tab",
      "section": "Hello World Section",
      "label": "Hello Model Page Link",
      "name": "helloPageLink",
      "type": "page-link"
    },
    {
      "classification": "Footer Tab",
      "section": "Footer Section",
      'label': 'Footer Text',
      'name': 'footerText',
      'options': {
        'readonly': False,
        'rows': 0
      },
      'type': 'text'
    }

  ]

  return jsonify(make_payload(properties))

def get_root_uri():
  return 'http://' + request.host

def get_instance_uri(instance_id, integration_cloud, widget_type):
  return get_root_uri() + '/{}/{}/{}'.format(integration_cloud, widget_type, instance_id)

@default_blueprint.route('/<string:integration_cloud>/<string:widget_type>/instances/<int:instance_id>/on-create-version', methods=['POST'])
def on_create_version(integration_cloud, widget_type, instance_id):
  r = request.get_json()
  if r['message'] == 'Nope':
    return make_response('Invalid Value', 400)

  return jsonify(make_payload(r))

@default_blueprint.route('/<string:integration_cloud>/<string:widget_type>/instances/<int:instance_id>/after-create-version', methods=['POST'])
def after_create_version(integration_cloud, widget_type, instance_id):
  r = request.get_json()
  return jsonify(make_payload(r))

def make_request(method, url, data=None):
  headers = {'Authorization': 'Bearer ' + str(g.pwa_jwt), 'Content-Type': 'application/json'}
  lumavate_url = os.environ.get('BASE_URL')
  url = '{}{}'.format(lumavate_url, url)
  s = Signer(os.environ.get('PUBLIC_KEY'), os.environ.get('PRIVATE_KEY'))
  url = s.get_signed_url(method, url, data, headers)
  if isinstance(data, dict):
    data = json.dumps(data)

  if method == 'get':
    return requests.get(url, headers=headers)
  elif method == 'post':
    return requests.post(url, headers=headers, data=data)
  else:
    print('unknown method:' + method)

##########################################################################
# For convenience, redirect to index.html, which will get things running
# 'under' the instance id
##########################################################################
@default_blueprint.route('/<string:integration_cloud>/<string:widget_type>/<int:instance_id>', methods=['GET'])
def default(integration_cloud, widget_type, instance_id):
  path = 'https://{}/{}/{}/{}/index.html'.format(request.host, integration_cloud, widget_type, instance_id)
  return redirect(path, 302)

@default_blueprint.route('/<string:integration_cloud>/<string:widget_type>/<int:instance_id>/index.html', methods=['GET'])
def render(integration_cloud, widget_type, instance_id):
  # Get the PWA JWT for basic auth context. This jwt will give enough access
  # to be able to query for config data within the microsite
  g.pwa_jwt = request.cookies.get('pwa_jwt')

  data_response = make_request('get', '/pwa/v1/widget-instances/{}'.format(instance_id))

  # Any non-200 status indicates a need to attempt a refresh of auth
  # credentials.  We can redirect to the root to refresh the cookie
  if data_response.status_code == 401:
    reauth = '{}?u={}'.format(get_root_uri(), get_instance_uri(instance_id, integration_cloud, widget_type))
    return redirect(reauth, 302)
  elif data_response.status_code == 404:
    return "Instance not found!"
  elif data_response.status_code != 200:
    return "Error getting widget data! status code=" +  str(data_response.status_code)

  # We made a successful call to discover the current config.  In this widget's
  # case this means we have the following payload:
  # {
  #   "message": "<Whatever the designer gave us>",
  #   "helloColor": "<Whatever the designer gave us>",
  #   "footerText": "<Whatever the designer gave us>",
  #   ... Other standard properties ...
  # }
  version_data = data_response.json()['payload']['data']

  api_context = {}
  res = make_request('get', '/pwa/v1/activation'.format(instance_id))
  if res.status_code == 200:
    api_context['activationData'] = res.json()['payload']['data']
  elif res.status_code == 404:
    api_context['activationData'] = 'No activation data'
  else:
    api_context['activationData'] = res.json()

  res = make_request('get', '/pwa/v1/token'.format(instance_id))
  if res.status_code == 200:
    api_context['tokenData'] = res.json()['payload']['data']
  elif res.status_code == 404:
    api_context['tokenData'] = 'No token data'
  else:
    api_context['tokenData'] = res.json()

  # We have the opportunity now to return a formatted message
  return render_template('render.html', context=version_data, api_context=api_context)

##########################################################################
# Included files - These files will be included directly upon rendering the main
# file.  Using the pwa_jwt without checking validity will be fine because
# the main file will do the checking
##########################################################################
@default_blueprint.route("/<string:integration_cloud>/<string:widget_type>/<int:instance_id>/push.js", methods=["GET"])
def push(integration_cloud, widget_type, instance_id):
  try:
    g.pwa_jwt = request.cookies.get('pwa_jwt')
    response = make_response(render_template('push.js', public_key=os.environ.get('PUSH_SERVER_PUBLIC_KEY'), token=str(g.pwa_jwt)))
    response.headers['Content-Type'] = 'application/x-javascript'

    return response

  except Exception as e:
    raise
    print(e, flush=True)
    abort(404)

##########################################################################
# APIs.  Critical that these don't read the jwt form teh cookis.  Should
# always be sent in as a header to avoid CSRF attacks
##########################################################################
@default_blueprint.route('/<string:integration_cloud>/<string:widget_type>/<int:instance_id>/delete-opt-in', methods=['DELETE'])
def delete_opt_in(integration_cloud, widget_type, instance_id):
  g.pwa_jwt = request.headers.get('Authorization')
  return jsonify(make_request('delete', '/pwa/v1/delete-opt-in').json())

@default_blueprint.route('/<string:integration_cloud>/<string:widget_type>/<int:instance_id>/notification-opt-ins', methods=['POST'])
def notification_opt_ins(integration_cloud, widget_type, instance_id):
  g.pwa_jwt = request.headers.get('Authorization')
  return jsonify(make_request('post', '/pwa/v1/notification-opt-ins').json(), data=request.get_data())

@default_blueprint.route('/<string:integration_cloud>/<string:widget_type>/<int:instance_id>/send-to-subscriber', methods=['POST'])
def send_to_subscriber(integration_cloud, widget_type, instance_id):
  g.pwa_jwt = request.headers.get('Authorization')
  return jsonify(make_request('post', '/pwa/v1/send-to-subscriber').json())

@default_blueprint.route('/<string:integration_cloud>/<string:widget_type>/<int:instance_id>/send-to-site', methods=['POST'])
def send_to_site(integration_cloud, widget_type, instance_id):
  g.pwa_jwt = request.headers.get('Authorization')
  return jsonify(make_request('post', '/pwa/v1/send-to-site').json())

##########################################################################
# Describe what files can & should be cached
##########################################################################
@default_blueprint.route('/<string:integration_cloud>/<string:widget_type>/discover/precache', methods=['GET'])
def precache(integration_cloud, widget_type):
  static_base = '{widgetPrefix}/discover'
  data_uri_base = '{widgetPrefix}/{instanceId}'

  try:
    git_revision = open('/revision', 'r')
    commit_hash = git_revision.readline().strip('\n')
    git_revision.close()
  except:
    commit_hash = 'develop'

  #return jsonify({
  #  'files': [{'file': static_base + '/file.json', 'versioned': False}],
  #  'apis': [data_uri_base + '/data'],
  #  'revision': '123'
  #})
  return jsonify({
    'preCache': [],
    'runtimeCache': [
      {'url': data_uri_base + '/index.html', 'versioned': True},
      {'url': data_uri_base + '', 'versioned': True},
      {'url': data_uri_base + '/push.js', 'versioned': True}
      ],
    'revision': commit_hash
  })

