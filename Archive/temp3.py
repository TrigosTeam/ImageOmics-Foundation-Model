import pandas as pd
import os 

# Pickle files
pkl_files = ["Data Selection/data_catalogue_idc_api.pkl", "Data Selection/data_catalogue_tcia_api.pkl"]

# make the big list
p1, p2 = "Data Selection/metadata_from_gcd_for_patientIDs_from_idc_api", "Data Selection/metadata_from_gcd_for_patientIDs_from_tcia_api"
pa1 = [f.replace("gdc_metadata_", "").replace(".tsv", "") for f in os.listdir(p1)]
pa2 = [f.replace("gdc_metadata_", "").replace(".tsv", "") for f in os.listdir(p2)]
pas = [pa1, pa2]

# Dictionary to hold counts
patient_modality_dict = {}

for pkl, pa in zip(pkl_files, pas) :
    # Load pickle file
    df = pd.read_pickle(pkl)

    df = df[df["Modality"].isin(["MR", "CT", "PT", "US", "DX", "MG", "CR"])]
    df = df[df["PatientID"].isin(pa)]

    # Check required columns
    if "PatientID" not in df.columns or "Modality" not in df.columns:
        raise ValueError(f"{pkl} is missing 'PatientID' or 'Modality' column!")

    # Group by PatientID and Modality, count rows
    counts = df.groupby(["Modality", "PatientID"]).size().reset_index(name="count")

    # Store counts in dictionary for merging
    for _, row in counts.iterrows():
        modality = row["Modality"]
        patient = row["PatientID"]
        count = row["count"]

        if modality not in patient_modality_dict:
            patient_modality_dict[modality] = {}

        try:
            temp = patient_modality_dict[modality][patient]
            print(patient, modality, temp,count) if temp!=count else None
        except: 
            patient_modality_dict[modality][patient] = count # If both TCIA and IDC have same patient, the TCIA count (second in loop) will override the IDC count (first in loop)
