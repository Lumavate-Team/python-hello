class IotException(Exception):
  def __init__(self, code, message):
    self.code = code
    self.message = message
    return super().__init__(message)
