# train_model.py

# imports
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import cross_val_score, train_test_split, KFold
import numpy as np
import random

# train_machine_learning_model method takes two parameters, X being the features and y being the
# feature to predict.
def train_machine_learning_model(X, y):
    # Set random seed for reproducibility
    random.seed(42)

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    # Create model
    RF_model = RandomForestRegressor(n_estimators=100, random_state=42)
    # Fit the model on the training data
    RF_model.fit(X_train, y_train)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # In perform_cross_validation function in cross_val.py, set a random_state in cross_val_score
    kf = KFold(n_splits=5, shuffle=True, random_state=42)
    scores = cross_val_score(RF_model, X_train, y_train, cv=kf, scoring='neg_mean_squared_error')
    rmse_scores = np.sqrt(-scores)

    # Calculate MAE and other metrics here
    y_pred = RF_model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r_squared = r2_score(y_test, y_pred)
    adjusted_r_squared = 1 - (1 - r_squared) * (len(y_test) - 1) / (len(y_test) - 4 - 1)
    mean_rmse = np.mean(rmse_scores)

    return RF_model, X_train, y_train, mae, mse, rmse, y_test, y_pred, r_squared, adjusted_r_squared, mean_rmse
