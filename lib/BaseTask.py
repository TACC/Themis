
class BaseTask:
  def __init__(self, name, **kwargs):
    self.__name = name

  def name(self):
    return self.__name

    
