import pandas as pd

input_file = "original_doc.csv"

df = pd.read_csv(input_file)

df = df[~df['type'].str.contains("project", case=False, na=False)]

data_type = [
    "Villa (Huis)", "Woning (Huis)", "Appartement", "Serviceflat (Appartement)", "Herenhuis (Huis)",
    "Penthouse (Appartement)", "Hoekwoning (Huis)", "Rijwoning (Huis)", "Hoeve (Huis)", "Loft (Appartement)",
    "Arbeiderswoning (Huis)", "Eengezinswoning (Huis)", "Gemengd gebruik (Huis)", "Studio (Appartement)",
    "Duplex (Appartement)", "Studio met slaaphoek (Appartement)", "Herenwoning (Huis)",
    "Gelijkvloers app. (Appartement)", "Uitzonderlijke woning (Huis)", "Kasteel (Huis)", "Fermette (Huis)",
    "Vakantiewoning (Huis)", "Villa-landhuis (Huis)", "Appartementsgebouw (Appartement)", "Chalet (Huis)",
    "Bungalow (Huis)", "Triplex (Appartement)", "Andere (Huis)", "Bel-étage (Huis)", "Pastorijwoning (Huis)",
    "Assistentie-appartement (Appartement)", "Boerderij (Huis)", "Koppelwoning (Huis)", "Kangoeroewoning (Huis)",
    "Huis", "Burgerswoning (Huis)", "Cottage (Huis)", "Koppelvilla (Huis)", "Dakappartement (Appartement)",
    "Moderne villa (Huis)", "Wooncaravan (Huis)", "Buitenverblijf (Huis)", "Brusselshuis (Huis)", "Flat (Appartement)",
    "Kelder app (Appartement)", "Split-level (Huis)", "App. vrij beroep (Appartement)"
]


# Delete the "project" lines
df = df[~df['type'].str.contains("project", case=False, na=False)]

# Extract type (appartment ou house)
df['main_type'] = df['type'].str.extract(r'\((.*?)\)', expand=False)
df['main_type'] = df['main_type'].fillna(df['type'])  # si pas de parenthèses
df['main_type'] = df['main_type'].str.lower().replace({'huis': 'house', 'appartement': 'appartment'})

# Extract subtype
df['subtype'] = df['type'].str.extract(r'^(.*?)\s*\(.*?\)', expand=False)
df['subtype'] = df.apply(lambda row: None if row['subtype'] == row['type'] else row['subtype'], axis=1)

# Change column names
df = df.rename(columns={'type': 'original_type'})
df = df[['main_type', 'subtype', 'original_type']]

# Sauvegarder si besoin
# df.to_csv("fichier_nettoye.csv", index=False)


print(df)

