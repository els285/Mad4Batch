# Mad4Batch

Simple partner repo for [MadLAD](https://github.com/tzuhanchang/MadLAD) for submitting large-scale MC production and post-processing. Pip-installable.

## Generation

`mad4condor.py` - Builds a directory containing HTCondor submission scripts for batch production.

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

As an alternative, can use :
`prep_hadd.py` - Builds `hadd` command for arbitrary number of output

