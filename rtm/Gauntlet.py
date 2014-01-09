from __future__ import print_function
from Dbg        import Dbg
from Engine     import MasterTbl, Error
from Tst        import Tst

import sys

dbg = Dbg()

class Gauntlet(object):

  def __init__(self, gauntletData):
    self.__gauntletData = gauntletData
    self.__applyA       = []
    
  def add(self, name, value):
    if ((value == None) or (type(value) == list and len(value) < 1)):
      return

    self.__gauntletData.dispatch_setup(name, value)
    self.__applyA.append(name)
    
  def apply(self, candidateTstT):
    for name in self.__applyA:
      self.__gauntletData.dispatch_apply(name, candidateTstT)
    
class GauntletData(object):

  def __init__(self):
    self.__data  = []
    self.__funcT = {
      'keywords' : ( self.save_list,     self.apply_keyword ),
      'NP'       : ( self.setup_np,      self.apply_np      ),
      'restart'  : ( self.setup_restart, self.apply_restart ),
      }
    self.__minNP = 0
    self.__maxMP = sys.maxsize

  def dispatch_setup(self, name, value):
    bound = self.__funcT[name][0].__get__(self, type(self))
    bound(name, value)

  def dispatch_apply(self, name, candidateTstT):
    bound = self.__funcT[name][1].__get__(self, type(self))
    bound(name, candidateTstT)

  def setup_restart(self, name, value):
    restart_valueT = {}
    test_resultT   = Tst.test_result_values()

    for v in value:
      v = v.lower()
      if (v == "wrong"):
        for vv in test_resultT:
          restart_valueT[vv] = (test_resultT[vv] < test_resultT['passed'])
      elif (test_resultT[v]):
        restart_valueT[v] = True
    self.__restart_valueT = restart_valueT
          
  def apply_restart(self, name, candidateTstT):
    restart_valueT = self.__restart_valueT
    for ident in candidateTstT:
      tst = candidateTstT[ident]
      if (tst.get('active')):
        result = tst.get('result')
        flag = restart_valueT.get(result)
        if (restart_valueT.get(result)):
          tst.set('active', True)
        else:
          tst.set('report', True)
          tst.set('active', False)
      dbg.print("ident: ", ident, ", result: ", result,", flag: ", flag,", active: ",tst.get("active"),"\n")
          
  def setup_np(self, name, value):
    if (type(value) != list or len(value) != 2):
      Error("bad value to setup_np")
    self.__minNP = value[0]
    self.__maxNP = value[1]
    
  def apply_np(self, name, candidateTstT):
    for ident in candidateTstT:
      tst = candidateTstT[ident]
      if (tst.get('active')):
        np = tst.get('np')
        tst.set('active', (self.__minNP <= np) and (np <= self.__maxNP))
   

  def save_list(self, name, value):
    for v in value:
      self.__data.append(v)

  def apply_keyword(self, name, candidateTstT):
    for ident in candidateTstT:
      tst = candidateTstT[ident]
      if (tst.get('active')):
        flag = tst.has_all_keywords(self.__data)

        tst.set('active', flag)
        
  
        
    
    
