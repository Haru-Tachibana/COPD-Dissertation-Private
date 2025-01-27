import pandas as pd

# Load the combined air quality dataset
file_path = "/Users/yangyangxiayule/Documents/GitHub/COPD-Project/AQ_daily/combined_air_quality.csv"
df = pd.read_csv(file_path)

# Calculate the missing value report
missing_report = df.isnull().sum().to_frame(name="Missing Count")
missing_report["Total Rows"] = len(df)
missing_report["Missing Percentage"] = (missing_report["Missing Count"] / len(df)) * 100
missing_report = missing_report[missing_report["Missing Count"] > 0].sort_values(by="Missing Percentage", ascending=False)

# Print missing data report
print("### Missing Data Report ###")
print(missing_report)

# Fill missing values with the mean of each column
for column in df.columns:
    if df[column].isnull().sum() > 0 and pd.api.types.is_numeric_dtype(df[column]):
        column_mean = df[column].mean()
        df[column].fillna(column_mean, inplace=True)

# Verify no missing values remain
remaining_nulls = df.isnull().sum().sum()

# Save the cleaned dataset
cleaned_file_path = "/Users/yangyangxiayule/Documents/GitHub/COPD-Project/AQ_daily/cleaned_air_quality.csv"
df.to_csv(cleaned_file_path, index=False)

# Output the final status
print(f"Missing data has been filled with column means.")
print(f"Total missing values remaining: {remaining_nulls}")
print(f"Cleaned dataset saved to: {cleaned_file_path}")