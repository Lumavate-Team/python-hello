from .base_component import BaseComponent
from flask import request, current_app
import iot_api_core

class LocationComponent(BaseComponent):
  @property
  def component_type(self):
    return 'location'

  @property
  def label(self):
    return 'Location'

  @property
  def properties(self):
    return [
      iot_api_core.TextProperty(None, None, 'address', 'Address', self.context, rows=3, default='46033'),
      iot_api_core.NumericProperty(None, None, 'height', 'Height', self.context, default=200, min_value=50, max_value=500),
      iot_api_core.NumericProperty(None, None, 'mapZoom', 'Map Zoom', self.context, default=12, min_value=12, max_value=21),
    ]

  def load(self, data):
    super().load(data)
    print(self.data['address'], flush=True)
    coord = self.context.lumavate.post('/iot/v1/geocode/coordinates', {'address': self.data['address']})
    self.data.update(coord)
