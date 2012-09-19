#!/usr/bin/env python

import os
import sys

import simplejson as json
from Bio.PDB.PDBParser import PDBParser


def load_chains(raw, pdb_id, pdb_type, known):
    parser = PDBParser()
    structure = parser.get_structure(pdb_id, raw)
    data = {'ordering': []}
    for model in structure:
        for chain in model:
            chain_id = chain.get_id()
            data[chain_id] = {'residues': [], 'sequence': []}
            for residue in chain:
                name = residue.resname.strip()
                if name in known:
                    res_id = residue.get_id()
                    id_data = [structure.get_id(), pdb_type, model.get_id(),
                               chain_id, res_id[1], residue.resname, res_id[2]]
                    id_data = [str(part).strip() for part in id_data]
                    unit_id = '_'.join(id_data)
                    data[chain_id]['residues'].append(unit_id)
                    data[chain_id]['sequence'].append(known[name])
                    data['ordering'].append(unit_id)

            if not data[chain_id]['residues']:
                del data[chain_id]
            else:
                data[chain_id]['sequence'] = ''.join(data[chain_id]['sequence'])
    return data


def load_known(known_file):
    with open(known_file, 'r') as raw:
        known = json.load(raw)
    return known


def main(pdb_file, name, pdb_type, known):
    with open(pdb_file, 'r') as raw:
        return load_chains(raw, name, pdb_type, known)


if __name__ == '__main__':
    known = load_known(sys.argv[1])
    for pdb_file in sys.argv[2:]:
        name = os.path.basename(pdb_file)
        name = os.path.splitext(name)[0]
        pdb_type = 'AU'
        # if pdb_file[4] != '.':
        #     pdb_type = 'BA' + pdb_file[4]
        data = {}
        data.update({name: main(pdb_file, name, pdb_type, known)})
        print(json.dumps(data))
