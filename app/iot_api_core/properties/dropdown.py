from .base import BaseProperty
import iot_api_core

class DropdownProperty(BaseProperty):
  def __init__(self, classification, section, name, label, context, default=None, options=None):
    if options is None:
      options = {}

    super().__init__(classification, section, name, label, context, options=options, default=default)

  @property
  def type_name(self):
    return 'dropdown'

  def read(self, from_values):
    val = from_values.get(self.name)
    check_hash = { str(x): x for x in self.options }
    check_hash['None'] = None

    if val is None:
      val = self.default

    if str(val) not in check_hash:
      raise iot_api_core.IotException(400, 'Invalid Value: ' + str(val) + ' - must be in set ' + ','.join(list(self.options.keys())))

    self.value = check_hash[str(val)]

    return self.value
