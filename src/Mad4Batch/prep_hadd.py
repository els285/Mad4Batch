from os import listdir, getcwd, makedirs
from os.path import isfile, join, getsize
import sys 

mypath = "."

files_to_hadd = [f for f in listdir(mypath) if isfile(join(mypath, f)) and "delphes" in f and getsize(f)!=0][:10]

H = []
N = sys.aargv[1]
for i in range(0,len(files_to_hadd),N):
    H.append(files_to_hadd[i:i+N])
    
fname = getcwd().split("/")[-1]    

dirname = f"ROOT_outputs_N{N}"
makedirs(dirname,exist_ok=True)

with open("hadd_script.sh","w") as file:
    for i,L in enumerate(H):
        outname = f"{fname}_{i}.root"
        file.write(f"echo Writing {outname} \n")
        file.write(f"hadd {dirname}/{outname} " + " ".join(L) + "\n")


     