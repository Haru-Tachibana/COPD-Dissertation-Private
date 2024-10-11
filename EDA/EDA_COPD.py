#%%
import pandas as pd
import numpy as np

copd_data = pd.read_csv('/Users/yangyangxiayule/Documents/GitHub/COPD-Project/New CSV/copd_joint.csv')

copd_data['copd%_age'] = copd_data['copd%_age'].str.rstrip('%').astype('float')
copd_data['copd%_crude'] = copd_data['copd%_crude'].str.rstrip('%').astype('float')

# calculate the trend for each county
def calculate_trend(group):
    group = group.sort_values('Year')
    
    # calculate the slope (trend) for age-adjusted and crude COPD prevalence over time
    if len(group['Year'].unique()) > 1:  
        age_adjusted_slope = np.polyfit(group['Year'], group['copd%_age'], 1)[0]
        crude_slope = np.polyfit(group['Year'], group['copd%_crude'], 1)[0]
    else:
        age_adjusted_slope = 0
        crude_slope = 0
    
    return pd.Series({
        'age_adjusted_trend': age_adjusted_slope,
        'crude_trend': crude_slope
    })

# group the data by State and County
county_trend_data = copd_data.groupby(['State', 'County']).apply(calculate_trend).reset_index()

state_trend_data = county_trend_data.groupby('State').agg({
    'age_adjusted_trend': 'mean',  # average
    'crude_trend': 'mean'
}).reset_index()

# Find the state with the worst worsening trend
worst_state = state_trend_data.loc[state_trend_data['age_adjusted_trend'].idxmax()]

# Print the state with the most worsening trend
print("State with the most worsening trend (Age-Adjusted):")
print(worst_state)

# the full ranking (optional)
sorted_state_trends = state_trend_data.sort_values(by='age_adjusted_trend', ascending=False)
print("\nAll states ranked by worsening trend (Age-Adjusted):")
print(sorted_state_trends)