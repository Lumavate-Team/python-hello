from .checkbox import CheckboxProperty

class ToggleProperty(CheckboxProperty):
  @property
  def type_name(self):
    return 'toggle'
