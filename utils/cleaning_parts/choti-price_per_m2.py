import pandas as pd
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.abspath(os.path.join(current_dir, '..', '..', 'data', 'cleaned_data.csv'))
postcode = os.path.abspath(os.path.join(current_dir, '..', '..', 'data', 'postal-codes-belgium.csv'))
df = pd.read_csv(file_path)
postcode_df = pd.read_csv(postcode, sep=';')

df["price_per_m2"] = df["price"]/df["habitableSurface"]

df = df.drop("url", axis='columns')
df = df.drop("id", axis='columns')
df = df.drop("Unnamed: 0", axis='columns')

df = df[~df['locality'].str.contains('CADZAND', na=False)]

df['postCode'] = df['postCode'].astype(str)
postcode_df['Postal Code'] = postcode_df['Postal Code'].astype(str)
postcode_df = postcode_df.rename(columns={'Postal Code': 'postCode'})
postcode_df = postcode_df.rename(columns={'Municipality name (French)': 'municipality'})
df = df.merge(postcode_df[['postCode', 'municipality']], on='postCode', how='left')


output_path = os.path.abspath(os.path.join(current_dir, '..', '..', 'data', 'cleaned_data_modified.csv'))
df.to_csv(output_path, index=False)


