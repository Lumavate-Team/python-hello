from .base_component import BaseComponent
import iot_api_core

class MainToolbarComponent(BaseComponent):
  @property
  def component_type(self):
    return 'main-toolbar'

  @property
  def label(self):
    return 'Main Toolbar'

  @property
  def category(self):
    return 'toolbar'

  @property
  def properties(self):
    return [
      iot_api_core.ToggleProperty(None, 'Button Properties', 'displayToolbar', 'Display Toolbar', self.context, default=True),
      iot_api_core.ToggleProperty(None, 'Button Properties', 'displayHomeIcon', 'Include Home', self.context, default=True),
      iot_api_core.ToggleProperty(None, 'Button Properties', 'displayShareIcon', 'Include Share', self.context, default=True),
      iot_api_core.ToggleProperty(None, 'Button Properties', 'displaySettingsIcon', 'Include Settings', self.context, default=True),
      iot_api_core.ColorProperty(None, 'Toolbar Color', 'backgroundColor', 'Background Color', self.context, default='#000000'),
      iot_api_core.ColorProperty(None, 'Toolbar Color', 'iconColor', 'Icon Color', self.context, default='#ffffff'),
      iot_api_core.ColorProperty(None, 'Toolbar Color', 'selectedColor', 'Selected Color', self.context, default='#ffffff'),
    ]
