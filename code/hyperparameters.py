

timePeriodRSI = 13
dropout = 0.4
seed = 45
epochs = 30
batch_size = 128
verbose = 0
n0 = 100
n1 = 100
n2 = 100

n_input = 366
n_output = 366
n_units = 128

params_LGBMRegressor = { 
            "bagging_freq" : 1, # change to 1 
            "boosting_type" : 'gbdt', 
            "min_data_in_leaf" : 200, #15
            "num_leaves" : 50, #200
            "learning_rate" : 0.05, 
            "min_sum_hessian_in_leaf" : 5.0, 
            "reg_alpha" : 1.3, #1.3
            "reg_lambda" : 1.6, #1.6
            "max_depth" : 5, #9
            "feature_fraction" : 0.7, #change to 0.5
            "seed" : seed,#48
            "metrics" : 'rmse',
            'num_iterations': epochs,
            }         