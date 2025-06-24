import pandas as pd

# File paths
input_file = "./data/cleaned_data.csv"

df = pd.read_csv(input_file)

df["price_per_m2"] = df["price"]/df["habitableSurface"]

df.to_csv("./data/cleaned_data_modified.csv", index=False)