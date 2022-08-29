import numpy as np
import pandas as pd
import cpp_part.numpy_demo as numpy_demo
import py_library.factor as pf

#mat1 = numpy_demo.save_2d_numpy_array(np.zeros(shape=[10,10], dtype=np.float32), './data.dat')
#print(mat1)
data=pd.read_csv('cbond_data.csv')

factor=data.groupby('code').apply(pf.ACD)

print(data)





