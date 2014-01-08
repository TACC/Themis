from __future__ import print_function
from BaseTask   import BaseTask
from Engine     import MasterTbl, Error, files_in_tree
from Dbg        import Dbg
from fnmatch    import fnmatch
from Tst        import Tst
import os

dbg = Dbg()

def build_tstT(fn, test_descript, epoch):
  tstT = {}

  for idx, v in enumerate(test_descript.get('tests',[])):
    tst         = Tst(v, fn, test_descript, epoch, idx)
    ident       = tst.get('id')
    tstT[ident] = tst

  return tstT

class FindTests(BaseTask):
  def __init__(self,name):
    BaseTask.__init__(self, name)

  def execute(self, *args, **kwargs):
    masterTbl = MasterTbl()
    pargs     = masterTbl['pargs']        

    if (len(pargs) < 1):
      restartA = 
      if (masterTbl['restartA'] or masterTbl['analyze_flg']):
        self.find_last_rtm(pargs)
      else:
        pargs.append(".")
   
    
    
    
    for v in pargs:
      if (os.path.isfile(v) and fnmatch(v,"*.desc")):
        self.read_test_descript(v)
      elif(fnmatch(v,"*.rtm")):
        self.read_rtm_file(v)

      elif (os.path.isdir(v)):
        fileA = files_in_tree(v,"*.desc")
        for fn in fileA:
          self.read_test_descript(fn)

  def read_test_descript(self, fn):
    masterTbl     = MasterTbl()
    epoch         = masterTbl['currentEpoch']
    candidateTstT = masterTbl['candidateTstT']

    dbg.print("Found: ",fn,"\n")

    exec(open(fn).read())
    
    tstT = build_tstT(fn, test_descript, epoch)

    for ident in tstT:
      candidateTstT[ident] = tstT[ident]
    
    
    
