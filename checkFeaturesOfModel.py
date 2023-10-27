import joblib
from sklearn.model_selection import GridSearchCV


# Load the model from the .pkl file
loaded_model = joblib.load('NormalFocusEyesCEveryoneP5Implement.pkl')

# Check if the loaded model is a GridSearchCV object
if isinstance(loaded_model, GridSearchCV):
    # Access the best estimator from the GridSearchCV object
    best_estimator = loaded_model.best_estimator_
else:
    # If it's not a GridSearchCV, assume it's the model itself
    best_estimator = loaded_model

# Check if the model uses a linear kernel
if best_estimator.kernel == 'linear':
    # For linear kernel, you can access the coefficients
    num_features_expected = best_estimator.coef_.shape[1]
    print(f"Number of features used during model creation: {num_features_expected}")
else:
    # For non-linear kernel (e.g., RBF), explore support vectors and dual coefficients
    support_vectors_count = best_estimator.support_vectors_.shape[0]
    print(f"Number of support vectors used during model creation: {support_vectors_count}")
    
    # Access dual coefficients (for multi-class classification)
    dual_coefficients = best_estimator.dual_coef_
    print(f"Dual coefficients shape: {dual_coefficients.shape}")
