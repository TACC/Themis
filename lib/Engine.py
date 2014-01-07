from __future__ import print_function
from BaseTask   import BaseTask
from Dbg        import Dbg
from time       import localtime
import os, sys, imp, platform, re

master = {}

dbg = Dbg()

bad_charPat = re.compile('[ &\'"!(){}@#\]]')

def MasterTbl():
  return master

def fix_filename(fn):
  return bad_charPat.sub("_",fn)

def __print_tool(prefix, *a):
  sA = []
  sA.append(dbg.indent_string())
  sA.append(prefix)
  for v in a:
    sA.append(str(v))
  sA.append("\n")
  sys.stderr.write("".join(sA))

def Warning(*a):
  __print_tool("Warning: ",*a)

def Error(*a):
  __print_tool("Error: ",*a)
  sys.exit(-1)

def full_date_string(epoch):
  ymd = localtime(epoch)
  s   = '{:}_{:02}_{:02}_{:02}_{:02}_{:02}'.format(ymd.tm_year, ymd.tm_mon, ymd.tm_mday,
                                                   ymd.tm_hour, ymd.tm_min, ymd.tm_sec)
  return s

def get_platform():
  unameA  = platform.uname()
  nameA   = ('system', 'node', 'release', 'version', 'machine', 'processor')
  unameT  = {}
  targ_summary = os.environ.get("TARG_SUMMARY")
  if (targ_summary):
    unameT['targ_summary'] = targ_summary



  for idx in xrange(len(nameA)):
    unameT[nameA[idx]] = unameA[idx]

  unameT['os_mach'] = unameT['system'] + '-' + unameT['machine']
  return unameT


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

def find_fn_in_dir_tree(wd,fn):
  cwd        = os.getcwd()
  result_dir = None

  os.chdir(wd)

  while (True):
    fullFn = os.path.join(wd, fn)
    if (os.path.exists(fullFn)):
      result_dir = wd
      break
    if (wd == "/"):
      break
    os.chdir("..")
    wd = os.getcwd()

  if (result_dir == None):
    Error("You must be in a project!  Did not find: ", fn)
  os.chdir(cwd)
  return result_dir

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

  def load_project_data(self, projectDir, projectFn):
    fn = os.path.join(projectDir,projectFn)
    s  = open(fn).read()
    exec(s)
    return ProjectData


  def execute(self, themis_project_dir, execDir, execName):
    masterTbl                  = MasterTbl()
    taskDir                    = os.path.join(themis_project_dir, execName)
    masterTbl['taskDir']       = taskDir
    masterTbl['themisPrjDir']  = themis_project_dir
    defaultPrjFn               = "Themis.py"
    
    ProjectData                = self.load_project_data(themis_project_dir, defaultPrjFn)
    masterTbl['projectFn']     = ProjectData.get('projectFn', defaultPrjFn)
    masterTbl["ThemisVersion"] = ProjectData['ThemisVersion']
    masterTbl['task_searchA']  = (taskDir, os.path.join(themis_project_dir,"lib"))

    taskFileName               = os.path.join(taskDir, execName + ".tasks")
    sys.path.append(taskDir)


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

    
  
