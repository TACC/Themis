from __future__ import print_function
from BaseTask   import BaseTask
from Engine     import MasterTbl, Error
from Dbg        import Dbg
from Tst        import Tst
import os, sys

dbg = Dbg()

class SelectTests(BaseTask):
  def __init__(self,name):
    BaseTask.__init__(self, name)

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
    gauntlet.apply(candidateTstT)

    tstT = masterTbl['tstT']
    rptT = masterTbl['rptT']

    #-------------------------------------------------------
    #  Only run active tests.

    for ident in candidateTstT:
      tst         = candidateTstT[ident]
      dbg.print("select: id: ", ident, ", active: ", tst.get("active"),"\n")

      if (tst.get('active')):
        tstT[ident] = tst
        rptT[ident] = tst
        
  

    
    
    
