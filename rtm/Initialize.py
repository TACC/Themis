from __future__   import print_function
from BaseTask     import BaseTask
from Engine       import MasterTbl, Error, get_platform, full_date_string
from Dbg          import Dbg
from Gauntlet     import Gauntlet, GauntletData
from Version      import Version
import os,  time, sys

dbg = Dbg()


class Initialize(BaseTask):
  def __init__(self,name):
    super(Initialize, self).__init__(name)

  def execute(self, *args, **kwargs):
    masterTbl                  = MasterTbl()
    version                    = Version()
    epoch                      = time.time()
    masterTbl['testreportLoc'] = 'testreports'
    masterTbl['testReportDir'] = os.path.join(masterTbl['projectDir'],
                                              masterTbl['testreportLoc'])
    masterTbl['testRptExt']    = '.rtm'
    masterTbl['descriptExt']   = '.desc'
    masterTbl['ThemisVersion'] = 'Themis ' + version.tag()
    masterTbl['currentEpoch']  = epoch
    masterTbl['origEpoch']     = masterTbl['currentEpoch']
    masterTbl['target']        = os.environ.get("TARG_SUMMARY") or ""
    masterTbl['errors']        = 0
    masterTbl['diffCount']     = 0
    masterTbl['failCount']     = 0
    masterTbl['resultMaxLen']  = 12
    masterTbl['minNP']         = 0
    masterTbl['maxNP']         = sys.maxsize

    #------------------------------------------------------------
    # Add projectDir to PYTHONPATH for user functions
    sys.path.append(masterTbl['projectDir'])
    unameT                     = get_platform()
    currentUUID = full_date_string(epoch) + "-" + unameT['os_mach']
    for k in unameT:
      masterTbl[k] = unameT[k]
    
    masterTbl['hostname'] = unameT['machine']
    #------------------------------------------------------------
    # Setup gauntlet
    masterTbl['gauntlet'] = Gauntlet(GauntletData())

    # masterTbl['gauntlet'] = None --> for later

    masterTbl['candidateTstT'] = {}
    masterTbl['tstT'] = {}
    masterTbl['rptT'] = {}
