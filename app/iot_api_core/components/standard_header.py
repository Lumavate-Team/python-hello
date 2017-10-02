from .base_component import BaseComponent
import iot_api_core

class StandardHeaderComponent(BaseComponent):
  @property
  def component_type(self):
    return 'standard-header'

  @property
  def label(self):
    return 'Standard Header'

  @property
  def category(self):
    return 'header'

  @property
  def properties(self):
    return [
      iot_api_core.ToggleProperty(None, None, 'displayHeader', 'Display Header', self.context, default=True),
      iot_api_core.ToggleProperty(None, None, 'displayImage', 'Display Header Image', self.context, default=True),
      iot_api_core.ModelImageProperty(None, None, 'image', 'Header Image', self.context),
      iot_api_core.ToggleProperty(None, None, 'displayTitle', 'Display Header Title', self.context, default=True),
      iot_api_core.HeaderTitleProperty(None, None, 'title', 'Header Title', self.context),
      iot_api_core.ColorProperty(None, None, 'backgroundColor', 'Header Background Color', self.context, default='#cccccc'),
    ]
