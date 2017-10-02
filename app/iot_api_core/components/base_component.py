from flask import request, current_app
import os

class BaseComponent:
  def __init__(self, context):
    self.context = context
    self.data = {}

  @property
  def display_name(self):
    return self.label

  @property
  def section(self):
    return 'General'

  @property
  def label(self):
    return 'Component'

  @property
  def category(self):
    return 'body'

  @property
  def icon_url(self):
    proto = request.headers.get('X-Forwarded-Proto', 'http')
    host = request.host

    return '/icons/iot/' + current_app.config['WIDGET_ID'] + '/api/instances/icons/' + self.component_type + '.svg'

  def get_properties(self):
    return [x.to_json() for x in self.properties]

  def get_property(self, name):
    return next((p for p in self.properties if p.name == name), None)

  def load(self, data):
    self.data = {}

    for x in self.properties:
      self.data[x.name] = x.read(data)

  def to_json(self):
    return self.data
