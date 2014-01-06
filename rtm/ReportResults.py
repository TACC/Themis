from __future__      import print_function
from BaseTask        import BaseTask
from Engine          import MasterTbl, Error
from Dbg             import Dbg
from Tst             import Tst
from getTerminalSize import getTerminalSize
import os, time

dbg = Dbg()

class ReportResults(BaseTask):
  def __init__(self,name):
    BaseTask.__init__(self, name)

  def execute(self, *args, **kwargs):
    masterTbl   = MasterTbl()
    rows, width = getTerminalSize()
    rptT        = masterTbl['rptT']
    humanDataA  = ()
    tstSummaryT = masterTbl['tstSummaryT']
    totalTime   = time.strftime("%T", time.gmtime(masterTbl['totalTestTime']))
    totalTime  += "{:.02}".format(masterTbl['totalTestTime'] - int(masterTbl['totalTestTime']))[1:]
    
    
    testresultsT = Tst.test_results_values()
    tstSummaryT  = masterTbl['tstSummaryT']
    
    HDR = "*"*width
    TR  = "*** Test Results"
    TS  = "*** Test Summary"
    TRl = width - len(TR) - 3
    TR  = TR + " "*TRl + "***" 
    TS  = TS + " "*TRl + "***"
    
    humanDataA.append(0)
    humanDataA.append(HDR)
    humanDataA.append(TR)
    humanDataA.append(HDR)
    humanDataA.append(" ")
    humanDataA.append(0)

        
    humanDataA.append(2)
    humanDataA.append(["Date:",            masterTbl['date']])
    humanDataA.append(["TARGET:",          masterTbl['target']])
    humanDataA.append(["Themis Version:",  masterTbl['ThemisVersion']])
    humanDataA.append(["Total Test Time:", totalTime])
    humanDataA.append(-2)

    humanDataA.append(0)
    humanDataA.append(HDR)
    humanDataA.append(TS)
    humanDataA.append(HDR)
    humanDataA.append(" ")
    humanDataA.append(0)

    humanDataA.append(2)
    humanDataA.append(["Total: ", tstSummaryT['total']])
    for k in tstSummaryT:
      count = tstSummary[v]
      if (k != "total" and count > 0):
        humanDataA.append([k+":", count])
    humanDataA.append(-2)

    humanDataA.append(0)
    humanDataA.append(" ")
    humanDataA.append(0)

    humanDataA.append(5)
    humanDataA.append(["*******","*","****","*********","***************"])
    humanDataA.append(["Results","R","Time","Test Name","version/message"])
    humanDataA.append(["*******","*","****","*********","***************"])
   
    resultA = []
    
    for ident in rptT:
      tst    = rptT[ident]
      aFlag  = " "
      if (tst.get("active")): aFlag = "R"
      result  = tst.get('result')
      runtime = tst.get('runtime')
      rIdx    = str(testresultT[result])
      txt     = " "
      if (result in testresultT):
        resultA.append((rIdx, result, aFlag, runtime,  ident, txt))
    
    sorted(resultA, key lambda result: str(10-result[0]) + "-" + result[4])
    
    for v in resultA:
      humanDataA.append(v[1:])
    humanDataA.append(-5)
    
    humanDataA.append(0)
    humanDataA.append(" ")
    humanDataA.append(0)
