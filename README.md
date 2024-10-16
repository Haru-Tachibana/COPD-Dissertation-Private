# Content Description
## Datasets - original datasets downloaded from official websites
- Air quality data (2018-2024): Pre-generated data from EPA (United States Environmental Protection Agency).<https://aqs.epa.gov/aqsweb/airdata/download_files.html>
- Fine resolution AQ data: Air Quality System (AQS) API <https://aqs.epa.gov/aqsweb/documents/data_api.html>
- COPD data: National Environmental Public Health Tracking Network <https://ephtracking.cdc.gov/DataExplorer/>
- Demographic data: Census data from the Office for National Statistics. <https://www.ons.gov.uk/census>
- the StateFIPS for South Dakota is 46.

## New CSV - all data files (csv) generated from original datasets
- Note seperate AQ data is not being used at this stage.

## Data cleaning - Python code files for data cleaning & pre-processing
- Ignore AQ_cleaning_join copy.py and AQ_remane.py files. (wrong methods)

## EDA -  Python code files for exploratory data analysis
- EDA_COPD.py: national level ranking of COPD prevalence and annual trends.
- SouthDakota.py: State level.

## Figures - visualisation which can be used in dissertation

## Literature Summary - List of papers

## fetchData.js 
--> didn't work as expected, need further investigation. One niticed issue: missing data from API source (i.e., not every single county in the state have AQ data per qtr)
