from xgboost import XGBRegressor
from sklearn.model_selection import TimeSeriesSplit, train_test_split, GridSearchCV
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

# Train and evaluate XGBoost model
def train_and_evaluate_xgboost(X, y):
    # Split into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Hyperparameter tuning with GridSearchCV
    param_grid = {
        'max_depth': [3, 5, 7],
        'learning_rate': [0.01, 0.05, 0.1],
        'n_estimators': [100, 200],
        'subsample': [0.7, 1.0],
        'colsample_bytree': [0.7, 1.0],
        'reg_alpha': [0, 0.1],
        'reg_lambda': [0, 1]
    }

    xgb = XGBRegressor(random_state=42)
    grid_search = GridSearchCV(estimator=xgb, param_grid=param_grid, cv=3, scoring='neg_mean_squared_error')
    grid_search.fit(X_train, y_train)

    best_params = grid_search.best_params_
    print(f"Best Hyperparameters: {best_params}")

    best_model = grid_search.best_estimator_
    best_model.fit(X_train, y_train, eval_set=[(X_test, y_test)], early_stopping_rounds=10, verbose=True)

    y_pred = best_model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)

    print(f"XGBoost Performance:\nMAE: {mae:.4f}, RMSE: {rmse:.4f}, R²: {r2:.4f}")
    
    # Time Series Cross-Validation
    tscv = TimeSeriesSplit(n_splits=5)
    cv_scores = cross_val_score(best_model, X, y, cv=tscv, scoring='r2')
    print(f"5-Fold TimeSeries CV R²: {cv_scores.mean():.4f}")
    
    # Feature Importance
    importance = pd.DataFrame({'feature': X.columns, 'importance': best_model.feature_importances_})
    print("\nFeature Importance:")
    print(importance.sort_values('importance', ascending=False))

# Assuming X, y are already prepared and cleaned
train_and_evaluate_xgboost(X, y)
