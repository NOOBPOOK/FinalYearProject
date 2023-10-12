import numpy as np
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn import svm

data = pd.read_csv('C:\\Users\\rutuj\\OneDrive\\Desktop\\FinalData.csv')
data1 = data.dropna()
x = data1[['LowAlpha','LowAlphaPhase','HighAlpha','HighAlphaPhase','LowBeta','LowBetaPhase','HighBeta','HighBetaPhase','LowGamma','LowGammePhase','HighGamma','HighGammaPhase','avgAlphaPrevious3','avgBetaPrevious3','avgGammaPrevious3','avgAlphaPrevious2','avgBetaPrevious2','avgGammaPrevious2','avgAlphaPrevious1','avgBetaPrevious1','avgGammaPrevious1']].values
y = data1[['eyes']]  

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

joblib.dump(model,'Prev3Model.pkl')
print("Model saved successfully")