from __future__ import print_function
from BaseTask   import BaseTask
from Engine     import MasterTbl, Error
from Dbg        import Dbg
from fnmatch    import fnmatch
import os,  sys, json

dbg = Dbg()

def files_in_tree(path,pattern):
  fileA = []
  for root, dirs, files in os.walk(path):
    for name in files:
      fn = os.path.join(root, name)
      if (fnmatch(fn,pattern)):
        fileA.append(fn)
  return fileA  

class FindTests(BaseTask):
  def __init__(self,name):
    BaseTask.__init__(self, name)

  def execute(self, *args, **kwargs):
    masterTbl = MasterTbl()
    pargs     = masterTbl['pargs']        

    if (len(pargs) < 1):
      pargs.append(".")
    

    
    for v in pargs:
      if (os.path.isfile(v) and fnmatch(v,"*.desc")):
        self.read_test_descript(v)
      elif (os.path.isdir(v)):
        fileA = files_in_tree(v,"*.desc")
        for fn in fileA:
          self.read_test_descript(fn)

  def read_test_descript(fn):
    masterTbl    = MasterTbl()
    epoch        = masterTbl['epoch']
    testdescript = 

    
