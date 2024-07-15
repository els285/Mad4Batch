import yaml
import sys
import os 
from os import listdir
from os.path import isfile, join
from datetime import datetime



class Mad4Condor(object):
    
    def __init__(self,config_name,cfg,Njobs):
        self.config_name    = config_name
        self.cfg            = cfg
        self.Njobs          = Njobs
        self.name           = self.cfg["gen"]["block_model"]["save_dir"]
        
        self.create_directory()
        self.write_job_script()
        self.write_submit_file()
        # self.write_delphes_hadd_script()
        

    
    def create_directory(self):
        
        dt = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        self.condor_directory_name = f"{self.name}_condorrun_{dt}"
        assert not os.path.isdir(self.condor_directory_name), f"{self.condor_directory_name} is already a directory and will not be over-written"
        os.mkdir(self.condor_directory_name)
        

    def write_job_script(self):
        text = f"""#!/bin/bash

# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$('/data/zihanzhang/pkgs/miniforge3/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/data/zihanzhang/pkgs/miniforge3/etc/profile.d/conda.sh" ]; then
        . "/data/zihanzhang/pkgs/miniforge3/etc/profile.d/conda.sh"
    else
        export PATH="/data/zihanzhang/pkgs/miniforge3/bin:$PATH"
    fi
fi
unset __conda_setup
# <<< conda initialize <<<
conda activate madlad

cd MadLAD   # Execute in MadLAD folder
python -m madlad.generate --config-name={self.config_name} gen.block_run.iseed=$RANDOM
cd -        # Return to condor work directory

        """
        
        with open(f"{self.condor_directory_name}/job.sh","w") as file:
            file.write(text)
        
        
        
    def write_submit_file(self):
        
        text=f"""# Submit file for HTCondor
universe   = vanilla
executable = job.sh
arguments  = $(RandomNumber)
output     = $(ClusterId).$(Process).out
error      = $(ClusterId).$(Process).err
log        = $(ClusterId).$(Process).log
request_cpus = 12
request_memory = 50 GB
request_disk = 1 GB
transfer_executable = True
should_transfer_files = YES
transfer_input_files    = ../MadLAD
transfer_output_files = MadLAD/{self.name}.root
transfer_output_remaps = "{self.name}.root = delphes_$(Cluster)_$(Process).root"

when_to_transfer_output = ON_EXIT 

queue {self.Njobs}"""

        with open(f"{self.condor_directory_name}/submit.sub","w") as file:
            file.write(text)
            

    # def write_delphes_hadd_script(self):
        
    #     hadd_string = """hadd combined_delphes_output.root"""
        
    #     onlyfiles = [f for f in listdir(self.condor_directory_name) if isfile(join(self.condor_directory_name, f)) and "delphes" in f and f[-5:]==".root"]
        
    #     for f in onlyfiles:
    #         hadd_string += f
            
    #     with open(f"{self.condor_directory_name}/hadd_outputs.txt","w") as file:
    #         file.write(hadd_string)
       
       
       
       
def main():
    
    # config_filepath = f"MadLAD/processes/{sys.argv[1]}"
    config_filepath = sys.argv[1]
    Njobs           = sys.argv[2]
    
    with open(config_filepath) as stream:
        try:
            cfg = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            
    config_name = config_filepath.split("/")[-1]
    
    RUN = Mad4Condor(config_name,cfg,Njobs)
    
main()