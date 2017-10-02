import iot_api_core
import behavior
from flask import redirect

class InstanceVersion:
  class InstanceVersionBehavior(iot_api_core.InstanceVersionBaseBehavior):
    def __init__(self, namespace, instance_id):
      super().__init__('redirect', namespace, instance_id)
      self._properties = None

    @property
    def components(self):
      f = iot_api_core.Components.ComponentFactory

      return [
        f(iot_api_core.Components.SimpleToolbarComponent, self)
      ]

    @property
    def properties(self):
      if self._properties is None:
        self._properties = [
          iot_api_core.ExperienceProperty(None, None, 'experienceId', 'Experience', self),
          self.instance_name_property(),
          self.instance_page_type_property(),
          self.page_security_property,
          iot_api_core.TextProperty('General','General Settings','redirectURL','Redirect URL',self, default='')
        ]

      return self._properties

    def get_config_data(self):
      config = super().get_config_data()
      lang = 'en-us'

      toolbar = config.get('toolbar', {}).get('componentData', {})

      result = {
        'toolbar': {
          'backgroundColor': toolbar.get('backgroundColor', '#000000'),
          'color': toolbar.get('color', '#ffffff'),
          'title': toolbar.get('title', { lang: 'My Support' })
        }
      }

      return self.handle_language_fields(result)

    def get_widget_data(self):
      instance = self.rest_get_single(self.instance_id)
      return instance[self.get_current_version() + 'Version']['data']
