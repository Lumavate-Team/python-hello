from .base_component import BaseComponent
from flask import request, current_app
import iot_api_core

class SpacerComponent(BaseComponent):
  @property
  def component_type(self):
    return 'spacer'

  @property
  def label(self):
    return 'Spacer'

  @property
  def properties(self):
    return [
      iot_api_core.NumericProperty(None, None, 'height', 'Height (pixels)', self.context, default=16, min_value=0, max_value=50),
      iot_api_core.ColorProperty(None, None, 'color', 'Color', self, default='#cccccc'),
    ]

