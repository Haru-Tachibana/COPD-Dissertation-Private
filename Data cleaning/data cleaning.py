#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

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

copd_joint = pd.merge(copd_age, copd_crude, how='inner', on=['County', 'Year'])
copd_joint.to_csv("/Users/yangyangxiayule/Documents/GitHub/COPD-Project/New CSV/copd_joint.csv", index=False)
