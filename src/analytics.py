import pandas as pd
import sqlite3
import numpy as np

# Step 1: Load the data from the Excel file
file_path = '../data/analytical_engineering_data.xlsx'

# Verify that the file exists at the specified path
try:
    excel_file = pd.ExcelFile(file_path)
    print("Available sheet names:", excel_file.sheet_names)
except FileNotFoundError:
    print(f"The file at path {file_path} was not found.")
    exit(1)

# Verify the sheet names
sheet_names = excel_file.sheet_names
print(f"Sheet names in the Excel file: {sheet_names}")

# Load the data if the sheets exist
required_sheets = ['Data', 'Cover', 'Use', 'Entitlement', 'Garaged']
missing_sheets = [sheet for sheet in required_sheets if sheet not in sheet_names]

if missing_sheets:
    print(f"The following required sheets are missing: {missing_sheets}")
    exit(1)

policies_df = pd.read_excel(file_path, sheet_name='Data')
cover_df = pd.read_excel(file_path, sheet_name='Cover')
use_df = pd.read_excel(file_path, sheet_name='Use')
entitlement_df = pd.read_excel(file_path, sheet_name='Entitlement')
garaged_df = pd.read_excel(file_path, sheet_name='Garaged')

# Step 2: Define the mapping dictionaries from the dataframes
cover_dict = dict(zip(cover_df['Value in Data'], cover_df['Description']))
use_dict = dict(zip(use_df['Value in Data'], use_df['Description']))
entitlement_dict = dict(zip(entitlement_df['Value in Data'], entitlement_df['Description']))
garaged_dict = dict(zip(garaged_df['Value in Data'], garaged_df['Description']))

# Step 3: Replace raw values with human-readable equivalents
policies_df['cover'] = policies_df['cover'].map(cover_dict)
policies_df['vehicle_use'] = policies_df['vehicle_use'].map(use_dict)
policies_df['entitlement'] = policies_df['entitlement'].map(entitlement_dict)
policies_df['overnight_location'] = policies_df['overnight_location'].map(garaged_dict)

# Step 4: Calculate the number of years a customer has held their licence
policies_df['licence_test_date'] = pd.to_datetime(policies_df['licence_test_date'], errors='coerce')
policies_df['start_date'] = pd.to_datetime(policies_df['start_date'], errors='coerce')

policies_df['years_held_licence'] = (policies_df['start_date'] - policies_df['licence_test_date']).dt.days / 365.25

# Handle negative values and round off to 2 decimal places
policies_df['years_held_licence'] = policies_df['years_held_licence'].apply(lambda x: max(x, 0)).round(2)

# Step 5: Round vehicle value to the nearest 1000
policies_df['vehicle_value'] = policies_df['vehicle_value'].apply(pd.to_numeric, errors='coerce').fillna(0)
policies_df['rounded_vehicle_value'] = policies_df['vehicle_value'].round(-3)

# Save the transformed data to a new CSV file
policies_df.to_csv('transformed_policies.csv', index=False)

#Display a sample of the transformed data
print(policies_df.head())


# Load the transformed data
policies_df = pd.read_csv('transformed_policies.csv')

# Save the data to an SQLite database
conn = sqlite3.connect('policies.db')
policies_df.to_sql('policies', conn, if_exists='replace', index=False)
conn.close()