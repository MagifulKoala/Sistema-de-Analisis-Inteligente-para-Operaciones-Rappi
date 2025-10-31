# module for data cleaning

#%% 
import pandas as pd
import numpy as np


#%% Load datasets
print("=" * 80)
print("LOADING DATASETS")
print("=" * 80)

#raw file path
# orders_file_path = r"raw_data\Rappi - Dummy Data - RAW_ORDERS.csv"
# metrics_file_path = r"raw_data\Rappi - Dummy Data - RAW_INPUT_METRICS.csv"

#clean file paths
orders_file_path = r"clean_data\Rappi - Dummy Data - RAW_ORDERS.csv"
metrics_file_path = r"clean_data\Rappi - Dummy Data - RAW_INPUT_METRICS.csv"

# Load the CSV files
df_orders = pd.read_csv(orders_file_path)
df_metrics = pd.read_csv(metrics_file_path)

# %%
print(f"Loaded RAW_ORDERS: {df_orders.shape[0]} rows × {df_orders.shape[1]} columns")
print(f"Loaded RAW_INPUT_METRICS: {df_metrics.shape[0]} rows × {df_metrics.shape[1]} columns")

#%% Preview RAW_ORDERS dataset
print("\n" + "=" * 80)
print("RAW_ORDERS DATASET - EXPLORATORY ANALYSIS")
print("=" * 80)

print("\n1. FIRST FEW ROWS:")
print(df_orders.head())

print("\n2. DATASET INFO:")
print(df_orders.info())

print("\n3. DATA TYPES:")
print(df_orders.dtypes)

print("\n4. DESCRIPTIVE STATISTICS:")
print(df_orders.describe())

print("\n5. NULL VALUES:")
null_counts = df_orders.isnull().sum()
null_pct = (df_orders.isnull().sum() / len(df_orders)) * 100
null_summary = pd.DataFrame({
    'Null Count': null_counts,
    'Null %': null_pct
})
print(null_summary[null_summary['Null Count'] > 0])

print("\n6. UNIQUE VALUES PER COLUMN:")
for col in df_orders.columns:
    unique_count = df_orders[col].nunique()
    print(f"  {col}: {unique_count} unique values")

print("\n7. CATEGORICAL COLUMNS - VALUE COUNTS:")
categorical_cols = df_orders.select_dtypes(include=['object']).columns
for col in categorical_cols:
    print(f"\n  {col}:")
    print(df_orders[col].value_counts().head(10))

print("\n8. NUMERIC COLUMNS - RANGES:")
numeric_cols = df_orders.select_dtypes(include=[np.number]).columns
for col in numeric_cols:
    print(f"  {col}: Min={df_orders[col].min()}, Max={df_orders[col].max()}")


#%% Preview RAW_INPUT_METRICS dataset
print("\n" + "=" * 80)
print("RAW_INPUT_METRICS DATASET - EXPLORATORY ANALYSIS")
print("=" * 80)

print("\n1. FIRST FEW ROWS:")
print(df_metrics.head())

print("\n2. DATASET INFO:")
print(df_metrics.info())

print("\n3. DATA TYPES:")
print(df_metrics.dtypes)

print("\n4. DESCRIPTIVE STATISTICS:")
print(df_metrics.describe())

print("\n5. NULL VALUES:")
null_counts_m = df_metrics.isnull().sum()
null_pct_m = (df_metrics.isnull().sum() / len(df_metrics)) * 100
null_summary_m = pd.DataFrame({
    'Null Count': null_counts_m,
    'Null %': null_pct_m
})
print(null_summary_m[null_summary_m['Null Count'] > 0])

print("\n6. UNIQUE VALUES PER COLUMN:")
for col in df_metrics.columns:
    unique_count = df_metrics[col].nunique()
    print(f"  {col}: {unique_count} unique values")

print("\n7. CATEGORICAL COLUMNS - VALUE COUNTS:")
categorical_cols_m = df_metrics.select_dtypes(include=['object']).columns
for col in categorical_cols_m:
    print(f"\n  {col}:")
    print(df_metrics[col].value_counts().head(10))

print("\n8. NUMERIC COLUMNS - RANGES:")
numeric_cols_m = df_metrics.select_dtypes(include=[np.number]).columns
for col in numeric_cols_m:
    print(f"  {col}: Min={df_metrics[col].min()}, Max={df_metrics[col].max()}")

print("\n" + "=" * 80)
print("EXPLORATORY ANALYSIS COMPLETE")
print("=" * 80)

# ***************************************************************************************
# **********************    DATA CLEANING         ***************************************
# ***************************************************************************************

#%% DATA CLEANING - RAW_ORDERS
print("\n" + "=" * 80)
print("DATA CLEANING - RAW_ORDERS")
print("=" * 80)

# Convert object columns to string type
print("\n1. CONVERTING COLUMNS TO STRING TYPE:")
columns_to_convert = ['COUNTRY', 'CITY', 'ZONE', 'METRIC']
for col in columns_to_convert:
    df_orders[col] = df_orders[col].astype(str)
    print(f"{col}: {df_orders[col].dtype}")

# Replace null values with 0 in numeric columns (L8W through L0W)
print("\n2. REPLACING NULL VALUES WITH 0 IN NUMERIC COLUMNS:")
numeric_week_columns = ['L8W', 'L7W', 'L6W', 'L5W', 'L4W', 'L3W', 'L2W', 'L1W', 'L0W']

print("\n  Before:")
for col in numeric_week_columns:
    null_count = df_orders[col].isnull().sum()
    print(f"    {col}: {null_count} null values")

df_orders[numeric_week_columns] = df_orders[numeric_week_columns].fillna(0)

print("\n  After:")
for col in numeric_week_columns:
    null_count = df_orders[col].isnull().sum()
    print(f"    {col}: {null_count} null values")

print("\n3. CLEANED DATASET INFO:")
print(df_orders.info())

print("\n4. VERIFICATION - NULL VALUES IN ENTIRE DATASET:")
total_nulls = df_orders.isnull().sum().sum()
print(f"  Total null values remaining: {total_nulls}")

print("\n" + "=" * 80)
print("DATA CLEANING COMPLETE")
print("=" * 80)

#%% DATA CLEANING - RAW_INPUT_METRICS
print("\n" + "=" * 80)
print("DATA CLEANING - RAW_INPUT_METRICS")
print("=" * 80)

# Convert object columns to string type
print("\n1. CONVERTING COLUMNS TO STRING TYPE:")
columns_to_convert_metrics = ['COUNTRY', 'CITY', 'ZONE', 'ZONE_TYPE', 'ZONE_PRIORITIZATION', 'METRIC']
for col in columns_to_convert_metrics:
    df_metrics[col] = df_metrics[col].astype(str)
    print(f"  ✓ {col}: {df_metrics[col].dtype}")

# Replace null values with 0 in numeric roll columns
print("\n2. REPLACING NULL VALUES WITH 0 IN NUMERIC COLUMNS:")
numeric_roll_columns = ['L8W_ROLL', 'L7W_ROLL', 'L6W_ROLL', 'L5W_ROLL', 'L4W_ROLL', 'L3W_ROLL', 'L2W_ROLL', 'L1W_ROLL']

print("\n  Before:")
for col in numeric_roll_columns:
    null_count = df_metrics[col].isnull().sum()
    null_pct = (null_count / len(df_metrics)) * 100
    print(f"    {col}: {null_count} null values ({null_pct:.2f}%)")

df_metrics[numeric_roll_columns] = df_metrics[numeric_roll_columns].fillna(0)

print("\n  After:")
for col in numeric_roll_columns:
    null_count = df_metrics[col].isnull().sum()
    print(f"    {col}: {null_count} null values")

print("\n3. CLEANED DATASET INFO:")
print(df_metrics.info())

print("\n4. VERIFICATION - NULL VALUES IN ENTIRE DATASET:")
total_nulls_metrics = df_metrics.isnull().sum().sum()
print(f"  Total null values remaining: {total_nulls_metrics}")

print("\n" + "=" * 80)
print("DATA CLEANING - RAW_INPUT_METRICS COMPLETE")
print("=" * 80)


#%% SAVE CLEANED DATA
print("\n" + "=" * 80)
print("SAVING CLEANED DATASETS")
print("=" * 80)

# Save cleaned orders dataset
output_path_orders = 'clean_data/Rappi - Dummy Data - RAW_ORDERS.csv'
df_orders.to_csv(output_path_orders, index=False)
print(f"\nSaved cleaned RAW_ORDERS to: {output_path_orders}")
print(f"Shape: {df_orders.shape[0]} rows × {df_orders.shape[1]} columns")


#%%
# Save cleaned metrics dataset
output_path_metrics = 'clean_data/Rappi - Dummy Data - RAW_INPUT_METRICS.csv'
df_metrics.to_csv(output_path_metrics, index=False)
print(f"\n✓ Saved cleaned RAW_INPUT_METRICS to: {output_path_metrics}")
print(f"  Shape: {df_metrics.shape[0]} rows × {df_metrics.shape[1]} columns")


#%%
print("\n" + "=" * 80)
print("ALL OPERATIONS COMPLETE")
print("=" * 80)
