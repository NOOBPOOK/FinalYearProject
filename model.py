#importing lib
import tensorflow as tf
import numpy as np
import pandas as pd
import joblib
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

test =pd.DataFrame(pd.read_csv('C:\\Users\\hp\\Downloads\\Voltage_Adruino_Dynamic\\AdruinoData2.csv', encoding='ISO-8859-1'))
test1 = test.dropna()
x=test1[['dvalue']]
y=test1[['voltage']]

xtrain, xtest, ytrain, ytest = train_test_split(x, y, test_size=0.2, random_state=42)
m=LinearRegression()
m.fit(xtrain.values,ytrain.values)

joblib.dump(m, 'trained_model.pkl')