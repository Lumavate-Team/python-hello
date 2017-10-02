from flask import g, request, current_app, make_response, jsonify
from itsdangerous import URLSafeSerializer
from functools import wraps, partial
import iot_api_core
import requests
import time
import json
import os

def log_time(func):
  def do_log_time(*args, **kwargs):
    start = time.time()
    try:
      return func(*args, **kwargs)

    finally:
      duration = time.time() - start
      if func.__name__ in ['get', 'put', 'post', 'delete']:
        print(str(duration) + ':' + func.__name__ + '(' + args[1] + ')', flush=True)
      else:
        print(str(duration) + ':' + func.__name__, flush=True)

  return do_log_time

class Lumavate:
  def __init__(self):
    pass

  @property
  def token(self):
    if hasattr(g, 'lumavate_context'):
      return g.lumavate_context['token']
    else:
      raise iot_api_core.IotException(401, 'Not Authorized')

  @log_time
  def get(self, path):
    response_text = ''
    results = {}

    with requests.Session() as s:
      res = s.get(self.url(path), headers=self.headers(), stream=True, timeout=None)
      res.encoding = 'utf-8' if not(res.encoding) else res.encoding
      for chunk in res.iter_content(chunk_size=512, decode_unicode=True):
        if chunk:
          response_text = response_text + chunk

      if(res.status_code == 200):
        results = json.loads(response_text)

    return self.handle_response(res, results)

  @log_time
  def post(self, path, payload):
    response_text = ''
    results = {}

    with requests.Session() as s:
      res = s.post(self.url(path), headers=self.headers(), data=json.dumps(payload), stream=True, timeout=None)
      res.encoding = 'utf-8' if not(res.encoding) else res.encoding
      for chunk in res.iter_content(chunk_size=512, decode_unicode=True):
        if chunk:
          response_text = response_text + chunk

      if(res.status_code == 200):
        results = json.loads(response_text)

    return self.handle_response(res, results)

  @log_time
  def put(self, path, payload):
    response_text = ''
    results = {}

    with requests.Session() as s:
      res = s.put(self.url(path), headers=self.headers(), data=json.dumps(payload), stream=True, timeout=None)
      res.encoding = 'utf-8' if not(res.encoding) else res.encoding
      for chunk in res.iter_content(chunk_size=512, decode_unicode=True):
        if chunk:
          response_text = response_text + chunk

      if(res.status_code == 200):
        results = json.loads(response_text)

    return self.handle_response(res, results)

  def delete(self, path):
    response_text = ''
    results = {}

    with requests.Session() as s:
      res = s.delete(self.url(path), headers=self.headers(), stream=True, timeout=None)
      res.encoding = 'utf-8' if not(res.encoding) else res.encoding
      for chunk in res.iter_content(chunk_size=512, decode_unicode=True):
        if chunk:
          response_text = response_text + chunk

      if(res.status_code == 200):
        results = json.loads(response_text)

    return self.handle_response(res, results)

  def handle_response(self, res, data = None):

    response_data = data
    #if not response_data:
    #  response_data = res.json()

    if res.status_code == 200:
      if 'payload' in response_data:
        return response_data['payload']['data']
      else:
        return response_data

    else:
      raise Exception('Error making request ' + res.url + ':' + res.request.method + ' - ' + str(res.status_code))

  def headers(self):
    return {
      'Authorization': self.token,
      'Content-Type': 'application/json'
    }

  def url(self, path=""):
    if path.startswith('/'):
      return os.getenv('BASE_URL') + path
    else:
      return path
