import os
import random
import pandas as pd
from pathlib import Path
from tqdm import tqdm

# --- Configuration ---
INPUT_FILE = Path("Data Selection/patientIDs_tcia_api.xlsx")
FOLDER = Path("Data Selection/metadata_from_gcd_for_patientIDs_from_tcia_api")

# --- Load Patient IDs ---
df = pd.read_excel(INPUT_FILE, header=None)
patient_ids = set(df.iloc[:, 0].dropna().astype(str).tolist())

# --- Iterate with tqdm ---
for filepath in tqdm(list(FOLDER.iterdir()), desc="Processing files"):
    if filepath.is_file():
        # Extract ID from filename
        fname = filepath.stem.replace("gdc_metadata_", "")
        
        if fname not in patient_ids:
            tqdm.write(f"Deleting: {filepath}")
            filepath.unlink()       # delete file
        else:
            None
            # tqdm.write(f"Keeping:  {filepath}")
