from __future__ import print_function
from BaseTask   import BaseTask
from Engine     import MasterTbl
from Dbg        import Dbg

dbg = Dbg()

class A(BaseTask):
  def __init__(self,name):
    super(A, self).__init__(name)

  def execute(self, *args, **kwargs):

    s = dbg.indent_string()
    print(s, "In class A", sep = "")
    masterTbl = MasterTbl()
    print(s, "masterTbl['abc']: ", masterTbl['abc'], sep = "")
