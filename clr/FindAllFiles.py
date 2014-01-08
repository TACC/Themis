from __future__ import print_function
from BaseTask   import BaseTask
from Engine     import MasterTbl, Error, files_in_tree
from Dbg        import Dbg
import os

dbg = Dbg()

class FindAllFiles(BaseTask):
  def __init__(self,name):
    BaseTask.__init__(self, name)

  def execute(self, *args, **kwargs):
    masterTbl         = MasterTbl()
    test_rpt_root_dir = masterTbl['testRptRootDir']
    keep              = masterTbl['keep']
    
    fileA = files_in_tree(test_rpt_root_dir,"*.rtm")
    
    fileA = sorted(fileA)
    
    if (keep > 0):
      del fileA[-keep:]
      
    masterTbl['fileA'] = fileA
    
    
