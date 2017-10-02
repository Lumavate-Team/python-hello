from .base import BaseProperty

class TranslatedTextProperty(BaseProperty):
  def __init__(self, classification, section, name, label, context, default=None, rows=0):
    options = {'rows': rows}
    super().__init__(classification, section, name, label, context, default=default, options=options)

  @property
  def type_name(self):
    return 'translated-text'

  def read(self, from_values):
    val = from_values.get(self.name)
    if val is None:
      val = self.default

    if not isinstance(val, dict):
      val = {'en-us': str(val)}

    return val
