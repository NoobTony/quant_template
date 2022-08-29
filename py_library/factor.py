import os
import pickle
from functools import partial
import multiprocessing
import datetime

import numpy as np
import pandas as pd
from scipy.optimize import minimize,LinearConstraint,NonlinearConstraint,Bounds
from joblib import Parallel, delayed


def savepath_decorator(fun):
    """
    this decorator is used to save factors calculated by factor function,
    and the default file name is 'factor name+ paras'
    """
    def wrapper(*args, **kwargs):
        fun_name=fun.__name__
        filename=fun_name.replace('get_','')+'_'+'_'.join([*args,*list(kwargs.values())])+'.pkl'
        dir_name='data/'+fun_name.replace('get_','')+'/'
        try :
            os.mkdir(dir_name)
            os.mkdir('data')
        except:
            pass
        savepath=dir_name+filename
        if os.path.exists(savepath)and os.path.getsize(savepath):
            return pickle.load(open(savepath,'rb')) 
        else:
            result=fun(*args, **kwargs)
            pickle.dump(result,open(savepath,'wb'))
            return result  
    return wrapper

def ACD(df,para=20):
    """    广发证券_20210730_多因子Alpha系列报告之（四十二）：海量技术指标掘金Alpha因子
    计算市场的净收集力量，了解市场强弱

    ACD指标将市场分为两股收集（买入）及派发（估出）的力量。若当天收盘价
    高于昨天收盘价，则收集力量等于当天收盘价与真实低位之差。真实低位是当天低
    位与昨天收盘价两者中的最低者。若当天收盘价低于昨天收盘价，则派发力量等于
    当天当天收盘价与真实高位之差。真实高位是当天高位与昨天收盘价两者较高者；
    若将收集力量（正数）及派发力量（负数）相加，便可得到市场的净收集力量，从
    而了解市场的强弱。"""
    if para<0:
            return
    df['preclose']=df['close'].shift(1)
    df['min_low_preclose']=df[['low','preclose']].min(axis=1)
    df['max_high_preclose']=df[['high','preclose']].max(axis=1)
    #exactly ternary operator
    df['dif']=(df['close']-df['min_low_preclose'])*(df['close']>df['preclose'])+\
        (df['close']-df['max_high_preclose'])*(df['close']<=df['preclose'])
    df['factor_value']=df['dif'].rolling(para).sum()
    df['time']=df.index
    df=df.reset_index(drop=True)
    return df[['code','time','factor_value']]


def UOS_hf(df,para1=5,para2=10,para3=20):
    """    广发证券_20210730_多因子Alpha系列报告之（四十二）：海量技术指标掘金Alpha因子
        终极波动（UOS）指标，由拉里·威廉姆斯（Larry Williams）所创。他认为
        现行使用的各种振荡指标，对于周期参数的选择相当敏感。不同市况、不同参数设
        定的振荡指标，产生的结果截然不同。因此，选择最佳的参数组合，成为使用振荡
        指标之前最重要的一道手续。"""
    df['PreClose']=df['close'].shift(1)
    df['TH']=(df['high']>df['PreClose'])*df['high']+(df['high']<=df['PreClose'])*df['PreClose']
    df['TL']=(df['low']<df['PreClose'])*df['low']+(df['low']<df['PreClose'])*df['PreClose']
    df['DiffTHTL']=df['TH']-df['TL']
    df['temp']=(df['close']-df['TL'].rolling(para1).sum())
    df['ACC1']=df['temp']/df['DiffTHTL'].rolling(para1).sum()
    df['ACC2']=df['temp']/df['DiffTHTL'].rolling(para2).sum()
    df['ACC3']=df['temp']/df['DiffTHTL'].rolling(para3).sum()
    df['factor_value']=(df['ACC1']*para2*para3+df['ACC2']*para1*para3+df['ACC3']*para1*para2)*100/(para1*para2+para1*para3+para2*para3)
    df['time']=df.index
    df=df.reset_index(drop=True)
    return df[['inst','time','factor_value']]