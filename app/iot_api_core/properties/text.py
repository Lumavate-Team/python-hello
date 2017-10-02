from .base import BaseProperty

class TextProperty(BaseProperty):
  def __init__(self, classification, section, name, label, context, default=None, rows=0, readonly=False):
    options = {'rows': rows, 'readonly':readonly}
    super().__init__(classification, section, name, label, context, default=default, options=options)

  @property
  def type_name(self):
    return 'text'

  def read(self, from_values):
    val = from_values.get(self.name)
    if val is None:
      val = self.default

    self.value = val
    return str(val)
