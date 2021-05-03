from program import rgbavg
import numpy as np
import pickle
import os
from sklearn.tree import DecisionTreeRegressor

def predict(filepath):
    boolarray=[True, True, True]
    print(filepath)
    rmean, gmean, bmean = rgbavg(filepath, 16)
    features = np.append(rmean,(gmean,bmean))
    print(features)
    features = np.array([features])
    print(np.size(features))
    modelpath = os.path.join(os.path.expanduser('~'), 'PycharmProjects', 'image_splicing_ml', 'models', 'tanvi_model.sav')

    regressor = pickle.load(open(modelpath, 'rb'))
    result = regressor.predict(features)
    #print(int(result))

    if int(result) == 0 :
        boolarray = [True]
    else:
        boolarray = [False]

    modelpath = os.path.join(os.path.expanduser('~'), 'PycharmProjects', 'image_splicing_ml', 'models', 'shreepad_model.sav')

    regressor = pickle.load(open(modelpath, 'rb'))
    result = regressor.predict(features)
    #print(result)

    if int(result) == 0 :
        boolarray.append(True)
    else:
        boolarray.append(False)

    rmean, gmean, bmean = rgbavg(filepath, 18)
    features = np.append(rmean, (gmean, bmean))
    #print(features)
    features = np.array([features])
    #print(np.size(features))

    modelpath = os.path.join(os.path.expanduser('~'), 'PycharmProjects', 'image_splicing_ml', 'models', 'shiv_i_model.sav')

    regressor = pickle.load(open(modelpath, 'rb'))
    result = regressor.predict(features)
    #print(result)
    if int(result) == 0 :
        boolarray.append(True)
    else:
        boolarray.append(False)

    print(boolarray)
    return boolarray


