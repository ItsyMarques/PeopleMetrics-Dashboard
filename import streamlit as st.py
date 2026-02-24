import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Talent Command Center 2025",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- STYLING & TEXT UTILS ---
st.markdown("""
    <style>
        .block-container { padding-top: 2rem; }
        .metric-card {
            background-color: #ffffff;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            padding: 15px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        h1, h2, h3 { color: #2c3e50; }
        .stAlert { border-radius: 8px; }
    </style>
""", unsafe_allow_html=True)

# --- DATA PARSING FUNCTIONS (ROBUST) ---
def parse_messy_table(df, start_keyword, end_condition_func, col_mapping=None):
    """
    Finds a table inside a messy CSV based on a keyword and extracts it.
    """
    # Find start row
    start_idx = df[df.apply(lambda row: row.astype(str).str.contains(start_keyword, case=False, na=False).any(), axis=1)].index
    if len(start_idx) == 0:
        return pd.DataFrame()
    
    header_row_idx = start_idx[0] + 1  # Assuming header is immediately after title
    header_row = df.iloc[header_row_idx]
    
    # Iterate to find end
    data_rows = []
    for i in range(header_row_idx + 1, len(df)):
        row = df.iloc[i]
        if end_condition_func(row):
            break
        data_rows.append(row)
        
    extracted_df = pd.DataFrame(data_rows)
    
    # Handle columns
    if col_mapping and len(col_mapping) <= extracted_df.shape[1]:
         extracted_df = extracted_df.iloc[:, :len(col_mapping)]
         extracted_df.columns = col_mapping
    else:
        extracted_df.columns = header_row
        
    return extracted_df

def normalize_departments(df, col_name):
    """
    Standardizes department names for merging (e.g., IT - Front -> IT).
    """
    if df.empty or col_name not in df.columns:
        return df
        
    mapping = {
        'CUSTOMER SERVICE': 'Customer Service',
        'CS': 'Customer Service',
        'PROJECT/PRODUCT': 'Product',
        'Project/ Product': 'Product',
        'IT - DEVELOPER': 'Tech & IT',
        'IT - BACKOFFICE': 'Tech & IT',
        'IT - UIUX': 'Tech & IT',
        'IT - FRONT': 'Tech & IT',
        'IT ': 'Tech & IT',
        'IT': 'Tech & IT',
        'HR-CORPORATE': 'HR',
        'HR': 'HR',
        'Finance, Legal and Payments': 'Finance/Legal',
        'ACCOUNTING': 'Finance/Legal',
        'TAX': 'Finance/Legal',
        'PAYMENTS': 'Finance/Legal',
        'PAID MARKETING': 'Marketing',
        'ORGANIC MARKETING': 'Marketing',
        'SEO': 'Marketing',
        'DBI': 'Data/BI'
    }
    df['Dept_Unified'] = df[col_name].map(mapping).fillna('Other')
    return df

@st.cache_data
def load_and_process_data():
    data = {}
    try:
        # 1. HEADCOUNT (Time Series)
        hc_file = 'Copy of Personal activo 2022-2026.xlsx'
        df_hc = pd.read_excel(hc_file, sheet_name='Hoja 1')
        df_hc['Fecha'] = pd.to_datetime(df_hc['Fecha'])
        df_hc = df_hc.sort_values('Fecha')
        cols_fill = ['Leadtech', 'Randstad', 'Deel', 'Freelance']
        for c in cols_fill:
            if c in df_hc.columns:
                df_hc[c] = df_hc[c].fillna(0)
        data['hc'] = df_hc

        # 2. INTERNAL EXITS (Departments & Types)
        exits_file = '2025.xlsx'
        df_exits_raw = pd.read_excel(exits_file, sheet_name='Internal exits', header=None)
        
        # Parse Voluntary by Dept
        df_vol = parse_messy_table(
            df_exits_raw, 
            "Voluntary exit per Department", 
            lambda r: pd.isna(r[0]) or str(r[0]).lower() == 'total',
            col_mapping=['Department', 'Count']
        )
        df_vol['Type'] = 'Voluntary'
        
        # Parse Disciplinary by Dept
        df_dis = parse_messy_table(
            df_exits_raw, 
            "Disciplinary dismissal", 
            lambda r: pd.isna(r[0]) or str(r[0]).lower() == 'total',
            col_mapping=['Department', 'Count']
        )
        df_dis['Type'] = 'Dismissal'
        
        # Merge Exits
        df_exits_dept = pd.concat([df_vol, df_dis])
        df_exits_dept['Count'] = pd.to_numeric(df_exits_dept['Count'], errors='coerce').fillna(0)
        data['exits_dept'] = normalize_departments(df_exits_dept, 'Department')

        # 3. TRAINING INVESTMENT
        train_file = '2025.xlsx'
        df_train_raw = pd.read_excel(train_file, sheet_name='Training investment', header=None)
        df_train = parse_messy_table(
            df_train_raw,
            "Training investment by department",
            lambda r: pd.isna(r[0]) or str(r[0]).lower() == 'total',
            col_mapping=['Department', 'Investment', 'Hours']
        )
        df_train['Investment'] = pd.to_numeric(df_train['Investment'], errors='coerce').fillna(0)
        data['training'] = normalize_departments(df_train, 'Department')

        return data
        
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

# --- LOAD DATA ---
data = load_and_process_data()

if data:
    df_hc = data['hc']
    df_exits_dept = data['exits_dept']
    df_training = data['training']

    # --- SIDEBAR ---
    st.sidebar.title("🎛️ Controls")
    
    # Date Filter
    st.sidebar.subheader("Timeframe")
    min_date = df_hc['Fecha'].min().date()
    max_date = df_hc['Fecha'].max().date()
    start_date, end_date = st.sidebar.date_input("Select Range", [min_date, max_date])
    
    # Filter HC Data
    mask = (df_hc['Fecha'].dt.date >= start_date) & (df_hc['Fecha'].dt.date <= end_date)
    df_hc_filtered = df_hc.loc[mask]

    # Department Filter (Global)
    all_depts = sorted(list(set(df_training['Dept_Unified'].unique()) | set(df_exits_dept['Dept_Unified'].unique())))
    selected_depts = st.sidebar.multiselect("Filter Departments", all_depts, default=all_depts)

    # --- MAIN KPI HEADER ---
    st.title("🚀 Talent Command Center 2025")
    st.markdown("### Executive Intelligence Review")

    latest = df_hc_filtered.iloc[-1]
    total_hc = latest['Leadtech'] + latest['Randstad'] + latest['Deel']
    
    # Calculate Dismissal Rate (Hardcoded from summary stats in file for robustness)
    # In a real dynamic DB, this would be a sum of the filtered rows.
    # Total Exits: 127. Dismissals: 87. Voluntary: 40.
    involuntary_rate = (87 / 127) * 100
    
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("Active Headcount", f"{int(total_hc)}", f"+{int(latest['Leadtech'] - df_hc_filtered.iloc[0]['Leadtech'])} vs Period Start")
    kpi2.metric("Growth Velocity", "Aggressive", "Leadtech Core Scaling")
    kpi3.metric("Dismissal Rate", f"{involuntary_rate:.1f}%", "CRITICAL RISK", delta_color="inverse")
    kpi4.metric("NPS (eNPS)", "11.8", "Fragile / Watch", delta_color="off")

    st.divider()

    # --- TABS LAYOUT ---
    tab1, tab2, tab3 = st.tabs(["📈 Growth & Stability", "🚨 Quality & Risk", "💰 ROI Analysis"])

    # --- TAB 1: GROWTH & STABILITY ---
    with tab1:
        st.subheader("Workforce Evolution")
        col_t1_1, col_t1_2 = st.columns([2, 1])
        
        with col_t1_1:
            # Stacked Area Chart
            fig_hc = px.area(
                df_hc_filtered, 
                x='Fecha', 
                y=['Leadtech', 'Randstad', 'Deel'],
                title="Headcount Evolution by Contract Type",
                color_discrete_map={'Leadtech': '#2c3e50', 'Randstad': '#e74c3c', 'Deel': '#f1c40f'},
                labels={'value': 'Headcount', 'variable': 'Workforce Segment'}
            )
            fig_hc.update_layout(hovermode="x unified")
            st.plotly_chart(fig_hc, use_container_width=True)
            
        with col_t1_2:
            st.info("""
            **Analyst Note:**
            - **Internal Growth (Leadtech):** Consistent upward trajectory indicates successful scaling.
            - **Agency Volatility (Randstad):** Extreme spikes (red area) show operational instability.
            - **Dependency:** Contractor usage (Deel) is solidifying as a permanent layer.
            """)
            
            # Dependency Metric
            ext_ratio = ((latest['Randstad'] + latest['Deel']) / total_hc) * 100
            st.metric("External Workforce Dependency", f"{ext_ratio:.1f}%", "Target: <20%")

    # --- TAB 2: QUALITY & RISK (The Diagnosis) ---
    with tab2:
        st.subheader("Why are people leaving?")
        
        col_t2_1, col_t2_2 = st.columns(2)
        
        with col_t2_1:
            # Donut Chart for Exit Types (Hardcoded Summary for Safety, can be dynamic)
            # 59 Disciplinary, 28 Objective, 40 Voluntary
            exit_data = pd.DataFrame({
                'Type': ['Voluntary (Regrettable)', 'Disciplinary (Performance)', 'Objective (Restructure)'],
                'Count': [40, 59, 28]
            })
            fig_pie = px.pie(exit_data, values='Count', names='Type', 
                             title="Exit Composition (2025)",
                             color='Type',
                             color_discrete_map={
                                 'Voluntary (Regrettable)': '#2ecc71',
                                 'Disciplinary (Performance)': '#e74c3c',
                                 'Objective (Restructure)': '#e67e22'
                             },
                             hole=0.6)
            st.plotly_chart(fig_pie, use_container_width=True)
            
        with col_t2_2:
            # Bar Chart: Exits by Department & Type
            df_exits_filtered = df_exits_dept[df_exits_dept['Dept_Unified'].isin(selected_depts)]
            
            fig_bar = px.bar(
                df_exits_filtered,
                x='Dept_Unified',
                y='Count',
                color='Type',
                title="Churn Hotspots by Department",
                barmode='stack',
                color_discrete_map={'Voluntary': '#2ecc71', 'Dismissal': '#e74c3c'}
            )
            st.plotly_chart(fig_bar, use_container_width=True)

        st.warning("""
        **🚩 Critical Insight:** The high volume of **Dismissals (Red)** in Product and CS suggests a breakdown in **Recruitment Quality** or **Onboarding**. 
        We are hiring candidates who fail to meet performance standards within the first year.
        """)

    # --- TAB 3: ROI ANALYSIS (Cost of Churn) ---
    with tab3:
        st.subheader("Training Investment Efficiency")
        
        # Aggregate Data for Scatter
        train_agg = df_training.groupby('Dept_Unified')['Investment'].sum().reset_index()
        exit_agg = df_exits_dept[df_exits_dept['Type'] == 'Voluntary'].groupby('Dept_Unified')['Count'].sum().reset_index()
        
        df_roi = pd.merge(train_agg, exit_agg, on='Dept_Unified', how='inner')
        df_roi = df_roi[df_roi['Dept_Unified'].isin(selected_depts)]
        
        col_t3_1, col_t3_2 = st.columns([3, 1])
        
        with col_t3_1:
            fig_scatter = px.scatter(
                df_roi,
                x='Investment',
                y='Count',
                size='Count',
                color='Dept_Unified',
                text='Dept_Unified',
                title="Cost Risk Matrix: Investment vs. Voluntary Exits",
                labels={'Investment': 'Training Spend (€)', 'Count': 'Voluntary Exits'},
                size_max=60
            )
            fig_scatter.update_traces(textposition='top center')
            fig_scatter.add_vline(x=df_roi['Investment'].mean(), line_dash="dash", annotation_text="Avg Spend")
            fig_scatter.add_hline(y=df_roi['Count'].mean(), line_dash="dash", annotation_text="Avg Churn")
            st.plotly_chart(fig_scatter, use_container_width=True)
            
        with col_t3_2:
            st.markdown("### Quadrant Analysis")
            st.markdown("""
            **Top-Right (High Spend, High Churn):**
            *Customer Service & Product*
            ⚠️ **Risk:** "Sunken Cost". We invest heavily in people who leave.
            
            **Bottom-Right (High Spend, Low Churn):**
            *Tech & IT*
            ✅ **Good ROI:** Training is likely aiding retention here.
            
            **Action:**
            Audit CS/Product training. Is it developmental or remedial?
            """)

else:
    st.info("Awaiting Data...")