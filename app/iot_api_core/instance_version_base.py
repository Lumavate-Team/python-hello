from flask import g, request, current_app
import iot_api_core
import time

class InstanceVersionBaseBehavior():
  def __init__(self, widget_type, namespace, instance_id):
    self.widget_type = widget_type
    self.namespace = namespace
    self.instance_id = instance_id
    self.lumavate = iot_api_core.Lumavate()
    self.temp = {}
    self.post_version_create_handlers = []
    self.experience_info = None
    self._instance = None
    self.status_id = None
    data = request.get_json(silent=True)
    if data:
      self.status_id = data.get('statusId')

    if self.namespace is None:
      self.namespace = self.rest_get_single(self.instance_id)['namespace']

  @property
  def properties(self):
    return []

  @property
  def components(self):
    return []

  @property
  def page_security_property(self):
    page_security = {
      'always': 'Always Render',
      'user-logged-in': 'Only Render When User Logged In',
      'user-not-logged-in': 'Only Render When User NOT Logged In',
      'prod-registered': 'Only Render When Product Registered',
      'device-authorized': 'Only Render When Device Authorized',
      'prod-not-registered': 'Only Render When Product NOT Registered',
      'device-not-authorized': 'Only Render When Device NOT Authorized',
    }

    return iot_api_core.DropdownProperty('General', 'General Settings', 'pageSecurity', 'Page Security', self, default='always', options=page_security)

  @property
  def experience_id(self):
    self.load_experience_info()
    return self.experience_info.get('id')

  @property
  def model_id(self):
    self.load_experience_info()
    return self.experience_info.get('modelId')

  def load(self, version_name):
    instance = self.rest_get_single(self.instance_id)
    data = instance[version_name + 'Version']['data']

    for x in self.properties:
      if not x.name.startswith('instance__'):
        x.read(data)

  def get_general_properties(self, include_auth=False):
    return [
      self.instance_name_property(),
      self.instance_page_type_property(include_auth=include_auth),
      iot_api_core.ToggleProperty('General', 'General Settings', 'displayBackgroundImage', 'Display Background Image', self, default=False),
      iot_api_core.ImageProperty('General', 'General Settings', 'backgroundImage', 'Background Image', self),
      iot_api_core.ColorProperty('General', 'General Settings', 'backgroundColor', 'Background Color', self, default='#e2e2e2'),
      self.page_security_property
    ]

  def load_experience_info(self):
    if not self.experience_info:
      results = self.lumavate.get('/iot/v1/experiences?siteName=' + self.namespace)
      if len(results) > 0:
        self.experience_info = results[0]
        self.model_info = self.lumavate.get('/iot/v1/models/' + str(self.experience_info['modelId']))
      else:
        self.experience_info = {}
        self.model_info = {}

  def rest_get_single(self, id):
    if self._instance is None:
      self._instance  = self.lumavate.get('/iot/v1/widget-instances/' + str(id))

    return self._instance

  def get_version_id(self, instance_id, version_name):
    instance = self.rest_get_single(instance_id)
    return str(instance[version_name + 'VersionId'])

  def get_property(self, name):
    return next((p for p in self.properties if p.name == name), None)

  def get_collection_rest_uri(self):
    return '/iot/v1/widget-instances/' + str(self.instance_id) + '/versions'

  def get_single_rest_uri(self, version_id):
    return self.get_collection_rest_uri() + '/' + str(version_id)

  def rest_get_collection(self):
    return self.lumavate.get(self.get_collection_rest_uri())

  def instance_name_property(self):
    instance = self.rest_get_single(self.instance_id)
    return iot_api_core.TextProperty('General', 'General Settings', 'instance__name', 'Page Name', self, rows=0, default=instance['name'])

  def resolve_images(self, data):
    if isinstance(data, dict):
      if 'key' in data and 'versionId' in data:
        image_data = self.lumavate.post('/iot/v1/files/preview/' + data['key'] + '/' + data['versionId'], {})
        for f in ['contentType', 'url', 'mobileUrl']:
          if f in data:
            image_data[f] = data.get(f)

        return image_data

      else:
        return { k: self.resolve_images(data[k]) for k in data }

    elif isinstance(data, list):
      return [self.resolve_images(x) for x in data]

    else:
      return data

  def collapse_language(self, data):
    lang = 'en-us'

    if isinstance(data, dict):
      if lang in data:
        return data[lang]
      else:
        return { k: self.collapse_language(data[k]) for k in data }

    elif isinstance(data, list):
      return [self.collapse_language(x) for x in data]

    else:
      return data

  def instance_page_type_property(self, include_auth=False):
    page_types = {
      'home': 'Home',
      'registration': 'Registration',
      'auth': 'Auth',
      'error': 'Error',
      'normal': '<Normal>'
    }
    if include_auth == False:
      del page_types['auth']

    return iot_api_core.DropdownProperty('General', 'General Settings', 'pageType', 'Page Type', self, default='normal', options=page_types)

  def rest_create(self):
    instance = self.rest_get_single(self.instance_id)
    if instance:
      payload = {'data': self.validate_data(request.get_json())}
      results = self.lumavate.post(self.get_collection_rest_uri() + '-direct', payload)
      instance['futureVersionId'] = results['id']
      for vch in self.post_version_create_handlers:
        vch()
      self.post_version_create_handlers = []

      if instance.get('futureVersion') is not None:
        results['delta'] = self.get_delta_document(instance.get('futureVersion').get('data'), results['data'])
      else:
        results['delta'] = results.get('data')

      return results

  def background(self, function, args=[], kwargs={}):
    data = {
      'namespace': self.namespace,
      'widgetInstanceId': self.instance_id,
      'widgetType': current_app.config['WIDGET_ID'],
      'method': function.__name__,
      'args': args,
      'kwargs': kwargs,
      'statusId': self.status_id
    }
    self.lumavate.post('/iot/v1/background', data)

  def run_background(self):
    self.lumavate.put('/iot/v1/statuses/' + self.status_id, {'percent': 100})

    return {'a': 4}
    data = request.get_json()
    method = data.get('method')
    args = data.get('args')
    kwargs = data.get('kwargs')
    getattr(self, method)(*args, **kwargs)

  def publish(self, version_name):
    instance = self.rest_get_single(self.instance_id)
    if not instance:
      return

    if version_name not in ['future', 'draft', 'production', 'current']:
      return

    version = instance.get(version_name + 'Version')
    #for x in self.properties:
    #  x.read(version['data'])
    #  x.publish()
    if self.status_id:
      self.lumavate.put('/iot/v1/statuses/' + self.status_id, {'percent': 100})
    else:
      print('NOPE', flush=True)

    return {'Status': 'Ok'}

  def store_data(self, category, record_id, data, latitude=None, longitude=None, version='future'):
    version_id = self.get_version_id(self.instance_id, version)
    payload = {
      'recordId': str(record_id),
      'data': data,
      'latitude': latitude,
      'longitude': longitude
    }
    return self.lumavate.post(self.get_single_rest_uri(version_id) + '/data/' + category, payload)

  def clear_data(self, category, version='future'):
    version_id = self.get_version_id(self.instance_id, version)
    return self.lumavate.delete(self.get_single_rest_uri(version_id) + '/data/' + category)

  def get_current_version(self):
    if hasattr(g, 'iot_context'):
      return g.iot_context['token_data']['version']
    else:
      return 'future'

  def get_data(self, category, default=[], qs=''):
    version_id = self.get_version_id(self.instance_id, self.get_current_version())

    res = self.lumavate.get('/iot/v1/widget-instances/' + str(self.instance_id) + '/versions/' + version_id + '/data/' + category + '?' + qs)
    for x in res:

      if 'distance' in x:
        x['data']['distance'] = x['distance']

    res = [x['data'] for x in res]

    if len(res) == 0:
      return default
    else:
      return res

  def load_activation_info(self):
    api_result = {}
    try:
      api_result = self.lumavate.get('/iot/v1/labels/' + str(g.iot_context['token_data'].get('activationId', 0)))
    except Exception as e:
      pass

    return {
      'key': api_result.get('key'),
      'serialNumber': api_result.get('serialNumber')
    }

  def get_config_data(self):
    # Check if there is a valid version for the current context
    instance = self.rest_get_single(self.instance_id)
    if instance[self.get_current_version() + 'Version'] is None:
      raise Exception('Version ' + self.get_current_version() + ' does not exist for instance ' + str(self.instance_id))

    result = instance[self.get_current_version() + 'Version']['data']

    # Is there any activation to report?
    result['activation'] = self.load_activation_info()

    # Are there any 'special' pages that the UI should know about?
    result['authCheck'] = None
    if g.iot_context['token_data'].get('authUrl') is not None:
      root, part, instance = g.iot_context['token_data']['authUrl'].rpartition('/')
      result['authCheck'] = '{}/api/instances/{}/check-login-status'.format(root, instance)

    return result

  def default_image_data(self, data, prop):
    return {
      'preview': data.get(prop, {}).get('preview', '/icons/iot/page/api/instances/icons/no_image_available.png'),
      'previewLarge': data.get(prop, {}).get('previewLarge', '/icons/iot/page/api/instances/icons/no_image_available.png'),
      'previewMedium': data.get(prop, {}).get('previewMedium', '/icons/iot/page/api/instances/icons/no_image_available.png'),
      'previewSmall': data.get(prop, {}).get('previewSmall', '/icons/iot/page/api/instances/icons/no_image_available.png')
    }

  def get_delta_document(self, original, current):
    if original is None:
      return current
    else:
      result = {}

      for x in self.properties:
        dd = x.delta_doc(original.get(x.name), current.get(x.name))
        if dd is not None:
          result[x.name] = dd

      return result

  def validate_data(self, data):
    result = {}
    instance_payload = {}

    for x in self.properties:
      if x.name.startswith('instance__'):
        field = x.name.split('__')[-1]
        new_val = x.read(data)
        if self._instance[field] != new_val:
          self._instance[field] = new_val
          instance_payload[x.name.split('__')[-1]] = x.read(data)
      else:
        result[x.name] = x.read(data)

    if len(instance_payload.keys()) > 0:
      self.lumavate.put('/iot/v1/widget-instances/' + str(self.instance_id), instance_payload)

    return result

  def get_all_components(self):
    return [
      {
        'label': x.instantiate().label,
        'type': x.instantiate().component_type,
        'icon': x.instantiate().icon_url,
        'section': x.instantiate().section,
        'category': x.instantiate().category
      } for x in self.components
    ]

  def get_component_properties(self, component_type):
    comp = next((x.instantiate() for x in self.components if x.instantiate().component_type == component_type), None)
    if comp:
      return comp.get_properties()

  def get_component_property(self, component_type, property_name):
    comp = next((x.instantiate() for x in self.components if x.instantiate().component_type == component_type), None)
    if comp:
      return comp.get_property(property_name)

  def get_widget_properties(self):
    return [x.to_json() for x in self.properties]

  def handle_language_fields(self, data):
    lang = 'en-us'

    if isinstance(data, dict):
      if lang in data:
        return self.handle_language_fields(data[lang])
      else:
        return { k: self.handle_language_fields(data[k]) for k in data }
    if isinstance(data, list):
      return [ self.handle_language_fields(x) for x in data ]
    else:
      return data

