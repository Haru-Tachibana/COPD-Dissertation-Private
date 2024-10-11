#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

aq18 = pd.read_csv("/Users/yangyangxiayule/Documents/GitHub/COPD-Project/Datasets/AQ_18-24_county/annual_aqi_by_county_2018.csv")
aq19 = pd.read_csv("/Users/yangyangxiayule/Documents/GitHub/COPD-Project/Datasets/AQ_18-24_county/annual_aqi_by_county_2019.csv")
aq20 = pd.read_csv("/Users/yangyangxiayule/Documents/GitHub/COPD-Project/Datasets/AQ_18-24_county/annual_aqi_by_county_2020.csv")
aq21 = pd.read_csv("/Users/yangyangxiayule/Documents/GitHub/COPD-Project/Datasets/AQ_18-24_county/annual_aqi_by_county_2021.csv")
#predict
aq22 = pd.read_csv("/Users/yangyangxiayule/Documents/GitHub/COPD-Project/Datasets/AQ_18-24_county/annual_aqi_by_county_2022.csv")
aq23 = pd.read_csv("/Users/yangyangxiayule/Documents/GitHub/COPD-Project/Datasets/AQ_18-24_county/annual_aqi_by_county_2023.csv")
aq24 = pd.read_csv("/Users/yangyangxiayule/Documents/GitHub/COPD-Project/Datasets/AQ_18-24_county/annual_aqi_by_county_2024.csv")

#18-19-20-21
aq18['State_County_Year'] = aq18['State'] + aq18['County'] + aq18['Year'].astype(str)
aq18.dropna(axis=1, inplace=True)
aq18.dropna(axis=0, inplace=True)
aq18.drop(columns=['State', 'County', 'Year'], inplace=True)
print(aq18.columns.to_list())
print(aq18.head())
aq18.to_csv("/Users/yangyangxiayule/Documents/GitHub/COPD-Project/New CSV/aq18_new.csv", index=False)

#2019
aq19['State_County_Year'] = aq19['State'] + aq19['County'] + aq19['Year'].astype(str)
aq19.dropna(axis=1, inplace=True)
aq19.dropna(axis=0, inplace=True)
aq19.drop(columns=['State', 'County', 'Year'], inplace=True)
print(aq19.columns.to_list())
print(aq19.head())
aq19.to_csv("/Users/yangyangxiayule/Documents/GitHub/COPD-Project/New CSV/aq19_new.csv", index=False)

#2020
aq20['State_County_Year'] = aq20['State'] + aq20['County'] + aq20['Year'].astype(str)
aq20.dropna(axis=1, inplace=True)
aq20.dropna(axis=0, inplace=True)
aq20.drop(columns=['State', 'County', 'Year'], inplace=True)
print(aq20.columns.to_list())
print(aq20.head())
aq20.to_csv("/Users/yangyangxiayule/Documents/GitHub/COPD-Project/New CSV/aq20_new.csv", index=False)

#2021
aq21['State_County_Year'] = aq21['State'] + aq21['County'] + aq21['Year'].astype(str)
aq21.dropna(axis=1, inplace=True)
aq21.dropna(axis=0, inplace=True)
aq21.drop(columns=['State', 'County', 'Year'], inplace=True)
print(aq21.columns.to_list())
print(aq21.head())
aq21.to_csv("/Users/yangyangxiayule/Documents/GitHub/COPD-Project/New CSV/aq21_new.csv", index=False)

frames = [aq18, aq19, aq20, aq21]
all_aq_1821 = pd.concat(frames)
all_aq_1821['State_County_Year'] = all_aq_1821['State_County_Year'].str.lower()
all_aq_1821['State_County_Year'] = all_aq_1821['State_County_Year'].str.strip()

def remove_space(x):
    return(''.join(x.split()))

all_aq_1821['State_County_Year'] = all_aq_1821['State_County_Year'].astype(str).apply(lambda x: remove_space(x))


print(all_aq_1821.head())
all_aq_1821.to_csv("/Users/yangyangxiayule/Documents/GitHub/COPD-Project/New CSV/airqualitydata_18to21.csv", index=False)

#aq1819 = pd.merge(aq18, aq19, how='left', on=['State_County_Year'])
#print(aq1819.head())
#aq1819.to_csv("/Users/yangyangxiayule/Documents/GitHub/COPD-Project/New CSV/aq1819.csv", index=False)

#print(aq_joint_1821.head())
#print(aq_joint_1821.columns.to_list())

#aq_joint_1821.to_csv("/Users/yangyangxiayule/Documents/GitHub/COPD-Project/New CSV/aq_joint_1821.csv", index=False)