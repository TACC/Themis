from Tst    import Tst
from Engine import fix_filename
import json, os

def write_table(fn, t):
  s = json.dumps(t, sort_keys=True, indent=2, separators=(',', ': '))
  f = open(fn,"w")
  f.write(s)
  f.close()

def build_test_reportT(human_data, masterTbl):
  test_reportT = {
    'HumanData'    : human_data.split("\n"),
    'date'         : masterTbl['date'],
    'currentEpoch' : masterTbl['currentEpoch'],
    'origEpoch'    : masterTbl['origEpoch'],
    'machType'     : masterTbl['os_mach'],
    'hostname'     : masterTbl['hostname'],
    'target'       : masterTbl['target'],
    'version'      : masterTbl['ThemisVersion'],
    'testA'        : []
    }
  testfieldA = Tst.test_fields()

  rptT = masterTbl['rptT']
  
  testA = test_reportT['testA']

  for ident in rptT:
    tst = rptT[ident]
    test_dataT = {}
    for key in testfieldA:
      test_dataT[key] = tst.get(key)

    testA.append(test_dataT)
  return test_reportT

def fullFn(projectDir,fn):
  return fix_filename(os.path.join(projectDir, fn))

