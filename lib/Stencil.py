#!/usr/bin/env python
# -*- python -*-
from __future__ import print_function
from Dbg        import Dbg
import os, sys, re

fnstrtPat       = re.compile(r'\$\(')
parenPat        = re.compile(r'[()]')
wspacePat       = re.compile(r'\s')
quote_commaPat  = re.compile(r'[\'\",]')
dbg             = Dbg()

class StencilException(Exception):
  def __init__(self, *a):
    sA = []
    for v in a:
      sA.append(str(v))
    
    s = "".join(sA)
    self.value = s
    sys.stderr.write(s)
    if (s[-1] != "\n"): 
      sys.stderr.write("\n")
      

class Stencil(object):
  def __init__(self, argA = [], tbl={}, envTbl={}, funcTbl={}):
    self.__argA  = argA
    self.__tbl   = tbl
    self.__envT  = envTbl
    self.__funcT = funcTbl


  def __find_cmd(self, s):
    dbg.start("Stencil.__find_cmd",s)
    m   = fnstrtPat.search(s)
    if (not m):
      return (None, None)
    
    iparen = 1
    ja  = m.start()
    jb  = m.end()
    idx = jb
    
    while (True):
      m  = parenPat.search(s,idx)
      if (not m):
        raise StencilException("unequal number of parens\n")
      jc = m.start()
      jd = m.end()
        
      c = s[jc:jd]
      if (c == '('): 
        iparen += 1
      if (c == ')'):
        iparen -= 1
        if (iparen == 0):
          break
      idx = jd
    dbg.fini("Stencil.__find_cmd")
    return (ja, jd)
      
  def __assign_one_arg(self, s, argA, argT):
    ja = s.find('=')
    if (ja == -1):
      argA.append(s.strip())
    else:
      key   = s[0:ja].strip()
      value = s[ja+1:].strip()
      argT[key] = value


  def __find_key_args(self, s):
    dbg.start("Stencil.__find_key_args",s)
    argA = []
    argT = {}

    s = s.strip()
    m = wspacePat.search(s)
    if (not m):
      dbg.fini("Stencil.__find_key_args")
      return s, argA, argT
    ja  = m.start()
    key = s[0:ja-1]
    s   = s[ja:]

    ss   = None
    rA   = []
    q    = None
    qidx = None   
    idx  = 0
    while (True):
      m = quote_commaPat.search(s,idx)
      if (not m):
        rA.append(s[idx:])
        ss = "".join(rA)
        self.__assign_one_arg(ss, argA, argT)
        break
      ja = m.start()
      c  = s[ja:ja+1]

      if (c == '"' or c == "'"):
        if (q == None):
          rA.append(s[idx:ja])
          qidx = ja
          q    = c
        elif (c == q):
          rA.append(s[qidx+1:ja])
          qidx = None
          q    = None
      elif (c == ',' and q == None):
        rA.append(s[idx:ja])
        ss = "".join(rA)
        self.__assign_one_arg(ss,argA,argT)
        rA = []
      else:
        rA.append(s[idx:ja])
      idx = ja
    dbg.fini("Stencil.__find_key_args")
    return key, argA, argT
    
  def expand(self, s):
    dbg.start("Stencil.expand",s)
    argA  = self.__argA
    tbl   = self.__tbl
    envT  = self.__envT
    funcT = self.__funcT

    sA = []
    
    while (True):
      ja, jb = self.__find_cmd(s)
      dbg.print("ja: ", ja, ", jb: ", jb,"\n")

      if (ja == None):
        sA.append(s)
        break
      
      sA.append(s[0:ja])
      q               = s[ja+2:jb-1]
      key, argA, argT = self.__find_key_args(self.expand(q))
      if (funcT and funcT.has_function(key)):
        v = funcT.funcT(key, argA, argT, envT, funcT)
      else:
        v = tbl.get(key) or envT.get(key) or os.environ.get(key)
      if (v == None):
        raise StencilException("No replacement value for key: \"",key,"\" found\n")
      if (type(v) != str):
        v = str(v)
      s = v + s[jb:]
    
    dbg.fini("Stencil.expand")
    return "".join(sA)
    
def main():


  tbl = { 'a' : 'A', 'b' : "BB", 'c' : 'CCC', 'd' : '$(b)' }

  sA = [
    "Now is the time for $(a) to be replaced with $(b) asasdf $(d) asdklj",
    "Now is the time for $(a(()) to be replaced with $(b) asasdf $(d) asdklj",
    "Now is the time for $(aa) to be replaced with $(b) asasdf $(d) asdklj",
  ]


  stencil = Stencil(tbl=tbl)

  for idx, s in enumerate(sA):
    print("\nInput:",s)
    try: 
      ss = stencil.expand(s)
    except Exception as e:    
      continue
    print("      ",ss)
  

  print("\nShow erroring out:")

  try: 
    ss = stencil.expand(sA[2])
  except Exception as e:    
    sys.exit(-1)



  


if ( __name__ == '__main__'): main()
