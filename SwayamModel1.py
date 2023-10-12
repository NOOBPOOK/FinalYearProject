import numpy as np
import joblib

loaded_m=joblib.load('SwayamModel.pkl')



val = [['','','','','','','','','','','','']]

for i in val:
    v=loaded_m.predict([[i]])
    print("Input value: ",i)
    print("Predicted value: ",v)