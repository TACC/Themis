from __future__ import print_function
from BaseTask   import BaseTask
from Engine     import MasterTbl, Error
from Dbg        import Dbg
from Tst        import Tst
from util       import fullFn
import os, json

dbg = Dbg()

class AnalyzeTests(BaseTask):
  def __init__(self,name):
    BaseTask.__init__(self, name)

  def execute(self, *args, **kwargs):
    masterTbl  = MasterTbl()
    projectDir = masterTbl['projectDir']
    tstT       = masterTbl['tstT']
    rptT       = masterTbl['rptT']

    tstSummaryT = {}
    testValueT  = Tst.test_result_values()

    for k in testValueT:
      tstSummaryT[k] = 0
    tstSummaryT['total'] = 0

    masterTbl['error']         = 0
    masterTbl['diffCnt']       = 0
    masterTbl['failCnt']       = 0
    masterTbl['totalTestTime'] = 0.0

    epoch = masterTbl['currentEpoch']
    if (not tstT):
      epoch = masterTbl['origEpoch']

    status = 'passed'
    if (not rptT):
      status = ' '

    for ident in rptT:
      tst = rptT[ident]

      if (tst.get('runInBackground')):
        continue

      resultFn = fullFn(projectDir, tst.get('resultFn'))

      resultT  = json.loads(open(resultFn).read())
      result   = resultT['testresult']
      tst.set('result', result)

      if (not result in testValueT):
        Error("Unknown test result: ",result," from: ",resultFn)

      tstSummaryT[result]  += 1
      tstSummaryT['total'] += 1

      if (testValueT[result] < testValueT[status]):
        status = result

      if (result != "passed"):
        masterTbl['errors'] += 1

      if (result == "diff"):
        masterTbl['diff'] += 1

      if (result == "failed"):
        masterTbl['failed'] += 1

      runtimeFn = fullFn(projectDir, tst.get('runtimeFn'))
      runtimeT = json.loads(open(runtimeFn).read())
      

      if (runtimeT['T0'] < 0 or runtimeT['T1'] < 0):
        t       = -1.0
        tstTime = "****"
      else:
        t       = runtimeT['T1'] - runtimeT['T0']
        tstTime = "%10.3f" % t
        tstTime = tstTime.strip()
        masterTbl['totalTestTime'] += t

      tst.set('runtime',    t)
      tst.set('strRuntime', tstTime)

      for k in runtimeT:
        tst.set(k, runtimeT[k])

    if (masterTbl['totalTestTime'] <= 0):
      masterTbl['errors'] = 0
    masterTbl['tstSummaryT'] = tstSummaryT
    masterTbl['status']      = status
    masterTbl['epoch']       = epoch
