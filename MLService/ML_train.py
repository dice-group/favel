import pandas as pd
import os
from sklearn import preprocessing
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.linear_model import *
from sklearn.ensemble import *
from sklearn.tree import *
# from sklearn.metrics import classification_report
import pandas as pd
from sklearn.model_selection import KFold
import numpy as np
# from sklearn.model_selection import cross_val_score
# from sklearn.model_selection import StratifiedKFold
from sklearn.naive_bayes import *
from sklearn.neighbors import *
import pickle, sklearn
from sklearn.neural_network import *
from pathlib import Path
from sklearn.metrics import *
# from sklearn.svm import *
from sklearn.pipeline import *
from sklearn.preprocessing import *
from joblib import dump, load
import pickle
import sys
import csv,sys
from functools import reduce
import operator
import sys
from sklearn.model_selection import *
from sklearn.svm import *

from sklearn import *
import warnings
if not sys.warnoptions:
    warnings.simplefilter("ignore")

def trn_data_triples(df):
    df.fillna(0, inplace=True)
    
    
    X=df.drop(['true_value','subject','object','predicate'
              ], axis=1)
    y=df.true_value

    X.fillna(0, inplace=True)
    y.fillna(0, inplace=True)
    
    X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.33, random_state=42)

    trn_data=pd.DataFrame({
        'X_train':[X_train],
        'X_test':[X_test],
        'y_train':[y_train],
        'y_test':[y_test],
    })
    return trn_data


def trn_data_wo_triples(df):
    df.fillna(0, inplace=True)
    
    X=df.drop(['true_value',
               'subject',
               'predicate',
               'object'
              ], axis=1)
    y=df.true_value


    X.fillna(0, inplace=True)
    y.fillna(0, inplace=True)
    
    X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.33, random_state=42)

    trn_data=pd.DataFrame({
        'X_train':[X_train],
        'X_test':[X_test],
        'y_train':[y_train],
        'y_test':[y_test],
    })
    return trn_data



def train_model(X_train, X_test, y_train, y_test, model, result_df):
    model=model.fit(X_train, y_train)
    mdl_name=model.__class__.__name__ if model.__class__.__name__!='Pipeline' else model[1].__class__.__name__
    tmpdf=pd.DataFrame({'method_name': [mdl_name], 
                        'method': [model], 
                        'accuracy':[model.score(X_test, y_test)], 
                        'auc_roc':[roc_auc_score(y_test, model.predict_proba(X_test)[:, 1])]})
    result_df=pd.concat([result_df, tmpdf])
    return result_df



def main(df, models_list, output_path):
    result_df=pd.DataFrame()    
    
    for model in models_list:
        trn_data = trn_data_triples(df)
        result_df=train_model(trn_data.X_train.item(), 
                              trn_data.X_test.item(), 
                              trn_data.y_train.item(), 
                              trn_data.y_test.item(), 
                              model, 
                              result_df)
    
    print(result_df)   
    print(result_df.auc_roc.idxmax())
    result_df=result_df.reset_index(drop=True) 
    best_method=result_df.loc[result_df.auc_roc.idxmax()]
    
    print(f'''
        Best Model: {best_method.method_name}
        Auc_Roc:    {best_method.auc_roc}
        Accuracy:   {best_method.accuracy}

    '''
    )
    
    Path(output_path).mkdir(parents=True, exist_ok=True)    
    
    with open(f'{output_path}/classifier.pkl','wb') as fp: pickle.dump(best_method.method,fp)

    return result_df.reset_index(drop=True)


if __name__=="__main__":
    
    output_path = "models/"
    
    # model_df = pd.read_csv(sys.argv[2])
    # models_list=model_df['model_lists'].to_list()
    
    models_list=[
    AdaBoostClassifier(),
    GradientBoostingClassifier(n_estimators=100, learning_rate=1.0, max_depth=1, random_state=0),
    RandomForestClassifier(n_estimators=50,oob_score = True),
    StackingClassifier(estimators=[('dt',DecisionTreeClassifier()), ('rf',RandomForestClassifier(random_state=0))], final_estimator=GradientBoostingClassifier(random_state=0)),
    DecisionTreeClassifier(), BaggingClassifier(DecisionTreeClassifier(), max_samples=0.5, max_features = 1.0, n_estimators =50), 
    make_pipeline(StandardScaler(), SVC(gamma='auto', probability=True))
    ]
    df = pd.read_csv(sys.argv[1])

    main(df, models_list, output_path)        