
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeRegressor
import pickle
from sklearn import metrics

font = {'size': 7}

plt.rc('font', **font)

def create_model(filepath):
    print(filepath)
    df=pd.read_csv(filepath)
    filename = os.path.basename(filepath)
    filename = os.path.splitext(filename)[0]


    print(df.head())
    df.Class=pd.Categorical(df.Class)
    df['class_code'] = df.Class.cat.codes
    print(df.head())
    features = []
    for x in range(1,19):
        features.append("R"+str(x))
    for x in range(1,19):
        features.append("G"+str(x))
    for x in range(1,19):
        features.append("B"+str(x))
    print(features)

    # Plot correlation graph

    plt.matshow(df.corr())
    plt.xticks(np.arange(58), df.columns, rotation = 90)
    plt.yticks(np.arange(58), df.columns, rotation=0)
    plt.colorbar()
    plt.savefig(filename+'_correlation', dpi=400)

    X = np.array(df[features])
    y = np.array(df['class_code'])
    X_train, X_test, y_train, y_test = train_test_split(X, y,test_size= 0.2 ,random_state= 42 , shuffle=True)

    regressor = DecisionTreeRegressor(random_state=0)
    regressor.fit(X_train, y_train)

    filename = filename+"_model.sav"
    pickle.dump(regressor, open("models\\",filename, 'wb'))

    # open model and test giving results

    loaded_model = pickle.load(open("models\\",filename, 'rb'))
    y_pred = loaded_model.predict(X_test)
    print(filename, "Results")
    print(metrics.classification_report(y_test, y_pred))
    print("f1 score:", metrics.f1_score(y_test, y_pred))
    result = loaded_model.score(X_test, y_test)
    print("Score:", result)




if __name__ == '__main__':
    create_model("csv/shiv_i.csv")
