#!/usr/bin/env python
# -*- python -*-

from __future__ import print_function
from Engine     import Engine, MasterTbl
import sys

def main():

  masterTbl  = MasterTbl()
  engine     = Engine()
  projectDir = sys.argv[1]
  del sys.argv[0:2]
  
  
  execDir, execName = engine.split_cmdname(sys.argv[0])

  return engine.execute(projectDir, execDir, execName)


if ( __name__ == '__main__'):
  iret = main()
  sys.exit(iret)
