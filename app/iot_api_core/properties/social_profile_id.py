from .int import IntProperty

class SocialProfileIdProperty(IntProperty):
  @property
  def type_name(self):
    return 'socialProfileId'

  def read(self, from_values):
    val = super().read(from_values)

    try:
      self.temp['social_profile_info'] = self.lumavate.get('/model/v1/social/profiles/' + str(version_data['data']['socialProfileId']))
    except:
      pass

    self.value = val
    return val

