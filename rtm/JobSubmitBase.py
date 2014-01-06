from __future__  import print_function
from Dbg         import Dbg
from Tst         import Tst
from Interactive import Interactive
from Batch       import Batch
from Stencil     import Stencil
import os, sys, time, json

dbg = Dbg()

def find_py_file(name):
  for path in sys.path:
    fn = os.path.join(path, name)
    if (os.isfile(fn)):
      return fn

class JobSubmitBase(object):
  def __init__(self)
    pass

  def batchTbl():
    return self.__batchTbl


  def build(self, name, masterTbl, batch_hostname=None):
    self.masterTbl    = masterTbl
    self.resultMaxLen = masterTbl['resultMaxLen']

    batch_hostname = batch_hostname or "INTERACTIVE"
    if (name.lower() == "interactive"):
      obj = Interactive(masterTbl)
    else:
      obj = Batch(masterTbl)

    baseFn    = find_py_file("DefaultSystems.py")
    derivedFn = find_py_file("Systems.py")
    
    exec(open(baseFn).read())
    exec(open(derivedFn).read())

    self.__batchTbl = {}
    if (batch_hostname == "INTERACTIVE"):
      self.__batchTbl = DefaultSystems['INTERACTIVE']
    else:
      for k in Systems:
        if (batch_hostname in Systems[k]):
          self.__batchTbl = DefaultSystems[k].copy()
          self.__batchTbl.update(Systems[k][batch_hostname])
    
    if (not self.__batchTbl):
      Error("Unable to find BatchSystems entry for ",batch_hostname)

    return obj

  def formatMsg(self, result, iTest, passed, failed, num_tests, ident)
    blank    = " "
    r        = result or "failed"
    blankLen = self.resultMaxLen - r:len()
    msg      = "{}{} : {} tst: {}/{} P/F: {}:{}, {}".format(
                           blank*(blankLen),
                           result,
                           date("%X"),
                           iTest, num_tests,
                           passed, failed,
                           ident)

    return msg

  def msg(self, messageStr, iTest, num_tests, ident, resultFn, background)
    masterTbl = self.masterTbl
    msgExtra = ""  
    if (messageStr != "Started" and not background):
      msgExtra = "\n"  
      resultT  = json.loads(open(resultFn).read())
      myResult = resultT.testresult

      if (myResult == "passed"):
        masterTbl['passed'] += 1
      else:
        masterTbl['failed'] += 1

      messageStr = myResult

    print(self.formatMsg(self, messageStr, iTest, masterTbl['passed'],
                           masterTbl['failed'], num_tests, ident)),msgExtra)
      
  def findcmd(tbl):
    result = None
    cmd  = tbl.cmd;
    pathA = split(tbl.path or os.environ['path'] or "", ":")
    for path in pathA:
      fn = os.path.join(path, cmd)
      if (os.path.exists(fn)):
        result = fn
        break
      
    return fn

  def mpr(tbl, envTbl, funcTbl):
    batchTbl = self.batchTbl()
    stencil  = Stencil(tbl=tbl, envTbl=envTbl, funcTbl=funcTbl)
    return stencil.expand(batchTbl['mprCmd'])

  def CWD(tbl, envTbl, funcTbl):
    batchTbl = self.batchTbl()
    return batchTbl['CurrentWD']

  def submit(tbl, envTbl, funcTbl):
    batchTbl = self.batchTbl()
    stencil  = Stencil(tbl=tbl, envTbl=envTbl, funcTbl=funcTbl)
    return stencil.expand(batchTbl['submitHeader'])
  


    
    
    
