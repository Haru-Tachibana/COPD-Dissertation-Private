import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
from sklearn.linear_model import LinearRegression

sns.set_theme()

def clean_percentage(x):
    if isinstance(x, str) and '%' in x:
        return float(x.strip('%'))
    return x

# Load and clean data
df = pd.read_csv('/Users/yangyangxiayule/Documents/GitHub/COPD-Project/final data/demographic_data.csv')
copd_df = pd.read_csv('/Users/yangyangxiayule/Documents/GitHub/COPD-Project/final data/copd_data.csv')
copd_df['copd%_age'] = copd_df['copd%_age'].apply(clean_percentage)
merged_df = pd.merge(df, copd_df, on=['County', 'Year'], how='left')

# Filter for 2018-2021
data = merged_df[merged_df['Year'].between(2018, 2021)].copy()

# Log transform income and healthcare data (to balance scale)
data['log_income'] = np.log(data['income'])
data['log_healthcare'] = np.log(data['healthcare'])

# Define variables
dependent_var = 'copd%_age'
independent_vars = {'log_income': 'Log Income', 'log_healthcare': 'Log Healthcare Access', 'smoking': 'Smoking Rate'}

# Store regression results
regression_results = []

# Generate separate regression plots
for ind_var, label in independent_vars.items():
    # Fit linear model
    X = data[[ind_var]]
    y = data[dependent_var]
    model = LinearRegression().fit(X, y)
    a = model.coef_[0]
    b = model.intercept_
    r_squared = model.score(X, y)
    correlation, p_value = stats.pearsonr(data[ind_var], data[dependent_var])
    
    # Save regression coefficients
    regression_results.append({'Variable': label, 
                               'Slope (a)': round(a, 3), 
                               'Intercept (b)': round(b, 3), 
                               'R²': round(r_squared, 3),
                               'Correlation': round(correlation, 3),
                               'P-value': p_value})
    
    # Plot
    plt.figure(figsize=(8, 6))
    sns.regplot(x=data[ind_var], y=data[dependent_var], scatter_kws={'alpha': 0.5}, line_kws={'color': 'red'})
    plt.title(f'{label} vs COPD Prevalence (2018 - 2021)')
    plt.xlabel(label)
    plt.ylabel('COPD Prevalence (%)')
    plt.text(min(data[ind_var]), max(data[dependent_var]) - 1, 
             f'COPD = {round(a, 3)} * {label} + {round(b, 3)}\n'
             f'R² = {round(r_squared, 3)}\n'
             f'Correlation = {round(correlation, 3)}\n'
             f'P-value = {p_value}', 
             fontsize=12, color='black', weight='bold', bbox=dict(facecolor='white', alpha=0.7))
    plt.show()

# Save regression coefficients as CSV
regression_df = pd.DataFrame(regression_results)
regression_df.to_csv('regression_results.csv', index=False)