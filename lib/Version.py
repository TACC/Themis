class Version(object):
  def __init__(self):
    pass
  def tag(self):
    return "0.3"
  def git(self):
    return "@git@"
  def date(self):
    return ""
  def name(self):
    sA = []
    sA.append(self.tag())
    sA.append(self.git())
    sA.append(self.date())
    return " ".join(sA)
