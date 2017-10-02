from .base import BaseProperty

class CheckboxProperty(BaseProperty):
  @property
  def type_name(self):
    return 'checkbox'

  def read(self, from_values):
    val = from_values.get(self.name)
    if val is None:
      val = self.default

    return str(val).lower() == 'true'
