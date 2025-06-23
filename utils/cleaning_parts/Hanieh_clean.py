import pandas as pd

# Load your CSV file
df = pd.read_csv('./data/immoweb-dataset.csv')
#************************************************************************************************
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
# Drop 'hasLivingRoom' column
df.drop(['hasLivingRoom'], axis=1, inplace=True)






# Step 5: Save the cleaned dataframe to a new CSV
df.to_csv("./data/cleaned_data.csv", index=False)