from .base import BaseProperty
import iot_api_core

class HeaderTitleProperty(BaseProperty):
  def __init__(self, classification, section, name, label, context, options=None, default=None):
    if default is None:
      default = {}

    super().__init__(classification, section, name, label, context, options=options, default=default)

  @property
  def type_name(self):
    return 'header-title'

  def read(self, from_values):
    val = from_values.get(self.name)
    result = {}
    if val is None:
      val = self.default

    result['mode'] = str(val.get('mode', 'model-name'))
    if result['mode'] not in ['model-name', 'custom']:
      raise iot_api_core.IotException(400, 'Invalid mode: ' + result['mode'])

    if result['mode'] == 'custom':
      result['title'] = val.get('title')
    else:
      if self.context.model_id:
        result['title'] = self.context.model_info['name']
      else:
        result['title'] = {'en-us': 'My Product'}

    self.value = result
    return result

