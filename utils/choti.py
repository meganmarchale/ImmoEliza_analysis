import pandas as pd

filename = "./data/immoweb-dataset.csv"
df = pd.read_csv(filename)

#price 
df = df.dropna(subset=["price"])
print("total na in price:", df['price'].isna().sum())


#habitable surface
df = df.dropna(subset=["habitableSurface"])
print("total na in habitableSurface:", df['habitableSurface'].isna().sum())


#EPC
common_EPC_per_buildingCondition = df.groupby('buildingCondition')['epcScore'].agg(lambda x: x.mode())
print(common_EPC_per_buildingCondition)
df['epcScore'] = df['epcScore'].fillna(df['buildingCondition'].map(common_EPC_per_buildingCondition))
df['epcScore'] = df['epcScore'].fillna("unknown")
print("total na in epc:", df['epcScore'].isna().sum())


#buildingCondition fill with unknow
df['buildingCondition'] = df['buildingCondition'].fillna("unknown")


#drop floorCount, livingRoomSurface , floodZoneType 
df = df.drop("floorCount", axis='columns')
df = df.drop("livingRoomSurface", axis='columns')
df = df.drop("floodZoneType", axis='columns')


# toiletCount: if no info for bathroom + toilet : drop rows. 
no_info_bathroom_toilet = df[(df["toiletCount"].isna()) & (df["bathroomCount"].isna())]
no_info_bathroom_toilet_index = no_info_bathroom_toilet.index
print(no_info_bathroom_toilet[["toiletCount","bathroomCount"]])
df.drop(no_info_bathroom_toilet_index, inplace=True)

#If toilet count > 0 but no bathroom count — drop rows.

toilet_without_bathroom =df[(df["toiletCount"] > 0) & (df["bathroomCount"].isna())]
toilet_without_bathroom_index = toilet_without_bathroom.index
print(toilet_without_bathroom[["toiletCount","bathroomCount"]])
df.drop(toilet_without_bathroom_index, inplace=True)

# If missing toilet value ::assume that toilet in the bathroom — value = 0
df['toiletCount'] = df['toiletCount'].fillna(0)
print("total na in toiletCount:", df['toiletCount'].isna().sum())
print("total na in bathroomCount:", df['bathroomCount'].isna().sum())


print(f"There are {len(df)} rows of data")

df.to_csv("./data/cleaned_data.csv", index=False)