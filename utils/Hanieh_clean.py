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
df_cleaned = df.drop(columns=cols_to_drop)
print(len(df_cleaned.columns))
#************************************************************************************************
# Replace missing values with True_False (kitchenSurface and kitchenType)
df_cleaned['kitchenSurface'].fillna(0, inplace=True)
df_cleaned['kitchenType'].fillna('Not installed', inplace=True)
# Create the 'kitchen_installed' column
df_cleaned['kitchen_installed'] = ~(
    (df_cleaned['kitchenSurface'] == 0) & (df_cleaned['kitchenType'] == 'Not installed'))
# (optional): Drop the original columns
df_cleaned.drop(['kitchenSurface', 'kitchenType'], axis=1, inplace=True)
#************************************************************************************************
# Fill missing items with 0, 'False', 'missing' and 'unknown' value
df_cleaned['terraceSurface'].fillna(0, inplace=True)
df_cleaned['hasTerrace'].fillna(False, inplace=True)
df_cleaned['parkingCountOutdoor'].fillna(0, inplace=True)
df_cleaned['parkingCountIndoor'].fillna(0, inplace=True)
df_cleaned['hasLift'].fillna('False', inplace=True)
df_cleaned['hasSwimmingPool'].fillna('False', inplace=True)
df_cleaned['bedroomCount'].fillna('missing', inplace=True)
df_cleaned['hasBasement'].fillna('False', inplace=True)
#************************************************************************************************
# Compute percentiles on non-zero terrace surfaces
non_zero_terraces = df_cleaned[df_cleaned['terraceSurface'] > 0]['terraceSurface']
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
df_cleaned['terraceSurface'] = df.apply(categorize_terrace, axis=1)

df_cleaned.drop(['hasTerrace'], axis=1, inplace=True)
#************************************************************************************************
# Only run this if 'hasGarden' and 'gardenSurface' exist in the dataframe
if 'hasGarden' in df_cleaned.columns and 'gardenSurface' in df_cleaned.columns:
    # Define function to categorize garden surface
    def categorize_garden(row):
        if not row['hasGarden'] or row['gardenSurface'] == 0:
            return 'No garden'
        else:
            return row['gardenSurface']

    # Apply function
    df_cleaned['gardenSurface'] = df_cleaned.apply(categorize_garden, axis=1)

    # Drop 'hasGarden' column
    df_cleaned.drop(['hasGarden'], axis=1, inplace=True)
else:
    print("Missing 'hasGarden' or 'gardenSurface' column in the dataframe.")
# Check for terraceSurface
if 'gardenSurface' in df_cleaned.columns:
    print(df_cleaned['gardenSurface'])
else:
    print("'gardenSurface' column not found.")

df_cleaned['gardenSurface'].fillna('missing', inplace=True)
#************************************************************************************************
# Drop 'roomCount' column
df_cleaned.drop(['roomCount'], axis=1, inplace=True)
# Drop 'hasLivingRoom' column
df_cleaned.drop(['hasLivingRoom'], axis=1, inplace=True)






# Step 5: Save the cleaned dataframe to a new CSV
df.to_csv("./data/cleaned_data.csv", index=False)