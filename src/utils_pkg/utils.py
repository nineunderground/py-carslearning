# Different util methods
import numpy as np

def get_serie_ids(x):
    '''Function returns a pandas series consisting of ids, 
       corresponding to objects in input pandas series x
       Example: 
       get_series_ids(pd.Series(['a','a','b','b','c'])) 
       returns Series([0,0,1,1,2], dtype=int)'''

    values = np.unique(x)
    values2nums = dict(zip(values,range(len(values))))
    return x.replace(values2nums)