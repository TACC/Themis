from Tst import Tst

def build_test_reportT(human_data, masterTbl):
  test_resultT = {
    'HumanData'    : human_data:split("\n"),
    'date'         : masterTbl['date'],
    'currentEpoch' : masterTbl['currentEpoch'],
    'origEpoch'    : masterTbl['origEpoch'],
    'machType'     : masterTbl['os_mach'],
    'hostname'     : masterTbl['hostname'],
    'target'       : masterTbl['target'],
    'version'      : masterTbl['ThemisVersion'],
    'testA'        : {}
    }
  testfieldA = Tst:test_fields()

  rptT = masterTbl['rptT']
  
  testA = test_resultT['testA']

  for ident in rptT
    tst = rptT[ident]
    test_dataT = {}
    for key in testfieldA
      test_dataT[key] = tst.get(key)

    testA.append(test_dataT)
  return test_resultT
  
  
