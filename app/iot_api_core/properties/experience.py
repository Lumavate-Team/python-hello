from .int import IntProperty

class ExperienceProperty(IntProperty):
  @property
  def type_name(self):
    return 'experienceId'

  def read(self, from_values):
    val = super().read(from_values)

    try:
      self.temp['experience-info'] = self.context.lumavate.get('/model/v1/experience/' + str(val))
      self.temp['modelNumbers'] = self.temp['experience_info']['selectedModelNumbers']
      if self.temp['modelNumbers'] is None:
        self.temp['modelNumbers'] = []

    except Exception as e:
      pass

    try:
      self.temp['model-info'] = self.context.lumavate.get('/model/v1/models/' + str(self.temp['experience-info'].get('modelId')))
      self.temp['modelYear'] = self.temp['model-info']['modelYear']
    except Exception as e:
      pass

    self.value = val
    return val
