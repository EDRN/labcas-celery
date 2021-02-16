# script to list the BRSI data directory and submit all ML jobs
import os
import sys

DATA_DIR = "/efs-ecs/docker/labcas/Combined_Imaging_and_Blood_Biomarkers_for_Breast_Cancer_Diagnosis"
STRING_OUT = "/efs-ecs/docker/labcas/Combined_Imaging_and_Blood_Biomarkers_for_Breast_Cancer_Diagnosis"
STRING_IN  = "/data/BRSI"

def main():
    
    for root, dirs, files in os.walk(DATA_DIR):
        if 'PROC' in root:
            for file in files:
                fp = os.path.join(root, file)
                print("Processing: %s" % fp)
                
                image_path = fp.replace(STRING_OUT, STRING_IN)
                command = "airflow trigger_dag  --conf '{\"image_path\": \"%s\"}' brsi" % image_path
                print(f"Executing command={command}")
                os.system(command)
       
if __name__ == "__main__":
    main()
