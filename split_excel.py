
import pandas as pd
import os
import glob

# specific directory
TARGET_DIR = r"C:\Users\ÍtaloMarquesMouzinho\.antigravity\PeopleMetrics"

def process_excel_files():
    # Find all xlsx files in the target directory
    print(f"Target Directory: {TARGET_DIR}")
    xlsx_path = os.path.join(TARGET_DIR, "*.xlsx")
    xlsx_files = glob.glob(xlsx_path)
    
    print(f"Found files: {xlsx_files}")

    for file_path in xlsx_files:
        filename = os.path.basename(file_path)
        if filename.startswith('~$'): continue 
        
        print(f"Processing {filename}...")
        try:
            xls = pd.ExcelFile(file_path)
            for sheet_name in xls.sheet_names:
                df = pd.read_excel(file_path, sheet_name=sheet_name)
                # Construct CSV string
                csv_filename = f"{filename} - {sheet_name}.csv"
                output_path = os.path.join(TARGET_DIR, csv_filename)
                df.to_csv(output_path, index=False)
                print(f"  Created: {csv_filename}")
        except Exception as e:
            print(f"  Error processing {filename}: {e}")

if __name__ == "__main__":
    process_excel_files()
