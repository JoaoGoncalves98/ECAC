import numpy as np
import pandas as pd
import os

# Devemos dividir os dados do train e usa-los tb para test e ver qual é o melhor a partir daí
# e depois usamos o com maior eficiencia no ficheiro de test.
os.chdir('data')
heart = pd.read_csv('loan_train.csv', sep=',', header=0)
heart.head()

train_y = heart.iloc[:,6]
train_x = heart.iloc[:,:6]

heart = pd.read_csv('loan_test.csv', sep=',', header=0)
heart.head()

test_y = heart.iloc[:,6]
test_x = heart.iloc[:,:6]


# Aqui aplicamos um algoritmo para calcular os valores e para a % de acertamento

LR = LogisticRegression(random_state=-1, solver='lbfgs', multi_class='ovr').fit(X, y)
LR.predict(X.iloc[200:,:])
round(LR.score(X,y), 3)