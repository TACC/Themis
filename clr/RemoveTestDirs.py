from __future__ import print_function
from BaseTask   import BaseTask
from Engine     import MasterTbl, Error, files_in_tree
from Dbg        import Dbg
import os, json, shutil, re

dbg = Dbg()
testDirPat = re.compile('(.*)/([^/]*)/(.*)')
fnIdPat    = re.compile('([^/]*)/(.*)')


class RemoveTestDirs(BaseTask):
  def __init__(self,name):
    BaseTask.__init__(self, name)

  def execute(self, *args, **kwargs):
    masterTbl  = MasterTbl()
    fileA      = masterTbl['fileA']
    projectDir = masterTbl['projectDir']
    keep       = masterTbl['keep']
    
    for rpt in fileA:
      self.removeDir(projectDir, keep, rpt)
      os.remove(rpt)
 
  def removeDir(self, projectDir, keep, rpt):
    dbg.start("RemoveTestDirs",rpt)
    rptT  = json.loads(open(rpt).read())
    testA = rptT['testA']

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
      

      outputDir = os.path.join(projectDir, tst['outputDir'])
      if (os.path.isdir(outputDir)):
        dbg.print("rm -rf ",outputDir,"\n")
        shutil.rmtree(outputDir)
        
      id_dir = os.path.join(projectDir, my_dir, idTag)
      listA  = files_in_tree(id_dir, "*")
      
      if (len(listA) == 0 or keep == 0):
        dbg.print("rm -rf ",id_dir,"\n")
        shutil.rmtree(id_dir)

    dbg.fini("RemoveTestDirs")
        
    
      
    
    
    
