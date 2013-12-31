from __future__ import print_function
from BaseTask   import BaseTask
from Engine     import MasterTbl
from Dbg        import Dbg
from Engine     import find_fn_in_dir_tree
import os

dbg = Dbg()

class ReadProject(BaseTask):
  def __init__(self,name):
    BaseTask.__init__(self, name)

  def execute(self, *args, **kwargs):
    masterTbl = MasterTbl()
    masterTbl['projectDir'] = find_fn_in_dir_tree(os.getcwd(), masterTbl['projectFn'])
    dbg.print("projectDir: ", masterTbl['projectDir'], "\n")
    
