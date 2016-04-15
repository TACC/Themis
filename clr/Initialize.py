from __future__ import print_function
from BaseTask   import BaseTask
from Engine     import MasterTbl, Error, get_platform
from Dbg        import Dbg
import os

dbg = Dbg()

class Initialize(BaseTask):
  def __init__(self,name):
    super(Initialize, self).__init__(name)

  def execute(self, *args, **kwargs):
    masterTbl = MasterTbl()
    masterTbl['testRptLoc']     = "testreports"
    masterTbl['testRptExt']     = ".rtm"
    masterTbl['descriptExt']    = ".desc"
    masterTbl['testRptRootDir'] = os.path.join(masterTbl['projectDir'], masterTbl['testRptLoc'])
    platformT                   = get_platform()

    masterTbl['os_mach']  = platformT['os_mach']
    masterTbl['hostname'] = platformT['node']
    masterTbl['target']   = platformT.get('targ_summary',"")
    
    
    
