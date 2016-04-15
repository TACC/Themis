from __future__  import print_function
from Dbg         import Dbg
from Tst         import Tst
from Stencil     import Stencil
import os, sys, time, json

dbg = Dbg()

def find_py_file(name):
  for path in sys.path:
    fn = os.path.join(path, name)
    if (os.path.isfile(fn)):
      return fn

class JobSubmitBase(object):
  def __init__(self, masterTbl):
    self.__funcT = {
      'CWD'    : self.CWD,
      'findcmd': self.findcmd,
      'mpr'    : self.mpr,
      'queue'  : self.queue,
      'submit' : self.submit,
    }
    self.__masterTbl  = masterTbl
    self.resultMaxLen = masterTbl['resultMaxLen']
    baseFn    = find_py_file("DefaultSystems.py")
    derivedFn = find_py_file("Systems.py")
    
    namespace = {}
    exec(open(baseFn).read(),    namespace)
    exec(open(derivedFn).read(), namespace)
    Systems        = namespace['Systems']
    DefaultSystems = namespace['DefaultSystems']

    self.__batchTbl = {}
    batch_hostname = os.environ.get("BATCH_HOSTNAME","INTERACTIVE")
    if (batch_hostname == "INTERACTIVE"):
      self.__batchTbl = DefaultSystems['INTERACTIVE']
    else:
      for k in Systems:
        if (batch_hostname in Systems[k]):
          self.__batchTbl = DefaultSystems[k].copy()
          self.__batchTbl.update(Systems[k][batch_hostname])
    
    if (not self.__batchTbl):
      Error("Unable to find BatchSystems entry for ",batch_hostname)
      
  def has_function(self, name):
    return name in self.__funcT

  def funcT(self, name, argA, argT, envTbl, funcTbl):
    bound = self.__funcT[name].__get__(self, type(self))
    s = bound(argA, argT, envTbl, funcTbl)
    return s

  def batchTbl(self):
    return self.__batchTbl

  def masterTbl(self):
    return self.__masterTbl


  @staticmethod
  def build(name, masterTbl):
    if (name.lower() == "interactive"):
      obj = Interactive(masterTbl)
    else:
      obj = Batch(masterTbl)
    return obj

  def formatMsg(self, result, iTest, passed, failed, num_tests, ident):
    blank    = " "
    r        = result or "failed"
    blankLen = self.resultMaxLen - len(r)
   #msg      = "{}{} : {} tst: {}/{} P/F: {}:{}, {}".format(
    msg      = "%s%s : %s tst: %d/%d P/F: %d:%d, %s" % (
                           blank*(blankLen),
                           result,
                           time.strftime("%X",time.localtime(time.time())),
                           iTest, num_tests,
                           passed, failed,
                           ident)

    return msg

  def msg(self, messageStr, iTest, num_tests, ident, resultFn, background):
    if (messageStr != "Started" and background):
      print("")
      return

    masterTbl = self.__masterTbl
    msgExtra  = ""  

    if (messageStr != "Started" and not background):
      msgExtra = "\n"  
      resultT  = json.loads(open(resultFn).read())
      myResult = resultT['testresult']

      if (myResult == "passed"):
        masterTbl['passed'] += 1
      else:
        masterTbl['failed'] += 1

      messageStr = myResult

    print(self.formatMsg(messageStr, iTest, masterTbl['passed'],
                         masterTbl['failed'], num_tests, ident), msgExtra)
      

  def CWD(self, argA, argT, envTbl, funcTbl):
    batchTbl = self.batchTbl()
    return batchTbl['CurrentWD']

  def findcmd(self, argA, argT, envTbl, funcTbl):
    result = None
    cmd  = argT.get('cmd',"")
    pathA = split(argT.get('path') or os.environ.get('PATH',""), ":")
    for path in pathA:
      fn = os.path.join(path, cmd)
      if (os.path.exists(fn)):
        result = fn
        break
      
    return fn

  def mpr(self, argA, argT, envTbl, funcTbl):
    batchTbl = self.batchTbl()
    stencil  = Stencil(argA = argA, tbl=argT, envTbl=envTbl, funcTbl=funcTbl)
    return stencil.expand(batchTbl['mprCmd'])

  def queue(self,argA, argT, envTbl, funcTbl):
    return ""

  def submit(self, argA, argT, envTbl, funcTbl):
    batchTbl = self.batchTbl()
    stencil  = Stencil(argA = argA, tbl=argT, envTbl=envTbl, funcTbl=funcTbl)
    s        = stencil.expand(batchTbl['submitHeader'])
    dbg.print("submit: s:\n",s,"\n")
    return s

class Batch(JobSubmitBase):
  def __init__(self, masterTbl):
    super(Batch, self).__init__(masterTbl)

  def queue(self, argA, argT, envTbl, funcTbl):
    batchTbl = self.batchTbl()
    queueT   = batchTbl['queueTbl']
    name     = argT.get('name',"") 
    return queueT.get(name) or name

  def runtest(self, **kw):
    masterTbl = self.masterTbl()
    batchTbl  = self.batchTbl()
    logFileNm = masterTbl.get('batchLog') or kw['idtag'] + ".log"

    sA = []
    sA.append(batchTbl.get('submitCmd') or "")
    sA.append(kw['scriptFn'])
    sA.append(">>")
    sA.append(logFileNm)
    sA.append("2>&1 < /dev/null")

    s = " ".join(sA)
    os.system(s)


class Interactive(JobSubmitBase):
  def __init__(self, masterTbl):
    super(Interactive, self).__init__(masterTbl)

  def runtest(self, **kw):
    sA = []
    sA.append("./" + kw['scriptFn'])
    sA.append(">")
    sA.append(kw['idtag'] + ".log")
    sA.append("2>&1 < /dev/null")
    if (kw['background']):
      sA.append("&")

    s = " ".join(sA)
    os.system(s)
      
