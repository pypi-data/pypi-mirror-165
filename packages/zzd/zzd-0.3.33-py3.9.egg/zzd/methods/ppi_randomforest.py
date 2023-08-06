import os
import numpy as np
from Bio import SeqIO
from sklearn.ensemble import RandomForestClassifier
from zzd.feature_encode.feature_combine import feature_combine


def load_data(ppi_file, seqs_file, a_features, b_features, data_file_dict):
    """
    ppi_file: tab format file with 3 column : a_id b_id    label.
    seqs_file:fasta format file.
    a_features:list of protein a feature. such as ac,dpc,ct,...
    b_features:list of protein b feature. such as ac,dpc,ct,...
    data_file_dict:dictionary of personal features that key is name and value is a pkl file.
        pkl file represent a dictionary in which key is protein id and values is a 1d numpy array.
    """
    ppis = np.genfromtxt(ppi_file,str)
    X,Y = np.array(ppis[:,:2],str), np.array(ppis[:,2],int)
    seqs = {i.id:str(i.seq) for i in SeqIO.parse(seqs_file,'fasta')}
    encode = feature_combine(a_features,
                    b_features,
                    seqs,
                    data_file_dict)
    return encode.encode(X),Y


def ppi_randomforest(
                train_file, 
                test_file, 
                seqs_file, 
                a_features,
                b_features,
                data_file_dict = dict(),
                n_estimators=200,
                n_jobs=-1, ):
    """
    train_file: tab format ppi train file with three column: a_id b_id and label
    test_file:  tab format ppi test  file with three column: a_id b_id and label

    seqs_file: fasta sequence
    feature_encode: AC,DPC,CT,CKSAAP,...
    data_file_dict:optional, 
    """
    x_train, y_train = load_data(
                        train_file,
                        seqs_file,
                        a_features,
                        b_features,
                        data_file_dict)

    x_test, y_test = load_data(
                        test_file,
                        seqs_file,
                        b_features,
                        b_features,
                        data_file_dict)
    
    model = RandomForestClassifier(
                        n_estimators=n_estimators,
                        n_jobs=n_jobs, 
                        random_state=1)

    model.fit(x_train,y_train)
    
    y_test_pred = model.predict_proba(x_test)[:, 1]
    return y_test_pred


def ppi_randomforest_predict(
            query_file,
            seqs_file,
            a_features,
            b_features,
            model_file = None,
            data_file_dict = dict(),
            n_estimators = 200,
            n_jobs=-1
            ):

    X = np.genfromtxt(query_file,str) 
    seqs = {i.id:str(i.seq) for i in SeqIO.parse(seqs_file,'fasta')}
    encode = feature_combine(a_features , b_features, seqs_file, data_file_dict)
    x = encode.ensemble(X)

    model = None
    y_pred =  model.predict_proba(x)[:, 1]
    return y_pred

    








