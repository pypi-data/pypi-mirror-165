import numpy as np
import os

class esm_mean:
    def __init__(self,esm_mean_file=f"{os.environ['HOME']}/.local/zzd/lib/esm_mean.pkl"):
        self.esm_mean = None
        self.esm_mean_file = esm_mean_file
    
    def __getitem__(self,index):
        if self.esm_mean == None:
            self.esm_mean = np.load(self.esm_mean_file, allow_pickle=True)
        return self.esm_mean[index]

if __name__ == "__main__":
    test = esm_mean()['AT3G17090']
    print(test,test.shape)
