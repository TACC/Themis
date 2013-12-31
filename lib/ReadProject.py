from __future__ import print_function
from BaseTask   import BaseTask
from Engine     import MasterTbl
from Dbg        import Dbg

dbg = Dbg()

class ReadProject(BaseTask):
  def __init__(self,name):
    BaseTask.__init__(self, name)

  def execute(self, *args, **kwargs):

    s = dbg.indent_string()
    print(s, "In class", self.name(), sep = "")
