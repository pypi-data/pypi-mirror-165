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
    return sp.coo_matrix(rd)

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
def pdb2graph_atom(pdb_file,threshold=9):
    atom_name2num = {'C':0, 'CA':1, 'N':2}
    res_name2num = {
        'ALA':0, 'ARG':1, 'ASN':2, 'ASP':3, 'CYS':4, 'GLN':5, 'GLU':6, 'GLY':7, 'HIS':8, 'ILE':9,
        'LEU':10, 'LYS':11, 'MET':12, 'PHE':13, 'PRO':14, 'SER':15, 'THR':16, 'TRP':17, 'TYR':18, 'VAL':19 }
    sec_structure2num = {i:idx for idx,i in enumerate("BCEGHIST")}

    model = pdb.PDBFile.read(pdb_file).get_structure(model=1)
    
    #(5)compute solvent accessible of atom
    atom_sasa = struc.sasa(model,vdw_radii="Single")
    feature_atom_sasa = np.array([(i,i,i) for i in res_sasa]).ravel().reshape(-1,1)
    
    atom_type  = np.array([atom_name2num[i] for i in model.atom_name if i in atom_name2num.keys()])
    atom_res   = np.array([res_name2num[b] for a,b in zip(model.atom_name, model.res_name) if a in atom_name2num.keys()])
    atom_coord = np.array([b for a,b in zip(model.atom_name,model.coord) if a in atom_name2num.keys()])
   
    res  = "".join([b for a,b in zip(model.atom_name, model.res_name) if a =="CA"])
    #(1)compute reverse distance matrix
    rd = get_rdist(atom_coord, threshold) 

    #(2)atom type: 3 classes: C, CA, N.
    feature_atom_type = sp.coo_matrix(np.eye(3,dtype=np.float32)[atom_type])

    #(3)atom amino type:20 classes
    feature_atom_res = sp.coo_matrix(np.eye(20,dtype=np.float32)[atom_res])
    

    #(4)secondary structure:8 classes
    sec = get_second_structure(pdb_file)
    sec = np.array([(i,i,i) for i in sec]).ravel()
    feature_atom_sec =  sp.coo_matrix(np.eye(8,dtype=np.float32)[sec]) #shape(n,1)(np.float32)


    feature = sp.hstack([feature_atom_type, feature_atom_res, feature_atom_sec, feature_atom_sasa])
    return rd, feature, res
    




