from __future__ import print_function
from BaseTask   import BaseTask
import os, sys

master = {}

def MasterTbl():
  return master


def task():
  pass


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


  def execute(self, projectDir, execDir, execName):
    masterTbl                  = MasterTbl()
    taskDir                    = os.path.join(projectDir, execName)
    masterTbl['taskDir']       = taskDir

    ProjectData                = self.load_project_data(projectDir)
    masterTbl["ThemisVersion"] = ProjectData['ThemisVersion']     

    sys.path.append(taskDir)

    taskFileName               = os.path.join(taskDir, execName + ".tasks")
    exec(open(taskFileName).read())
    
    

    return 

    
  
