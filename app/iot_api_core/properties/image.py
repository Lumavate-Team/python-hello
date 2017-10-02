from .base import BaseProperty
import iot_api_core
from .image_base import ImageBase

class ImageProperty(BaseProperty, ImageBase):
  def __init__(self, classification, section, name, label, context, options=None, default=None):
    if default is None:
      default = {}

    super().__init__(classification, section, name, label, context, options=options, default=default)

  @property
  def type_name(self):
    return 'image-upload'

  def read(self, from_values):
    val = from_values.get(self.name)
    if val is None:
      val = self.default

    result = self.read_image(val)

    self.value = result
    return result
