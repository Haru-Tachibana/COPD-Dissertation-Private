import pandas as pd

local_file = '/Users/yangyangxiayule/Documents/GitHub/COPD-Project/New CSV/copd_joint.csv'
full_copd_data = pd.read_csv(local_file)

copd = full_copd_data.loc[full_copd_data['StateFIPS'] == 54]

# Preview data
print(copd.head())

copd.to_csv("/Users/yangyangxiayule/Documents/GitHub/COPD-Project/Datasets/copd_wv.csv", index=False)
