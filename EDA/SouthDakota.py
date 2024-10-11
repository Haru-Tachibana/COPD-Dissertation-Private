import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

copd_data = pd.read_csv('/Users/yangyangxiayule/Documents/GitHub/COPD-Project/New CSV/copd_joint.csv')

copd_data['copd%_age'] = copd_data['copd%_age'].str.rstrip('%').astype('float')
copd_data['copd%_crude'] = copd_data['copd%_crude'].str.rstrip('%').astype('float')

sd_data = copd_data[copd_data['State'] == 'South Dakota']

def calculate_sd_trend(group):
    group = group.sort_values('Year')
    
    if len(group['Year'].unique()) > 1:
        age_adjusted_slope = np.polyfit(group['Year'], group['copd%_age'], 1)[0]
        crude_slope = np.polyfit(group['Year'], group['copd%_crude'], 1)[0]
    else:
        age_adjusted_slope = 0
        crude_slope = 0
    
    return pd.Series({
        'age_adjusted_trend': age_adjusted_slope,
        'crude_trend': crude_slope,
        'latest_age_adjusted': group['copd%_age'].iloc[-1],
        'latest_crude': group['copd%_crude'].iloc[-1]
    })

sd_trend_data = sd_data.groupby('County').apply(calculate_sd_trend).reset_index()

sd_summary = {
    'Total_Counties': sd_trend_data.shape[0],
    'Highest_Age_Adjusted_Prevalence': sd_trend_data['latest_age_adjusted'].max(),
    'County_with_Highest_Age_Adjusted': sd_trend_data.loc[sd_trend_data['latest_age_adjusted'].idxmax(), 'County'],
    'Overall_Age_Adjusted_Trend': sd_trend_data['age_adjusted_trend'].mean(),
    'Overall_Crude_Trend': sd_trend_data['crude_trend'].mean()
}

print("Summary of COPD Prevalence and Trends in South Dakota:")
for key, value in sd_summary.items():
    print(f"{key}: {value}")

sd_avg_data = sd_data.groupby('Year').agg({
    'copd%_age': 'mean',
    'copd%_crude': 'mean'
}).reset_index()

plt.figure(figsize=(10, 6))
plt.plot(sd_avg_data['Year'], sd_avg_data['copd%_age'], label='Age-Adjusted COPD Prevalence (SD)', color='blue')
plt.plot(sd_avg_data['Year'], sd_avg_data['copd%_crude'], label='Crude COPD Prevalence (SD)', color='orange')
plt.xlabel('Year')
plt.ylabel('COPD Prevalence (%)')
plt.title('COPD Prevalence in South Dakota Over Time')
plt.legend()
plt.grid()
plt.show()