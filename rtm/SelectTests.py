from __future__ import print_function
from BaseTask   import BaseTask
from Engine     import MasterTbl, Error
from Dbg        import Dbg
from Tst        import Tst
import os

dbg = Dbg()

class SelectTests(BaseTask):
  def __init__(self,name):
    BaseTask.__init__(self, name)

  def execute(self, *args, **kwargs):
    masterTbl = MasterTbl()

    candidateTstT = masterTbl['candidateTstT']

    tstT = masterTbl['tstT']
    rptT = masterTbl['rptT']

    #-------------------------------------------------------
    #  Currently all tests are selected

    for ident in candidateTstT:
      tst         = candidateTstT[ident]
      tstT[ident] = tst
      rptT[ident] = tst
  

    
    
    
