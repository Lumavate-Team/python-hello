from .image_base import ImageBase
from .base import BaseProperty
from flask import current_app
import iot_api_core

class ModelImageProperty(BaseProperty, ImageBase):
  def __init__(self, classification, section, name, label, context, options=None, default={}):
    super().__init__(classification, section, name, label, context, options=options, default=default)

  @property
  def type_name(self):
    return 'model-image-upload'

  def read(self, from_values):
    val = from_values.get(self.name)
    result = {}
    if val is None:
      val = self.default

    no_image = '/icons/iot/' + current_app.config['WIDGET_ID'] + '/api/instances/icons/no_image_available.png'
    no_image_payload = {
      'preview': no_image,
      'previewLarge': no_image,
      'previewMedium': no_image,
      'previewSmall': no_image
    }

    result['mode'] = str(val.get('mode', 'model-image'))
    if result['mode'] not in ['model-image', 'upload']:
      raise iot_api_core.IotException(400, 'Invalid mode: ' + result['mode'])

    if result['mode'] == 'upload':
      result.update(self.read_image(val))

    elif result['mode'] == 'model-image':
      if self.context.model_id:
        model_info = self.context.model_info
        if model_info['image'] and 'key' in model_info['image']:
          data = {
            'key': model_info['image']['key'],
            'version': model_info['image']['versionId']
          }
          payload = self.context.lumavate.get('/iot/v1/files/preview/' + model_info['image']['key'] + '/' + model_info['image']['versionId'])
          result.update(payload)
          result['modelKey'] = result['key']
          result['modelVersion'] = result['version']
          del result['key']
          del result['version']

        else:
          result.update(no_image_payload)

      else:
        result.update(no_image_payload)

    self.value = result
    return result

