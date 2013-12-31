from __future__ import print_function
from BaseTask   import BaseTask
from Engine     import MasterTbl, Error, get_platform
from Dbg        import Dbg

import os, json, time, platform

dbg = Dbg()

validA = ("passed", "failed", "diff")

class Finish(BaseTask):
  def __init__(self,name):
    BaseTask.__init__(self, name)

  def __parse_input_fn(self, fn):

    if (not os.path.exists(fn)):
      return "failed"
    
    f = open(fn)
    lineA = f.readlines()
    f.close()

    found  = False
    result = "passed"

    for line in lineA:
      line = line.strip()
      if (line[0] == "#" or len(line) < 1):
        continue

      found = True
      idx = line.find(",")
      if (idx > 0):
        line = line[0:idx]
      line = line.lower()
      if (line != "passed"):
        result = line
        break

    if (not result in validA or not found):
      result = "failed"

    return result

  def execute(self, *args, **kwargs):
    masterTbl  = MasterTbl()
    result_fn  = masterTbl['result_fn']
    runtime_fn = masterTbl['runtime_fn']
    input_fn   = masterTbl['pargs'][0]

    result     = self.__parse_input_fn(input_fn)

    my_result = { 'testresult' : result }
    f = open(result_fn,"w")
    f.write(json.dumps(my_result))
    f.close()

    if (not os.path.exists(runtime_fn)):
      Error("Unable to open: ", runtime_fn)

    f = open(runtime_fn)
    runtime = json.loads(f.read())
    f.close()

    t1 = time.time()

    runtime['T1'] = t1
    runtime['TT'] = t1 - runtime['T0']

    unameT = get_platform()

    for k in unameT:
      runtime[k] = unameT[k]

    f = open(runtime_fn,"w")
    f.write(json.dumps(runtime, sort_keys=True, indent=2, separators=(', ', ': ')))
    f.close()
