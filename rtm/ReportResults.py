from __future__      import print_function
from BaseTask        import BaseTask
from Engine          import MasterTbl, Error
from Dbg             import Dbg
from Tst             import Tst
from getTerminalSize import getTerminalSize
import os

dbg = Dbg()

class ReportResults(BaseTask):
  def __init__(self,name):
    BaseTask.__init__(self, name)

  def execute(self, *args, **kwargs):
    masterTbl   = MasterTbl()
    rows, width = getTerminalSize()
    rptT        = masterTbl['rptT']
    humanDataA  = ()
    tstSummaryT = masterTbl['tstSummaryT']
    
    
