import pandas as pd

df = pd.read_csv('../data/ads_all.csv').drop(['ad_id','link'], axis=1)

print('Columns: ', df.columns)
print(df)