import math
from sklearn.metrics import mean_squared_error

def get_RMSE(true, pred):
    
    score = math.sqrt(mean_squared_error(true,pred))
    
    return score

