from .base import BaseProperty
import iot_api_core

class ComponentsProperty(BaseProperty):
  def __init__(self, classification, section, name, label, context, category, default=None):
    options = { 'categories': [category] }
    super().__init__(classification, section, name, label, context, options=options, default=default)
    self.category = category

  @property
  def type_name(self):
    return 'components'

  def read(self, from_values):
    self.component_lookup = {
      x.type: x.instantiate
      for x in self.context.components if x.category == self.category
    }

    val = from_values.get(self.name)
    if val is None:
      val = self.default

    components = []
    for c in val:
      comp_values = {}

      component_type = c.get('componentType', '__NOTYPE__')
      component_data = c.get('componentData', {})
      component_factory = self.component_lookup.get(component_type)
      if component_factory:
        component = component_factory()
        component.load(component_data)
        result = {
          'componentType': component.component_type,
          'componentData': component.to_json(),
          'displayName': component.display_name
        }
        components.append(result)
      else:
        raise iot_api_core.IotException(400, 'Invalid Value: ' + component_type)

    self.value = components
    return components
