from sklearn import preprocessing 


def scalingMean(data):
    scaler = preprocessing.StandardScaler().fit(data)
    data[data.columns] = scaler.transform(data[data.columns])
    return data , scaler
    
  
def scaling_train_test(train_original,test_original):
    train,test = train_original.copy(),test_original.copy()
    train, scaler = scalingMean(train)
    test[test.columns] = scaler.transform(test[test.columns])
    return train, test, scaler


