import talib
import numpy as np

import hyperparameters as hp


def lag(df, target_list, number_lag):

    for target in target_list:
        for var in range(1,number_lag+1):
            df['LAG_'+str(var)+'_'+target] = df[target].shift(-var,axis = 0)
        
    return df

def sma(df, target_list):

    for target in target_list:

        df['SMA_SHORT_'+target] = talib.SMA(df[target], 30)
        df['SMA_LONG_'+target] = talib.SMA(df[target], 60)        
        df['CROSS_SMA_'+target] = np.where(df['SMA_LONG_'+target]>=df['SMA_LONG_'+target], 1 ,0)
        
    return df
  
def ma(df, target_list):

    for target in target_list:

        df['MA_SHORT_'+target] = talib.MA(df[target], 20)
        df['MA_LONG_'+target] = talib.MA(df[target], 100)        
        df['CROSS_MA_'+target] = np.where(df['MA_LONG_'+target]>=df['MA_LONG_'+target], 1 ,0)
        
    return df

def wma(df, target_list):

    for target in target_list:

        df['WMA_SHORT_'+target] = talib.WMA(df[target], 20)
        df['WMA_LONG_'+target] = talib.WMA(df[target], 50)        
        df['CROSS_WMA_'+target] = np.where(df['WMA_LONG_'+target]>=df['WMA_LONG_'+target], 1 ,0)
        
    return df


def stoch_rsi(df, target_list):

    for target in target_list:
        fastk, fastd = talib.STOCHRSI(df[target], timeperiod=14, fastk_period=5, fastd_period=3, fastd_matype=0) 

        for value in fastd:
            df['S_RSI_FASTD_'+target] = value
            
        for value in fastk:
            df['S_RSI_FASTK_'+target] = value

    return df
     

def rsi(df, target_list):

    for target in target_list:
        value = talib.RSI(df[target], hp.timePeriodRSI)
        value = np.nan_to_num(value)
        
        rsiValueCorrect, pastVar = [], 50
        for val in value: 
            if(val == 0):  rsiValueCorrect.append(float(pastVar))
            else:
                rsiValueCorrect.append(float(val))
                pastVar = val
            
        value = np.asarray(rsiValueCorrect)
        df['RSI_'+target] = value
        
        trend = talib.LINEARREG_SLOPE(value, hp.timePeriodRSI)
        df['RSI_TREND_'+target] = trend
        
        df['RSI_TREND_UP_'+target] = np.where(df['RSI_TREND_'+target]>=0, 1 ,0)
        df['RSI_OB_'+target] = np.where(df['RSI_'+target]>=70, 1 ,0)
        df['RSI_OS_'+target] = np.where(df['RSI_'+target]<=30, 1 ,0)
        
            
    return df

def trend(df, target_list):
    for target in target_list:
        trend = talib.LINEARREG_ANGLE(df[target], timeperiod=10)
    
        df['TREND_'+target] = trend
    
    
    return df


