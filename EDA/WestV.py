import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

copd_data = pd.read_csv('/Users/yangyangxiayule/Documents/GitHub/COPD-Project/New CSV/copd_joint.csv')

# Clean the data
copd_data['copd%_age'] = copd_data['copd%_age'].str.rstrip('%').astype('float')
copd_data['copd%_crude'] = copd_data['copd%_crude'].str.rstrip('%').astype('float')

# Filter the dataset for West Virginia
wv_data = copd_data[copd_data['State'] == 'West Virginia']

# Define a function to calculate the trend for each county
def calculate_trend(group):
    group = group.sort_values('Year')
    
    if len(group['Year'].unique()) > 1:  # Check if there are multiple years to calculate the trend
        age_adjusted_slope = np.polyfit(group['Year'], group['copd%_age'], 1)[0]
        crude_slope = np.polyfit(group['Year'], group['copd%_crude'], 1)[0]
    else:
        age_adjusted_slope = 0
        crude_slope = 0
    
    return pd.Series({
        'age_adjusted_trend': age_adjusted_slope,
        'crude_trend': crude_slope
    })

# Group the data by County and apply the trend calculation function
wv_trend_data = wv_data.groupby('County').apply(calculate_trend).reset_index()

# Find the county with the worst worsening trend in West Virginia
worst_wv_county = wv_trend_data.loc[wv_trend_data['age_adjusted_trend'].idxmax()]

print("County in West Virginia with the most worsening trend (Age-Adjusted):")
print(worst_wv_county)

# Optionally, plot the overall trends for West Virginia
wv_avg_data = wv_data.groupby('Year').agg({
    'copd%_age': 'mean',
    'copd%_crude': 'mean'
}).reset_index()

# Plot the overall trends
plt.figure(figsize=(10, 6))
plt.plot(wv_avg_data['Year'], wv_avg_data['copd%_age'], label='Age-Adjusted COPD Prevalence (WV)')
plt.plot(wv_avg_data['Year'], wv_avg_data['copd%_crude'], label='Crude COPD Prevalence (WV)')
plt.xlabel('Year')
plt.ylabel('COPD Prevalence (%)')
plt.title('COPD Prevalence in West Virginia Over Time')
plt.legend()
plt.show()