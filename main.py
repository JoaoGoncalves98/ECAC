import os
import numpy as np
import pandas as pd
from sklearn.naive_bayes import GaussianNB
from sklearn import metrics
import csv

# Devemos dividir os dados do train e usa-los tb para test e ver qual é o melhor a partir daí
# e depois usamos o com maior eficiencia no ficheiro de test.
os.chdir('data')
heart = pd.read_csv('loan_train.csv', sep=';', header=0)
heart.head()

train_y = heart.iloc[:,6]
train_x = heart.iloc[:,:6]

heart = pd.read_csv('loan_test.csv', sep=';', header=0)
heart.head()

test_y = heart.iloc[:,6]
test_x = heart.iloc[:,:6]

# Aqui aplicamos um algoritmo para calcular os valores e para a % de acertamento
gnb = GaussianNB()
model = gnb.fit(train_x, train_y)
preds = gnb.predict(test_x)



# Criar o ficheiro csv
loan_id = list(heart.iloc[:,0])
results = list(preds)

print(metrics.auc(preds, list(test_y)))

os.chdir('..')
f=open('submission.csv','w')
f.write("Id,Predicted")
for i,j in zip(loan_id,results):
    f.write("\n"+str(i)+","+str(j))
f.close()