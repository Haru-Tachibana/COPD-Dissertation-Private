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
#predict
aq22 = pd.read_csv("/Users/yangyangxiayule/Documents/GitHub/COPD-Project/Datasets/AQ_18-24_county/annual_aqi_by_county_2022.csv")
aq23 = pd.read_csv("/Users/yangyangxiayule/Documents/GitHub/COPD-Project/Datasets/AQ_18-24_county/annual_aqi_by_county_2023.csv")
aq24 = pd.read_csv("/Users/yangyangxiayule/Documents/GitHub/COPD-Project/Datasets/AQ_18-24_county/annual_aqi_by_county_2024.csv")

print(aq18.count())
print(aq19.count())
print(aq20.count())
print(aq21.count())


#18-19-20-21
aq18.rename(columns={
    'Days with AQI': 'AQI_records_18',
    'Good Days': 'Good_18',
    'Moderate Days': 'Moderate_18',
    'Unhealthy for Sensitive Groups Days': 'Unhealthy_sens_18',
    'Unhealthy Days': 'Unhealthy_18',
    'Very Unhealthy Days': 'Very_unhealthy_18',
    'Hazardous Days': 'Hazardous_18',
    'Max AQI': 'Max_AQI_18',
    '90th Percentile AQI': '90th_Percentile_AQI_18',
    'Median AQI': 'Median_AQI_18', 
    'Days CO': 'CO_18', 
    'Days NO2': 'NO2_18', 
    'Days Ozone': 'O3_18', 
    'Days PM2.5': 'PM2.5_18', 
    'Days PM10': 'PM10_18'
}, inplace=True)
aq18['State_County_Year'] = aq18['State'] + aq18['County'] + aq18['Year'].astype(str)
aq18.dropna(axis=1, inplace=True)
aq18.dropna(axis=0, inplace=True)
aq18.drop(columns=['State', 'County', 'Year'], inplace=True)
print(aq18.columns.to_list())
print(aq18.head())
aq18.to_csv("/Users/yangyangxiayule/Documents/GitHub/COPD-Project/New CSV/aq18.csv", index=False)

#2019
aq19.rename(columns={
    'Days with AQI': 'AQI_records_19',
    'Good Days': 'Good_19',
    'Moderate Days': 'Moderate_19',
    'Unhealthy for Sensitive Groups Days': 'Unhealthy_sens_19',
    'Unhealthy Days': 'Unhealthy_19',
    'Very Unhealthy Days': 'Very_unhealthy_19',
    'Hazardous Days': 'Hazardous_19',
    'Max AQI': 'Max_AQI_19',
    '90th Percentile AQI': '90th_Percentile_AQI_19',
    'Median AQI': 'Median_AQI_19', 
    'Days CO': 'CO_19', 
    'Days NO2': 'NO2_19', 
    'Days Ozone': 'O3_19', 
    'Days PM2.5': 'PM2.5_19', 
    'Days PM10': 'PM10_19'
}, inplace=True)
aq19['State_County_Year'] = aq19['State'] + aq19['County'] + aq19['Year'].astype(str)
aq19.dropna(axis=1, inplace=True)
aq19.dropna(axis=0, inplace=True)
aq19.drop(columns=['State', 'County', 'Year'], inplace=True)
print(aq19.columns.to_list())
print(aq19.head())
aq19.to_csv("/Users/yangyangxiayule/Documents/GitHub/COPD-Project/New CSV/aq19.csv", index=False)

#2020
aq20.rename(columns={
    'Days with AQI': 'AQI_records_20',
    'Good Days': 'Good_20',
    'Moderate Days': 'Moderate_20',
    'Unhealthy for Sensitive Groups Days': 'Unhealthy_sens_20',
    'Unhealthy Days': 'Unhealthy_20',
    'Very Unhealthy Days': 'Very_unhealthy_20',
    'Hazardous Days': 'Hazardous_20',
    'Max AQI': 'Max_AQI_20',
    '90th Percentile AQI': '90th_Percentile_AQI_20',
    'Median AQI': 'Median_AQI_20', 
    'Days CO': 'CO_20', 
    'Days NO2': 'NO2_20', 
    'Days Ozone': 'O3_20', 
    'Days PM2.5': 'PM2.5_20', 
    'Days PM10': 'PM10_20'
}, inplace=True)
aq20['State_County_Year'] = aq20['State'] + aq20['County'] + aq20['Year'].astype(str)
aq20.dropna(axis=1, inplace=True)
aq20.dropna(axis=0, inplace=True)
aq20.drop(columns=['State', 'County', 'Year'], inplace=True)
print(aq20.columns.to_list())
print(aq20.head())
aq20.to_csv("/Users/yangyangxiayule/Documents/GitHub/COPD-Project/New CSV/aq20.csv", index=False)

#2021
aq21.rename(columns={
    'Days with AQI': 'AQI_records_21',
    'Good Days': 'Good_21',
    'Moderate Days': 'Moderate_21',
    'Unhealthy for Sensitive Groups Days': 'Unhealthy_sens_21',
    'Unhealthy Days': 'Unhealthy_21',
    'Very Unhealthy Days': 'Very_unhealthy_21',
    'Hazardous Days': 'Hazardous_21',
    'Max AQI': 'Max_AQI_21',
    '90th Percentile AQI': '90th_Percentile_AQI_21',
    'Median AQI': 'Median_AQI_21', 
    'Days CO': 'CO_21', 
    'Days NO2': 'NO2_21', 
    'Days Ozone': 'O3_21', 
    'Days PM2.5': 'PM2.5_21', 
    'Days PM10': 'PM10_21'
}, inplace=True)
aq21['State_County_Year'] = aq21['State'] + aq21['County'] + aq21['Year'].astype(str)
aq21.dropna(axis=1, inplace=True)
aq21.dropna(axis=0, inplace=True)
aq21.drop(columns=['State', 'County', 'Year'], inplace=True)
print(aq21.columns.to_list())
print(aq21.head())
aq21.to_csv("/Users/yangyangxiayule/Documents/GitHub/COPD-Project/New CSV/aq21.csv", index=False)

#aq1819 = pd.merge(aq18, aq19, how='left', on=['State_County_Year'])
#print(aq1819.head())
#aq1819.to_csv("/Users/yangyangxiayule/Documents/GitHub/COPD-Project/New CSV/aq1819.csv", index=False)

#print(aq_joint_1821.head())
#print(aq_joint_1821.columns.to_list())

#aq_joint_1821.to_csv("/Users/yangyangxiayule/Documents/GitHub/COPD-Project/New CSV/aq_joint_1821.csv", index=False)