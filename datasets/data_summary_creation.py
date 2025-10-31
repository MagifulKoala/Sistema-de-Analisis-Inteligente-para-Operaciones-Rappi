#%%
import pandas as pd
import numpy as np
import os
#%%
#clean file paths
#csv_file_path = r"clean_data\Rappi - Dummy Data - RAW_ORDERS.csv"
csv_file_path = r"clean_data\Rappi - Dummy Data - RAW_INPUT_METRICS.csv"

# Load the CSV files
df_current = pd.read_csv(csv_file_path)
answer = ""

#%% Preview RAW_INPUT_METRICS dataset
print("\n" + "=" * 80)
print("RAW_INPUT_METRICS DATASET - EXPLORATORY ANALYSIS")
print("=" * 80)

column_names_index = df_current.columns
column_list = ";".join([column_name for column_name in column_names_index])
answer += f"Columns in dataset: \n{column_list}\n"

print("\n1. FIRST FEW ROWS:")
head = df_current.head()
print(head)
answer += "\n1. FIRST FEW ROWS:\n"
answer += f"{head}\n"

print("\n2. DATASET INFO:")
info = df_current.info()
print(info)
answer += "\n2. DATASET INFO:\n"
answer += f"{str(info)}\n"

print("\n3. DATA TYPES:")
data_types = df_current.dtypes
print(data_types)
answer += "\n3. DATA TYPES:\n"
answer += f"{data_types}\n"

print("\n4. DESCRIPTIVE STATISTICS:")
statistics = df_current.describe()
print(statistics)
answer += "\n4. DESCRIPTIVE STATISTICS:\n"
answer += f"{statistics}\n"

print("\n5. NULL VALUES:")
null_counts_m = df_current.isnull().sum()
null_pct_m = (df_current.isnull().sum() / len(df_current)) * 100
null_summary_m = pd.DataFrame({
    'Null Count': null_counts_m,
    'Null %': null_pct_m
})
print(null_summary_m[null_summary_m['Null Count'] > 0])
answer += "\n5. NULL VALUES:\n"
answer += f"{null_summary_m[null_summary_m['Null Count'] > 0]}\n"

print("\n6. UNIQUE VALUES PER COLUMN:")
answer += "\n6. UNIQUE VALUES PER COLUMN:\n"
for col in df_current.columns:
    unique_count = df_current[col].nunique()
    print(f"  {col}: {unique_count} unique values")
    answer += f"  {col}: {unique_count} unique values \n"

print("\n7. CATEGORICAL COLUMNS - VALUE COUNTS:")
categorical_cols_m = df_current.select_dtypes(include=['object']).columns
answer += "\n7. CATEGORICAL COLUMNS - VALUE COUNTS:\n"
for col in categorical_cols_m:
    print(f"\n  {col}:")
    print(df_current[col].value_counts().head(10))
    answer += f"\n  {col}:\n"
    answer += f"{df_current[col].value_counts().head(10)}\n"

print("\n8. NUMERIC COLUMNS - RANGES:")
numeric_cols_m = df_current.select_dtypes(include=[np.number]).columns
answer += "\n8. NUMERIC COLUMNS - RANGES:\n"
for col in numeric_cols_m:
    print(f"  {col}: Min={df_current[col].min()}, Max={df_current[col].max()}")
    answer += f"  {col}: Min={df_current[col].min()}, Max={df_current[col].max()}\n"

#%%
summary_folder_path = "summary_data/"
summary_file_name = f"{csv_file_path.split("\\")[1].split(".")[0]}_summary.txt"
summary_final_path = os.path.join(summary_folder_path,summary_file_name)

print(f"Final path: {summary_final_path}")

with open(summary_final_path, "w", encoding="utf-8") as f:
    f.write(answer)

# %%
