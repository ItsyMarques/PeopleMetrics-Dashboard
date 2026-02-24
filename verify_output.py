
import pandas as pd
import os

FILE_PATH = r"C:\Users\ÍtaloMarquesMouzinho\.antigravity\PeopleMetrics\Talent_Metrics_Model_2025.xlsx"

try:
    xls = pd.ExcelFile(FILE_PATH)
    print("Sheets found:", xls.sheet_names)
    
    expected_tabs = [
        'DB_Retention_Tenure', 'DB_Dept_Health', 'DB_Cost_of_Churn', 
        'DB_Workforce_Mix', 'DB_Hiring_Forecast'
    ]
    
    for tab in expected_tabs:
        if tab in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name=tab)
            print(f"\n--- {tab} ---")
            print(df.head(3))
            if df.empty:
                print(f"WARNING: {tab} is empty!")
        else:
            print(f"\nERROR: {tab} MISSING!")
            
except Exception as e:
    print(f"Error verification: {e}")
