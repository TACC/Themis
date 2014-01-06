from JobSubmitBase import JobSubmitBase

class Interactive(JobSubmitBase):
  def __init__(self):
    JobSubmitBase.__init__(self)

  def runtest(self, *kw):
    sA = []
    sA.append("./" + kw['scriptFn'])
    sA.append(">")
    sA.append(kw['idtag'] + ".log")
    sA.append("2>&1 < /dev/null")
    if (kw['background']):
      sA.append("&")

    s = " ".join(sA)
    os.system(s)
