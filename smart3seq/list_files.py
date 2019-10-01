'''
Utility script to list files in the Smart-3seq project directory
for inclusion in the yaml config file.
'''

from os import listdir
from os.path import isfile, join

#project_dir = "/efs/docker/labcas/mcl/archive/Smart-3Seq/MDAnderson_Maitra/fastq"
#project_dir = "/efs/docker/labcas/mcl/archive/Smart-3Seq/UCSD/190603_K00180_0830_AH75HCBBXY_PE_SR75_ComboA/fastq"
#project_dir = "/efs/docker/labcas/mcl/archive/Smart-3Seq/UCSD/190627_K00180_0847_AH7MGKBBXY_SR75_Combo/fastq"
project_dir = "/efs/docker/labcas/mcl/archive/Smart-3Seq/UCSD/190807_K00180_0875_BH7GGGBBXY_SR75_Combo/fastq"
list_file = "fastq_files.txt"

fastq_files = sorted([f for f in listdir(project_dir) if isfile(join(project_dir, f))])
with open(list_file, 'w') as list_file:

   for f in fastq_files:
      if f.endswith(".fastq.gz"):
         list_file.write("  - \"%s\"\n" % f.replace(".fastq.gz", ""))

