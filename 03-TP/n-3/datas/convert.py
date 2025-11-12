import numpy as np
import pandas as pd

seq = ' '.join(['C{0} D{0}'.format(i) for i in range(1, 6)])
seq = seq.split()

print(seq)

N = 100
datas_out = pd.DataFrame()
for j in range(len(seq)) :
    datas = pd.read_excel("{}.ods".format(seq[j]))
    datas = datas[["Time (s)","WE(1).Potential (V)"]]
    
    t, U = datas.to_numpy().T
    
    tval = np.linspace(t.min(), t.max(), num = N, endpoint = True)
    
    Uval = np.interp(tval, t, U)
    
    datas_out['t_' + seq[j]] = tval
    datas_out['U_' + seq[j]] = Uval

datas_out.to_excel("DataOut.ods")
print(datas_out)
