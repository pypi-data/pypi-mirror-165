import numpy as np

def dpc(seq):
    aminos = "AGVCDEFILPHNQWKRMSTY"
    dpc_dict = {i+j:0 for i in aminos for j in aminos}
    #seq = seq.replace("X","")
    seq = "".join([i for i in seq if i in aminos])

    for i in range(len(seq)-1):
        dpc_dict[seq[i:i+2]] += 1
    values = np.array(list(dpc_dict.values())) / (len(seq)-1)
    return values


