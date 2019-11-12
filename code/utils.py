import gc
import numpy as np
import pandas as pd
from numpy import array

def data_formatting(bullet_sales , handgun_sales):
    
    bullet_sales['Maker']= bullet_sales['Maker'].replace({'Henry Lever': 'Henry_Lever'})
    handgun_sales['Maker'] = handgun_sales['Maker'].replace({'Henry Lever': 'Henry_Lever'})
    
    bullet_sales= bullet_sales.rename(columns={"Quantity": "Quantity_bullets", "Bullets": "Bullets_type"})
    handgun_sales= handgun_sales.rename(columns={"Quantity": "Quantity_guns"})
    
    conditions = [
        (handgun_sales['Maker'] == 'Remington') & (handgun_sales['Model'] == 'model_1'),
        (handgun_sales['Maker'] == 'Remington') & (handgun_sales['Model'] == 'model_2'),
        (handgun_sales['Maker'] == 'Remington') & (handgun_sales['Model'] == 'model_3'),
        (handgun_sales['Maker'] == 'Henry_Lever') & (handgun_sales['Model'] == 'model_1'),
        (handgun_sales['Maker'] == 'Henry_Lever') & (handgun_sales['Model'] == 'model_2'),
        (handgun_sales['Maker'] == 'Henry_Lever') & (handgun_sales['Model'] == 'model_3')]
    
    choices = ['Gun_w_bullets_A', 'Gun_w_bullets_B', 'Gun_w_bullets_C','Gun_w_bullets_A','Gun_w_bullets_A','Gun_w_bullets_B']
    
    handgun_sales['Bullets_type'] = np.select(conditions, choices, default='black')
    
    return bullet_sales , handgun_sales



def groupBy_Date(df, values, rs_and_tf): 
    
    temp = df.groupby(['Date','Bullets_type']).sum().reset_index()
    temp = temp.pivot(index='Date', columns='Bullets_type', values=values)
    inputs = temp
    del temp
    
    if(rs_and_tf == True):
        temp = df.groupby(['Date','Maker']).sum().reset_index()
        temp = temp.pivot(index='Date', columns='Maker', values=values)
        inputs = inputs.join(temp)
        del temp

        df['Maker_Model'] = df['Maker'] +'_'+ df['Model']
        temp = df.groupby(['Date','Maker_Model']).sum().reset_index()

        temp = df.pivot(index='Date', columns='Maker_Model', values=values)    
        inputs = inputs.join(temp) 
        del temp
        
    gc.collect
    
    return inputs

def join_all_set(input_handguns,input_bullet_sales_TF,input_bullet_sales_RS):
    
    input_handguns.columns = ['HG_'+c for c in input_handguns.columns]
    input_bullet_sales_TF.columns = ['BTF_'+c for c in input_bullet_sales_TF.columns]
    input_bullet_sales_RS.columns = ['BRS_'+c for c in input_bullet_sales_RS.columns]
    
    full_set = input_handguns.join(input_bullet_sales_TF).join(input_bullet_sales_RS)
    
    return full_set

def add_date(df):
    
    temp = pd.DataFrame(df.index.str.split('-').tolist(),columns = ['year','month','day'])
    temp.index = df.index
    temp['WEEKDAY'] = pd.to_datetime(temp.index).dayofweek
    temp['WEEKEND'] = np.where(temp['WEEKDAY']>=5, 1 ,0)
    temp = temp.astype('int32')
    df = df.join(temp)
    
    del temp
    gc.collect
    
    return df
    
def get_index_1817(index):
        temp = index.tolist()
        temp.insert(0,'1816-01-01')
        temp.remove('1816-02-29')
        temp = [c.replace("1816-", "1817-") for c in temp]
        return temp

def agg_handguns(pred,weight_A,weight_B):
    
    tempC = pred[['RS_bullets_C']].copy()
    tempC.columns = ['Remington_model_3']
    
    tempA = pred[['RS_bullets_A']].copy()
    tempA.columns = ['Henry_Lever_model_1']
    tempA['Henry_Lever_model_2'] = tempA['Henry_Lever_model_1']
    tempA['Remington_model_1'] = tempA['Henry_Lever_model_1']
    tempA = tempA.mul(weight_A)
    
    
    tempB = pred[['RS_bullets_B']].copy()
    tempB.columns = ['Henry_Lever_model_3']
    tempB['Remington_model_2'] = tempB['Henry_Lever_model_3']
    tempB = tempB.mul(weight_B)
    
    pred_temp = tempA.join(tempB)
    pred_temp = pred_temp.join(tempC)
    
    del tempA
    del tempB
    del tempC

    return pred_temp





    