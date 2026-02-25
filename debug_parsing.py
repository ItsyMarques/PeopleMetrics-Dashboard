import pandas as pd
import numpy as np

def parse_messy_table(df, start_keyword, end_condition_func, col_mapping=None):
    start_idx = df[df.apply(lambda row: row.astype(str).str.contains(start_keyword, case=False, na=False).any(), axis=1)].index
    print(f"Keyword: {start_keyword}, Start Indexes: {list(start_idx)}")
    if len(start_idx) == 0:
        return pd.DataFrame()
    
    header_row_idx = start_idx[0] + 1
    header_row = df.iloc[header_row_idx]
    print(f"Header Row at {header_row_idx}: {header_row.values}")
    
    data_rows = []
    for i in range(header_row_idx + 1, len(df)):
        row = df.iloc[i]
        if end_condition_func(row):
            print(f"End condition met at index {i}: {row.values[:2]}")
            break
        data_rows.append(row)
        
    extracted_df = pd.DataFrame(data_rows)
    print(f"Extracted DF shape: {extracted_df.shape}")
    
    if col_mapping and not extracted_df.empty and len(col_mapping) <= extracted_df.shape[1]:
         extracted_df = extracted_df.iloc[:, :len(col_mapping)]
         extracted_df.columns = col_mapping
    elif not extracted_df.empty:
        extracted_df.columns = header_row
        
    return extracted_df

try:
    exits_file = '2025.xlsx'
    print(f"Reading {exits_file} - Internal exits...")
    df_exits_raw = pd.read_excel(exits_file, sheet_name='Internal exits', header=None)
    
    df_vol = parse_messy_table(
        df_exits_raw, 
        "Voluntary exit per Department", 
        lambda r: pd.isna(r[0]) or str(r[0]).lower() == 'total',
        col_mapping=['Department', 'Count']
    )
    
    df_dis = parse_messy_table(
        df_exits_raw, 
        "Disciplinary dismissal", 
        lambda r: pd.isna(r[0]) or str(r[0]).lower() == 'total',
        col_mapping=['Department', 'Count']
    )

    train_file = '2025.xlsx'
    print(f"\nReading {train_file} - Training investment...")
    df_train_raw = pd.read_excel(train_file, sheet_name='Training investment', header=None)
    df_train = parse_messy_table(
        df_train_raw,
        "Training investment by department",
        lambda r: pd.isna(r[0]) or str(r[0]).lower() == 'total',
        col_mapping=['Department', 'Investment', 'Hours']
    )

except Exception as e:
    import traceback
    print(f"ERROR: {e}")
    traceback.print_exc()
