from .base_component import BaseComponent
from flask import request, current_app
import iot_api_core

class VideoComponent(BaseComponent):
  @property
  def component_type(self):
    return 'video'

  @property
  def label(self):
    return 'Video'

  @property
  def properties(self):
    return [
      iot_api_core.NumericProperty(None, None, 'padding', 'Padding (pixels)', self.context, default=24, min_value=0, max_value=50),
      iot_api_core.NumericProperty(None, None, 'thickness', 'Thickness (pixels)', self.context, default=4, min_value=1, max_value=10),
      iot_api_core.ColorProperty(None, None, 'color', 'Color', self, default='#cccccc')
    ]

