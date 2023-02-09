import pandas as pd
import numpy as np
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
# from joblib import dump, load
import pickle






def get_features(df):
    # Get the features fro the dataframe
    # Input:
        # df: Dataframe
    # Output: 
        # X - Features
        # y - users
    
    # According the to Figure 1. from the challenge file 
    # The Hold Time (HT) and Release-Press Time (RPT) are calculated by taking the difference between the consecutive keys (columns)
    htrpt = df.drop(columns=['user']).diff(axis=1, periods=1).drop(columns=['press-0'])
    # Even number of columns of the resulted dataframe is equal to HT
    ht = htrpt.loc[:, ::2].abs()
    # and odd number of columns are RPT
    rpt = htrpt.iloc[:, np.arange(htrpt.shape[1]) % 2 !=0].abs()
    
    # Difference between two keys (columns) resulted in Press-Press Time (PPT) and Release-Release Time (RRT)
    ppt_rrt = df.drop(columns=['user']).diff(axis=1, periods=2).drop(columns=['press-0','release-0'])

    # Even columns corresponds to ppt and odd to rrt
    ppt = ppt_rrt.loc[:, ::2].abs()
    rrt = ppt_rrt.iloc[:, np.arange(ppt_rrt.shape[1]) % 2 !=0].abs()
    

    # Mean and STD of the features

    df['HT_mean'] = ht.mean(axis=1)
    df['HT_std']= ht.std(axis=1)
    df['RPT_mean'] = rpt.mean(axis=1)
    df['RPT_std']= rpt.std(axis=1)
    df['PPT_mean'] = ppt.mean(axis=1)
    df['PPT_std']= ppt.std(axis=1)
    df['RRT_mean'] = rrt.mean(axis=1)
    df['RRT_std']= rrt.std(axis=1)


    # Features dataframe
    features = df[['HT_mean', 'HT_std', 'RPT_mean', 'RPT_std','PPT_mean', 'PPT_std','RRT_mean', 'RRT_std']]

    
    # X is the numpy arrays for the features data
    X = features.values
    # y is the corresponding labels for the features in X
    y = df['user'].values

    return X, y-1

df = pd.read_csv('Train_keystroke.csv')
X, y = get_features(df)

# RandomForestClassifier
rf_clf = RandomForestClassifier()
rf_clf.fit(X,y)


# SVM classifier
clf = svm.SVC()
clf.fit(X,y)


# XGBoost Classifier
xgb_clf = XGBClassifier()
xgb_clf.fit(X,y)


dump(clf, 'svm.joblib')
dump(rf_clf, 'rf_clf.joblib')
dump(xgb_clf, 'xgb_clf.joblib')


# print('saved')