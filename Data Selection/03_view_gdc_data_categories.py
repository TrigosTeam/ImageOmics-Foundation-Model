import pandas as pd
from pathlib import Path

# -------------------------
# Configuration
# -------------------------
FOLDER = Path("Data Selection/metadata_from_gcd_for_patientIDs_from_tcia_api")
OUTPUT_FILE = "Data Selection/data_categories_gdc.xlsx"

# Columns of interest (metadata)
META_COLS = ["data_category", "data_type", "experimental_strategy", "data_format"]

# -------------------------
# Processing
# -------------------------
records = []
patient_ids = []

# Read each TSV file and collect patient IDs
for file in FOLDER.glob("*.tsv"):
    patient_id = file.stem.replace("gdc_metadata_", "").replace(".tsv", "")
    patient_ids.append(patient_id)

    df = pd.read_csv(file, sep="\t")
    df = df.fillna("")
    df = df[df['access'] == "open"]

    df = df[META_COLS]
    df["patient_id"] = patient_id
    records.append(df)

# Combine all records into a single DataFrame
all_df = pd.concat(records, ignore_index=True)

# -------------------------
# Create summary pivot table
# -------------------------
summary = (
    all_df
    .groupby(META_COLS + ["patient_id"])
    .size()
    .reset_index(name="count")
)

# Pivot table: metadata as rows, patient IDs as columns
final_table = summary.pivot_table(
    index=META_COLS,
    columns="patient_id",
    values="count",
    fill_value=0
)

# Add any missing patient IDs (all zeros)
for pid in patient_ids:
    if pid not in final_table.columns:
        final_table[pid] = 0

# -------------------------
# Add "counts" column (number of non-zero patient entries per row)
# -------------------------
final_table["counts"] = (final_table > 0).sum(axis=1)

# -------------------------
# Sort patient ID columns alphabetically
# -------------------------
patient_cols_sorted = sorted([c for c in final_table.columns if c not in ["counts"]])

# -------------------------
# Reset index so metadata columns are normal columns
# -------------------------
final_table = final_table.reset_index()

# -------------------------
# Reorder final columns: metadata, counts, patients
# -------------------------
final_table = final_table[META_COLS + ["counts"] + patient_cols_sorted]

# -------------------------
# Save to Excel
# -------------------------
final_table.to_excel(OUTPUT_FILE, index=False)

print("Summary saved to", OUTPUT_FILE)

