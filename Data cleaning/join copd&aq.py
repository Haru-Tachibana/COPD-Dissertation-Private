#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

copd = pd.read_csv('/Users/yangyangxiayule/Documents/GitHub/COPD-Project/New CSV/copd_joint.csv')
aq = pd.read_csv('/Users/yangyangxiayule/Documents/GitHub/COPD-Project/New CSV/airqualitydata_18to21.csv')

print(copd.columns.to_list())
print(aq.columns.to_list())

copd_aq = pd.merge(copd, aq, how='left', on=['State_County_Year'])
copd_aq.to_csv('/Users/yangyangxiayule/Documents/GitHub/COPD-Project/New CSV/copd_aq.csv', index=False)