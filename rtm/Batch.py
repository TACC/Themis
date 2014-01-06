from JobSubmitBase import JobSubmitBase

class Batch(JobSubmitBase):

  def queue(tbl, envTbl, funcTbl):
    batchTbl = self.batchTbl()
    queueT   = batchTbl['queueTbl']
    return queueT.get('name') or tbl['name'] or ""


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
    os.execute(s)

  def queue(*kw):
    return ""
  
