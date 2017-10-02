from .base_component import BaseComponent
from flask import request, current_app
import iot_api_core

class TextComponent(BaseComponent):
  @property
  def component_type(self):
    return 'text'

  @property
  def label(self):
    return 'Text'

  @property
  def properties(self):
    return [
      iot_api_core.TranslatedTextProperty(None, None, 'value', 'Text', self.context, rows=5, default=''),
      iot_api_core.ColorProperty(None, None, 'color', 'Color', self, default='#000000'),
      iot_api_core.ColorProperty(None, None, 'backgroundColor', 'Background Color', self, default='rgba(0,0,0,0)'),
      iot_api_core.DropdownProperty(None, None, 'fontSize', 'Font Size', self.context, default='16', options={
        '45': '45',
        '34': '34',
        '24': '24',
        '20': '20',
        '16': '16',
        '14': '14',
        '12': '12'
      }),
      iot_api_core.DropdownProperty(None, None, 'fontWeight', 'Font Weight', self.context, default='400', options={
        '100': '100',
        '300': '300',
        '400': '400',
        '500': '500',
        '700': '700',
        '900': '900'
      }),
      iot_api_core.DropdownProperty(None, None, 'alignment', 'Alignment', self.context, default='left', options={'left': 'Left', 'right': 'Right', 'center': 'Center'}),
      iot_api_core.NumericProperty(None, None, 'padding', 'Padding (pixels)', self.context, default=10, min_value=0, max_value=50),
    ]

