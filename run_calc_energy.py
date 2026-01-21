import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

from calc_energy import calculate_daily_energy


# -----------------------------
# 1. Load parquet files
# -----------------------------
data_folder = Path("20221108")
parquet_files = list(data_folder.glob("*.parquet"))

dfs = []
for f in parquet_files:
    df = pd.read_parquet(f)
    df["source_file"] = f.stem  # use date only, no extension
    dfs.append(df)

combined_df = pd.concat(dfs, ignore_index=True)

print(f"Combined DataFrame shape: {combined_df.shape}")


# -----------------------------
# 2. Identify DC input columns
# -----------------------------
dc_columns = [
    col for col in combined_df.columns
    if "DC Input Power (kW)" in col
]

print(f"Found DC input columns: {len(dc_columns)}")
print(dc_columns[:10])


# -----------------------------
# 3. Calculate daily energy
# -----------------------------
daily_energy = calculate_daily_energy(
    combined_df,
    dc_columns,
    file_column="source_file"
)

print("Daily energy calculation complete.")
print(daily_energy.head())


# -----------------------------
# 4. Heatmap: discharged energy (grouped by inverter)
# -----------------------------
# Extract discharged energy only
discharged = daily_energy.xs("discharged_kWh", level=1, axis=1)

# Rename columns to inverter names only
def extract_inverter(col_name):
    return col_name.split("[")[-1].replace("]", "")

discharged.columns = [extract_inverter(c) for c in discharged.columns]

# Group DC inputs belonging to the same inverter
discharged_grouped = discharged.groupby(axis=1, level=0).sum()

plt.figure(figsize=(14, 6))
ax = sns.heatmap(
    discharged_grouped,
    cmap="viridis",
    linewidths=0.3,
    cbar_kws={"label": "Energy Discharged (kWh)"}
)


plt.title("Daily Energy Discharged by BESS Inverter (kWh)")
plt.xlabel("Battery Inverter")
plt.ylabel("Date")
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()


# -----------------------------
# 5. Outlier table (lowest energy)
# -----------------------------
total_charged = daily_energy.xs("charged_kWh", level=1, axis=1).sum()
total_discharged = daily_energy.xs("discharged_kWh", level=1, axis=1).sum()

outliers = pd.DataFrame({
    "total_charged_kWh": total_charged,
    "total_discharged_kWh": total_discharged
})

lowest_charged = outliers.sort_values("total_charged_kWh").head(5)
lowest_discharged = outliers.sort_values("total_discharged_kWh").head(5)

print("\nTop 5 BESS enclosures with lowest charged energy:")
print(lowest_charged)

print("\nTop 5 BESS enclosures with lowest discharged energy:")
print(lowest_discharged)

