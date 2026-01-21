# Describe project here

import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

from config import DATA_FOLDER, INTERVAL_HOURS
folder_path = DATA_FOLDER
interval_hours = INTERVAL_HOURS

# file path
#file_path = "20221108/20221030.parquet"

# see what is in files
#df = pd.read_parquet(file_path)
#print(df.columns)

# folder path
folder_path = Path("20221108")

# list all parquet files in folder_path
parquet_files = list(folder_path.glob("*.parquet"))

dfs = []
for file in parquet_files:
    print(f"Loading {file}...")
    df = pd.read_parquet(file)
    # add column to know which file the row came from
    df['source_file'] = file.name
    
    dfs.append(df)

# combine files into one big df
combined_df = pd.concat(dfs, ignore_index=True)

# drop the empty column
combined_df = combined_df.drop(columns=['Unnamed: 2812'])

# confirm shape
print("Combined DataFrame shape:", combined_df.shape)
#print("Columns:", combined_df.columns)

print(combined_df.head())
print(combined_df.tail())
print(combined_df['source_file'].value_counts())

##### explore data #####
# summary stats for BESS SOC and active power
metrics = ['BESS SOC (%) [BESS]', 'BESS active power (kW) [BESS]']

# Overall summary
print("=== Overall Summary ===")
print(combined_df[metrics].describe())

# Summary per file
print("\n=== Summary per source file ===")
per_file_summary = combined_df.groupby('source_file')[metrics].describe()
print(per_file_summary)

# For a quick time axis, just use row number
combined_df['row_number'] = combined_df.index

# Plot BESS SOC
plt.figure(figsize=(12, 5))
for file in combined_df['source_file'].unique():
    subset = combined_df[combined_df['source_file'] == file]
    plt.plot(subset['row_number'], subset['BESS SOC (%) [BESS]'], label=file)
plt.title("BESS SOC (%) Over Time")
plt.xlabel("Row Number (proxy for time)")
plt.ylabel("SOC (%)")
plt.legend()
plt.show()

# Plot BESS Active Power
plt.figure(figsize=(12, 5))
for file in combined_df['source_file'].unique():
    subset = combined_df[combined_df['source_file'] == file]
    plt.plot(subset['row_number'], subset['BESS active power (kW) [BESS]'], label=file)
plt.title("BESS Active Power (kW) Over Time")
plt.xlabel("Row Number (proxy for time)")
plt.ylabel("Active Power (kW)")
plt.legend()
plt.show()


