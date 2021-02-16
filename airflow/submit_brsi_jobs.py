# script to list the BRSI data directory and submit all ML jobs
import os

DATA_DIR = "/Users/cinquini/data/BRSI_Demo"
STRING_OUT = "/Users/cinquini/data/BRSI_Demo"
STRING_IN  = "/data/BRSI"

def main():
    
    for root, dirs, files in os.walk(DATA_DIR):
        if 'PROC' in root:
            for file in files:
                fp = os.path.join(root, file)
                print("Processing: %s" % fp)
                
                image_path = fp.replace(STRING_OUT, STRING_IN)
                command = "airflow trigger_dag  --conf '{\"image_path\": \"'${%s}'\"}' brsi" % image_path
                print(f"Executing command={command}")

if __name__ == "__main__":
    main()