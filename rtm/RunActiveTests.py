from __future__ import print_function
from BaseTask   import BaseTask
from Engine     import MasterTbl, Error, fix_filename
from Dbg        import Dbg
from Tst        import Tst
from util       import write_table
import os, json, time

comment_block = """
   Test Results:
      'notfinished': means that the test has started but not completed.
      'failed': means that the test has started but not completed.
      'notrun': test has not started running.
      'diff'  : Test has run but is different from gold copy.
      'passed': Test has run and matches gold copy.
"""

resultTbl = {
  'started' : {
    'testresult' : 'notfinished',
    'comment'    : comment_block,
    },
  'notrun' : {
    'testresult' : 'notrun',
    'comment'    : comment_block,
    },
}

runtimeT = { 'start_time' : -1, 'end_time' : -1 }

dbg = Dbg()
def fullFn(projectDir,fn):
  return fix_filename(os.path.join(projectDir, fn))


class RunActiveTests(BaseTask):
  def __init__(self,name):
    BaseTask.__init__(self, name)

  def execute(self, *args, **kwargs):
    masterTbl = MasterTbl()

    masterTbl['passed'] = 0
    masterTbl['failed'] = 0
    tstT                = masterTbl['tstT']
    num_tests           = len(tstT)
    projectDir          = masterTbl['projectDir']

    if (num_tests > 0):
      print("\nStarting Tests:\n")

    self.create_output_dirs(projectDir, tstT)

    i = 0
    for ident in tstT:
      i = i + 1
      self.run_test(masterTbl, tstT[ident], i, num_tests)

    if (num_tests > 0):
      print("\nFinished Tests\n")
    

  def create_output_dirs(self, projectDir, tstT)

    for ident in tstT:
      tst       = tstT[ident]
      os.makedirs(fullFn(projectDir, tst.get('outputDir')))

    for ident in tstT:
      tst       = tstT[ident]
      resultFn  = fullFn(projectDir, tst.get('resultFn'))
      runtimeFn = fullFn(projectDir, tst.get('runtimeFn'))
      write_table(resultFn,  resultTbl['notrun'])
      write_table(runtimeFn, runtimeT)

  def run_test(masterTbl, tst, iTest, num_tests):
    fn_envA = ['testDir', 'outputDir', 'resultFn',   'testdescriptFn',
               'cmdResultFn', 'messageFn', 'runtimeFn']
    envA    = ('idtag',   'test_name',  'packageName', 'packageDir',
               'TARGET', 'target', 'tag')
    envTbl  = {}

    for v in fn_envA:
      envTbl[v] = fix_filename(fullFn(projectDir, tst.get(v)))

    for v in envA:
      envTbl[v] = tst.get(v)

    envTbl['projectDir'] = masterTbl['projectDir']
     
    job_submit_method = tst.get('job_submit_method')

    job = JobSubmitBase.build(job_submit_method, masterTbl)

    run_script = tst.expand_run_script(envTbl, job)

    cwd = os.getcwd()
    os.chdir(envTbl['outputDir'])


    resultFn = fullFn(tst.get('resultFn'))

    write_table(resultFn, resultTbl['started'])

    stime = { 'start_time' : time.time(), 'end_time' : -1 }
    runtimeFn = fullFn(tst.get('runtimeFn'))
    write_table(runtimefn, stime)

    idtag    = tst.get('idtag')
    scriptFn = idtag + ".script"
    f        = open(scriptFn,"w")
    f.write(tst.top_of_script())
    f.write(run_script)
    f.close()

    os.chmod(scriptFn,"+x")
    ident      = tst.get('id')
    background = tst.get('background') or (job_submit_method == "BATCH")
    tst.set('runInBackground', background)

    job.msg('Started', iTest, num_test, ident, envTbl['resultFn'], background)
    job.runtest(scriptFn = scriptFn, idtag = idtag, background = background)
    job.msg('Finished', iTest, num_tests, ident, envTbl['resultFn'], background)

    os.chdir(cwd)
