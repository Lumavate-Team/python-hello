from .base import BaseProperty
import iot_api_core

class IntProperty(BaseProperty):
  @property
  def type_name(self):
    return 'int'

  def read(self, from_values):
    val = from_values.get(self.name)
    if val is None:
      val = self.default

    try:
      if val is not None:
        val = int(val)

    except:
      raise iot_api_core.IotException(400, 'Invalid Int: ' + str(val))

    self.value = val
    return val
