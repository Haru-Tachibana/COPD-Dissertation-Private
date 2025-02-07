import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, mean_absolute_percentage_error
from sklearn.pipeline import Pipeline
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
df = pd.read_csv('/Users/yangyangxiayule/Documents/GitHub/COPD-Project/final data/merged_data.csv')

# Feature Engineering
def create_features(df):
    # Create lagged features
    df_grouped = df.sort_values(['County', 'Year'])
    
    # Create rolling window features
    df_grouped['income_rolling_mean'] = df_grouped.groupby('County')['income'].rolling(window=3, min_periods=1).mean().reset_index(0, drop=True)
    df_grouped['healthcare_rolling_mean'] = df_grouped.groupby('County')['healthcare'].rolling(window=3, min_periods=1).mean().reset_index(0, drop=True)
    df_grouped['smoking_rolling_mean'] = df_grouped.groupby('County')['smoking'].rolling(window=3, min_periods=1).mean().reset_index(0, drop=True)
    
    # Create year-based features
    df_grouped['year_since_start'] = df_grouped.groupby('County')['Year'].rank(method='first')
    
    # Create interaction features
    df_grouped['income_smoking_interaction'] = df_grouped['income'] * df_grouped['smoking']
    df_grouped['healthcare_smoking_interaction'] = df_grouped['healthcare'] * df_grouped['smoking']
    
    return df_grouped

# Prepare data for modeling
def prepare_data(df):
    # Create features
    df_features = create_features(df)
    
    # Select features and target
    features = [
        'income', 'healthcare', 'smoking', 
        'income_rolling_mean', 'healthcare_rolling_mean', 'smoking_rolling_mean',
        'year_since_start', 
        'income_smoking_interaction', 'healthcare_smoking_interaction'
    ]
    
    X = df_features[features]
    y = df_features['copd_age']
    
    return X, y

# Prepare data
X, y = prepare_data(df)

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define models
models = {
    'Linear Regression': LinearRegression(),
    'Ridge Regression': Ridge(alpha=1.0),
    'Lasso Regression': Lasso(alpha=1.0),
    'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42),
    'Gradient Boosting': GradientBoostingRegressor(n_estimators=100, random_state=42)
}

# Evaluation function
def evaluate_model(y_true, y_pred, model_name):
    mse = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)
    mape = mean_absolute_percentage_error(y_true, y_pred)
    
    print(f"{model_name} Results:")
    print(f"MSE: {mse:.4f}")
    print(f"RMSE: {rmse:.4f}")
    print(f"MAE: {mae:.4f}")
    print(f"R2 Score: {r2:.4f}")
    print(f"MAPE: {mape:.4f}")
    
    return {
        'MSE': mse,
        'RMSE': rmse,
        'MAE': mae,
        'R2': r2,
        'MAPE': mape
    }

# Create pipelines with scaling
def create_pipeline(model):
    return Pipeline([
        ('scaler', StandardScaler()),
        ('regressor', model)
    ])

# Store results and models
results = {}
trained_models = {}

# Train and evaluate models
for name, model in models.items():
    # Create pipeline
    pipeline = create_pipeline(model)
    
    # Train model
    pipeline.fit(X_train, y_train)
    
    # Predict
    y_pred = pipeline.predict(X_test)
    
    # Evaluate
    results[name] = evaluate_model(y_test, y_pred, name)
    trained_models[name] = pipeline
    
    # 5-fold Cross-validation R2
    cv_scores = cross_val_score(pipeline, X, y, cv=5, scoring='r2')
    print(f"{name} 5-Fold CV R2: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
    
    # Export model
    joblib.dump(pipeline, f'{name.replace(" ", "_")}_model.joblib')

# Feature Importance for Tree-based Models
def plot_feature_importance(model, feature_names):
    # For Random Forest and Gradient Boosting
    if hasattr(model.named_steps['regressor'], 'feature_importances_'):
        importances = model.named_steps['regressor'].feature_importances_
        indices = np.argsort(importances)[::-1]
        
        plt.figure(figsize=(10,6))
        plt.title("Feature Importances")
        plt.bar(range(len(importances)), importances[indices])
        plt.xticks(range(len(importances)), [feature_names[i] for i in indices], rotation=45)
        plt.tight_layout()
        plt.savefig('feature_importance.png')
        plt.close()
        
        # Print feature importances
        for f in range(len(feature_names)):
            print("%2d) %-*s %f" % (f + 1, 30, feature_names[indices[f]], importances[indices[f]]))

# Plot feature importance for Random Forest and Gradient Boosting
for name in ['Random Forest', 'Gradient Boosting']:
    if name in trained_models:
        print(f"\nFeature Importance for {name}:")
        plot_feature_importance(trained_models[name], X.columns)

# Comparative Results Visualization
results_df = pd.DataFrame.from_dict(results, orient='index')
results_df.to_csv('model_comparison_results.csv')

# Optional: Plot model comparison
plt.figure(figsize=(10,6))
results_df['R2'].plot(kind='bar')
plt.title('Model Comparison - R2 Scores')
plt.ylabel('R2 Score')
plt.tight_layout()
plt.savefig('model_comparison.png')
plt.close()

print("\nModel training, evaluation, and export complete.")