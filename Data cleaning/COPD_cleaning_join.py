#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

copd_age = pd.read_csv("/Users/yangyangxiayule/Documents/GitHub/COPD-Project/Datasets/COPD data(csv)/AGE-ADJUSTED_PREVALENCE_COPD.csv")
copd_crude = pd.read_csv("/Users/yangyangxiayule/Documents/GitHub/COPD-Project/Datasets/COPD data(csv)/CRUDE_PREVALENCE_COPD.csv")

aq18 = pd.read_csv("/Users/yangyangxiayule/Documents/GitHub/COPD-Project/Datasets/AQ_18-24_county/annual_aqi_by_county_2018.csv")
aq19 = pd.read_csv("/Users/yangyangxiayule/Documents/GitHub/COPD-Project/Datasets/AQ_18-24_county/annual_aqi_by_county_2019.csv")
aq20 = pd.read_csv("/Users/yangyangxiayule/Documents/GitHub/COPD-Project/Datasets/AQ_18-24_county/annual_aqi_by_county_2020.csv")
aq21 = pd.read_csv("/Users/yangyangxiayule/Documents/GitHub/COPD-Project/Datasets/AQ_18-24_county/annual_aqi_by_county_2021.csv")
aq22 = pd.read_csv("/Users/yangyangxiayule/Documents/GitHub/COPD-Project/Datasets/AQ_18-24_county/annual_aqi_by_county_2022.csv")
aq23 = pd.read_csv("/Users/yangyangxiayule/Documents/GitHub/COPD-Project/Datasets/AQ_18-24_county/annual_aqi_by_county_2023.csv")
aq24 = pd.read_csv("/Users/yangyangxiayule/Documents/GitHub/COPD-Project/Datasets/AQ_18-24_county/annual_aqi_by_county_2024.csv")

annual_median_income_1820 = pd.read_csv("/Users/yangyangxiayule/Documents/GitHub/COPD-Project/Datasets/DEMOGRAPHICS & SOCIOECONOMICS/SOCIOECONOMIC ANNUAL MEDIAN HOUSEHOLD INCOME .csv")

smoke_age_1821 = pd.read_csv("/Users/yangyangxiayule/Documents/GitHub/COPD-Project/Datasets/lifestyle risk factors/SMOKING_AGE-ADJUSTED_PREVALENCE.csv")
smoke_crude = pd.read_csv("/Users/yangyangxiayule/Documents/GitHub/COPD-Project/Datasets/lifestyle risk factors/SMOKING_CRUDE_PREVALENCE.csv")

no_phyact_1821_age = pd.read_csv("/Users/yangyangxiayule/Documents/GitHub/COPD-Project/Datasets/lifestyle risk factors/NO_PHYSICAL_ACTIVITY_AGE-ADJUSTED.csv")
no_phyact_1821_crude = pd.read_csv("/Users/yangyangxiayule/Documents/GitHub/COPD-Project/Datasets/lifestyle risk factors/NO_PHYSICAL_ACTIVITYAGE_Crude.csv")

print(copd_age.columns.to_list())
copd_age.rename(columns={
    'Value': 'copd%_age',
    'Confidence Interval High': 'CI_high_copd_age',
    'Confidence Interval Low': 'CI_low_copd_age',
}, inplace=True)
copd_age.drop(columns=['Data Comment', '95% Confidence Interval'], inplace=True)
copd_age.dropna(axis=1, inplace=True)
copd_age.dropna(axis=0, inplace=True)
copd_age['State_County_Year'] = copd_age['State'] +copd_age['County'] + copd_age['Year'].astype(str)
copd_age['State_County'] = copd_age['State'] +copd_age['County']

copd_crude.rename(columns={
    'Value': 'copd%_crude',
    'Confidence Interval High': 'CI_high_copd_crude',
    'Confidence Interval Low': 'CI_low_copd_crude',
}, inplace=True)
copd_crude.drop(columns=['StateFIPS', 'CountyFIPS', 'Data Comment', '95% Confidence Interval'], inplace=True)
copd_crude.dropna(axis=1, inplace=True)
copd_crude.dropna(axis=0, inplace=True)
copd_crude['State_County_Year'] = copd_crude['State'] + copd_crude['County'] + copd_crude['Year'].astype(str)

print(copd_age.columns.to_list())
print(copd_crude.columns.to_list())

copd_joint = pd.merge(copd_age, copd_crude, how='left', on=['State_County_Year'])

copd_joint.rename(columns={
    'State_x': 'State',
    'Year_x': 'Year',
    'County_x': 'County'
}, inplace=True)
copd_joint.drop(columns=['State_y', 'County_y', 'Year_y'], inplace=True)
print(copd_joint.columns.to_list())
copd_joint.to_csv("/Users/yangyangxiayule/Documents/GitHub/COPD-Project/New CSV/copd_joint.csv", index=False)