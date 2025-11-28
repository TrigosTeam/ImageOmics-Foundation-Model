import pandas as pd
import os

# -------------------------
# Configuration
# -------------------------
pkl_files = [
    # "Data Selection/data_catalogue_idc_api.pkl",
    "Data Selection/data_catalogue_tcia_api.pkl"
]

# Metadata folders
p1, p2 = (
    "Data Selection/metadata_from_gcd_for_patientIDs_from_idc_api",
    "Data Selection/metadata_from_gcd_for_patientIDs_from_tcia_api"
)

# Clean patient IDs from filenames
pa1 = [f.replace("gdc_metadata_", "").replace(".tsv", "") for f in os.listdir(p1)]
pa2 = [f.replace("gdc_metadata_", "").replace(".tsv", "") for f in os.listdir(p2)]
pas = [
    # pa1,
    pa2
]

# Dictionary to hold counts
patient_modality_dict = {}

# -------------------------
# Process each pickle file
# -------------------------
for pkl, pa in zip(pkl_files, pas):
    # Load pickle
    df = pd.read_pickle(pkl)

    # Filter for desired modalities and patient IDs
    df = df[df["Modality"].isin(["MR", "CT", "PT", "US", "DX", "MG", "CR"])]
    df = df[df["PatientID"].isin(pa)]

    # Check required columns
    if "PatientID" not in df.columns or "Modality" not in df.columns:
        raise ValueError(f"{pkl} is missing 'PatientID' or 'Modality' column!")

    # Group by Modality and PatientID
    counts = df.groupby(["Modality", "PatientID"]).size().reset_index(name="count")

    # Store counts in dictionary
    for _, row in counts.iterrows():
        modality = row["Modality"]
        patient = row["PatientID"]
        count = row["count"]

        if modality not in patient_modality_dict:
            patient_modality_dict[modality] = {}
        # TCIA counts override IDC if duplicate
        patient_modality_dict[modality][patient] = count

# -------------------------
# Build final DataFrame
# -------------------------
summary_df = pd.DataFrame.from_dict(patient_modality_dict, orient="index").fillna(0).astype(int)

# Sort rows by modality
summary_df = summary_df.sort_index()

# Sort patient columns alphabetically, keep 'Modality' first
patient_cols = sorted([c for c in summary_df.columns if c != "Modality"])
summary_df = summary_df[patient_cols]  # Columns only
summary_df = summary_df.reset_index().rename(columns={"index": "Modality"})  # Add Modality column

# Add 'count' column right after 'Modality'
summary_df.insert(1, 'count', (summary_df.iloc[:, 2:] != 0).sum(axis=1))

# -------------------------
# Save to Excel
# -------------------------
summary_df.to_excel("Data Selection/data_categories_tcia.xlsx", index=False)

print("Done! Saved as tcia_data_categories.xlsx")
