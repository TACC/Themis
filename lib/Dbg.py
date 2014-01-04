#!/usr/bin/env python
from __future__ import print_function
import sys


class Dbg(object):
  _dbg_shared_state = {}
  _dbg_shared_state["active"]        = False
  _dbg_shared_state["indent_level"]  = 0
  _dbg_shared_state["my_indent_str"] = ""
  _dbg_shared_state['levelA']        = []
  _dbg_shared_state['current_level'] = 1
  _dbg_shared_state['vpl']           = 0

  def __new__(cls, *a, **k):
    obj = super(Dbg, cls).__new__(cls, *a, **k)
    obj.__dict__ = cls._dbg_shared_state
    return obj

  def activateDebug(self, level=1):
    self.active        = True
    self.current_level = level
    self.levelA.append(level)

  def is_active(self):
    return self.active

  def indent_string(self):
    return  self.my_indent_str

  def __change_indent_level(self, i):
    self.indent_level  = max( self.indent_level + i, 0)
    self.my_indent_str = " "*(self.indent_level*2)


  def __startVPL(self, level):
    vpl      = level or self.vpl
    self.vpl = vpl
    self.levelA.append(vpl)
    return vpl

  def start(self,name,*a,**kw):
    if (not self.active): return

    self.__startVPL(kw.get('level'))
    if (self.vpl > self.current_level): return


    sA = []
    sA.append(self.my_indent_str)
    sA.append(str(name))
    sA.append("(")

    for v in a:
      sA.append(str(v))
      sA.append(", ")

    if (sA[len(sA)-1] == ", "):
      sA[len(sA)-1] = ""

    sA.append("){\n")
    sys.stderr.write("".join(sA))
    self.__change_indent_level(1)

  def fini(self,*a):
    if (not self.active): return
    
    if (self.vpl <= self.current_level):
      self.__change_indent_level(-1)
      sA = []
      sA.append(self.my_indent_str)
      sA.append("}")
      for v in a:
        sA.append(" ")
        sA.append(str(v))
      sA.append("\n")
      sys.stderr.write("".join(sA))

    self.vpl = self.levelA.pop()
  
  def print(self,*a,**kw):
    if (not self.active): return
    
    vpl = kw.get('level') or self.vpl

    if (vpl > self.current_level):
      return

    sA = []
    sA.append(self.my_indent_str)
    for v in a:
      sA.append(str(v))

    sys.stderr.write("".join(sA))
      
def A():
  
  dbg.start("A")
  B()
  dbg.fini("A")

def B():
  dbg.start("B", level = 2)
  dbg.fini("B")
    

dbg = Dbg()

def main():

  dbg.start("do_not_print_main")
  dbg.print("do_not_print_main\n")
  dbg.fini("do_not_print_main")

  dbg.activateDebug()
  
  dbg.start("main")
  dbg.print("in Main\n")
  A()
  dbg.fini("main")

  print("\nSecond time:")

  dbg.activateDebug(2)
  dbg.start("main")
  dbg.print("in Main\n")
  A()
  dbg.fini("main")
  



if ( __name__ == '__main__'): main()
    
  
