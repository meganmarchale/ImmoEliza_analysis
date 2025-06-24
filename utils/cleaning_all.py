import pandas as pd

# File paths
input_file = "./data/immoweb-dataset.csv"

df = pd.read_csv(input_file)

"""CHOTI'S"""
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

"""HANIEH'S"""
# Calculate percentage of missing values per column
missing_percent = df.isnull().mean() * 100
print(f'number of featuers: {len(df.columns)}')
print(missing_percent)
# print(sorted(missing_percent))

# Identify columns to drop (more than 80% missing)
exceptions = ['hasSwimmingPool', 'hasGarden', 'gardenSurface']
cols_to_drop = [col for col in missing_percent.index 
                if missing_percent[col] > 80 and col not in exceptions]
print(f'number of dropping featuers: {len(cols_to_drop)}')
# Drop those columns
df = df.drop(columns=cols_to_drop)
print(len(df.columns))
#************************************************************************************************
# Replace missing values with True_False (kitchenSurface and kitchenType)
df['kitchenSurface'].fillna(0, inplace=True)
df['kitchenType'].fillna('Not installed', inplace=True)
# Create the 'kitchen_installed' column
df['kitchen_installed'] = ~(
    (df['kitchenSurface'] == 0) & (df['kitchenType'] == 'Not installed'))
# (optional): Drop the original columns
df.drop(['kitchenSurface', 'kitchenType'], axis=1, inplace=True)
#************************************************************************************************
# Fill missing items with 0, 'False', 'missing' and 'unknown' value
df['terraceSurface'].fillna(0, inplace=True)
df['hasTerrace'].fillna(False, inplace=True)
df['parkingCountOutdoor'].fillna(0, inplace=True)
df['parkingCountIndoor'].fillna(0, inplace=True)
df['hasLift'].fillna('False', inplace=True)
df['hasSwimmingPool'].fillna('False', inplace=True)
df['bedroomCount'].fillna('missing', inplace=True)
df['hasBasement'].fillna('False', inplace=True)
#************************************************************************************************
# Compute percentiles on non-zero terrace surfaces
non_zero_terraces = df[df['terraceSurface'] > 0]['terraceSurface']
q33 = non_zero_terraces.quantile(0.33)
q66 = non_zero_terraces.quantile(0.66)
# Define function to categorize terrace size
def categorize_terrace(row):
    if not row['hasTerrace'] or row['terraceSurface'] == 0:
        return 'No terrace'
    elif row['terraceSurface'] <= q33:
        return 'Small'
    elif row['terraceSurface'] <= q66:
        return 'Medium'
    else:
        return 'Big'

# Apply function to create new column
df['terraceSurface'] = df.apply(categorize_terrace, axis=1)

df.drop(['hasTerrace'], axis=1, inplace=True)
#************************************************************************************************
# Only run this if 'hasGarden' and 'gardenSurface' exist in the dataframe
if 'hasGarden' in df.columns and 'gardenSurface' in df.columns:
    # Define function to categorize garden surface
    def categorize_garden(row):
        if not row['hasGarden'] or row['gardenSurface'] == 0:
            return 'No garden'
        else:
            return row['gardenSurface']

    # Apply function
    df['gardenSurface'] = df.apply(categorize_garden, axis=1)

    # Drop 'hasGarden' column
    df.drop(['hasGarden'], axis=1, inplace=True)
else:
    print("Missing 'hasGarden' or 'gardenSurface' column in the dataframe.")
# Check for terraceSurface
if 'gardenSurface' in df.columns:
    print(df['gardenSurface'])
else:
    print("'gardenSurface' column not found.")

df['gardenSurface'].fillna('missing', inplace=True)
#************************************************************************************************
# Drop 'roomCount' column
df.drop(['roomCount'], axis=1, inplace=True)
df.drop(['streetFacadeWidth'], axis=1, inplace=True)
df.drop(['hasVisiophone'], axis=1, inplace=True)
# Drop 'hasLivingRoom' column
df.drop(['hasLivingRoom'], axis=1, inplace=True)

"""KLEBS"""

def buildingConstructionYear():
    df['buildingConstructionYear'] = df['buildingConstructionYear'].fillna('missing')
buildingConstructionYear()

def hasBasement():
    df['hasBasement'] = df['hasBasement'].fillna(False) # replace empty strings with None
hasBasement()



"""MEGAN'S"""
def get_region(province):
    if province in ["East Flanders", "Flemish Brabant", "Limburg", "West Flanders", "Antwerp"]:
        return "Flanders"
    elif province == "Brussels":
        return "Brussels"
    else:
        return "Wallonia"

df["region"] = df["province"].apply(get_region)

#print(df[["province", "region"]].head())


def facade_count():
    df["facedeCount"] = df["facedeCount"].fillna(0)
    df.loc[df["facedeCount"] > 4, "facedeCount"] = 0
    return df["facedeCount"]

facade_count()
#print(df["facedeCount"].head())

def land_surface():
    df.loc[df["type"].isin(["APARTMENT", "APARTMENT_GROUP"]), "landSurface"] = 0
    df.dropna(subset=["landSurface"], inplace=True)

land_surface()
#print(df["landSurface"].head())

def heating_type():
    df["heatingType"] = df["heatingType"].fillna("unknown")

heating_type()
#print(df["heatingType"].head)


df.to_csv("./data/cleaned_data.csv", index=False)

