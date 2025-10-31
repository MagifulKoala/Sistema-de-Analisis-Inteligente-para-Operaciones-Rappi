import pandas as pd
import numpy as np

orders_file_path = r"datasets/clean_data/Rappi - Dummy Data - RAW_ORDERS.csv"
metrics_file_path = r"datasets/clean_data/Rappi - Dummy Data - RAW_INPUT_METRICS.csv"

# Load the CSV files
df_orders = pd.read_csv(orders_file_path)
df_metrics = pd.read_csv(metrics_file_path)


SAFE_GLOBALS = {
    "__builtins__": {},  # disable builtins
    "pd": pd,
    "np":np
}

SAFE_LOCALS = {
    "orders": df_orders,
    "metrics": df_metrics,
}

def run_query(code: str):
    try:
        result = eval(code, SAFE_GLOBALS, SAFE_LOCALS)
        return {"result": result.to_dict() if hasattr(result, "to_dict") else str(result)}
    except Exception as e:
        return {"error": str(e)}