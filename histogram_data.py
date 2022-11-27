import numpy as np
import pandas as pd
# from ant_trace_simulation import *

def data_frame(vector):
    df = pd.DataFrame(vector,columns=['population'])
    # bin_size = 1.0/nbin
    # by default only 5 bins
    df['range']=0

    for i in range(len(df.index)):
        if df.loc[i,'population']<0.2:
            df.loc[i,'range']=0
        elif df.loc[i,'population']<0.4:
            df.loc[i,'range']=1
        elif df.loc[i,'population']<0.6:
            df.loc[i,'range']=2
        elif df.loc[i,'population']<0.8:
            df.loc[i,'range']=3
        else:
            df.loc[i,'range']=4 
    return df
    

def data_preparation(vector):
    df = pd.DataFrame(vector,columns=['population'])
    # bin_size = 1.0/nbin
    # by default only 5 bins
    df['range']=0

    for i in range(len(df.index)):
        if df.loc[i,'population']<0.2:
            df.loc[i,'range']=0
        elif df.loc[i,'population']<0.4:
            df.loc[i,'range']=1
        elif df.loc[i,'population']<0.6:
            df.loc[i,'range']=2
        elif df.loc[i,'population']<0.8:
            df.loc[i,'range']=3
        else:
            df.loc[i,'range']=4 

    s_count_1 = pd.DataFrame(df['range'].value_counts())
    s_count_1['index']=s_count_1.index
    s_count_2=pd.DataFrame(np.zeros(5),columns=['range'])
    s_count_2['index']=s_count_2.index
    s_count = pd.merge(s_count_1,s_count_2,on='index',how='outer')
    s_count = s_count.fillna(0)
    s_count['count'] = s_count[['range_x','range_y']].max(axis=1)
    s_count = s_count.rename(columns={'index':'range'})
    s_count=s_count.drop(['range_x','range_y'],axis=1)
    s_count['value']=['[0,0.2)','[0.2,0.4)','[0.4,0.6)','[0.6,0.8)','[0.8,1]']

    return s_count

