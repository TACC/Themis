Systems = {
  'SLURM' : {
    'stampede' : { 
      'maxCoresPerNode' : 16,
      'submitHeader'    : """
          # stampede
          #SBATCH -J $(JOBNAME)
          #SBATCH -o $(JOBNAME).%j.out
          #SBATCH -p $(QUEUE)
          #SBATCH -N $(NODES)
          #SBATCH -n $(NP)
          #SBATCH -t $(TIME)
          #SBATCH -A $(ACCOUNT)
          """,
      },
    },
    'SGE' : {
      'ls4' : {
         'maxCoresPerNode' : 12,
         'submitHeader'    : """
               # lonestar
               #$ -V
               #$ -cwd
               #$ -N $(JOBNAME)
               #$ -A $(ACCOUNT)
               #$ -pe $(NPway NP=$(NP), NODES=$(NODES), WAY=$(WAY))
               #$ -q  $(QUEUE)
               #$ -l h_rt=$(TIME)
         """,
      },
  },
}
