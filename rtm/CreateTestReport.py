from __future__ import print_function
from BaseTask   import BaseTask
from Engine     import MasterTbl, full_date_string
from Dbg        import Dbg
from util       import build_test_reportT
import os, json

dbg = Dbg()

class CreateTestReport(BaseTask):
  def __init__(self,name):
    BaseTask.__init__(self, name)

  def execute(self, *args, **kwargs):
    masterTbl = MasterTbl()
    target    = masterTbl['target']
    epoch     = masterTbl['origEpoch']
    prefix = ""

    if (target != "") then
      prefix = target + '-'

    uuid          = prefix + full_date_string(epoch) + '-' masterTbl['os_mach']
    tst_report_fn = os.path.join(masterTbl['testReportDir'],
                                 uuid + masterTbl['testRptExt'])
    masterTbl'tstReportFn'] = tst_report_fn

    #--------------------------------------------------------
    #  Do not create a report when there are no tests to run

    if (not masterTbl['tstT']):
      return

    human_data = ''
    test_results = build_test_reportT(human_data, masterTbl)

    dir_name, fn = os.path.split(tst_report_fn)
    if (not os.path.exists(dir_name)):
      os.makedirs(dir_name)

    rpt = json.dumps(test_results, sort_keys=True, indent=2, separators=(',', ': ')))
    f = open(test_report_fn,"w")
    f.write(rpt)
    f.close()