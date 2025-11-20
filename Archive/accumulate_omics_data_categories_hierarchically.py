import pandas as pd

# Load Excel
df = pd.read_excel("omics_data_categories.xlsx")
df = df.fillna("")

# Extract PatientID from source_file (assuming source_file contains something like "Patient123_file1")
# Adjust this line if source_file is already the patient ID
df["PatientID"] = df["source_file"]  # or some extraction logic

df = df[df['access'] != "open"] # Filtering to get only "open" access

# Group by combination + PatientID and count
grouped = (
    df.groupby(
        ["data_category", "data_type", "experimental_strategy", "data_format", "PatientID"]
    )
    .size()
    .reset_index(name="file_count")
)

# Pivot so that each patient is a column
pivot_table = grouped.pivot_table(
    index=["data_category", "data_type", "experimental_strategy", "data_format"],
    columns="PatientID",
    values="file_count",
    fill_value=0
).reset_index()

# Optional: sort hierarchically
pivot_table = pivot_table.sort_values(
    ["data_category", "data_type", "experimental_strategy", "data_format"]
)

pivot_table["nonzero_count"] = (pivot_table.iloc[:, 4:] != 0).sum(axis=1).astype(int)
pivot_table["actual_count"] = pivot_table.iloc[:, 4:-1].sum(axis=1).astype(int)


# Save to Excel
pivot_table.to_excel("combination_patient_counts.xlsx", index=False)

