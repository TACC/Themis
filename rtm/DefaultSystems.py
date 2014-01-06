def NPway(tbl, envTbl, funcTbl):
  batchTbl = funcTbl['batchTbl']
  np       = int(tbl['NP']) or -1
  maxWay   = batchTbl['maxCoresPerNode']
  userWay  = int(tbl.WAY) or -1
  if (userWay > 0 ):
    way = userWay
  else:
    way = batchTbl['maxCoresPerNode']

  nNodes    = -1
  userNodes = int(tbl['NODES']) or -1

  if (userNodes > 0):
    nNodes = userNodes

  if (nNodes > 0):
    npWay = str(way) + "way " + str(nNodes*maxWay)
  elif (np <= maxWay and way == maxWay):
    npWay = str(np) + "way " + maxWay
  else:
    nNodes = int(np/way) +1
    npWay  = way + "way " + str(nNodes*maxWay)
  return npWay
DefaultSystems = {
  'INTERACTIVE' : {
      'submitHeader'    : "",
      'mprCmd'          : "mpirun -np $(NP) $(CMD) $(CMD_ARGS)",
      'CurrentWD'       : ".",
      'maxCoresPerNode' : 1,
      'submitCmd'       : "",
  },
  'SLURM' : {
        'mprCmd'          : "ibrun $(CMD) $(CMD_ARGS)",
        'submitCmd'       : "sbatch ",
        'CurrentWD'       : ".",
        'maxCoresPerNode' : 1,
        'submitHeader'    : """
               #SBATCH -J $(JOBNAME)
               #SBATCH -o $(LOGNAME)
               #SBATCH -p $(QUEUE)
               #SBATCH -N $(NODES)
               #SBATCH -n $(NP)
               #SBATCH -t $(TIME)
               #SBATCH -A $(ACCOUNT)
         """,
  },
  'SGE' : {
         'submitHeader' : """
               #$ -V
               #$ -cwd
               #$ -N $(JOBNAME)
               #$ -A $(ACCOUNT)
               #$ -pe $(NPway NP=$(NP) NODES=$(NODES) WAY=$(WAY))
               #$ -q  $(QUEUE)
               #$ -l h_rt=$(TIME)
         """,
         'mprCmd'    : "ibrun $(CMD) $(CMD_ARGS)",
         'submitCmd' : "qsub ",
         'queueTbl'  : {'short':"development", 'medium':"normal",
                        'long':"long",         'systest':"systest"},
         'CurrentWD' : ".",
         'maxCoresPerNode' : 1,
         'NODES' : -1,
         'WAY'   : -1,
         'NPway' : NPway,
  },
}

  
    
