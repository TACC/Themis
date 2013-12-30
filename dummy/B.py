from __future__ import print_function
from BaseTask   import BaseTask
from Engine     import MasterTbl
from Dbg        import Dbg

dbg = Dbg()

class B(BaseTask):
  def __init__(self,name):
    BaseTask.__init__(self, name)

  def execute(self, *args, **kwargs):
    print(dbg.indent_string(), "In class B", sep = "")

    # for i,v in enumerate(args):
    #   print(dbg.indent_string(), i,v, sep="")
    #
    # for key in kwargs:
    #   print(dbg.indent_string(), key, kwargs[key])
      
    
