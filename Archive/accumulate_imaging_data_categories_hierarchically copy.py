import os
import pandas as pd

# Load metadata
series = pd.read_pickle("tcia_all_metadata.pkl")
series = series[series['ReleasedStatus'] != "Yes"] # Filtering to get only "open" access

# Path to folder containing GDC files
gdc_file_path = "gdc_metadata_files"

# List all files in the folder
files = os.listdir(gdc_file_path)

# Extract patient IDs from filenames (assuming pattern string[11:-4])
patient_list = [f[13:-4] for f in files]

# Filter the series dataframe to include only patients in the list
filtered_series = series[series['PatientID'].isin(patient_list)]

# Group by patientID and modality, then count
grouped = filtered_series.groupby(['PatientID', 'Modality']).size().reset_index(name='count')

# Pivot to get modalities as columns
count_table = grouped.pivot(index='PatientID', columns='Modality', values='count').fillna(0).astype(int)

# Reset index so patientID becomes a column
count_table = count_table.reset_index()


# Save to Excel
count_table.to_excel("patient_imaging_modality_counts.xlsx", index=False)



# from idc_index import index

# idc_client = index.IDCClient()