import numpy as np
import os

#def ara_node2vec_init():
#    zzd_lib = f"{os.environ['HOME']}/.local/zzd/lib"
#    if not os.path.exists(zzd_lib):
#        os.system(f"mkdir -p {zzd_lib}")
#
#    if not os.path.exists(f"{zzd_lib}/ara_node2vec_feature.txt"):
#        os.system(f"wget https://github.com/miderxi/zzd_lib/raw/main/zzd/lib/ara_node2vec_feature.tar.gz\
#            -O {zzd_lib}/ara_node2vec_feature.tar.gz")
#        os.system(f"tar -xvf {zzd_lib}/ara_node2vec_feature.tar.gz -C {zzd_lib}")
#
#ara_node2vec_init()
class ara_node2vec:
    def __init__(self,data_file=None):
        self.node2vec = {}
        self.data_file = data_file
        self.shape = None
    
    def __getitem__(self,index):
        if not self.node2vec:
            #print(self.data_file[-4:])
            if self.data_file[-4:] == ".pkl":
                self.node2vec = np.load(self.data_file,allow_pickle=True)
                temp = self.node2vec.popitem()
                self.node2vec.update({temp[0]:temp[1]})
                self.shape = temp[1].shape
            else:
                self.node2vec = {line[0]:np.array(line[1:],float) 
                    for line in np.genfromtxt(self.data_file,str,skip_header=1)}     
                temp = self.node2vec.popitem()
                self.node2vec.update({temp[0]:temp[1]})
                self.shape = temp[1].shape

        if index in self.node2vec.keys():
            v =  self.node2vec[index]
        else:
            v = np.zeros(self.shape)
        return v



