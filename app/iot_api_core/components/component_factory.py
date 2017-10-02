class ComponentFactory:
  def __init__(self, component_type, context):
    self.component_type = component_type
    self.context = context
    self.type = component_type(context).component_type
    self.category = component_type(context).category

  def instantiate(self):
    return self.component_type(self.context)
