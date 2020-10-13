import os
import numpy as np
import pandas as pd
from sklearn.naive_bayes import GaussianNB
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import csv

def get_train_values():
    os.chdir('data')
    heart = pd.read_csv('loan_train.csv', sep=';', header=0)
    heart.head()
    return heart
    
def get_test_values(values):
    heart = pd.read_csv('loan_test.csv', sep=';', header=0)
    heart.head()
    train_y = values.iloc[:,6]
    train_x = values.iloc[:,:6]
    test_y = heart.iloc[:,6]
    test_x = heart.iloc[:,:6]
    loan_id = list(heart.iloc[:,0])
    return (train_x, train_y, test_x, test_y, loan_id)

def train_split_random(values):
    values_y = values.iloc[:,6]
    values_x = values.iloc[:,:6]
    train_y, test_y = train_test_split(values_y, test_size=0.25, random_state=0, shuffle=True)
    train_x, test_x = train_test_split(values_x, test_size=0.25, random_state=0, shuffle=True)
    return(train_x, train_y, test_x, test_y)

def train_predict_96(values):
    values_train=values[(values['date'] > 930000) & (values['date'] < 960000)]
    values_test=values[values['date'] > 960000]
    train_y = values_train.iloc[:,6]
    train_x = values_train.iloc[:,:6]
    test_y = values_test.iloc[:,6]
    test_x = values_test.iloc[:,:6]
    return(train_x, train_y, test_x, test_y)

def apply_gaussian(train_x, train_y, test_x):
    gnb = GaussianNB()
    model = gnb.fit(train_x, train_y)
    return gnb.predict(test_x)

def create_file(loan_id,results):
    os.chdir('..')
    f=open('submission.csv','w')
    f.write("Id,Predicted")
    for i,j in zip(loan_id,results):
        f.write("\n"+str(i)+","+str(j))
    f.close()

# _____________________________________________________________________________________________________________

values = get_train_values()

# train_x, train_y, test_x, test_y = train_split_random(values)
train_x, train_y, test_x, test_y = train_predict_96(values)
# train_x, train_y, test_x, test_y, loan_id = get_test_values(values)

preds = list(apply_gaussian(train_x, train_y, test_x))

print(accuracy_score(test_y, preds))
# create_file(loan_id,preds)