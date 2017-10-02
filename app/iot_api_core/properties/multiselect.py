from .base import BaseProperty
import iot_api_core

class MultiselectProperty(BaseProperty):
  def __init__(self, classification, section, name, label, context, default=None, options=None):
    if options is None:
      options = {}

    if default is None:
      default = []

    super().__init__(classification, section, name, label, context, options=options, default=default)

  @property
  def type_name(self):
    return 'multiselect'

  def read(self, from_values):
    val = from_values.get(self.name)

    check_hash = { str(x['value']): x['value'] for x in self.options }
    check_hash['None'] = None

    if val is None:
      val = self.default

    val = [check_hash[str(x)] for x in val if check_hash.get(str(x))]
    self.value = val

    return val
