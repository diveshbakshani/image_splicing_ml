from program import rgbavg
import numpy as np
import pickle
from sklearn.tree import DecisionTreeRegressor

def predict(filename):
    boolarray=[True, True, True]
    filepath = 'uploads\\'+filename
    print(filepath)
    rmean, gmean, bmean = rgbavg(filepath, 16)
    features = np.append(rmean,(gmean,bmean))
    print(features)
    features = np.array([features])
    print(np.size(features))

    regressor = pickle.load(open('models\\tanvi_model.sav', 'rb'))
    result = regressor.predict(features)
    print(int(result))

    if int(result) == 0 :
        boolarray = [True]
    else:
        boolarray = [False]

    regressor = pickle.load(open('models\\shreepad_model.sav', 'rb'))
    result = regressor.predict(features)
    print(result)

    if int(result) == 0 :
        boolarray.append(True)
    else:
        boolarray.append(False)

    rmean, gmean, bmean = rgbavg(filepath, 18)
    features = np.append(rmean, (gmean, bmean))
    print(features)
    features = np.array([features])
    print(np.size(features))

    regressor = pickle.load(open('models\\shiv_i_model.sav', 'rb'))
    result = regressor.predict(features)
    print(result)
    if int(result) == 0 :
        boolarray.append(True)
    else:
        boolarray.append(False)

    print(boolarray)
    return boolarray


