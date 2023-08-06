import numpy as np
from numpy import linalg as LA
from Bio.PDB import *
import gzip

def get_average_coord(pdb_file=None, pdb_chain="A", pdb_id=""):
    """
    input:
        pdb_file:file of pdb 
    output
         seq and coordinate  of a pdb file.
    """
    amino2abv = {'ALA':'A',    'ARG':'R',  'ASN':'N',  'ASP':'D', 'CYS':'C',
              'GLN':'Q',    'GLU':'E',  'GLY':'G',  'HIS':'H',  'ILE':'I',
              'LEU':'L',    'LYS':'K',  'MET':'M',  'PHE':'F',  'PRO':'P',
              'SER':'S',    'THR':'T',  'TRP':'W',  'TYR':'Y',  'VAL':'V'}
    if pdb_file[-2:] == 'gz':
        with gzip.open(pdb_file,'rt') as f:
            structure = PDBParser().get_structure(pdb_id,f)
    else:
        structure = PDBParser().get_structure(pdb_id,pdb_file)

    chain = [j for i in list(structure[0]) if i.id == pdb_chain for j in list(i)]
    seq = ''.join([amino2abv[i.resname] for i in chain])
    coord = np.array([np.mean([j.coord for j in i],axis=0) for i in chain])
    return seq, coord


def get_Ca_coord(pdb_file=None, pdb_chain="A", pdb_id=""):
    """
    input:
        pdb_file:file of pdb 
    output
         seq and coordinate  of a pdb file.
    """
    amino2abv = {'ALA':'A',    'ARG':'R',  'ASN':'N',  'ASP':'D', 'CYS':'C',
              'GLN':'Q',    'GLU':'E',  'GLY':'G',  'HIS':'H',  'ILE':'I',
              'LEU':'L',    'LYS':'K',  'MET':'M',  'PHE':'F',  'PRO':'P',
              'SER':'S',    'THR':'T',  'TRP':'W',  'TYR':'Y',  'VAL':'V'}
    if pdb_file[-2:] == 'gz':
        with gzip.open(pdb_file,'rt') as f:
            structure = PDBParser().get_structure(pdb_id,f)
    else:
        structure = PDBParser().get_structure(pdb_id,pdb_file)

    chain = [j for i in list(structure[0]) if i.id == pdb_chain for j in list(i)]
    seq = ''.join([amino2abv[i.resname] for i in chain])
    coord = np.array([j.coord for i in chain for j in i if j.name=="CA"])
    return seq, coord

def calcute_adjacency(coord, threshold=9.5, max_length=None):
    """
    fetch normal adjacency of protein
    chain_amino_coord => distance_matrix => adjacency_matrix => normal_adjacency_matrix
    """
    distance_matrix =  LA.norm(np.array([i-coord  for i in coord]),axis=2)
    adjacency_matrix = np.array(distance_matrix < threshold, dtype=int)
    return adjacency_matrix

def get_Ca_distance(pdb_file,chain="A",threshold=12.5):
    seq,coord = get_Ca_coord(pdb_file,chain=chain)
    Ca_distance = calcute_adjacency(coord,threshold)
    return Ca_distance



