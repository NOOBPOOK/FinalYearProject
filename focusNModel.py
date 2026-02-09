import numpy as np
import joblib

loadmodel=joblib.load('focusNormalModel.pkl')

inp=np.array([['381.3147507','0.821931969','314.7529198','1.064583771','412.4781897','0.046096625','426.9408943','0.50757307','617.424999','2110.091104','3455.996174','-0.011155139']])
v=loadmodel.predict(inp)
print("Input value: ",inp)
print("Predicted value: ",v)