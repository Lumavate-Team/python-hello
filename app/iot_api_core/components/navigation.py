from .base_component import BaseComponent
import iot_api_core

class NavigationComponent(BaseComponent):
  @property
  def component_type(self):
    return 'nav-button'

  @property
  def label(self):
    return 'Navigate'

  @property
  def display_name(self):
    return self.label + ' - ' + str(self.data.get('title', {}).get('en-us'))

  @property
  def properties(self):
    return [
      iot_api_core.ImageProperty(None, None, 'imageUrl', 'Image Url', self.context),
      iot_api_core.TranslatedTextProperty(None, None, 'title', 'Title', self.context, default='Example Button'),
      iot_api_core.TranslatedTextProperty(None, None, 'description', 'Description', self.context, default='Example Description'),
      iot_api_core.PageLinkProperty(None, None, 'pageLink', 'Navigate To', self.context)
    ]
