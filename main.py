import os
import numpy as np
import pandas as pd
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
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

def apply_KNeighborsClassifier(train_x, train_y, test_x): # k-nearest neighbors
    knc = KNeighborsClassifier(n_neighbors=3)
    model = knc.fit(train_x, train_y)
    return knc.predict(test_x)

def create_file(loan_id,results):
    os.chdir('..')
    f=open('submission.csv','w')
    f.write("Id,Predicted")
    for i,j in zip(loan_id,results):
        f.write("\n"+str(i)+","+str(j))
    f.close()

def test_accuracy(values):
    train_x, train_y, test_x, test_y = train_split_random(values)
    preds = list(apply_svc(train_x, train_y, test_x))
    print("\nsplit random accuracy: " + str(accuracy_score(test_y, preds)))

    train_x, train_y, test_x, test_y = train_predict_96(values)
    preds = list(apply_svc(train_x, train_y, test_x))
    print("using previous years accuracy: " + str(accuracy_score(test_y, preds))+ "\n")

def submission(values):
    train_x, train_y, test_x, test_y, loan_id = get_test_values(values)
    preds = list(apply_gaussian(train_x, train_y, test_x))
    create_file(loan_id,preds)

# _____________________________________________________________________________________________________________

values = get_train_values()

test_accuracy(values) # Tests accuracy by using train file for train+test
# submission(values) # Creates submission file to be submited