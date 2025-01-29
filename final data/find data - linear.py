import pandas as pd
import numpy as np
from scipy.stats import linregress

# Define your data
data = {
    'County': ['Clay']*7,
    'Year': [2018, 2019, 2020, 2021, 2022, 2023, 2024],
    'Value': [np.nan, 88601, 87601, 86301, 85101, 83401, np.nan]
}

# Create DataFrame
df = pd.DataFrame(data)

# Filter out rows with missing values
known_data = df.dropna(subset=['Value'])

# Perform linear regression on the known data (2019–2023)
slope, intercept, _, _, _ = linregress(known_data['Year'], known_data['Value'])

# Predict the missing values (2018 and 2024)
df.loc[df['Year'] == 2018, 'Value'] = slope * 2018 + intercept
df.loc[df['Year'] == 2024, 'Value'] = slope * 2024 + intercept

# Output the updated DataFrame
print(df)
