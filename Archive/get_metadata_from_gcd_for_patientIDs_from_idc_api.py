"""
GDC Patient Metadata Downloader
--------------------------------
This script uses the Genomics Data Commons (GDC) API to download
metadata for patients listed in a given Excel file (from TCIA or similar sources).

Requirements:
    - pandas
    - requests
    - tqdm

Input:
    TCIA_unique_patientIDs.xlsx  (first column = patient IDs)

Output:
    gdc_metadata_<patient_id>.tsv  (metadata files for each patient)
    gdc_metadata_summary.xlsx      (summary of which patients had data)
"""

import requests
import pandas as pd
from pathlib import Path
import time
from tqdm import tqdm

# --- Configuration ---
INPUT_FILE = "Data Selection/patientIDs_idc_api.xlsx"
SUMMARY_FILE = "summary_metadata_from_gcd_for_patientIDs_from_idc_api.xlsx"
GDC_API_URL = "https://api.gdc.cancer.gov/files"
OUTPUT_DIR = Path("Data Selection/metadata_from_gcd_for_patientIDs_from_idc_api")
OUTPUT_DIR.mkdir(exist_ok=True)

# --- Load Patient IDs ---
df = pd.read_excel(INPUT_FILE, header=None)
patient_ids = df.iloc[:, 0].dropna().astype(str).tolist()

print(f"Loaded {len(patient_ids)} patient IDs from '{INPUT_FILE}'")

# --- Initialize results list ---
summary_data = []

# --- Main Loop with tqdm progress bar ---
for pid in tqdm(patient_ids, desc="Downloading GDC metadata", unit="patient"):
    payload = {
        "filters": {
            "op": "in",
            "content": {
                "field": "cases.submitter_id",
                "value": [pid]
            }
        },
        "format": "tsv",
        "size": "999999"
    }

    try:
        response = requests.post(GDC_API_URL, json=payload, timeout=30)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"\nRequest error for {pid}: {e}")
        summary_data.append([pid, -1])
        continue

    lines = response.text.strip().split("\n")
    if len(lines) > 1:  # Data exists
        filename = OUTPUT_DIR / f"gdc_metadata_{pid}.tsv"
        with open(filename, "w", newline='') as f:
            f.write(response.text)
        summary_data.append([pid, 1])
    else:
        summary_data.append([pid, 0])

    # Gentle delay to avoid hitting API rate limits
    # time.sleep(0.5)

# --- Save Summary ---
df_summary = pd.DataFrame(summary_data, columns=["PatientID", "HasData"])
df_summary.to_excel(SUMMARY_FILE, index=False)

print(f"\nSummary saved to '{SUMMARY_FILE}'")
print(f"Completed processing {len(patient_ids)} patients.")
