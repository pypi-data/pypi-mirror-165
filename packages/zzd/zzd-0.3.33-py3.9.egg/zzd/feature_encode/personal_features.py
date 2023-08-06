import numpy as np

class personal_features:
    def __init__(self, data_file=None):
        self.features = None
        self.data_file = data_file
        self.shape = None
    
    def __getitem__(self,index):
        if self.features == None:
            self.features = np.load(self.data_file,allow_pickle=True)
            temp = self.features.popitem()
            self.features.update({temp[0]:temp[1]})
            self.shape = temp[1].shape

        if index in self.features.keys():
            v =  self.features[index]
        else:
            v = np.zeros(self.shape)
        return v

