from __future__ import print_function
from BaseTask   import BaseTask
from Engine     import MasterTbl
from Dbg        import Dbg
from Engine     import find_fn_in_dir_tree
import os, re

dbg = Dbg()

def find_package_name(projectDir, fn):
  if (projectDir == fn):
    return ""

  patternStr  = "^" + re.escape(projectDir) + "/(.*)"
  pattern     = re.compile(patternStr)
  m           = pattern.search(fn)
  pathA       = m.group(1).split("/")
  packageName = pathA[0]

  return packageName

class ReadProject(BaseTask):
  def __init__(self,name):
    super(ReadProject, self).__init__(name)

  def execute(self, *args, **kwargs):
    masterTbl                = MasterTbl()
    projectDir               = find_fn_in_dir_tree(os.getcwd(), masterTbl['projectFn'])
    packageName              = find_package_name(projectDir, os.getcwd())
    masterTbl['projectDir']  = projectDir
    masterTbl['packageName'] = packageName
    masterTbl['packageDir']  = os.path.join(projectDir,packageName)
    dbg.print("projectDir:  ", masterTbl['projectDir'],  "\n")
    dbg.print("packageName: ", masterTbl['packageName'], "\n")
    dbg.print("packageDir:  ", masterTbl['packageDir'],  "\n")
  
