import pandas as pd
import os

def clean_data_in_csv(input_file):
    """
    Clean a CSV file by:
    1. Removing leading/trailing spaces from all string values.
    2. Removing duplicate rows.
    3. Removing rows with empty values.
    4. Saving the cleaned data as input_filename_clean.csv
    
    Parameters:
        input_file (str): The path to the input CSV file.

    Returns:
        None
    """
    # Load the CSV file
    df = pd.read_csv(input_file)

    # Strip leading/trailing spaces from all string cells
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    # Drop duplicate rows
    df = df.drop_duplicates()

    # Drop rows with any empty (NaN or empty string) values
    df = df.replace('', pd.NA).dropna()

    # Generate output filename
    fileName, _csv = os.path.splitext(input_file)
    output_file = f"{fileName}_clean{_csv}"

    # Save cleaned data
    df.to_csv(output_file, index=False)
    print(f"Cleaned data saved to: {output_file}")

# Example usage
clean_data_in_csv("properties06191148_modified.csv")
