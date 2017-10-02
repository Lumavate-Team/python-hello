from .base import BaseProperty
import iot_api_core

class PageLinkProperty(BaseProperty):
  def __init__(self, classification, section, name, label, context, options=None, default=None):
    if default is None:
      default = {}

    super().__init__(classification, section, name, label, context, options=options, default=default)

  @property
  def type_name(self):
    return 'page-link'

  def read(self, from_values):
    val = from_values.get(self.name)
    result = {}
    if val is None:
      val = self.default

    result['mode'] = val.get('mode', 'page')
    if result['mode'] not in ['page', 'custom']:
      raise iot_api_core.IotException(400, 'Invalid mode: ' + result['mode'])

    if result['mode'] == 'custom':
      result['url'] = val.get('url')
    else:
      result['instanceId'] = val.get('instanceId')
      if result['instanceId']:
        instance = self.context.lumavate.get('/iot/v1/widget-instances/' + str(result['instanceId']))
        result['url'] = instance['url']
      else:
        result['url'] = ''

    self.value = result
    return result
