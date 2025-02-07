import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, mean_absolute_percentage_error

# Load data
df = pd.read_csv('/Users/yangyangxiayule/Documents/GitHub/COPD-Project/final data/merged_data.csv')

def create_advanced_features(df):
    """Advanced feature engineering"""
    df_features = df.copy()
    
    # Rolling statistics
    df_features['income_rolling_mean'] = df_features.groupby('County')['income'].transform(lambda x: x.rolling(window=3, min_periods=1).mean())
    df_features['healthcare_rolling_mean'] = df_features.groupby('County')['healthcare'].transform(lambda x: x.rolling(window=3, min_periods=1).mean())
    df_features['smoking_rolling_mean'] = df_features.groupby('County')['smoking'].transform(lambda x: x.rolling(window=3, min_periods=1).mean())
    
    # Interaction features
    df_features['income_smoking_interaction'] = df_features['income'] * df_features['smoking']
    df_features['healthcare_smoking_interaction'] = df_features['healthcare'] * df_features['smoking']
    
    # Ratio features
    df_features['income_healthcare_ratio'] = df_features['income'] / (df_features['healthcare'] + 1)
    
    # Temporal features
    df_features['year_encoded'] = df_features['Year'] - df_features['Year'].min()
    
    # Polynomial features
    df_features['income_squared'] = df_features['income'] ** 2
    df_features['smoking_squared'] = df_features['smoking'] ** 2
    
    return df_features

# Prepare data
def prepare_data(df):
    df_features = create_advanced_features(df)
    
    features = [
        'income', 'healthcare', 'smoking', 
        'income_rolling_mean', 'healthcare_rolling_mean', 'smoking_rolling_mean',
        'income_smoking_interaction', 'healthcare_smoking_interaction',
        'income_healthcare_ratio', 'year_encoded',
        'income_squared', 'smoking_squared'
    ]
    
    X = df_features[features]
    y = df_features['copd_age']
    
    return X, y

# Prepare data
X, y = prepare_data(df)

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Hyperparameter tuning grid
param_grid = {
    'regressor__n_estimators': [100, 200, 300],
    'regressor__learning_rate': [0.01, 0.1, 0.5],
    'regressor__max_depth': [3, 4, 5],
    'regressor__min_samples_split': [2, 5, 10],
    'regressor__min_samples_leaf': [1, 2, 4]
}

# Create pipeline
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('regressor', GradientBoostingRegressor(random_state=42))
])

# Grid search
grid_search = GridSearchCV(
    pipeline, 
    param_grid, 
    cv=5, 
    scoring='neg_mean_squared_error', 
    n_jobs=-1
)

# Fit grid search
grid_search.fit(X_train, y_train)

# Best model
best_model = grid_search.best_estimator_
best_params = grid_search.best_params_

# Predictions
y_pred = best_model.predict(X_test)

# Evaluation metrics
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
mape = mean_absolute_percentage_error(y_test, y_pred)

# Print results
print("Best Hyperparameters:", best_params)
print(f"MSE: {mse:.4f}")
print(f"RMSE: {rmse:.4f}")
print(f"MAE: {mae:.4f}")
print(f"R2 Score: {r2:.4f}")
print(f"MAPE: {mape:.4f}")

# Feature importance
feature_importance = best_model.named_steps['regressor'].feature_importances_
feature_names = X.columns
importance_df = pd.DataFrame({
    'feature': feature_names,
    'importance': feature_importance
}).sort_values('importance', ascending=False)

print("\nFeature Importance:")
print(importance_df)

import pandas as pd
import numpy as np
import joblib
from sklearn.pipeline import Pipeline

# Save the trained model
joblib.dump(best_model, "copd_prediction_model.pkl")
print("Model saved successfully!")

# Load saved model
model = joblib.load("copd_prediction_model.pkl")

# Load new data (2022-2024)
df_new = pd.read_csv('/Users/yangyangxiayule/Documents/GitHub/COPD-Project/final data/demo_data_2022_2024.csv')

# Apply the same feature engineering
df_new_features = create_advanced_features(df_new)

# Select the same features as in training
features = [
    'income', 'healthcare', 'smoking', 
    'income_rolling_mean', 'healthcare_rolling_mean', 'smoking_rolling_mean',
    'income_smoking_interaction', 'healthcare_smoking_interaction',
    'income_healthcare_ratio', 'year_encoded',
    'income_squared', 'smoking_squared'
]

X_new = df_new_features[features]

# Predict COPD prevalence for 2022-2024
df_new_features['predicted_copd_age'] = model.predict(X_new)

# Save predictions
df_new_features[['County', 'Year', 'predicted_copd_age']].to_csv("copd_predictions_2022_2024.csv", index=False)
print("Predictions saved successfully!")