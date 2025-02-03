import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, mean_absolute_percentage_error
import xgboost as xgb
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
df = pd.read_csv('/Users/yangyangxiayule/Documents/GitHub/COPD-Project/final data/merged_data.csv')

# Comprehensive Preprocessing
def preprocess_data(df):
    # Create a deep copy to avoid SettingWithCopyWarning
    df_processed = df.copy()
    
    # Create lagged features using groupby and transform
    df_processed['healthcare_lag1'] = df_processed.groupby('County')['healthcare'].transform(lambda x: x.shift(1))
    df_processed['income_lag1'] = df_processed.groupby('County')['income'].transform(lambda x: x.shift(1))
    df_processed['smoking_lag1'] = df_processed.groupby('County')['smoking'].transform(lambda x: x.shift(1))
    
    # Drop rows with NaN (first year for each county)
    df_processed = df_processed.dropna()
    
    # Feature engineering with .loc
    df_processed.loc[:, 'healthcare_change'] = df_processed['healthcare'] - df_processed['healthcare_lag1']
    df_processed.loc[:, 'income_change'] = df_processed['income'] - df_processed['income_lag1']
    df_processed.loc[:, 'smoking_change'] = df_processed['smoking'] - df_processed['smoking_lag1']
    
    # Interaction and polynomial features
    df_processed.loc[:, 'healthcare_income_interact'] = df_processed['healthcare'] * df_processed['income']
    df_processed.loc[:, 'smoking_income_interact'] = df_processed['smoking'] * df_processed['income']
    df_processed.loc[:, 'smoking_squared'] = df_processed['smoking'] ** 2
    df_processed.loc[:, 'income_per_capita'] = df_processed['income'] / df_processed['healthcare']
    
    # Logarithmic transformations
    df_processed.loc[:, 'log_healthcare'] = np.log1p(df_processed['healthcare'])
    df_processed.loc[:, 'log_income'] = np.log1p(df_processed['income'])
    
    return df_processed

# Prepare data for modeling
df_processed = preprocess_data(df)

# Prepare features and target
features = [
    'healthcare', 'income', 'smoking', 
    'healthcare_lag1', 'income_lag1', 'smoking_lag1',
    'healthcare_change', 'income_change', 'smoking_change',
    'healthcare_income_interact', 'smoking_income_interact',
    'smoking_squared', 'income_per_capita',
    'log_healthcare', 'log_income'
]
X = df_processed[features]
y = df_processed['copd_age']

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Comprehensive Model Dictionary with Extensive Hyperparameter Tuning
models = {
    'Linear Regression': (LinearRegression(), {}),
    'Ridge Regression': (Ridge(), {
        'alpha': [0.01, 0.1, 1.0, 10.0]
    }),
    'Lasso Regression': (Lasso(), {
        'alpha': [0.01, 0.1, 1.0, 10.0]
    }),
    'Random Forest': (RandomForestRegressor(random_state=42), {
        'n_estimators': [100, 200, 300],
        'max_depth': [None, 10, 20, 30],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4],
        'max_features': ['auto', 'sqrt']
    }),
    'Gradient Boosting': (GradientBoostingRegressor(random_state=42), {
        'n_estimators': [100, 200, 300],
        'learning_rate': [0.01, 0.1, 0.2],
        'max_depth': [3, 4, 5],
        'min_samples_split': [2, 5],
        'min_samples_leaf': [1, 2]
    }),
    'XGBoost': (xgb.XGBRegressor(random_state=42), {
        'n_estimators': [100, 200, 300],
        'learning_rate': [0.01, 0.1, 0.2],
        'max_depth': [3, 4, 5, 6],
        'subsample': [0.6, 0.8, 1.0],
        'colsample_bytree': [0.6, 0.8, 1.0]
    })
}

# Comprehensive Evaluation Function
def evaluate_model(model, params, X_train, X_test, y_train, y_test):
    # Perform Grid Search Cross-Validation
    if params:
        grid_search = GridSearchCV(model, params, cv=5, scoring='neg_mean_squared_error', n_jobs=-1)
        grid_search.fit(X_train, y_train)
        best_model = grid_search.best_estimator_
        best_params = grid_search.best_params_
    else:
        best_model = model
        best_model.fit(X_train, y_train)
        best_params = {}
    
    # Predictions
    y_pred = best_model.predict(X_test)
    
    # Comprehensive Metrics
    metrics = {
        'MSE': mean_squared_error(y_test, y_pred),
        'RMSE': np.sqrt(mean_squared_error(y_test, y_pred)),
        'MAE': mean_absolute_error(y_test, y_pred),
        'MAPE': mean_absolute_percentage_error(y_test, y_pred),
        'R2': r2_score(y_test, y_pred),
        'Best Params': best_params
    }
    
    # Cross-validation
    cv_scores = cross_val_score(best_model, X_train, y_train, cv=5, scoring='neg_mean_squared_error')
    metrics['CV RMSE'] = np.sqrt(-cv_scores).mean()
    
    return metrics

# Evaluate Models
results = {}
feature_importances = {}

print("Comprehensive Model Performance Metrics:")
for name, (model, params) in models.items():
    results[name] = evaluate_model(model, params, X_train_scaled, X_test_scaled, y_train, y_test)
    print(f"\n{name}:")
    for metric, value in results[name].items():
        print(f"{metric}: {value}")
    
    # Feature importance for tree-based models
    if hasattr(model, 'feature_importances_'):
        feature_importances[name] = dict(zip(features, model.feature_importances_))

# Visualize Feature Importances
plt.figure(figsize=(15, 8))
# Prepare data for plotting
importance_df = pd.DataFrame(feature_importances).fillna(0)
importance_df.plot(kind='bar', figsize=(15, 8))
plt.title('Feature Importances Across Models')
plt.xlabel('Features')
plt.ylabel('Importance')
plt.legend(title='Models', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

# Correlation Heatmap
plt.figure(figsize=(16, 12))
correlation_matrix = X.corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0, fmt='.2f', linewidths=0.5)
plt.title('Comprehensive Feature Correlation Heatmap')
plt.tight_layout()
plt.show()

# Create a summary DataFrame of results
results_df = pd.DataFrame.from_dict(results, orient='index')
results_df.to_csv('model_performance_summary.csv')
print("\nDetailed results saved to model_performance_summary.csv")