'''
Utility script to list files in the Smart-3seq project directory
for inclusion in the yaml config file.
'''

from os import listdir
from os.path import isfile, join

project_dir = "/efs/docker/labcas/mcl/archive/Smart-3Seq/MDAnderson_Maitra/fastq"
list_file = "fastq_files.txt"

fastq_files = sorted([f for f in listdir(project_dir) if isfile(join(project_dir, f))])
with open(list_file, 'w') as list_file:

   for f in fastq_files:
      if f.endswith(".fastq.gz"):
         list_file.write("  - \"%s\"\n" % f.replace(".fastq.gz", ""))

