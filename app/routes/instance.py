from flask import Blueprint, jsonify, request, make_response, redirect, render_template, g
import requests
import os

default_blueprint = Blueprint('default_blueprint', __name__)

def make_payload(data):
  payload = {
    'payload': {
      'data': data
    }
  }

  return payload

@default_blueprint.route('/discover/properties', methods=['GET'])
def get_properties():
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
      "label": "Hello Model Image",
      "name": "helloModelImage",
      "type": "model-image-upload",
      "default": {
        "mode": "model-image"
      }
    },
    {
      "classification": "Hello World Tab",
      "section": "Hello World Section",
      "label": "Hello Model Header Title",
      "name": "helloModelHeaderTitle",
      "type": "header-title"
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
  return 'https://' + request.host

def get_instance_uri(instance_id):
  return get_root_uri() + '/ic/hello/' + str(instance_id)

@default_blueprint.route('/instances/<int:instance_id>/on-create-version', methods=['POST'])
def on_create_version(instance_id):
  r = request.get_json()
  if r['message'] == 'Nope':
    return make_response('Invalid Value', 400)

  return jsonify(make_payload(r))

@default_blueprint.route('/instances/<int:instance_id>/<int:version_id>/after-create-version', methods=['POST'])
def after_create_version(instance_id, version_id):
  r = request.get_json()
  return jsonify(make_payload(r))

def make_get_request(url):
  headers = {'Authorization': 'Bearer ' + str(g.pwa_jwt)}
  lumavate_url = os.environ.get('BASE_URL')
  url = '{}/{}'.format(lumavate_url, url)
  return requests.get(url, headers=headers)

@default_blueprint.route('/<int:instance_id>', methods=['GET'])
def render(instance_id):
  # Get the PWA JWT for basic auth context. This jwt will give enough access
  # to be able to query for config data within the microsite
  g.pwa_jwt = request.cookies.get('pwa_jwt')

  data_response = make_get_request('/pwa/v1/widget-instances/{}'.format(instance_id))

  # Any non-200 status indicates a need to attempt a refresh of auth
  # credentials.  We can redirect to the root to refresh the cookie
  if data_response.status_code != 200:
    reauth = '{}?u={}'.format(get_root_uri(), get_instance_uri(instance_id))
    return redirect(reauth, 302)

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
  res = make_get_request('/pwa/v1/activation'.format(instance_id))
  if res.status_code == 200:
    api_context['activationData'] = res.json()['payload']['data']
  elif res.status_code == 404:
    api_context['activationData'] = 'No activation data'
  else:
    api_context['activationData'] = res.json()

  res = make_get_request('/pwa/v1/token'.format(instance_id))
  if res.status_code == 200:
    api_context['tokenData'] = res.json()['payload']['data']
  else:
    api_context['tokenData'] = res.json()

  # We have the opportunity now to return a formatted message
  return render_template('render.html', context=version_data, api_context=api_context)
