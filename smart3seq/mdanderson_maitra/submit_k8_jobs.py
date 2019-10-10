'''
Utility script to create the configuration for and submit
all the MD Anderson Smart-3seq jobs.
'''

import os

# directory containing fastq files (must be accessible to Kubernetes pods)
project_dir = "/efs-ecs/docker/labcas/mcl/archive/Smart-3Seq/MDAnderson_Maitra/fastq"

# directory to write config files (must be accessible to Kubernetes pods)
configs_dir = "/efs-ecs/docker/labcas/smart3seq/mdanderson_maitra/configs"
os.makedirs(configs_dir, exist_ok=True)

# directory to write k8s jobs to
jobs_dir = "/efs-ecs/docker/labcas/smart3seq/mdanderson_maitra/jobs"
os.makedirs(jobs_dir, exist_ok=True)

# template files (in current directory)
config_template = "config-mdanderson-template.yaml"
with open(config_template, 'r') as file:
    config_data = file.read()

job_template = "k8s_job_template.yml"
with open(job_template, 'r') as file:
    job_data = file.read()

# loop over fastq files
fastq_files = sorted([f for f in os.listdir(project_dir) if os.path.isfile(os.path.join(project_dir, f))])
for f in fastq_files:
    if f.endswith(".fastq.gz"):
        
        # extract sample name
        sample = f.replace(".fastq.gz", "")
        
        # write config for this sample
        _config_file = os.path.join(configs_dir, "config-%s.yaml" % sample)
        _config_data = config_data.replace("@THE_SAMPLE@", sample)
        print("Writing config file: %s" % _config_file)
        with open(_config_file, 'w') as cf:
            cf.write(_config_data)
            
        # write k8s job spec
        _job_file = os.path.join(jobs_dir, "k8s_job_%s.yml" % sample)
        _job_data = job_data.replace("@THE_CONFIG_FILE@", _config_file).replace("@THE_SAMPLE@", sample)
        print("Writing job file: %s" % _job_file)
        with open(_job_file, 'w') as jf:
            jf.write(_job_data)
            
        # submit k8s job
        command = "kubectl create -f %s" % _job_file
        print("Executing command: %s" % command)
        os.system(command)
            
