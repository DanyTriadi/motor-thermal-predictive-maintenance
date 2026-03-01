import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "..", "data", "measures_v2.csv")

data = pd.read_csv(DATA_PATH)

print("\nDATASET:")
print("Type DataFrame :", type(data))
print("Total Rows     :", data.shape[0])
print("Total Columns  :", data.shape[1])

print("\nINFO DATASET:")
data.info()

print("\nCOLUMN DETAILS")
info_df = pd.DataFrame({
    "Column": data.columns,
    "Non-Null Count": data.notnull().sum().values,
    "Dtype": data.dtypes.values
})

print(info_df)


print("\n========== DATA PREVIEW ==========")
print(data.head())