from __future__ import print_function
from BaseTask   import BaseTask
from Engine     import MasterTbl, Error, files_in_tree
from Dbg        import Dbg
from fnmatch    import fnmatch
from Tst        import Tst
import os, re, json

dbg = Dbg()
testDirPat = re.compile('(.*)/([^/]*)/(.*)')
fnIdPat    = re.compile('([^/]*)/(.*)')

def build_tstT(fn, test_descript, epoch):
  tstT = {}

  for idx, v in enumerate(test_descript.get('tests',[])):
    tst         = Tst(v, fn, test_descript, epoch, idx)
    ident       = tst.get('id')
    tstT[ident] = tst

  return tstT

class FindTests(BaseTask):
  def __init__(self,name):
    super(FindTests, self).__init__(name)

  def execute(self, *args, **kwargs):
    masterTbl = MasterTbl()
    pargs     = masterTbl['pargs']        

    if (len(pargs) < 1):
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

  def find_last_rtm(self, pargs):
    masterTbl = MasterTbl()
    fileA     = files_in_tree(masterTbl['testReportDir'], "*.rtm")
    fileA     = sorted(fileA)
    pargs.append(fileA[-1])

  def read_rtm_file(self, fn):
    masterTbl  = MasterTbl()
    rptT       = json.loads(open(fn).read())
    testA      = rptT['testA']
    projectDir = masterTbl['projectDir']

    fileA = []
    for tst in testA:
      ident = tst['id']
      m = testDirPat.search(ident)
      
      if (not m):
        m      = fnIdPat.search(ident)
        my_dir = "./"
        fn     = m.group(1)
        idTag  = m.group(2)
      else:
        my_dir = m.group(1)
        fn     = m.group(2)
        idTag  = m.group(3)

      fileA.append(os.path.join(projectDir,my_dir, fn + ".desc"))

    for fn in fileA:
      self.read_test_descript(fn)
      
    tstkeyA = Tst.test_fields()
    candidateTstT = masterTbl['candidateTstT']

    #--------------------------------------------------------
    #  Copy results from previous run to current test.
    #  Active is controlled by user input not last run.
    for v in testA:
      ident       = v['id']
      tst         = candidateTstT[ident]
      v['active'] = tst.get('active')
      for key in tstkeyA:
        tst.set(key,v[key])

  def read_test_descript(self, fn):
    masterTbl     = MasterTbl()
    epoch         = masterTbl['currentEpoch']
    candidateTstT = masterTbl['candidateTstT']

    dbg.print("Found: ",fn,"\n")

    exec(open(fn).read())
    
    tstT = build_tstT(fn, test_descript, epoch)

    for ident in tstT:
      candidateTstT[ident] = tstT[ident]
    
    
    
