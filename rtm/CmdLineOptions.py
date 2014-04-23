from __future__ import print_function
from BaseTask   import BaseTask
from Engine     import MasterTbl, Error
from Dbg        import Dbg
from optparse   import OptionParser


dbg = Dbg()

class CmdLineOptions(BaseTask):
  def __init__(self,name):
    super(CmdLineOptions, self).__init__(name)

  def execute(self, *args, **kwargs):
    masterTbl = MasterTbl()
    usage  = "usage: %prog [options] [directory] [*.desc]"
    parser = OptionParser(usage)
    parser.add_option('-a', "--analyze",      dest="analyze_flg", action="store_true", help="Analyze results."            ) 
    parser.add_option('-b', "--batch",        dest="batch_flg",   action="store_true", help="Submit tests to batch queue" ) 
    parser.add_option('-i', "--interactive",  dest="inter_flg",   action="store_true", help="Submit tests to batch queue" ) 
    parser.add_option('-k', "--keyword",      dest="keywordA",    action="append"    , help="Keyword(s) to select tests"  )
    parser.add_option('-r', "--restart",      dest="restartA",    action="append"    , help='A restart criteria to select ' + \
                                                         'tests to rerun, "-r wrong" will restart all test that did not pass')
    parser.add_option('-m', "--minNP",        dest="minNP",       action="store",      help="The minimum number of processors that will be run")
    parser.add_option('-x', "--maxNP",        dest="maxNP",       action="store",      help="The maximum number of processors that will be run")
    parser.add_option('-v', "--verbose",      dest="v_count",     help="Verbosity",                   action="count")
    parser.add_option('-D', "--debug",        dest="d_count",     help="Debug flag",                  action="count")

    (options, args) = parser.parse_args()

    for k in options.__dict__:
      masterTbl[k] = options.__dict__[k]

    masterTbl['pargs'] = args

    if (masterTbl['inter_flg'] and masterTbl['batch_flg']):
      Error("Both interactive and batch options set, please chose one and try again!")
      
