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

copd = pd.read_csv('/Users/yangyangxiayule/Documents/GitHub/COPD-Project/New CSV/copd_joint.csv')
copd_income = pd.merge(copd, income_ind, how='left', on=['State_County_Year'])

copd_income.rename(columns={'Value': 'Median_Income'}, inplace=True)

print(copd_income.head())
print(copd_income.columns.to_list())

copd_income_SD = copd_income[copd_income["StateFIPS"] == 46]
copd_income_SD['Year'].astype(int)

#2021 income data missing
copd_income_SD.to_csv('/Users/yangyangxiayule/Documents/GitHub/COPD-Project/New CSV/copd_income_SD.csv', index=False)
print(copd_income_SD.columns.to_list())

copd_income_1820 = copd_income_SD.query('Year != 2021')
copd_income_1820.to_csv('/Users/yangyangxiayule/Documents/GitHub/COPD-Project/New CSV/copd_income_1820.csv', index=False)

