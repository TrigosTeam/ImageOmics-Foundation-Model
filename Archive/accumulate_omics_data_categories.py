import os
import pandas as pd

# ---- CONFIG ----
folder_path = "gdc_metadata_files"     # folder containing TSV files
output_excel = "omics_data_categories.xlsx"  # output file name

# ---- PROCESSING ----
all_rows = []  # will store each file's DF

for file in os.listdir(folder_path):
    if file.endswith(".tsv"):
        file_path = os.path.join(folder_path, file)
        print(f"Processing: {file}")

        # Read only necessary columns
        try:
            df = pd.read_csv(file_path, sep="\t", usecols=[
                "data_category",
                "data_type",
                "experimental_strategy",
                "data_format",
                "access"

            ])
        except Exception as e:
            print(f"❌ Skipping {file} (missing columns or read error): {e}")
            continue

        # Add the source filename
        df["source_file"] = file[13:-4]

        # Store for merging
        all_rows.append(df)

# ---- MERGE ALL ----
if all_rows:
    merged_df = pd.concat(all_rows, ignore_index=True)
    merged_df.to_excel(output_excel, index=False)
    print(f"\n✅ Done! Saved merged Excel file as: {output_excel}")
else:
    print("⚠ No valid TSV files found or processed.")
