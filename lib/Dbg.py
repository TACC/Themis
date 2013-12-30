#!/usr/bin/env python
from __future__ import print_function
import sys


class Dbg(object):
  _dbg_shared_state = {}
  _dbg_shared_state["active"]        = False
  _dbg_shared_state["indent_level"]  = 0
  _dbg_shared_state["my_indent_string"] = ""

  def __new__(cls, *a, **k):
    obj = super(Dbg, cls).__new__(cls, *a, **k)
    obj.__dict__ = cls._dbg_shared_state
    return obj

  def activateDebug(self):
    self.active        = True

  def is_active(self):
    return self.active

  def indent_string(self):
    return  self.my_indent_string 

  def __change_indent_level(self, i):
    self.indent_level  = max( self.indent_level + i, 0)
    self.my_indent_string = " "*(self.indent_level*2)


  def start(self,name,*a,**kw):
    if (not self.active): return
    sA = []
    sA.append(self.my_indent_string)
    sA.append(str(name))
    sA.append("(")

    for v in a:
      sA.append(str(v))
      sA.append(", ")

    for k in kw:
      sA.append(str(k))
      sA.append(" = ")
      sA.append(str(kw[k]))
      sA.append(", ")
      
    if (sA[len(sA)-1] == ", "):
      sA[len(sA)-1] = ""

    sA.append("){\n")
    sys.stderr.write("".join(sA))
    self.__change_indent_level(1)

  def fini(self,*a):
    if (not self.active): return
    self.__change_indent_level(-1)
    sA = []
    sA.append(self.my_indent_string)
    sA.append("}")
    for v in a:
      sA.append(" ")
      sA.append(str(v))
    sA.append("\n")
    sys.stderr.write("".join(sA))

  
  def print(self,*a,**kw):
    if (not self.active): return
    sys.stderr.write(self.my_indent_string)
    sA = []
    for v in a:
      sA.append(str(v))

    for key in kw:
      sA.append(",")
      sA.append(key)
      sA.append(" = ")
      sA.append(kw[key])
      
def main():

  dbg = Dbg()
  dbg.start("do_not_print_main")
  dbg.print("do_not_print_main\n")
  dbg.fini("do_not_print_main")

  dbg.activateDebug()
  
  dbg.start("main()")
  dbg.print("in Main\n")
  dbg.fini("main")


if ( __name__ == '__main__'): main()
    
  
