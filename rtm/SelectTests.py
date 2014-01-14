from __future__ import print_function
from BaseTask   import BaseTask
from Engine     import MasterTbl, Error
from Dbg        import Dbg
from Tst        import Tst
import os, sys

dbg = Dbg()

class SelectTests(BaseTask):
  def __init__(self,name):
    super(SelectTests, self).__init__(name)

  def execute(self, *args, **kwargs):
    masterTbl     = MasterTbl()
    gauntlet      = masterTbl['gauntlet']
    candidateTstT = masterTbl['candidateTstT']

    setNP = False
    procA = [ 0, sys.maxsize]
    if (masterTbl['minNP']):
      setNP = True
      procA[0] = masterTbl['minNP']

    if (masterTbl['maxNP']):
      setNP = True
      procA[1] = masterTbl['maxNP']
      
    if (setNP):
      gauntlet.add("NP", procA)
      
    gauntlet.add("keywords", masterTbl['keywordA'])
    gauntlet.add("restart",  masterTbl['restartA'])
    gauntlet.apply(candidateTstT)

    tstT = masterTbl['tstT']
    rptT = masterTbl['rptT']

    #-------------------------------------------------------
    #  Only run active tests.

    analyze_flg = masterTbl['analyze_flg']
    for ident in candidateTstT:
      tst = candidateTstT[ident]
      if (analyze_flg or tst.get('report')):
        rptT[ident] = tst
      elif (tst.get('active')):
        tstT[ident] = tst
        rptT[ident] = tst
        
  

    
    
    
