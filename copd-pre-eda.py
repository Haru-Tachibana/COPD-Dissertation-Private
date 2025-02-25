import pandas as pd

pre = pd.read_csv('/Users/yangyangxiayule/Documents/GitHub/COPD-Project/copd_predictions_2022_2024.csv')

county_stat = pre.groupby('County')['predicted_copd_age'].describe()

pre_2022 = pre[pre['Year'] == 2022]
pre_2023 = pre[pre['Year'] == 2023]
pre_2024 = pre[pre['Year'] == 2024]

sort_22 = pre_2022.sort_values(by='predicted_copd_age', ascending=False)
re_22 = sort_22.head(10)
print(re_22)

sort_23 = pre_2023.sort_values(by='predicted_copd_age', ascending=False)
re_23 = sort_23.head(10)
print(re_23)

sort_24 = pre_2024.sort_values(by='predicted_copd_age', ascending=False)
re_24 = sort_24.head(10)
print(re_24)