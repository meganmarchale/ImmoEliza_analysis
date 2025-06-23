import pandas as pd

# File paths
input_file = "/Users/meganmarchale/Documents/BeCode/Projects/ImmoEliza_analysis/data/immoweb-dataset.csv"



df = pd.read_csv(input_file)

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

