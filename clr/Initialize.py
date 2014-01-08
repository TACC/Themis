from __future__ import print_function
from BaseTask   import BaseTask
from Engine     import MasterTbl, Error, get_platform
from Dbg        import Dbg
from Tst        import Tst
import os

dbg = Dbg()

class Initialize(BaseTask):
  def __init__(self,name):
    BaseTask.__init__(self, name)

  def execute(self, *args, **kwargs):
    masterTbl = MasterTbl()
    masterTbl['testRptLoc']     = "testreports"
    masterTbl['testRptExt']     = ".rtm"
    masterTbl['descriptExt']    = ".desc"
    masterTbl['testRptRootDir'] = os.path.join(masterTbl.projectDir, masterTbl.testRptLoc)
    platformT                   = get_platform()

    masterTbl.os_mach  = platformT['os_mach']
    masterTbl.hostname = platformT['hostName']
    masterTbl.target   = platformT['target']
    
    
    
