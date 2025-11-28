import os
import random
import pandas as pd
from pathlib import Path
from tqdm import tqdm

p1, p2 = "Data Selection/metadata_from_gcd_for_patientIDs_from_idc_api", "Data Selection/metadata_from_gcd_for_patientIDs_from_tcia_api"

pa1 = [f.replace("gdc_metadata_", "").replace(".tsv", "") 
               for f in os.listdir(p1)]

pa2 = [f.replace("gdc_metadata_", "").replace(".tsv", "") 
               for f in os.listdir(p2)]

print(set(pa1)-set(pa2))
# print(set(pa2)-set(pa1))

print()