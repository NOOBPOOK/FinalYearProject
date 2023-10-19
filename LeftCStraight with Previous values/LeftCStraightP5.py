import numpy as np
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn import svm
"""
Left Closed-1
Straight-2
Accuracy- 96
"""
data = pd.read_csv('C:\\Users\\rutuj\\OneDrive\\Documents\\GitHub\\FinalYearProject\\LeftCStraight with Previous values\\LeftCStraightP5.csv')
data1 = data.dropna()
x = data1[['LowAlpha','LowAlphaPhase','HighAlpha','HighAlphaPhase','LowBeta','LowBetaPhase','HighBeta','HighBetaPhase','LowGamma','LowGammePhase','HighGamma','HighGammaPhase','AvgAlphaPrevious1','AvgBetaPrevious1','AvgGammaPrevious1','AvgAlphaPrevious2','AvgBetaPrevious2','AvgGammaPrevious2','AvgAlphaPrevious3','AvgBetaPrevious3','AvgGammaPrevious3','AvgAlphaPrevious4','AvgBetaPrevious4','AvgGammaPrevious4','AvgAlphaPrevious5','AvgBetaPrevious5','AvgGammaPrevious5']].values
y = data1[['eyesC']]  

print(data1)
xtrain, xtest, ytrain, ytest = train_test_split(x, y, test_size=0.2, random_state=42)

model = svm.SVC(kernel='rbf')
model.fit(xtrain, ytrain.values.ravel())  # Use ravel() to reshape ytrain

from sklearn.metrics import accuracy_score

# Make predictions on the test data
y_pred = model.predict(xtest)

# Calculate the accuracy score
accuracy = accuracy_score(ytest, y_pred)
print("Accuracy:",accuracy)

# Make predictions on the test data
y_pred= model.predict(xtest)

joblib.dump(model,'LeftCStraightP5.pkl')
print("Model saved successfully")