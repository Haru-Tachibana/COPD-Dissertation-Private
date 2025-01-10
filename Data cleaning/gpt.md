Here’s a collection of Python snippets and tools to help you fetch and preprocess the datasets on macOS. We'll use popular libraries such as `pandas`, `numpy`, `requests`, and GIS tools like `geopandas` for spatial data. Each snippet addresses a specific dataset type.

---

### **1. Fetching COPD Prevalence Data (CDC BRFSS)**
The CDC BRFSS data is usually available as CSV files.

```python
import pandas as pd

# Load COPD prevalence data from a local file or URL
url = "https://www.cdc.gov/brfss/data_documentation/index.htm"  # Replace with exact dataset URL
local_file = "/path/to/copd_data.csv"  # Replace with your local file path
copd_data = pd.read_csv(local_file)  # Or use url instead of local_file

# Preview data
print(copd_data.head())

# Save processed data
copd_data.to_csv("processed_copd_data.csv", index=False)
```

---

### **2. Fetching Air Quality Data (EPA AQS API)**

#### Install `requests` and `json` for API interaction:
```bash
pip install requests
```

#### Fetch air quality data:
```python
import requests
import pandas as pd

# API endpoint and parameters
base_url = "https://aqs.epa.gov/data/api/dailyData/byCounty"
params = {
    "email": "your_email@example.com",  # Register with the EPA API
    "key": "your_api_key",  # Replace with your API key
    "param": "44201",  # Example: Ozone (replace with desired pollutant code)
    "bdate": "20210101",  # Start date
    "edate": "20211231",  # End date
    "state": "54",  # State code for WV
    "county": "003"  # County code (example: Berkeley County)
}

response = requests.get(base_url, params=params)
data = response.json()

# Convert JSON to DataFrame
if "Data" in data:
    air_quality_df = pd.DataFrame(data["Data"])
    print(air_quality_df.head())
else:
    print("Error fetching data:", data)
```

---

### **3. COVID-19 Data (NYT GitHub Repository)**
NYT provides daily updated CSV files on GitHub.

```python
# Fetch COVID-19 dataset directly from NYT GitHub repository
url = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv"
covid_data = pd.read_csv(url)

# Filter for West Virginia
covid_wv = covid_data[covid_data['state'] == "West Virginia"]

# Save processed data
covid_wv.to_csv("covid_wv_data.csv", index=False)
```

---

### **4. Socioeconomic and Demographic Data (ACS API)**

#### Install `census` library for API access:
```bash
pip install census
```

#### Fetch ACS data:
```python
from census import Census

# Census API key (register at https://api.census.gov/)
API_KEY = "your_api_key"

# Fetch data
c = Census(API_KEY)
acs_data = c.acs5.state_county(('NAME', 'B01003_001E'), 54, "*")  # 54 is WV state code
acs_df = pd.DataFrame(acs_data)

# Rename columns
acs_df.rename(columns={'B01003_001E': 'Population'}, inplace=True)
print(acs_df.head())
```

---

### **5. Geographic Data (TIGER/Line Shapefiles)**

#### Install `geopandas` for spatial data handling:
```bash
pip install geopandas
```

#### Load TIGER/Line shapefiles:
```python
import geopandas as gpd

# Load shapefile
shapefile_path = "/path/to/tiger_shapefile.shp"  # Replace with your shapefile path
geo_data = gpd.read_file(shapefile_path)

# Plot the map
geo_data.plot()
```

---

### **6. Combining Data for Analysis**
Merge datasets by matching geographic identifiers such as FIPS codes.

```python
# Merge air quality data and COVID data on FIPS codes
merged_data = pd.merge(covid_wv, air_quality_df, on="fips", how="inner")
print(merged_data.head())

# Save merged dataset
merged_data.to_csv("merged_wv_data.csv", index=False)
```

---

### **7. Predictive Modeling (Random Forest Example)**
Use `scikit-learn` to build a model predicting COPD prevalence.

#### Install `scikit-learn`:
```bash
pip install scikit-learn
```

#### Random Forest Model:
```python
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

# Example dataset
features = merged_data[['PM2.5', 'O3', 'covid_cases']].dropna()
target = merged_data['COPD_Prevalence']

# Split data
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

# Train model
model = RandomForestRegressor()
model.fit(X_train, y_train)

# Evaluate model
predictions = model.predict(X_test)
mse = mean_squared_error(y_test, predictions)
print(f"Mean Squared Error: {mse}")
```

---

Let me know if you need help automating data fetching or further Python code for your analysis!