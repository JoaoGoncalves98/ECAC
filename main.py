# -*- coding: utf-8 -*-

import os
import numpy as np
import pandas as pd
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from sklearn.feature_selection import RFECV
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import roc_auc_score
from imblearn.over_sampling import SMOTE
from collections import Counter
import csv

def get_train_values():
    os.chdir('data')
    heart = pd.read_csv('gerado_train.csv', sep=',', header=0, low_memory=False)
    heart.head()
    return heart
    
def get_test_values(values):
    heart = pd.read_csv('gerado_test.csv', sep=',', header=0, low_memory=False)
    heart.head()
    train_y = values.iloc[:,15]
    train_x = values.iloc[:,:15]
    test_y = heart.iloc[:,15]
    test_x = heart.iloc[:,:15]
    loan_id = list(heart.iloc[:,0])
    return (train_x, train_y, test_x, test_y, loan_id)

def train_split_random(values):
    values_y = values.iloc[:,15]
    values_x = values.iloc[:,:15]
    train_y, test_y = train_test_split(values_y, test_size=0.25, random_state=0, shuffle=True)
    train_x, test_x = train_test_split(values_x, test_size=0.25, random_state=0, shuffle=True)
    return(train_x, train_y, test_x, test_y)

def train_split_year(values):
    values_train=values[(values['date'] > 930000) & (values['date'] < 960000)]
    values_test=values[values['date'] > 960000]
    train_y = values_train.iloc[:,15]
    train_x = values_train.iloc[:,:15]
    test_y = values_test.iloc[:,15]
    test_x = values_test.iloc[:,:15]
    return(train_x, train_y, test_x, test_y)

def apply_gaussian(train_x, train_y, test_x): # Naive Bayes
    gnb = GaussianNB()
    model = gnb.fit(train_x, train_y)
    return gnb.predict(test_x)

def apply_svc(train_x, train_y, test_x): # Support Vector Machines
    svc = SVC(kernel='rbf', gamma='auto')
    model = svc.fit(train_x, train_y)
    return svc.predict(test_x)

def apply_logisticRegression(train_x, train_y, test_x): # Logistic regression
    lrc = LogisticRegression(random_state=0, multi_class='auto', solver='lbfgs', max_iter=1000)
    model = lrc.fit(train_x, train_y)
    return lrc.predict(test_x)

def apply_kNeighborsClassifier(train_x, train_y, test_x): # k-nearest neighbors
    knc = KNeighborsClassifier(n_neighbors=3)
    model = knc.fit(train_x, train_y)
    return knc.predict(test_x)

def apply_randomForestClassifier(train_x, train_y, test_x): # k-nearest neighbors
    smt = SMOTE()
    train_x_SMOTE, train_y_SMOTE = smt.fit_resample(train_x, train_y)
    clf=RandomForestClassifier(n_estimators=20)
    selector = RFECV(clf, scoring='roc_auc')
    selector.fit(train_x_SMOTE, train_y_SMOTE)
    return selector.predict(test_x)

def create_file(loan_id,results):
    os.chdir('..')
    f=open('submission.csv','w')
    f.write("Id,Predicted")
    for i,j in zip(loan_id,results):
        f.write("\n"+str(i)+","+str(j))
    f.close()

def test_accuracy(values):
    train_x, train_y, test_x, test_y = train_split_year(values)
    preds = list(apply_randomForestClassifier(train_x, train_y, test_x))
    print("\nauc score: " + str(roc_auc_score(test_y, preds))+ "\n")


def submission(values):
    train_x, train_y, test_x, test_y, loan_id = get_test_values(values)
    preds = list(apply_randomForestClassifier(train_x, train_y, test_x))
    create_file(loan_id,preds)

# falta fazer feature selection + smote + colunas relevantes
# _____________________________________________________________________________________________________________

values = get_train_values()

test_accuracy(values) # Tests accuracy by using train file for train+test
submission(values) # Creates submission file to be submited