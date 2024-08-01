# Mad4Batch

Simple partner repo for [MadLAD](https://github.com/tzuhanchang/MadLAD) for submitting large-scale MC production and post-processing. Pip-installable.

## Generation

`condor.py` - Builds a directory containing HTCondor submission scripts for batch production.
Example:
```
python -m mad4batch.condor <MadLAD-config> <Nfiles> --lhe --hepmc
```

`<MadLAD-config>` should just be the name of the config with the `MadLAD` directory.
The optional flags `--lhe` and `--hepmc` will return the output LHE and HepMC files if specified.

## Post-Processing

`ROOT_skim.py` - ROOT-based skimming on output DELPHES file.

`ROOT_multiskim.py` - Skims all output DELPHES ROOT files, retaining classes e.g.
```bash
cd a_directory_with_many_delphes_outputs
python -m mad4batch.ROOT_multiskim HighLevel.root Muon Electron Jet MissingET
```
generates N files (`HighLevel_i.root`) containing the `Muon Electron Jet MissingET` classes.
These can then be combined through
```bash
hadd HighLevel_Combined.root HighLevel_*
```

### On Condor
The `skim4batch.py` file generates a job script and HTCondor submission script to run the skimming in parallel over many files which following the name convention `delphes_123456_i.root` where `i` is the integer of the HTCondor generation job. 
```
python -m mad4batch.skim4condor --input_file delphes_123456 --output_file outputskim.root --config branches4skim.txt
```
The `branches4skim.txt` file contains a list of the branches to retain.
