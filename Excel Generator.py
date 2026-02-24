
import pandas as pd
import numpy as np
from datetime import datetime
import os

# --- CONFIGURATION ---
BASE_DIR = r"C:\Users\ÍtaloMarquesMouzinho\.antigravity\PeopleMetrics"
OUTPUT_FILE = os.path.join(BASE_DIR, 'Talent_Metrics_Model_2025.xlsx')

# File names
FILE_HC = os.path.join(BASE_DIR, 'Headcount Evolution 2022-2026.xlsx - Hoja 1.csv')
FILE_EXITS = os.path.join(BASE_DIR, '2025.xlsx - Internal exits.csv')
FILE_TRAINING = os.path.join(BASE_DIR, '2025.xlsx - Training investment.csv')
FILE_NPS = os.path.join(BASE_DIR, '2025.xlsx - NPS.csv')
FILE_TURNOVER = os.path.join(BASE_DIR, '2025.xlsx - TurnoverRetention.csv')

# --- CONFIGURATION CONSTANTS For ESTIMATIONS ---
AVG_REPLACEMENT_COST_EUR = 12000 # Estimated Cost per Hire + Onboarding drag
AVG_OPS_LOST_VALUE_EUR = 8000 # Estimated lost productivity during vacancy

# --- PARSING HELPERS ---
def parse_messy_table(df, start_keyword, end_condition_func, col_mapping=None):
    """Finds and extracts a specific table from a messy CSV dump."""
    start_idx = df[df.apply(lambda row: row.astype(str).str.contains(start_keyword, case=False, na=False).any(), axis=1)].index
    if len(start_idx) == 0: 
        return pd.DataFrame()
    
    header_row_idx = start_idx[0] + 1
    if header_row_idx >= len(df): return pd.DataFrame()

    header_row = df.iloc[header_row_idx]
    
    data_rows = []
    for i in range(header_row_idx + 1, len(df)):
        row = df.iloc[i]
        if end_condition_func(row): break
        data_rows.append(row)
        
    extracted_df = pd.DataFrame(data_rows)
    
    if extracted_df.empty: return extracted_df

    if col_mapping and len(col_mapping) <= extracted_df.shape[1]:
         extracted_df = extracted_df.iloc[:, :len(col_mapping)]
         extracted_df.columns = col_mapping
    else:
        extracted_df.columns = header_row
        
    return extracted_df

def normalize_depts(df, col_name):
    """Standardizes department names."""
    if df.empty or col_name not in df.columns: return df
    mapping = {
        'CUSTOMER SERVICE': 'CS', 'IT - DEVELOPER': 'Tech/IT', 'IT - BACKOFFICE': 'Tech/IT',
        'PROJECT/PRODUCT': 'Product', 'IT - UIUX': 'Tech/IT', 'IT - FRONT': 'Tech/IT',
        'HR-CORPORATE': 'HR', 'PAID MARKETING': 'Marketing', 'ORGANIC MARKETING': 'Marketing',
        'DBI': 'Data', 'IT ': 'Tech/IT', 'IT': 'Tech/IT',
        'Project/ Product': 'Product', 'Project Product': 'Product',
        'Finance, Legal and Payments': 'Finance/Legal', 'FINANCE, LEGAL AND PAYMENTS': 'Finance/Legal',
        'Organic Marketing': 'Marketing', 'Paid Marketing': 'Marketing',
        'RRHH': 'HR', 'ASO': 'Marketing', 'Market Research': 'Marketing',
        'Ai Lab': 'Tech/IT'
    }
    # Case insensitive match helper could be added, but manual map for now
    df['Unified_Dept'] = df[col_name].map(mapping).fillna(df[col_name])
    return df

# --- MAIN PROCESSING ---
def generate_model():
    print("Loading data...")
    
    # ---------------------------
    # 1. LOAD BASE DATASETS
    # ---------------------------
    
    # HEADCOUNT
    try:
        df_hc = pd.read_csv(FILE_HC)
        if 'Fecha' in df_hc.columns:
             df_hc['Fecha'] = pd.to_datetime(df_hc['Fecha'])
             df_hc = df_hc.sort_values('Fecha')
             cols_to_keep = ['Fecha']
             for c in ['Leadtech', 'Randstad', 'Deel', 'Freelance']:
                 if c in df_hc.columns: cols_to_keep.append(c)
                 else: df_hc[c] = 0
             df_hc = df_hc[cols_to_keep].fillna(0)
             df_hc['Total_Workforce'] = df_hc['Leadtech'] + df_hc['Randstad'] + df_hc['Deel'] + df_hc['Freelance']
        else:
            df_hc = pd.DataFrame()
            print("Warning: HC file missing Fecha")
    except: df_hc = pd.DataFrame()

    # EXITS (Detailed)
    try:
        df_exits_raw = pd.read_csv(FILE_EXITS, header=None)
        
        # Voluntary
        df_vol = parse_messy_table(df_exits_raw, "Voluntary exit per Department", 
                                  lambda r: pd.isna(r[0]) or str(r[0]).lower() == 'total',
                                  ['Department', 'Count'])
        df_vol['Type'] = 'Voluntary'
        
        # Dismissals
        df_dis = parse_messy_table(df_exits_raw, "Disciplinary dismissal", 
                                  lambda r: pd.isna(r[0]) or str(r[0]).lower() == 'total',
                                  ['Department', 'Count'])
        df_dis['Type'] = 'Dismissal'
        
        df_exits = pd.concat([df_vol, df_dis])
        df_exits['Count'] = pd.to_numeric(df_exits['Count'], errors='coerce').fillna(0)
        df_exits = normalize_depts(df_exits, 'Department')
        
        # Tenure/Timing Table
        # Exit timing, Voluntary exits, Avg tenure (months)
        df_tenure = parse_messy_table(df_exits_raw, "Exit timing",
                                      lambda r: pd.isna(r[0]),
                                      ['Timing_Category', 'Count', 'Avg_Tenure_Months'])
        df_tenure['Count'] = pd.to_numeric(df_tenure['Count'], errors='coerce').fillna(0)
    except Exception as e:
        print(f"Error exits: {e}")
        df_exits = pd.DataFrame()
        df_tenure = pd.DataFrame()

    # TRAINING
    try:
        df_train_raw = pd.read_csv(FILE_TRAINING, header=None)
        df_train = parse_messy_table(df_train_raw, "Training investment by department", 
                                    lambda r: pd.isna(r[0]) or str(r[0]).lower() == 'total',
                                    ['Department', 'Investment_EUR', 'Hours'])
        df_train['Investment_EUR'] = pd.to_numeric(df_train['Investment_EUR'], errors='coerce').fillna(0)
        df_train = normalize_depts(df_train, 'Department')
    except: df_train = pd.DataFrame()

    # NPS
    try:
        df_nps_clean = pd.DataFrame([
            {'Metric': 'NPS Score', 'Value': 11.76},
            {'Metric': 'Promoters', 'Value': 35},
            {'Metric': 'Passives', 'Value': 41},
            {'Metric': 'Detractors', 'Value': 24}
        ])
    except: df_nps_clean = pd.DataFrame()

    # ---------------------------
    # 2. GENERATE NEW ANALYTICAL TABS
    # ---------------------------

    # A. DB_Retention_Tenure
    # View: Early (Probation) vs Late (Post-Probation) Churn
    # Logic: Use df_tenure
    if not df_tenure.empty:
        df_retention_view = df_tenure.copy()
        df_retention_view['Risk_Label'] = np.where(df_retention_view['Timing_Category'].str.contains('probation', case=False), 'Early Churn (Hiring Miss)', 'Regrettable Loss')
    else:
        df_retention_view = pd.DataFrame({'Info': ['No detailed tenure data available']})

    # B. DB_Dept_Health
    # View: Combined Risk of Dismissals + Voluntary Exits
    # Logic: Pivot Exits
    if not df_exits.empty:
        df_health = df_exits.groupby(['Unified_Dept', 'Type'])['Count'].sum().unstack(fill_value=0).reset_index()
        # Add Investment if available
        if not df_train.empty:
            df_inv = df_train.groupby('Unified_Dept')['Investment_EUR'].sum().reset_index()
            df_health = pd.merge(df_health, df_inv, on='Unified_Dept', how='left').fillna(0)
        
        df_health['Total_Exits'] = df_health.get('Dismissal', 0) + df_health.get('Voluntary', 0)
        df_health['Health_Status'] = np.where(df_health['Total_Exits'] > 5, 'High Risk', 'Stable')
    else:
        df_health = pd.DataFrame()

    # C. DB_Cost_of_Churn
    # View: Financial Impact
    # Logic: (Exits * Replacement Cost) + (Exits * Training Lost) approx
    if not df_health.empty:
        df_cost = df_health.copy()
        df_cost['Replacement_Cost'] = df_cost['Total_Exits'] * AVG_REPLACEMENT_COST_EUR
        df_cost['Productivity_Loss'] = df_cost['Total_Exits'] * AVG_OPS_LOST_VALUE_EUR
        # Sunk training (Assuming 50% of training investment is lost when people leave - simplified proxy)
        # Better: Training Investment per Head * Exits? No head count. 
        # Using Total Dept Investment * (Exits / Total Dept Exits Ratio? No). 
        # Let's just assume we lose the specific investment. Since we don't have inv per person, 
        # we will list Total Dept Investment as Context, and rely on Replacement Cost as the main Churn Cost.
        
        df_cost['Total_Estimated_Loss'] = df_cost['Replacement_Cost'] + df_cost['Productivity_Loss']
        
        # Summary Row
        total_row = pd.DataFrame({
            'Unified_Dept': ['TOTAL'],
            'Replacement_Cost': [df_cost['Replacement_Cost'].sum()],
            'Productivity_Loss': [df_cost['Productivity_Loss'].sum()],
            'Total_Estimated_Loss': [df_cost['Total_Estimated_Loss'].sum()]
        })
        df_cost = pd.concat([df_cost, total_row], ignore_index=True)
    else:
        df_cost = pd.DataFrame()

    # D. DB_Workforce_Mix
    # View: % Split of Internal vs External Over Time
    # Logic: Use df_hc
    if not df_hc.empty:
        df_mix = df_hc.copy()
        # Calculate percentages
        df_mix['Share_Internal'] = df_mix['Leadtech'] / df_mix['Total_Workforce']
        df_mix['Share_External'] = (df_mix['Randstad'] + df_mix['Deel'] + df_mix['Freelance']) / df_mix['Total_Workforce']
        
        df_mix_view = df_mix[['Fecha', 'Total_Workforce', 'Leadtech', 'Share_Internal', 
                              'Randstad', 'Deel', 'Share_External']].tail(24) # Last 2 years
    else:
        df_mix_view = pd.DataFrame()

    # E. DB_Hiring_Forecast
    # View: Predicted needs
    # Logic: Avg Churn Rate last 6 months -> Apply to current HC -> + Grow Target
    if not df_hc.empty:
        # 1. Calculate Monthly Churn (Approx from headcounts drops? No, specific exits are better but we don't have date-based exits)
        # We'll use the 'Turnover Rate' from the summary file for a global multiplier?
        # Or derive: Net Change = Hires - Exits. Exits are unknown per month.
        # Let's use a flat assumption based on the "17% turnover" from the CSV text analysis
        monthly_churn_rate = 0.17 / 12 # ~1.4% per month
        
        latest_hc = df_hc.iloc[-1]['Total_Workforce']
        latest_date = df_hc.iloc[-1]['Fecha']
        
        forecast_months = []
        current_hc = latest_hc
        
        for i in range(1, 7): # 6 Month Forecast
            next_date = latest_date + pd.DateOffset(months=i)
            # Predicted Exits
            pred_exits = int(current_hc * monthly_churn_rate)
            # Growth Target (Assume 1% net count growth per month)
            target_net_growth = int(current_hc * 0.01)
            
            # Hiring Needed = Exits + Net Growth
            hiring_needed = pred_exits + target_net_growth
            
            # Update HC
            current_hc = current_hc + target_net_growth
            
            forecast_months.append({
                'Month': next_date.date(),
                'Projected_Opening_HC': int(current_hc - target_net_growth),
                'Predicted_Attrition': pred_exits,
                'Net_Growth_Target': target_net_growth,
                'Recruitment_Target': hiring_needed
            })
            
        df_forecast = pd.DataFrame(forecast_months)
    else:
        df_forecast = pd.DataFrame()

    # ---------------------------
    # 3. WRITE OUTPUT
    # ---------------------------
    print(f"Writing to {OUTPUT_FILE}...")
    try:
        with pd.ExcelWriter(OUTPUT_FILE, engine='xlsxwriter') as writer:
            
            # ORIGINAL DATA TABS
            if not df_hc.empty: df_hc.to_excel(writer, sheet_name='Data_Headcount', index=False)
            if not df_exits.empty: df_exits.to_excel(writer, sheet_name='Data_Exits_Detailed', index=False)
            if not df_train.empty: df_train.to_excel(writer, sheet_name='Data_Training', index=False)
            if not df_nps_clean.empty: df_nps_clean.to_excel(writer, sheet_name='Data_NPS', index=False)
            
            # NEW INSIGHT TABS
            if not df_retention_view.empty:
                df_retention_view.to_excel(writer, sheet_name='DB_Retention_Tenure', index=False)
            if not df_health.empty:
                df_health.to_excel(writer, sheet_name='DB_Dept_Health', index=False)
            if not df_cost.empty:
                df_cost.to_excel(writer, sheet_name='DB_Cost_of_Churn', index=False)
            if not df_mix_view.empty:
                df_mix_view.to_excel(writer, sheet_name='DB_Workforce_Mix', index=False)
            if not df_forecast.empty:
                df_forecast.to_excel(writer, sheet_name='DB_Hiring_Forecast', index=False)

            # FORMATTING
            workbook = writer.book
            for sheet in writer.sheets.values():
                sheet.set_column(0, 5, 20)

        print("Done! File generated.")
    except Exception as e:
        print(f"Error writing output file: {e}")

if __name__ == "__main__":
    generate_model()