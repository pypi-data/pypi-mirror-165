"""
generate protein structure feature for GCN.
features:
    adjacency_matrix:we replace adjcency matrix  with revsered distance which turn out work better
    onehot encode for sequece:
    secondary structure of protein:
    solvent accessible surface area of protein
    amino partial charge
    dihedral angles of a protein structure
    hydrogen donor
    dydorgen acceptor
    mass of amino acid
    max solvent accessible surface area of amino acid
    pka1 of amino acid
    pka2 of aminoa acid   
"""
import numpy as np
from numpy import linalg as LA
from Bio.PDB import *
import scipy.sparse as sp
from Bio.PDB.DSSP import DSSP

import gzip
import biotite.structure.io.pdb as pdb
import biotite.structure as struc
import biotite.application.dssp as dssp


def get_rdist(coord, threshold=9, max_length=None):
    """  normal adjacency of protein """
    d =  LA.norm(np.array([i.reshape(-1,1) - i.reshape(1,-1) for i in coord.T]),axis=0)
    d = d + sp.eye(d.shape[0],dtype=np.float32)
    d[d > threshold] = 0

    rd = np.power(d,-1)
    rd[np.isinf(rd)] = 0
    return rd

def get_second_structure(pdb_file,pdb_chain=0):
    sec_structure2num = {i:idx for idx,i in enumerate("BCEGHIST")}
    sec = ""
    model2 = PDBParser().get_structure("",pdb_file)[0]
    bio_dssp = DSSP(model2, pdb_file)
    for z in range(len(bio_dssp)):
        a_key = list(bio_dssp.keys())[z]
        sec += bio_dssp[a_key][2]
        sec = sec.replace("-","C")
    sec=np.array([sec_structure2num[_] for _ in sec])
    return sec

"""


"""
def pdb2graph_surface_atom(pdb_file,rd_threshold=9, res_threshold=5, atom_threshold=0.5):
    #atom_name2num = {'C':0, 'CA':1, 'N':2}
    atom2num = {'O': 0, 'CD1': 1, 'OD2': 2, 'ND2': 3, 'CD2': 4, 'CE1': 5, 'OE1': 6, 'OG1': 7, 'CE2': 8, 'NE1': 9, 
                'OH': 10, 'NZ': 11, 'OG': 12, 'OD1': 13, 'OXT': 14, 'NE2': 15, 'CA': 16, 'SG': 17, 'SD': 18, 'CG1': 19, 
                'CD': 20, 'NE': 21, 'CZ3': 22, 'CB': 23, 'CE': 24, 'CG2': 25, 'C': 26, 'CZ2': 27, 'CG': 28, 'CH2': 29, 
                'OE2': 30, 'NH1': 31, 'NH2': 32, 'CZ': 33, 'N': 34, 'CE3': 35, 'ND1': 36}

    res2num = { 'ALA':0, 'ARG':1, 'ASN':2, 'ASP':3, 'CYS':4, 'GLN':5, 'GLU':6, 'GLY':7, 'HIS':8, 'ILE':9,
                'LEU':10, 'LYS':11, 'MET':12, 'PHE':13, 'PRO':14, 'SER':15, 'THR':16, 'TRP':17, 'TYR':18, 'VAL':19 }
    
    res2abbr = { 'ALA':'A', 'ARG':'R', 'ASN':'N', 'ASP':'D', 'CYS':'C', 'GLN':'Q', 'GLU':'E', 'GLY':'G', 'HIS':'H', 'ILE':'I',
                'LEU':'L', 'LYS':'K', 'MET':'M', 'PHE':'F', 'PRO':'P', 'SER':'S', 'THR':'T', 'TRP':'W', 'TYR':'Y', 'VAL':'V' }
    
    sec2num = {i:idx for idx,i in enumerate("BCEGHIST")}
    
    #(0) read pdb_file
    model = pdb.PDBFile.read(pdb_file).get_structure(model=1)
    res = "".join([res2abbr[i[1]] for i in sorted(set(zip(model.res_id,model.res_name))) ])

    #(1)compute solvent accessible of atom
    model_res_id = np.repeat(np.arange(len(set(model.res_id))),np.bincount(model.res_id)[np.bincount(model.res_id)>0])
    
    atom_sasa = struc.sasa(model,vdw_radii="Single")
    res_sasa  = struc.apply_residue_wise(model, atom_sasa, np.sum)
    atom_res_sasa = np.array([res_sasa[i] for i in model_res_id]).ravel()

    atom_index = np.arange(len(atom_sasa))[(atom_res_sasa > res_threshold) 
                                            & (atom_sasa>atom_threshold) 
                                            & np.array([_ in atom2num.keys() for _  in model.atom_name])]

    feature_atom_sasa = atom_sasa[atom_index].reshape(-1,1)

    #(2) compute atom type
    feature_atom_type =sp.coo_matrix(np.eye(37,dtype=np.float32)[np.array([atom2num[i] for i in model.atom_name[atom_index]])])
   
    #(3) compute reversed distance matrix
    atom_coord = model.coord[atom_index]
    rd = get_rdist(atom_coord, rd_threshold)

    #(4)atom amino type:20 classes
    atom_res_num = [res2num[i] for i in model.res_name[atom_index]]
    feature_atom_res = sp.coo_matrix(np.eye(20,dtype=np.float32)[atom_res_num])
    
    #(5)secondary structure:8 classes
    sec = get_second_structure(pdb_file)   
    atom_sec = np.repeat(sec,np.bincount(model_res_id))
    feature_atom_sec =  sp.coo_matrix(np.eye(8,dtype=np.float32)[ atom_sec[atom_index]]) #shape(n,1)(np.float32)
   

    rd = sp.coo_matrix(rd)
    feature = sp.hstack([feature_atom_type, feature_atom_res, feature_atom_sec, feature_atom_sasa])
    return rd, feature, res
    


#hydrogy = {'H', 'H2', 'H3', 'HA', 'HA2', 'HA3', 'HB', 'HB1', 'HB2', 'HB3', 'HD1', 'HD11', 'HD12',
#           'HD13', 'HD2', 'HD21', 'HD22', 'HD23', 'HD3', 'HE', 'HE1', 'HE2', 'HE21', 'HE22', 'HE3',
#           'HG', 'HG1', 'HG11', 'HG12', 'HG13', 'HG2', 'HG21', 'HG22', 'HG23', 'HG3', 'HH', 'HH11', 
#           'HH12', 'HH2', 'HH21', 'HH22', 'HZ', 'HZ1', 'HZ2', 'HZ3',}
    

