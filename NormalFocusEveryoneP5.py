import numpy as np
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn import svm

data = pd.read_csv('C:\\Users\\rutuj\\OneDrive\\Documents\\GitHub\\FinalYearProject\\NormalFocusEveryoneP5.csv')
data1 = data.dropna()
x = data1[['LowAlpha','LowAlphaPhase','HighAlpha','HighAlphaPhase','LowBeta','LowBetaPhase','HighBeta','HighBetaPhase','LowGamma','LowGammePhase','HighGamma','HighGammaPhase','PrevAlpha1','PrevBeta1','PrevGamma1','PrevAlpha2','PrevBeta2','PrevGamma2','PrevAlpha3','PrevBeta3','PrevGamma3','PrevAlpha4','PrevBeta4','PrevGamma4','PrevAlpha5','PrevBeta5','PrevGamma5']].values
y = data1[['focus']]  

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

joblib.dump(model,'NormalFocusEveryoneP5.pkl')
print("Model saved successfully")