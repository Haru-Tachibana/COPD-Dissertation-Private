#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

copd = pd.read_csv('/Users/yangyangxiayule/Documents/GitHub/COPD-Project/New CSV/copd_joint.csv')
aq18 = pd.read_csv('/Users/yangyangxiayule/Documents/GitHub/COPD-Project/New CSV/aq18.csv')

aq18['Year'] = 2018
print(copd.columns.to_list())
print(aq18.columns.to_list())
merged_1 = pd.merge(copd, aq18, on=['County', 'Year'], how='left')
print(merged_1.head())
