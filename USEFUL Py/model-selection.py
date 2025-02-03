import pandas as pd
import numpy as np
from sklearn.model_selection import TimeSeriesSplit
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import xgboost as xgb
from scipy.stats import zscore

def load_and_prepare_data(demographic_data, copd_data, aq_data):
    # Check columns in the datasets
    print("Demographic Data Columns:", demographic_data.columns)
    print("COPD Data Columns:", copd_data.columns)
    print("Air Quality Data Columns:", aq_data.columns)

    # Merge datasets on the correct columns
    merged_data = demographic_data.merge(copd_data, on=['County', 'Year'], how='inner')  # Adjusted to 'County' and 'Year'
    merged_data = merged_data.merge(aq_data, left_on=['County', 'Year'], right_on=['County_', 'Year_'], how='inner')  # Adjusted to 'County_' and 'Year_' for air quality data
    
    # Check the merged data
    print("Merged Data Sample:")
    print(merged_data.head())

    # Assuming 'target' column is COPD prevalence (adjust if needed)
    X = merged_data.drop(columns=['copd%_age'])  # Replace 'copd%_age' with actual target column
    y = merged_data['copd%_age']  # Replace with actual target column
    
    print("X Sample:")
    print(X.head())
    print("y Sample:")
    print(y.head())
    
    return X, y


def train_and_evaluate_models(X, y):
    # Clean the target variable y (remove percentage symbol and convert to float)
    y_clean = y.str.replace('%', '').astype(float) / 100.0  # Convert percentages to decimals
    
    # Check for missing values
    print(f"Missing values in y: {y_clean.isnull().sum()}")
    
    # Only select numeric columns for z-score calculation
    X_numeric = X.select_dtypes(include=['number'])

    # Standardize the data using z-score
    z_scores = np.abs(zscore(X_numeric))

    # Select features based on z-score threshold (e.g., features with z-score > 3 are outliers)
    threshold = 3
    selected_features = X_numeric.columns[(z_scores < threshold).all(axis=0)]

    # Use the selected features to train and evaluate models
    X_selected = X[selected_features]
    
    # Now, proceed with your model training and evaluation (e.g., cross-validation)
    results = {}  # Store results of models
    
    if X_selected.empty or y_clean.empty:
        print("Warning: Empty dataset detected!")
        return results
    
    # Example model, replace with your actual model training process
    from sklearn.linear_model import LinearRegression
    model = LinearRegression()
    
    from sklearn.model_selection import cross_val_score
    r2_scores = cross_val_score(model, X_selected, y_clean, cv=5, scoring='r2')
    
    # Ensure the results are populated
    if len(r2_scores) > 0:
        results['mean_r2'] = r2_scores.mean()  # Store the mean R² score
    
    # Check if results are populated
    if not results:
        print("No results found!")
    return results


def main():
    # Load data from the paths you've provided
    print("Loading data...")
    demographic_data = pd.read_csv('/Users/yangyangxiayule/Documents/GitHub/COPD-Project/final data/demographic_data.csv')
    copd_data = pd.read_csv('/Users/yangyangxiayule/Documents/GitHub/COPD-Project/final data/copd_data.csv')
    aq_data = pd.read_csv('/Users/yangyangxiayule/Documents/GitHub/COPD-Project/final data/air_quality_statistics_by_year.csv')
    
    # Prepare the data
    X, y = load_and_prepare_data(demographic_data, copd_data, aq_data)
    
    # Check if data is properly prepared
    if X.empty or y.empty:
        print("Error: Prepared data is empty!")
        return
    
    # Train models and evaluate
    results = train_and_evaluate_models(X, y)
    
    # Check the results content
    print("Results:", results)
    
    # Convert results to DataFrame and transpose for better readability
    if results:
        summary = pd.DataFrame([results])  # Ensure it's in a column format
        print("\nModel Performance Summary:")
        print(summary)
    
    # Access the best model (highest R²)
    best_model_index = summary['mean_r2'].idxmax() if not summary.empty else None
    print(f"\nBest Model: Fold {best_model_index}")


if __name__ == "__main__":
    main()
