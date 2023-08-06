import numpy as np

class ara_net_node2vec:
    def __init__(self, data_file=None):
        self.features = None
        self.data_file = data_file #pkl file of a dictionary in which key is arabidopsis gene id and value is 1d numpy array.
        self.shape = None
    
    def __getitem__(self,index):
        if self.features == None:
            self.features = np.load(self.data_file,allow_pickle=True)
            temp = self.features.popitem()
            self.features.update({temp[0]:temp[1]})
            self.shape = temp[1].shape

        if index in self.node2vec.keys():
            v =  self.features[index]
        else:
            v = np.zeros(self.shape)
        return v
