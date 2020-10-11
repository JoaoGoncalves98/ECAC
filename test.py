import os
import numpy as np
import pandas as pd
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

import csv

# Devemos dividir os dados do train e usa-los tb para test e ver qual é o melhor a partir daí
# e depois usamos o com maior eficiencia no ficheiro de test.
os.chdir('data')
heart = pd.read_csv('loan_train.csv', sep=';', header=0)
heart.head()

values_93 = heart[(heart['date'] > 930000) & (heart['date'] < 940000)]
values_94 = heart[(heart['date'] > 940000) & (heart['date'] < 950000)]
values_95 = heart[(heart['date'] > 950000) & (heart['date'] < 960000)]
values_96 = heart[heart['date'] > 960000]


train_y = values_93.iloc[:,6]
train_x = values_93.iloc[:,:6]

test_y = values_94.iloc[:,6]
test_x = values_94.iloc[:,:6]
# train_y, test_y = train_test_split(values_y, test_size=0.25, random_state=0, shuffle=True)
# train_x, test_x = train_test_split(values_x, test_size=0.25, random_state=0, shuffle=True)
# Aqui aplicamos um algoritmo para calcular os valores e para a % de acertamento

gnb = GaussianNB()
model = gnb.fit(train_x, train_y)
preds = gnb.predict(test_x)

# print(preds)
print(accuracy_score(test_y, preds))