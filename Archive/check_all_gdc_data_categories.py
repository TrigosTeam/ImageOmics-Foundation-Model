import os
import pandas as pd
from collections import defaultdict

# Path to your folder containing TSV files
folder_path = "gdc_metadata_files"

# Nested dictionary: category -> type -> {formats, strategies}
category_dict = defaultdict(lambda: defaultdict(lambda: {"data_format": set(), "experimental_strategy": set()}))

# Loop through all TSV files
for file in os.listdir(folder_path):
    if file.endswith(".tsv"):
        file_path = os.path.join(folder_path, file)
        print(f"Processing: {file}")
        
        try:
            df = pd.read_csv(file_path, sep='\t')
        except Exception as e:
            print(f"⚠️ Error reading {file}: {e}")
            continue
        
        # Make columns case-insensitive
        cols_lower = [col.lower() for col in df.columns]
        required_cols = ["data_category", "data_type", "data_format", "experimental_strategy"]
        if not all(col in cols_lower for col in required_cols):
            print(f"⚠️ Required columns not found in {file}")
            continue
        
        # Map actual column names
        col_map = {col: df.columns[cols_lower.index(col)] for col in required_cols}
        
        # Iterate rows
        for _, row in df.iterrows():
            category = row[col_map["data_category"]]
            dtype = row[col_map["data_type"]]
            dformat = row[col_map["data_format"]]
            strategy = row[col_map["experimental_strategy"]]
            
            if pd.notna(category) and pd.notna(dtype):
                if pd.notna(dformat):
                    category_dict[category][dtype]["data_format"].add(dformat)
                if pd.notna(strategy):
                    category_dict[category][dtype]["experimental_strategy"].add(strategy)

# Prepare rows for Excel
rows = []
for category, dtypes in category_dict.items():
    for dtype, info in dtypes.items():
        row = {
            "data_category": category,
            "data_type": dtype,
            "data_format": ", ".join(sorted(info["data_format"])),
            "experimental_strategy": ", ".join(sorted(info["experimental_strategy"]))
        }
        rows.append(row)

# Convert to DataFrame
df_excel = pd.DataFrame(rows)

# Save to Excel
output_file = "gdc_data_categories_summary.xlsx"
df_excel.to_excel(output_file, index=False)

print(f"\n✅ Nested data successfully saved to {output_file}")
