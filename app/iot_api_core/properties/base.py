class BaseProperty:
  def __init__(self, classification, section, name, label, context, options=None, default=None):
    self.classification = classification
    self.section = section
    self.name = name
    self.label = label
    self.default = default
    self.options = options
    self.context = context
    self.temp = {}
    self.value = None

  def to_json(self):
    return {
      'classification': self.classification,
      'section': self.section,
      'name': self.name,
      'label': self.label,
      'type': self.type_name,
      'options': self.options
    }

  def delta_doc(self, old_version, new_version):
    if old_version != new_version:
      return new_version

  def publish(self):
    pass
