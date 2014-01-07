#!/usr/bin/env python
# -*- python -*-
from __future__ import print_function
import os, sys, re

def getTerminalSize():
  """
  returns (lines:int, cols:int)
  """
  import os, struct
  def ioctl_GWINSZ(fd):
      import fcntl, termios
      return struct.unpack("hh", fcntl.ioctl(fd, termios.TIOCGWINSZ, "1234"))
  # try stdin, stdout, stderr
  if (not sys.stdout.isatty()):
    return (25, 80)

  fd = 1
  try:
    return ioctl_GWINSZ(fd)
  except:
    pass
  # try os.ctermid()
  try:
    fd = os.open(os.ctermid(), os.O_RDONLY)
    try:
      return ioctl_GWINSZ(fd)
    finally:
      os.close(fd)
  except:
    pass
  # try `stty size`
  try:
    return tuple(int(x) for x in os.popen("stty size", "r").read().split())
  except:
    pass
  # try environment variables
  try:
    return tuple(int(os.getenv(var)) for var in ("LINES", "COLUMNS"))
  except:
    pass
  # i give up. return default.
  return (25, 80)

def main():
  rows, columns = getTerminalSize()
  
  s = "rows: "+str(rows)+" columns: "+str(columns)+"\n"

  sys.stderr.write(s)


if ( __name__ == '__main__'): main()
