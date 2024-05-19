import pandas as pd
from ydata_profiling import ProfileReport

df = pd.read_csv('../data/ads_all.csv').drop(['ad_id','link'], axis=1)

# Generate the profile report
profile = ProfileReport(df, title='Data Profiling Report')
profile.to_file("reports/ads_all_before_cleaning.html")

# Cleaning the data
df.drop(['id','tags'], axis=1, inplace=True)
df.dropna(axis=0, how='all',inplace=True)
df['price'] = df['price'].str.replace(',','').astype(float)
df['km'] = df['km'].str.replace(' km','').str.replace(',','').astype(float)

# Dictionary for location mapping
location_mapping = {
    'Dubai': 'Dubai',
    'Abu Dhabi': 'Abu Dhabi',
    'Sharjah': 'Sharjah',
    'Fujeirah': 'Fujeirah',
    'Al Ain': 'Al Ain',
    'Ras Al Khaimah': 'Ras Al Khaimah',
    'Ajman':'Ajman',
    'Umm Al Qawain':'Umm Al Qawain'
}

# Function to rename locations
def rename_location(location):
    if pd.isna(location):
        return 'other'
    for key in location_mapping:
        if key in location:
            return location_mapping[key]
    return 'other'

# Apply the function to the 'location' column
df['location_cleaned'] = df['location'].apply(rename_location)

# Generate the profile report
profile = ProfileReport(df, title='Data Profiling Report')
profile.to_file("reports/ads_all_after_cleaning.html")