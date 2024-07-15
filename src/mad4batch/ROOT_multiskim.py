from os import listdir, getcwd, makedirs
from os.path import isfile, join, getsize
from tqdm import tqdm
import argparse
from itertools import chain

from mad4batch.ROOT_skim import skim_delphes
from mad4batch.delphes_branches import branches as DB

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Skim multiple Delphes ROOT file")
    parser.add_argument("output_file", type=str, help="Path to the output ROOT file")
    parser.add_argument("branches", type=str, nargs='+', help="Branches to keep")

    args = parser.parse_args()
    print("Retaining these branches categories")
    print(args.branches)
    
    branch_dict = {k: DB[k] for k in (DB.keys() & args.branches)}
    branches_to_keep  = list(chain(*list(branch_dict.values())))
    print("Retaining these branches")
    for br in branches_to_keep:
        print(f" - {br}")
    
    mypath = "."
    files_to_hadd = [f for f in listdir(mypath) if isfile(join(mypath, f)) and "delphes" in f and getsize(f)!=0]
    print(f"Skimming {len(files_to_hadd)} files")
    
    for i,file in tqdm(enumerate(files_to_hadd)):
        outname = args.output_file.replace(".root",f"_{i}.root")
        skim_delphes(file, outname, branches_to_keep)


