import os
import pandas as pd
from tqdm import tqdm

# Load your metadata DataFrame
series = pd.read_pickle("tcia_all_metadata.pkl")
# Ensure consistent column names
series.columns = series.columns.str.strip()

# Folder containing the files
folder_path = "gdc_metadata_files"

# List to store results
results = []

# Iterate through files with progress bar
for filename in tqdm(os.listdir(folder_path), desc="Processing files"):
    # Extract patient ID from filename (adjust slicing if needed)
    patient_id = filename[13:-4]

    # Filter dataframe once per patient
    patient_data = series[series['PatientID'] == patient_id]

    # Get unique values as comma-separated strings
    unique_collections = ', '.join(map(str, patient_data['Collection'].unique()))
    unique_bodyparts = ', '.join(map(str, patient_data['BodyPartExamined'].unique()))

    # Append to results
    results.append([patient_id, unique_collections, unique_bodyparts])

# Convert results to DataFrame
df_output = pd.DataFrame(results, columns=["PatientID", "Collection", "BodyPartExamined"])

# Save to Excel
excel_filename = "image_omics_patientIDs.xlsx"
df_output.to_excel(excel_filename, index=False)

print(f"Saved {len(df_output)} entries to {excel_filename}")
