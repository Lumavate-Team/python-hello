from .base import BaseProperty
import iot_api_core

class NumericProperty(BaseProperty):
  def __init__(self, classification, section, name, label, context, default=None, min_value=None, max_value=None):
    number_options = {
      'min': min_value,
      'max': max_value
    }
    super().__init__(classification, section, name, label, context, options=number_options, default=default)

  @property
  def type_name(self):
    return 'numeric'

  def read(self, from_values):
    val = from_values.get(self.name)
    if val is None:
      val = self.default

    try:
     val = int(val)

    except Exception as e:
      raise iot_api_core.IotException(400, 'Invalid Number: ' + str(val))

    if (self.options['min'] is not None and val < self.options['min']) or (self.options['max'] is not None and val > self.options['max']):
      raise iot_api_core.IotException(400, 'Invalid Number: ' + str(val) + ' - must be in range ' + str(self.options['min']) + ' to ' + str(self.options['max']))

    self.value = val
    return str(val)

