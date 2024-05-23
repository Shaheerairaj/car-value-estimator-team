import pandas as pd
from ydata_profiling import ProfileReport

def clean_data(df):
    df.drop(['tags'], axis=1, inplace=True)
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

    return df

def data_report(data):
    report_name = input('Please enter name of html report: ')

    # Generate the profile report
    profile = ProfileReport(data, title='Data Profiling Report')
    profile.to_file(f"reports/{report_name}.html")

def main():
    df = pd.read_csv('../data_private/ads_all.csv').drop(['ad_id','link'], axis=1)
    data_report(df)
    df = clean_data(df)
    data_report(df)
    df.to_csv('../data/ads_all_cleaned.csv', index=False)

if __name__== '__main__':
    main()