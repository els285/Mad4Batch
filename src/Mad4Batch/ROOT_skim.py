import ROOT
import argparse

def skim_delphes(input_file, output_file, branches_to_keep):
    # Open the input file
    input_root_file = ROOT.TFile.Open(input_file, "READ")
    input_tree = input_root_file.Get("Delphes")

    # Create the output file and a new tree
    output_root_file = ROOT.TFile.Open(output_file, "RECREATE")
    output_tree = input_tree.CloneTree(0)
    output_tree.SetBranchStatus("*", 0)
    
    for branch in branches_to_keep:
        output_tree.SetBranchStatus(branch,1)

    # Copy the events to the new tree
    # for event in input_tree:
    #     output_tree.Fill()

    # Write the new tree to the output file
    output_tree.Write()
    output_root_file.Close()
    input_root_file.Close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Skim a Delphes ROOT file")
    parser.add_argument("input_file", type=str, help="Path to the input Delphes ROOT file")
    parser.add_argument("output_file", type=str, help="Path to the output ROOT file")
    parser.add_argument("branches", type=str, nargs='+', help="Branches to keep")

    args = parser.parse_args()

    skim_delphes(args.input_file, args.output_file, args.branches)
