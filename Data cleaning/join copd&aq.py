#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

copd = pd.read_csv('/Users/yangyangxiayule/Documents/GitHub/COPD-Project/New CSV/copd_joint.csv')
aq18 = pd.read_csv('/Users/yangyangxiayule/Documents/GitHub/COPD-Project/New CSV/aq18.csv')
aq19 = pd.read_csv('/Users/yangyangxiayule/Documents/GitHub/COPD-Project/New CSV/aq19.csv')
aq20 = pd.read_csv('/Users/yangyangxiayule/Documents/GitHub/COPD-Project/New CSV/aq20.csv')
aq21 = pd.read_csv('/Users/yangyangxiayule/Documents/GitHub/COPD-Project/New CSV/aq21.csv')


print(copd.columns.to_list())
print(aq18.columns.to_list())


#copd_aq.to_csv('/Users/yangyangxiayule/Documents/GitHub/COPD-Project/New CSV/copd_aq.csv', index=False)