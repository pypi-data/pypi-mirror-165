# -*- coding: utf-8 -*-
"""
Created on Thu Aug 25 15:07:32 2022

@author: User
"""
import json
from sklearn.model_selection import train_test_split
import os
import lightgbm as lgb 
import shap
import data_science_helper.helper_general as hg
#hg.set_base_path()
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")
import lightgbm as lgb 

import data_science_helper.helper_classification_model as hcm
import data_science_helper.model.general as mg
import data_science_helper.helper_dataframe as hd
import data_science_helper.helper_output as ho
import pandas as pd
import numpy as np
from datetime import datetime
import random
from optuna.trial import Trial
from data_science_helper.model import optuna as ot

from lightgbm import early_stopping
from lightgbm import log_evaluation

from sklearn.datasets import load_breast_cancer
import pandas as pd
from sklearn.model_selection import train_test_split, KFold
from sklearn.metrics import roc_auc_score
import lightgbm as lgb
import numpy as np

from sklearn.metrics import f1_score , precision_score, recall_score
from sklearn.model_selection import cross_val_score, KFold, StratifiedKFold, train_test_split, StratifiedShuffleSplit


random_state = 42
data = load_breast_cancer()
X = pd.DataFrame(data.data, columns=data.feature_names)
y = pd.Series(data.target)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=random_state)

#y_train.reset_index(inplace=True,drop=True)   

num_rounds=9999999

#folds = KFold(5, random_state=42,shuffle=True)
n_splits = 5
folds = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=random_state)

result, best_params, best_value, trials_dataframe  = get_num_leaves_lgbm(X_train,y_train,folds=folds,random_state=random_state)


trial_number_nob = ot.get_best_trial_number_nob(result)

kpis_by_trial_number   = ot.get_kpis_by_trial_number(result,trial_number_nob)  
params_by_trial_number = ot.get_params_by_trial_number(trials_dataframe,trial_number_nob)


def get_num_leaves_lgbm(X,y,n_trials=200,fast_check=False,metric="f1",folds = None, n_jobs=3,early_stop=200,log=0,random_state=42):
    num_rounds = 9999999
    def get_params_optuna(trial: Trial):
        
        train_params = {    
            "min_data_in_leaf": trial.suggest_int("min_data_in_leaf", 10, 50, step=5),
            "num_leaves": trial.suggest_int("num_leaves", 31, 2000, step=10),          
        }

        dataset_params = {"max_bin": trial.suggest_int("max_bin", 10, 300, step=10)}
        #dataset_params = None

        return train_params, dataset_params
    
    args_opt = {"X_train":X,"y_train":y, "fn_params":get_params_optuna,"metric":metric,
                "neg_bagging_fraction":False, "folds":folds, "random_state":random_state,
                "n_trials":n_trials, "fast_check": fast_check, "n_jobs": n_jobs, 
                "num_rounds":num_rounds,"early_stop":early_stop,"log":log
            } 

    #result, best_params, best_value, trials_dataframe = ot.lgb_model_optuna(**args_opt)
    return ot.lgb_model_optuna(**args_opt)
    
    
#np.argmax(np.array([0.5,0.5]), axis=0)    
    
for train_idx, val_idx in folds.split(X_train,y_train):
    
    data_trd = lgb.Dataset(X_train.iloc[train_idx], 
                           y_train.iloc[train_idx],
                          
                           #params=params_dataset
                          )    
    
    for train_idx, valid_idx in folds.split(X_train, y_train):
        train_data = X_train.iloc[train_idx,:], y_train[train_idx]
        
        valid_data = X_train.iloc[valid_idx,:], y_train[valid_idx]


def lgb_f1_score(y_hat, data):
    y_true = data.get_label()
    y_hat = np.round(y_hat) # scikits f1 doesn't like probabilities
    return 'f1', f1_score(y_true, y_hat), True


def get_feval(score):     
    if(score=="f1"):
        feval=lgb_f1_score
        
    return feval