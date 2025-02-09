import pandas as pd

demo_df = pd.read_csv('/Users/yangyangxiayule/Documents/GitHub/COPD-Project/final data/demographic_data.csv')

yearly_stats = demo_df.groupby('Year')[['healthcare', 'income', 'smoking']].describe()

overall_stats = demo_df[['healthcare', 'income', 'smoking']].describe()

yearly_stats.to_csv('/Users/yangyangxiayule/Documents/GitHub/COPD-Project/final data/demo_stat.csv')

# Display yearly and overall statistics
print("\nYearly Summary Statistics:")
print(yearly_stats)
print("\nOverall Summary Statistics:")
print(overall_stats)
