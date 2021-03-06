#!/usr/bin/env python
# -*- python -*-
from __future__ import print_function
from Dbg        import Dbg
from Engine     import MasterTbl, Error, full_date_string, fix_filename
from Stencil    import Stencil
import os, sys, re, time

blankPat    = re.compile("\n\s\s*#")
bad_charPat = re.compile(r'[\'\\ ?/*"[\]]')
dbg         = Dbg()

class Tst(object):

  def __init__(self, testparams, fn, test_descript, epoch, idx):
    masterTbl = MasterTbl()
    masterTbl['date'] = time.strftime("%c", time.localtime(epoch))

    projectDir = masterTbl['projectDir']
    patternStr = "^" + re.escape(projectDir) + "/(.*)\.desc"

    pattern    = re.compile(patternStr)
    m = pattern.search(fn)

    base_id    = m.group(1)
    test_dir   = os.path.dirname(base_id) or "./"
    
    ident      = testparams.get('id')
    test_name  = test_descript.get("test_name")
    target     = masterTbl['target']

    self.valid_name("id",        ident)
    self.valid_name("test_name", test_name)

    self.test_descript     = test_descript
    self.test              = testparams
    self.id                = os.path.join(base_id,ident)
    self.idtag             = ident
    self.start_epoch       = -1
    self.runtime           = -1
    self.strRuntime        = "***"
    self.result            = 'notrun'
    self.active            = True
    self.report            = False
    self.testDir           = test_dir
    self.testdescript_fn   = base_id + '.desc'
    self.testName          = fix_filename(test_name)
    self.packageName       = masterTbl['packageName']
    self.packageDir        = masterTbl['packageDir']
    self.parent_dir        = os.path.join(test_dir, ident)
    self.prog_version      = ""
    self.message           = ""
    self.os_mach           = ""
    self.machine           = ""
    self.fn                = fn
    self.version           = ""
    self.release           = ""
    self.processor         = ""
    self.targ_summary      = ""
    self.node              = ""
    self.system            = ""
    self.T0                = ""
    self.T1                = ""
    self.TT                = ""
    self.hostname          = ""
    self.target            = target
    self.TARGET            = target
    self.start_time        = -1
    self.end_time          = -1
    self.background        = False
    self.runInBackground   = False
    self.at_top_of_script  = "#!/bin/bash\n# -*- shell-script -*-\n"

    self.setup_output_dir_names(epoch, target)
    active = test_descript.get('active')
    if (active != None):
      self.active = active

    submit_method = test_descript.get('job_submit_method') or "INTERACTIVE"

    if (masterTbl['inter_flg']):
      submit_method = "INTERACTIVE"

    if (masterTbl['batch_flg']):
      submit_method = "BATCH"

    self.job_submit_method = submit_method
    keywordT               = {}
    for key in test_descript.get('keywords',[]):
      keywordT[key] = True
    self.keywordT          = keywordT
    
    self.np = self.test.get('np') or 1
    
  def valid_name(self,key, value):
    m = bad_charPat.search(value)
    if (m):
      Error(key, ": \"",name,"\" has an illegal character: '",m.group(),"'",
            "\nIllegal characters are: \" ?/*\" and the quote characters: ' and '\"'")
  
            
  def setup_output_dir_names(self, epoch, target=""):
    masterTbl = MasterTbl()
    prefix = ''
    if (len(target) > 0):
      prefix = target + "-"

    uuid           = prefix + full_date_string(epoch) + '-' + masterTbl['os_mach']
    self.uuid      = uuid
    self.outputDir = os.path.join(self.parent_dir,uuid + '-' + self.testName)
    self.resultFn  = os.path.join(self.outputDir, self.idtag + ".result")
    self.runtimeFn = os.path.join(self.outputDir, self.idtag + ".runtime")
    self.versionFn = os.path.join(self.outputDir, 'version.lua')
    self.messageFn = os.path.join(self.outputDir, 'message.lua')

  @staticmethod
  def test_fields():
    fieldA = (
      "id", "idtag", "start_epoch", "runtime", "result", "active", "report" , "strRuntime",
      "outputDir", "testName", "uuid", "resultFn", "runtimeFn", "versionFn", "target","message", 
    )
    return fieldA

 
  @staticmethod
  def test_result_values():
    valueT = {
      'notrun' : 1, 'notfinished' : 2, 'failed'   : 3,
      'diff'   : 4, 'passed'      : 5, 'inactive' : 6
    }
    return valueT

  def get(self, key):
    value = self.__dict__.get(key)
    if (value != None):
      return value
    return self.test_descript.get(key,"")

  def set(self, key, value):
    result = key in self.__dict__
    if (not result):
      Error('Tst.set: Unknown key: "',key,'"')
    self.__dict__[key] = value


  def has_any_keywords(self, keyA):
    keyT = self.get("keywordT")
    result = False
    for v in keyA:
      if (v in keyT):
        result = True
        break
    return result

  def has_all_keywords(self, keyA):
    keyTst = self.get("keywordT")
    result = True
    for v in keyA:
      if (not  (v in keyTst)):
        result = False
        break
    return result

  def top_of_script(self):
    return self.at_top_of_script

  def expand_run_script(self, envTbl, funcTbl):
    stencil = Stencil(tbl=self.test, envTbl = envTbl, funcTbl = funcTbl)
    run_script = self.test_descript.get('run_script')
    if (not run_script):
      Error("No run script for test:", self.test_name,"\n")

    run_script = stencil.expand(run_script).strip()
    run_script = blankPat.sub(r"\n#",run_script)

    aa = []
    for k in envTbl:
      aa.append("export " + k + "=\"" + envTbl[k]+"\"")


    mark  = False
    a     = []
    aaa   = []

    lineA = run_script.split("\n")

    for line in lineA:
      if (not line.startswith("#")):
        mark = True
      if (not mark):
        a.append(line)
      else:
        aaa.append(line)

    sA = []
    sA.append("\n".join(a))
    sA.append("\n".join(aa))
    sA.append("\n".join(aaa))
    s = "\n".join(sA)

    return s
