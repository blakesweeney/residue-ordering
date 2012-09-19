# Compute Nucleotide Ordering #

This is a tool to compute the ordering or nucleotides in a PDB file.


## Usage ##

Put PDB files in `tmp/` and run `make`. This will produce a `out/resolved.json`
which will contain all data processed by `bin/resolved.py`. 

Note that many structures are discontinuous, which will cause BioPython to spit
out lots of warnings.


## Files ##

* requirements.txt

    A pip requirements file for this.

* `in/known.json`

    This is a json file of all known residue types. This is used to filter
results from reading a PDB to only extract known residues. Many chains have a
lot of water and ions or ligands in them. We wish to skip these so anything not
found in this file is skipped. Currently it only contains RNA nucleotides and
modified nucleotides.

    The format is a simple modified-type -> standard-type object. This mapping
is used to determine the sequence of each chain. For example `2MA` which is a
modified `A` will be represented as an `A` in the sequence. While the nucleotide
ids will use the correct `2MA` unit.


## Scripts ##

### `bin/resolved.py` ###

#### `bin/resolved.py in/known.json PDB_1 PDB_2 ...` ####

  This is a script to parse one or more PDB files and determine the ordering of
nucleotides, the resolved sequence and the nucleotide ids. This will produce one
JSON object written to standard out of the form:

        {"pdb_id": {"ordering": [nt1, nt2, ...]
                    chain_id: {"sequence": sequence_string, "residues": [nt1, nt2] }
                   }
         ...
         }

  This assumes that each file is named pdb_id.pdb. The ordering entry is the
global ordering of all nucleotides in the file, while the residue entries for
each object are the residues in order for that chain.

Currently this does not determine asymmetric unit/biological assembly correctly,
it always assumes asymmetric unit.


# Author #
Blake Sweeney <bsweene@bgsu.edu>
