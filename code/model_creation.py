import hyperparameters as hp
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout
import numpy as np
import lightgbm  as lgb

np.random.seed(hp.seed)

def LSTM_model(number_features):

    model = Sequential()
    model.add(LSTM(hp.n0,activation='relu', input_shape=(1, number_features),return_sequences=True,kernel_initializer='glorot_uniform'))
    model.add(Dropout(hp.dropout))
    model.add(LSTM(hp.n1,activation='relu',return_sequences=True))
    model.add(Dropout(hp.dropout))
    model.add(LSTM(hp.n2,activation='relu',return_sequences=False))
    model.add(Dense(3,activation='linear'))
    model.compile(loss='mean_squared_error', optimizer='adadelta')
    
    return model


def LGBM_model(X_train,X_valid,y_train,y_valid):

    trn_data = lgb.Dataset(X_train, label=y_train)
    val_data = lgb.Dataset(X_valid, label=y_valid)
    
    evals_result = {}
    
    if(len(X_valid) != 0 ):     valid_sets = [trn_data, val_data]
    else:        valid_sets = [trn_data]
    
    if(len(X_train) != 0):
        model_LGBM = lgb.train(hp.params_LGBMRegressor,   trn_data,100,valid_sets = valid_sets,early_stopping_rounds=20,
                        verbose_eval = False,evals_result=evals_result)
    else:
        model_LGBM = 0
    
    if(len(X_train) != 0)and(len(X_valid) != 0 ):      train_pred = model_LGBM.predict(X_train)      
    if(len(X_train) != 0)and(len(X_valid) != 0 ):      test_pred = model_LGBM.predict(X_valid)

    train_pred[train_pred < 0] = 0
    test_pred[test_pred < 0] = 0
            
    return train_pred, test_pred , model_LGBM