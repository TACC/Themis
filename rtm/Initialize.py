from __future__ import print_function
from BaseTask   import BaseTask
from Engine     import MasterTbl, Error, get_platform, full_date_string
from Dbg        import Dbg
from Version    import Version
import os,  time, sys

dbg = Dbg()


class Initialize(BaseTask):
  def __init__(self,name):
    BaseTask.__init__(self, name)

  def execute(self, *args, **kwargs):
    masterTbl                  = MasterTbl()
    version                    = Version()
    masterTbl['testreportLoc'] = 'testreports'
    masterTbl['testReportDir'] = os.path.join(masterTbl['projectDir'],
                                              masterTbl['testreportLoc'])
    masterTbl['testRptExt']    = '.rtm'
    masterTbl['descriptExt']   = '.desc'
    masterTbl['version']       = 'Themis ' + version.name()
    masterTbl['currentEpoch']  = time.time()
    masterTbl['origEpoch']     = masterTbl['currentEpoch']
    masterTbl['target']        = os.environ.get("TARG_SUMMARY") or ""
    masterTbl['errors']        = 0
    masterTbl['diffCount']     = 0
    masterTbl['failCount']     = 0

    #------------------------------------------------------------
    # Add projectDir to PYTHONPATH for user functions
    sys.path.append(masterTbl['projectDir'])
    unameT                     = get_platform()
    currentUUID = full_date_string() + "-" + unameT['os_mach']
    
    #------------------------------------------------------------
    # Setup gauntlet

    # masterTbl['gauntlet'] = None --> for later

    masterTbl['candidateTsts'] = {}
    masterTbl['tstT'] = {}
    masterTbl['rptT'] = {}
