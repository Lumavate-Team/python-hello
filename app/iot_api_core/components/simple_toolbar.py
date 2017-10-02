from .base_component import BaseComponent
from flask import request, current_app
import iot_api_core

class SimpleToolbarComponent(BaseComponent):
  @property
  def component_type(self):
    return 'simple-toolbar'

  @property
  def label(self):
    return 'Standard Toolbar'

  @property
  def category(self):
    return 'toolbar'

  @property
  def properties(self):
    return [
      iot_api_core.TranslatedTextProperty(None, None, 'title', 'Toolbar Title', self.context, rows=0, default=''),
      iot_api_core.ColorProperty(None, None, 'backgroundColor', 'Toolbar Background Color', self, default='#000000'),
      iot_api_core.ColorProperty(None, None, 'color', 'Toolbar Text Color', self, default='#ffffff')
    ]

