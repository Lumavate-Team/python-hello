from flask import g, request, current_app, make_response, jsonify
from itsdangerous import URLSafeSerializer
from functools import wraps, partial
import iot_api_core
import requests
import json
import os

def api_response(f):
  @wraps(f)
  def decorated_function(*args, **kwargs):
    try:
      response = { 'payload':
                  { 'data' : {} }
                  }

      results_raw = f(*args, **kwargs)

      if results_raw is None:
        results_raw = make_response(json.dumps({'payload' : { 'error': 'Not Found' }}), 404)

      elif (isinstance(results_raw, list)):
        response['payload']['data'] = results_raw
        results_raw = jsonify(**response)

      elif (isinstance(results_raw, dict)):
        response['payload']['data'] = results_raw
        results_raw = jsonify(**response)

    #except ApiException as e:
    #  pyro.db.session.rollback()
    #  results_raw = make_response(json.dumps({'payload': e.to_dict()}), e.status_code)

    except iot_api_core.IotException as e:
      if e.code == 400:
        results_raw = make_response(json.dumps({'payload': { 'error': e.message}}), e.code)
      else:
        results_raw = make_response(json.dumps({'payload': { 'error': 'unexpected error'}}), 500)

    except Exception as e:
      raise e
      results_raw = make_response(json.dumps({'payload': { 'error': 'unexpected error'}}), 500)

    return results_raw

  return decorated_function

def set_up_microsite_context(auth_header):
  context_req = os.environ.get('BASE_URL') + '/iot/microsite-context'
  headers = { 'Authorization': auth_header }
  context = requests.get(context_req, headers=headers)
  g.iot_context = context.json()['payload']['data']['iotContext']
  g.lumavate_context = context.json()['payload']['data']['lumavateContext']
  g.namespace = g.iot_context['token_data']['namespace']

def microsite_protected(f):
  @wraps(f)
  def decorated_function(*args, **kwargs):
    try:
      set_up_microsite_context(request.headers['Authorization'])

    except Exception as e:
      return make_response(json.dumps({'payload': { 'error': 'Not Authorized'}}), 401)

    return f(*args, **kwargs)

  return decorated_function

def lumavate_protected(f):
  @wraps(f)
  def decorated_function(*args, **kwargs):
    try:
      g.lumavate_context = {
        'token': request.headers['Authorization']
      }
      iot_api_core.Lumavate().get('/iot/lumavate-context')
      data = request.get_json(silent=True)
      if data is not None and data.get('namespace') is not None:
        g.namespace = data.get('namespace')

    except Exception as e:
      return make_response(json.dumps({'payload': { 'error': 'Not Authorized'}}), 401)

    return f(*args, **kwargs)

  return decorated_function
