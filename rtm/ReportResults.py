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
    totalTime  += "{:.02}".format(masterTbl['totalTestTime'] -
                                  int(masterTbl['totalTestTime']))[1:]
    
    
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
      rIdx    = str(testresultT.get(result,0))
      txt     = " "
      if (result in testresultT):
        resultA.append((rIdx, result, aFlag, runtime,  ident, txt))
    
    sorted(resultA, key =lambda result: str(10-result[0]) + "-" + result[4])
    
    for v in resultA:
      humanDataA.append(v[1:])
    humanDataA.append(-5)
    
    humanDataA.append(0)
    humanDataA.append(" ")
    humanDataA.append(0)

    if(tstSummaryT['total'] != tstSummaryT['passed']):
      humanDataA.append(2)
      humanDataA.append(["*******",  "****************"])
      humanDataA.append(["Results",  "Output Directory"])
      humanDataA.append(["*******",  "****************"])
      
      resultA = []

      for ident in rptT:
        tst    = rptT[ident]
        result = tst.get('result')
        if (result != "passed" and result in testresultT)
          resultA.append((result, fullFn(tst.get('outputDir'))))
      sorted(resultA, key = lambda result: result[0] + "-" + result[1])

      for v in resultA:
        humanDataA.append(v)
      humanDataA.append(-2)

    humanData = self.formatHumanData(humanDataA)
    if (tstSummaryT['total'] > 0):
      print(humanData)

      testreportT = build_test_reportT(humanData, masterTbl)
      write_table(masterTbl['tstReportFn'), testreportT)
      
  def format_human_data(self, humanDataA):
    sA      = []
    blkA    = []
    istart  = 1
    sz      = len(humanDataA)
    numCols = humanData[0]

    for idx in xrange(sz):
      v = humanDataA[idx]
      if (type(v) == int):
        if (numCol == -v):
          # Time to build block
          blkA.append(build_block(sA, numCols))
          numCols = None
          sA      = []
        else:
          numCols = v
      else:
        sA.append(v)
    return "".join(blkA)

  def build_block(self, sA, numCols):
    if (numCols == 0):
      sA.append("\n")
      return "\n".join(sA)

    for idx in xrange(numCols):
      widthA.append(0)

    for row in sA:
      for icol, v in enumerate(row):
        if (type(v) != str):
          v = str(v)
        widthA[icol] = math.max(len(w), widthA[icol])
          
    aa = []
    for row in sA:
      for icol, v in enumerate(row):
        if (type(v) != str):
          v = str(v)
        w = widthA[icol]
        blankLen = w - len(v)
        v = v + " "*blankLen
        aa.append(v)
      aa.append("\n")

    return "".join(aa)
      
            
  
        
