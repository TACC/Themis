#!/usr/bin/env python
# -*- python -*-
from __future__ import print_function
from Engine     import Error, full_date_string, fix_filename
from Stencil    import Stencil
import os, sys, re, time

blankPat    = re.compile("\n\s\s*#")
bad_charPat = re.compile(r'[\'\\ ?/*"[\]]')

class Tst(object):

  def __init__(self, testparams, fn, test_descript, epoch, idx):
    masterTbl = MasterTbl()
    masterTbl['date'] = time.strftime("%c", time.localtime(epoch))

    projectDir = masterTbl['projectDir']
    pattern    = re.compile("^" + re.escape(projectDir) + "/(.*)\.desc")
    m = pattern.search(fn)

    base_id   = m.group(1)
    tst_dir   = os.path.dirname(base_id) or "./"
    
    ident     = testparams.get('id')
    test_name = test_descript.get("test_name")

    self.valid_name("id",        ident)
    self.valid_name("test_name", test_name)

    self.test_descript     = test_descript
    self.test              = testparams
    self.id                = pathjoin(base_id,ident)
    self.idtag             = ident
    self.start_epoch       = -1
    self.runtime           = -1
    self.job_submit_method = test_descript.get('job_submit_method') or False
    self.str_runtime       = "***"
    self.result            = 'notrun'
    self.active            = True
    self.test_dir          = tst_dir
    self.testdescript_fn   = baseid + '.desc'
    self.testName          = fix_filename(test_name)
    self.package_name      = masterTbl['packageName']
    self.packageDir        = masterTbl['packageDir']
    self.parent_dir        = os.path.join(test_dir, idtag)
    self.prog_version      = ""
    self.message           = ""
    self.os_name           = ""
    self.mach_name         = ""
    self.hostname          = ""
    self.target            = masterTbl['target']
    self.TARGET            = masterTbl['target']
    self.start_time        = -1
    self.end_time          = -1
    self.background        = False
    self.at_top_of_script  = "#!/bin/bash\n# -*- shell-script -*-\n"
  

    self.setup_output_dir_names(epoch, target)
    active = test_descript.get('active')
    if (active != None):
      self.active = active

    keywordT               = {}
    for key in test_descript.get('keywords') or []
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
    self.outputDir = os.path.join(self.parent_dir,uuid + '-' + self.test_name)
    self.resultFn  = os.path.join(self.outputDir, self.idtag + "result")
    self.runtimeFn = os.path.join(self.outputDir, self.idtag + "runtime")
    self.versionFn = os.path.join(self.outputDir, 'version.lua')
    self.messageFn = os.path.join(self.outputDir, 'message.lua')

  def test_fields(self):
    fieldA = (
      "id", "idTag", "start_epoch", "runtime", "result", "active", "report" , "strRuntime",
      "outputDir", "testName", "reason", "uuid", "resultFn", "runtimeFn", "cmdResultFn",
      "versionFn","osName","machName","hostName","target","ProgVersion","message","tag",
      "userActive"
    )

   return fieldA
 def test_result_values(self):
   valueT = {
      'notrun' : 1, 'notfinished' : 2, 'failed'   : 3,
      'diff'   : 4, 'passed'      : 5, 'inactive' : 6
   }
   return valueT

 def get(self, key):
   return self.__dict__.get(key) or self.test_descript.get(key,"")

 def set(self, key, value):
   result = key in self.__dict__
   if (not result):
     Error('Tst.set: Unknown key: "',key,'"')
   self.__dict__[key] = value
 def has_any_keywords(self, keyA):
   keyT = self.get("keywords")
   result = False
   for v in keyA:
     if (key in keyT):
       result = True
       break
   return result

 def has_all_keywords(self, keyA):
   keyT = self.get("keywords")
   result = True
   for v in keyA:
     if (not  key in keyT):
       result = False
       break
   return result

 def top_of_script(self):
   return self.at_top_of_script

 def expand_run_script(self, envTbl, funcTbl)
   stencil = Stencil(tbl=self.test, envTbl = envTbl, funcTbl = funcTbl)
   run_script = self.test_descript.get('run_script')
   if (not run_script):
     Error("No run script for test:", self.test_name,"\n")

   run_script = stencil.expand(run_script).strip()
   run_script = blankPat.sub(r"\n#",run_script)

   aa = []
   for k in envTbl:
     aa.append("export " + k + "=\"" + envTbl[k])


   mark  = false
   a     = []
   aaa   = []

   lineA = run_script.split("\n")

   for line in lineA:
     if (line[0] != "#"):
       mark = True
     if (not mark):
       a.append(line)
     else:
       aaa.append(line)

   sA = []
   sA.append("\n",a)
   sA.append("\n",aa)
   sA.append("\n",aaa)
   return "\n".join(sA)
   
    
            
    

    
  
