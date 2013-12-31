from __future__ import print_function
from BaseTask   import BaseTask
from Dbg        import Dbg
import os, sys, imp

master = {}

dbg = Dbg()

def MasterTbl():
  return master

def load_from_file(search_dirA, mod_name):
  class_inst = None
  expected_class = 'BaseTask'
  extA = [ ".py", ".pyc" ]

  fn     = None
  fn_ext = None
  found  = False
  for d in search_dirA:
    for ext in extA:
      fn = os.path.join(d, mod_name+ext)
      if (os.path.exists(fn)):
        file_ext = ext
        found = True
        break
    if (found): break

  if (file_ext == '.py'):
    py_mod = imp.load_source(mod_name, fn)
  elif (file_ext == '.pyc'):
    py_mod = imp.load_compiled(mod_name, fn)

  if hasattr(py_mod, expected_class):
    class_inst = py_mod.__dict__[mod_name](mod_name)

  return class_inst

def task(name, *args, **kwargs):
  masterTbl = MasterTbl()
  my_task   = load_from_file(masterTbl['task_searchA'], name)
  dbg.start(name, *args, **kwargs)
  my_task.execute(*args, **kwargs)
  dbg.fini(name)
  
class Engine:

  def __init__(self):
    pass
    
  def split_cmdname(self, path):
    return os.path.split(path)

  def load_project_data(self, projectDir):
    fn = os.path.join(projectDir,"Themis.py")
    s  = open(fn).read()
    exec(s)
    return ProjectData


  def execute(self, themis_project_dir, execDir, execName):
    masterTbl                  = MasterTbl()
    taskDir                    = os.path.join(themis_project_dir, execName)
    masterTbl['taskDir']       = taskDir
    masterTbl['themisPrjDir']  = themis_project_dir
    ProjectData                = self.load_project_data(themis_project_dir)
    masterTbl["ThemisVersion"] = ProjectData['ThemisVersion']     
    masterTbl['task_searchA']  = (taskDir, os.path.join(themis_project_dir,"lib"))

    taskFileName               = os.path.join(taskDir, execName + ".tasks")
    exec(open(taskFileName).read())
    
    verboseCount = 0
    debugCount   = 0
    for v in sys.argv:
      if (v == "-v" or v == "--verbose"): verboseCount += 1
      if (v == "-D" or v == "--debug"  ): debugCount   += 1

    if (verboseCount + debugCount > 0):
      dbg.activateDebug()

    dbg.start("Engine")
    iret = taskMain()
    dbg.fini("Engine")

    return iret

    
  
