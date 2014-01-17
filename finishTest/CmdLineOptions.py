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
    usage  = "usage: %prog [options] result.csv"
    parser = OptionParser(usage)
    parser.add_option('-o', "--output",  dest="result_fn",  help="Translated Python result file.", metavar="FILE") 
    parser.add_option('-t', "--timer",   dest="runtime_fn", help="Testing Timing file",            metavar="FILE")
    parser.add_option('-v', "--verbose", dest="v_count",    help="Verbosity",                      action="count")
    parser.add_option('-D', "--debug",   dest="d_count",    help="Debug flag",                     action="count")
    (options, args) = parser.parse_args()

    if (len(args) != 1):
      Error("Incorrect number of arguments: You must have a result file")

    for k in options.__dict__:
      masterTbl[k] = options.__dict__[k]

    masterTbl['pargs'] = args
    
