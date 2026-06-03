import pandas as pd

original_data_path = (
    "datasets/Parking_Violations_Issued_-_Fiscal_Year_2025_20260603.csv"
)
sample_data_path = "datasets/sample_parking_violations_2025.csv"

data = pd.read_csv(original_data_path, low_memory=False)
sample_data = data.sample(n=10000, random_state=42)
sample_data.to_csv(sample_data_path, index=False)
