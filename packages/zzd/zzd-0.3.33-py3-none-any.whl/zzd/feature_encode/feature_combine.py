import os
import numpy as np
from zzd.feature_encode.ac import ac
from zzd.feature_encode.dpc import dpc
from zzd.feature_encode.ct import ct
from zzd.feature_encode.cksaap import cksaap
from zzd.feature_encode.personal_features import personal_features

class feature_combine:
    def __init__(self, a_features, b_features, seqs, data_file_dict = dict()):
        self.seqs = seqs
        self.a_features = a_features
        self.b_features = b_features
        
        self.features = {"ac":ac,  "dpc":dpc,  "ct":ct, "cksaap":cksaap}
        self.more_features = {k:personal_features(v) for k,v in data_file_dict.items()}

    def encode(self,ppis):
        x = []
        for a,b in ppis:
            temp_a = []
            temp_b = []
            for feature in self.a_features:
                if feature in self.more_features.keys():
                    temp_a.append(self.more_features[feature][a])
                else:
                    temp_a.append(self.features[feature](self.seqs[a]))
            
            for feature in self.b_features:
                if feature in self.more_features.keys():
                    temp_b.append(self.more_features[feature][b])
                else:
                    temp_b.append(self.features[feature](self.seqs[b]))

            temp_a = np.hstack(temp_a)
            temp_b = np.hstack(temp_b)
            x.append(np.hstack((temp_a,temp_b)))
        return np.array(x)


