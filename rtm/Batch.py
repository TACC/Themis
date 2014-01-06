from JobSubmitBase import JobSubmitBase

class Batch(JobSubmitBase):
  def __init__(self):
    JobSubmitBase.__init__(self)

  def queue(argA, argT, envTbl, funcTbl):
    batchTbl = self.batchTbl()
    queueT   = batchTbl['queueTbl']
    name     = argT.get('name',"") 
    return queueT.get(name) or name

  def runtest(self, *kw):
    masterTbl = self.masterTbl
    batchTbl  = self.batchTbl()
    logFileNm = masterTbl.get('batchLog')) or tbl['idtag'] + ".log"

    sA = []
    sA.append(batchTbl.get('submitCmd') or "")
    sA.append(kw['scriptFn'])
    sA.append(">>")
    sA.append(logFileFn)
    sA.append("2>&1 < /dev/null")

    s = " ".join(sA)
    os.system(s)

  
