from __future__ import print_function
from BaseTask   import BaseTask
from Engine     import MasterTbl, Error
from Dbg        import Dbg
from optparse   import OptionParser

dbg = Dbg()

class CmdLineOptions(BaseTask):
  def __init__(self,name):
    BaseTask.__init__(self, name)

  def execute(self, *args, **kwargs):
    masterTbl = MasterTbl()
    usage  = "usage: %prog [options] result.csv"
    parser = OptionParser(usage)
    parser.add_option('-a', "--analyze", dest="analyze_flg", help="Analyze results.",            action="store_true") 
    parser.add_option('-b', "--batch",   dest="batch_flg",   help="Submit tests to batch queue", action="store_true") 
    parser.add_option('-k', "--keyword", dest="keywordA",    help="Keyword(s) to select tests",  action="append")
    parser.add_option('-r', "--restart", dest="restartA",    help='A restart criteria to select tests to rerun, "-r wrong" will restart all test that did not pass',
                     action="append")
    parser.add_option('-m', "--minNP",   dest="minNP",       help="The minimum number of processors that will be run",
                     action="store")
    parser.add_option('-x', "--maxNP",   dest="maxNP",       help="The maximum number of processors that will be run",
                     action="store")
    parser.add_option('-v', "--verbose", dest="v_count",     help="Verbosity",                   action="count")
    parser.add_option('-D', "--debug",   dest="d_count",     help="Debug flag",                  action="count")

    (options, args) = parser.parse_args()

    if (len(args) != 1):
      Error("Incorrect number of arguments: You must have a result file")

    for k in options.__dict__:
      masterTbl[k] = options.__dict__[k]

    masterTbl['pargs'] = args
