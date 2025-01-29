import pandas as pd

# Load your data
data = pd.read_csv("/Users/yangyangxiayule/Documents/GitHub/COPD-Project/demographic data/merged_wv_counties_reordered.csv")

# Reshape the data from wide to long format
reshaped_data = pd.melt(data, 
                        id_vars=['County'], 
                        value_vars=[col for col in data.columns if 'income' in col or 'healthcare' in col or 'smoking' in col], 
                        var_name='Year_Variable', 
                        value_name='Value')

# Split the 'Year_Variable' into two columns: 'Year' and 'Variable'
reshaped_data[['Variable', 'Year']] = reshaped_data['Year_Variable'].str.split('_', expand=True)

# Convert 'Year' to integer for comparison purposes
reshaped_data['Year'] = reshaped_data['Year'].astype(int)

# Replace the rows with 'McDowell^' in the 'County' column
reshaped_data = reshaped_data[reshaped_data['County'] != 'McDowell^']
reshaped_data = reshaped_data[reshaped_data['County'] != 'West Virginia']

# Fill the missing values for McDowell county
reshaped_data.loc[(reshaped_data['County'] == 'McDowell') & (reshaped_data['Year'] == 2020) & (reshaped_data['Variable'] == 'smoking'), 'Value'] = 30.0
reshaped_data.loc[(reshaped_data['County'] == 'McDowell') & (reshaped_data['Year'] == 2022) & (reshaped_data['Variable'] == 'smoking'), 'Value'] = 34.0
reshaped_data.loc[(reshaped_data['County'] == 'McDowell') & (reshaped_data['Year'] == 2023) & (reshaped_data['Variable'] == 'smoking'), 'Value'] = 34.0

reshaped_data.loc[(reshaped_data['County'] == 'Clay') & (reshaped_data['Year'] == 2018) & (reshaped_data['Variable'] == 'healthcare'), 'Value'] = 90071.0
reshaped_data.loc[(reshaped_data['County'] == 'Clay') & (reshaped_data['Year'] == 2024) & (reshaped_data['Variable'] == 'healthcare'), 'Value'] = 82331.0

# Pivot the data so that we have columns for income, smoking, and healthcare
final_data = reshaped_data.pivot_table(index=['County', 'Year'], 
                                       columns='Variable', 
                                       values='Value', 
                                       aggfunc='first').reset_index()

# Set the output path
output_path = "/Users/yangyangxiayule/Documents/GitHub/COPD-Project/final data"

# Save the final data to a CSV file
final_data.to_csv(output_path + '/demographic_data.csv', index=False)