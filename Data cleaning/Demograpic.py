#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

annual_median_income_1820 = pd.read_csv("/Users/yangyangxiayule/Documents/GitHub/COPD-Project/Datasets/DEMOGRAPHICS & SOCIOECONOMICS/SOCIOECONOMIC ANNUAL MEDIAN HOUSEHOLD INCOME .csv")
print(annual_median_income_1820.columns.to_list())

#annual_median_income_1820.rename(columns={
#    'Value': 'copd%_crude',
#    'Confidence Interval High': 'CI_high_annual_median_income_1820',
#    'Confidence Interval Low': 'CI_low_annual_median_income_1820',
#}, inplace=True)

annual_median_income_1820.drop(columns=['CountyFIPS', 'Data Comment'], inplace=True)
annual_median_income_1820.dropna(axis=1, inplace=True)
annual_median_income_1820.dropna(axis=0, inplace=True)
annual_median_income_1820['State_County_Year'] = annual_median_income_1820['State'] + annual_median_income_1820['County'] + annual_median_income_1820['Year'].astype(str)

annual_median_income_1820['State_County_Year'] = annual_median_income_1820['State_County_Year'].str.lower()
annual_median_income_1820['State_County_Year'] = annual_median_income_1820['State_County_Year'].str.strip()

def remove_space(x):
    return(''.join(x.split()))

annual_median_income_1820['State_County_Year'] = annual_median_income_1820['State_County_Year'].astype(str).apply(lambda x: remove_space(x))


SD_income = annual_median_income_1820[annual_median_income_1820["StateFIPS"] == 46]

print(SD_income.head())

income_ind = SD_income.drop(columns=['StateFIPS', 'State', 'County', 'Year'])
print(income_ind.head())

SD_income.to_csv('/Users/yangyangxiayule/Documents/GitHub/COPD-Project/New CSV/SD_income.csv', index=False)
income_ind.to_csv('/Users/yangyangxiayule/Documents/GitHub/COPD-Project/New CSV/income_ind.csv', index=False)