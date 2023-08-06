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

def get_rdist(coord, threshold=9.5, max_length=None):
    """  normal adjacency of protein """
    distance_matrix =  LA.norm(np.array([i-coord  for i in coord]),axis=2)
    d = distance_matrix + sp.eye(distance_matrix.shape[0],dtype=np.float32)
    rd = np.power(d,-1)
    rd[np.isinf(d)] = 0
    rd = np.multiply(rd,rd>1/threshold)
    #rd = sp.csr_matrix(rd) 
    return rd


def pdb2graph(pdb_file,threshold=9.5):
    """

    """
    amino2abv = {
        'ALA':'A',    'ARG':'R',  'ASN':'N',  'ASP':'D',  'CYS':'C',
        'GLN':'Q',    'GLU':'E',  'GLY':'G',  'HIS':'H',  'ILE':'I',
        'LEU':'L',    'LYS':'K',  'MET':'M',  'PHE':'F',  'PRO':'P',
        'SER':'S',    'THR':'T',  'TRP':'W',  'TYR':'Y',  'VAL':'V' }
    amino2mass = {
        "A": 89.1,   "R": 174.2,    "N": 132.12,    "D": 133.11,    "C": 121.16,
        "Q": 146.15, "E": 147.13,   "G": 75.07,     "H": 155.16,    "I": 131.18,
        "L": 131.18, "K": 146.19,   "M": 149.21,    "F": 165.19,    "P": 115.13,
        "S": 105.09, "T": 119.12,   "W": 204.23,    "Y": 181.19,    "V": 117.15, }
    amino2MaxASA={
        "A":129,    "R":274,    "N":195,    "D":193,    "C":167,
        "E":223,    "Q":225,    "G":104,    "H":224,    "I":197,
        "L":201,    "K":236,    "M":224,    "F":240,    "P":159,
        "S":155,    "T":172,    "W":285,    "Y":263,    "V":174,}#https://en.wikipedia.org/wiki/Relative_accessible_surface_area
    amino2pka1={
        "A":2.34,   "R":2.17,   "N":2.02,   "D":1.88,   "C":1.96,
        "E":2.19,   "Q":2.17,   "G":2.34,   "H":1.82,   "I":2.36,
        "L":2.36,   "K":2.18,   "M":2.28,   "F":1.83,   "P":1.99,
        "S":2.21,   "T":2.09,   "W":2.83,   "Y":2.2,    "V":2.32 }#https://www.chem.ucalgary.ca/courses/351/Carey5th/Ch27/ch27-1-4-2.html
    amino2pka2={
        "A":9.69,   "R":9.04,   "N":8.8,    "D":9.6,    "C":8.18,
        "E":9.67,   "Q":9.13,   "G":9.6,    "H":9.17,   "I":9.6,
        "L":9.6,    "K":8.95,   "M":9.21,   "F":9.13,   "P":10.6,
        "S":9.15,   "T":9.1,    "W":9.39,   "Y":9.11,   "V":9.62,}#https://www.chem.ucalgary.ca/courses/351/Carey5th/Ch27/ch27-1-4-2.html
    amino2Hydropathy ={
        "A":1.8,    "C":2.5,    "D":-3.5,   "E":-3.5,   "F":2.8,
        "G":-0.4,   "H":-3.2,   "I":4.5,    "K":-3.9,   "L":3.8,
        "M":1.9,    "N":-3.5,   "P":-1.6,   "Q":-3.5,   "R":-4.5,
        "S":-0.8,   "T":-0.7,   "V":4.2,    "W":-0.9,   "Y":-1.3}#https://www.cgl.ucsf.edu/chimera/docs/UsersGuide/midas/hydrophob.html; A simple method for displaying the hydropathic character of a protein. K;
    amino2volume={
        "A":88.6,   "R":173.4,  "N":114.1,  "D":111.1,  "C":108.5,
        "Q":143.8,  "E":138.4,  "G":60.1,   "H":153.2,  "I":166.7,
        "L":166.7,  "K":168.6,  "M":162.9,  "F":189.9,  "P":112.7,
        "S":89,     "T":116.1,  "W":227.8,  "Y":193.6,  "V":140, }#https://www.imgt.org/IMGTeducation/Aide-memoire/_UK/aminoacids/abbreviation.html
    #amino2polarity={
    #"A":-0.591, "R":1.538,  "N":0.945,  "D":1.05,   "C":-1.343,
    #"Q":0.931,  "E":1.357,  "G":-0.384, "H":0.336,  "I":-1.239,
    #"L":-1.019, "K":1.831,  "M":-0.663, "F":-1.006, "P":0.189,
    #"S":-0.228, "T":-0.032, "W":-0.595, "Y":0.26,   "V":-1.337}

    amino2num = {i:idx for idx,i in enumerate('ARNDCQEGHILKMFPSTWYV')}
    sec2num = {i:idx for idx,i in enumerate("BCEGHIST")}

    #(1)compute reverse distance matrix
    if pdb_file[-3:] == ".gz":
        with gzip.open(pdb_file,'rt') as f:
            model = pdb.PDBFile.read(f).get_structure(model=1)
    else:
        with open(pdb_file,'r') as f:
            model = pdb.PDBFile.read(f).get_structure(model=1)

    res = "".join([amino2abv[i.res_name] for i in model if i.atom_name=="CA"])   #sequence of a protein.
    coord = [i.coord for i in model if i.atom_name=="CA"]               #C alpha atom coord of a protein.
    rd = get_rdist(coord,threshold) #shape(n,n)(np.float32)
    
    #(2)seq onehot 
    seq_arr = [amino2num[_] for _ in res]
    res_onehot = np.eye(20,dtype=np.float32)[seq_arr]#shape(n,20)(np.float32)
    

    #(3)computer secondary structure
    sec = dssp.DsspApp.annotate_sse(model)  #this function have bug that sometime not work very well!!!
    if len(sec) != len(coord):              #when meet bug,we try biopython method recompute secondary structure.
        sec = ""
        if pdb_file[-3:] == ".gz":
            with gzip.open(pdb_file,"rt") as f:
                structure2 = PDBParser().get_structure("",f)
        else:
            structure2 = PDBParser().get_structure("",pdb_file)
        model2 = structure2[0]
        bio_dssp = DSSP(model2, pdb_file)
        for z in range(len(bio_dssp)):
            a_key = list(bio_dssp.keys())[z]
            sec += bio_dssp[a_key][2]
            sec = sec.replace("-","C")

    sec=np.array([sec2num[_] for _ in sec])
    res_sec_structure = np.eye(8,dtype=np.float32)[sec]#shape(n,1)(np.float32)

    #(4)compute solvent accessible surface area
    atom_sasa = struc.sasa(model,vdw_radii="Single")
    res_sasa = struc.apply_residue_wise(model, atom_sasa, np.sum)/250
    res_sasa = res_sasa.reshape(-1,1)#shape(n,1)(np.float32)

    #(5)comput relative accessible surface area
    res_rsa = struc.apply_residue_wise(model, atom_sasa, np.sum)/np.array([amino2MaxASA[_] for _ in res],dtype=np.float32)
    res_rsa = res_rsa.reshape(-1,1)

    #(7)compute the dihedral angles of a protein structure
    phi,psi,omega = struc.dihedral_backbone(model)
    res_dihedral_angles = np.stack([np.rad2deg(phi), np.rad2deg(psi)]).T/180
    res_dihedral_angles[np.isnan( res_dihedral_angles)]=0.5 #shape(n,2)(np.float32)
    
    #(6)amino partial charge
    model.bonds = struc.connect_via_residue_names(model)
    atom_partial_charge = struc.partial_charges(model)
    res_partial_charge = struc.apply_residue_wise(model,atom_partial_charge,np.sum)*50
    res_partial_charge = res_partial_charge.reshape(-1,1)#shape(n,)(np.float32)


    #(8)Hydrogen donor
    triplets = struc.hbond(model)
    res_donor = np.zeros(len(res),dtype=np.float32)#shape(n,1)(np.float32)
    for _ in triplets[:,0]:
        res_donor[model[_].res_id-1]+=1
    res_donor = res_donor.reshape(-1,1)/6

    #(9)Hydorgen acceptor
    res_acceptor = np.zeros(len(res),dtype=np.float32)#shape(n,1)(np.float32)
    for _ in triplets[:,2]:
        res_acceptor[model[_].res_id-1]+=1
    res_acceptor = res_acceptor.reshape(-1,1)/6

    #(10)mass
    #res_mass = np.array([amino2mass[_] for _ in res],dtype=np.float32).reshape(-1,1)/256#shape(n,1)(np.float32)

    #(11)MaxASA
    #res_MaxASA = np.array([amino2MaxASA[_] for _ in res],dtype=np.float32).reshape(-1,1)/512#shape(n,1)(np.float32)

    #(11)Pka(COOH)
    #res_pka1 = np.array([amino2pka1[_] for _ in res],dtype=np.float32).reshape(-1,1)/4#shape(n,1)(np.float32)
    
    #(12)PKa(NH3+)
    #res_pka2 = np.array([amino2pka2[_] for _ in res],dtype=np.float32).reshape(-1,1)/16#shape(n,1)(np.float32)
    
    #(13)hydropathy
    #res_hydropathy = np.array([amino2Hydropathy[_] for _ in res],dtype=np.float32).reshape(-1,1)/8#shape(n,1)(np.float32)

    #(14)volume
    #res_volume = np.array([amino2volume[_] for _ in res],dtype=np.float32).reshape(-1,1)/256


    #compress features to sparse matrix
    #res_onehot,res_sasa,res_sec_structure,res_dihedral_angles,res_partial_charge,res_donor,res_acceptor,res_volume
    rd = sp.coo_matrix(rd)
    feature = sp.coo_matrix(np.hstack([res_onehot, res_sasa,res_sec_structure]))
    return rd,feature,res
    




