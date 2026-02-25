import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="TalentIntel 2025",
    page_icon="\U0001f4ca",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- BRAND CONSTANTS ---
PINK   = "#e9437c"
PURPLE = "#a37dff"
BLUE   = "#4285f4"
GREEN  = "#44de97"
YELLOW = "#f7b53e"
DARK   = "#1e293b"
MUTED  = "#64748b"

# --- GLOBAL CSS ---
st.markdown(f"""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');
  html, body, [class*="css"] {{ font-family: 'Roboto', sans-serif !important; }}
  .block-container {{ padding-top: 1.5rem; padding-bottom: 3rem; }}

  .kpi-gradient {{
    background: linear-gradient(135deg, {BLUE}, {PURPLE});
    color: white; border-radius: 14px; padding: 1.5rem 1.8rem;
    box-shadow: 0 8px 24px rgba(66,133,244,0.25);
  }}
  .kpi-gradient .label {{
    font-size: 0.7rem; font-weight: 700; text-transform: uppercase;
    letter-spacing: 0.12em; opacity: 0.8; margin-bottom: 0.3rem;
  }}
  .kpi-gradient .value  {{ font-size: 3rem; font-weight: 700; line-height: 1; margin-bottom: 0.5rem; }}
  .kpi-gradient .badge  {{
    display: inline-flex; align-items: center; gap: 0.3rem;
    background: rgba(255,255,255,0.15); color: {PINK};
    font-size: 0.75rem; font-weight: 600; padding: 0.25rem 0.6rem; border-radius: 6px;
  }}

  .narrative-card {{
    background: white; border-radius: 14px; border-left: 4px solid {PINK};
    padding: 1.4rem 1.8rem; box-shadow: 0 2px 12px rgba(0,0,0,0.06); height: 100%;
  }}
  .narrative-card h3 {{ color: {DARK}; font-size: 1rem; font-weight: 700; margin: 0 0 0.5rem 0; }}
  .narrative-card p  {{ color: {MUTED}; font-size: 0.875rem; margin: 0; line-height: 1.6; }}

  .metric-tile {{
    background: white; border-radius: 12px; padding: 1.1rem 1.4rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06); border: 1px solid #f1f5f9;
  }}
  .metric-tile .mt-label  {{
    font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.1em;
    color: {MUTED}; font-weight: 700; margin-bottom: 0.3rem;
  }}
  .metric-tile .mt-value  {{ font-size: 1.6rem; font-weight: 700; color: {DARK}; line-height: 1.1; }}
  .metric-tile .mt-delta  {{ font-size: 0.75rem; margin-top: 0.3rem; font-weight: 500; }}

  .insight-card {{
    background: white; border-radius: 12px; padding: 1.3rem 1.4rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06); border: 1px solid #f1f5f9;
    border-top-width: 4px; height: 100%; transition: transform 0.2s ease;
  }}
  .insight-card:hover {{ transform: translateY(-3px); }}
  .insight-card .ic-icon-wrap {{
    display: inline-flex; align-items: center; justify-content: center;
    width: 36px; height: 36px; border-radius: 8px; font-size: 1.1rem; margin-bottom: 0.8rem;
  }}
  .insight-card h4    {{ font-size: 0.95rem; font-weight: 700; color: {DARK}; margin: 0 0 0.6rem 0; }}
  .insight-card p     {{ font-size: 0.82rem; color: {MUTED}; line-height: 1.55; margin: 0 0 0.8rem 0; }}
  .insight-card .rec-label {{
    font-size: 0.65rem; font-weight: 700; text-transform: uppercase;
    letter-spacing: 0.1em; color: {DARK}; border-top: 1px solid #f1f5f9; padding-top: 0.6rem;
  }}
  .insight-card .rec-text {{ font-size: 0.78rem; color: #94a3b8; margin-top: 0.3rem; line-height: 1.4; }}

  .risk-critical {{ background:#fff1f4; border:1px solid #fecdd8; border-radius:12px; padding:1rem; }}
  .risk-stable   {{ background:#f0fdf4; border:1px solid #bbf7d0; border-radius:12px; padding:1rem; }}
  .risk-medium   {{ background:#fffbeb; border:1px solid #fde68a; border-radius:12px; padding:1rem; }}
  .risk-neutral  {{ background:white;   border:1px solid #e2e8f0; border-radius:12px; padding:1rem; }}
  .risk-badge    {{
    font-size: 0.65rem; font-weight: 700; text-transform: uppercase;
    padding: 0.2rem 0.5rem; border-radius: 20px; float: right;
  }}
  .risk-badge.critical {{ background:rgba(233,67,124,0.12); color:{PINK}; }}
  .risk-badge.stable   {{ background:rgba(68,222,151,0.18); color:#16a34a; }}
  .risk-badge.medium   {{ background:rgba(247,181,62,0.18); color:#b45309; }}

  .cta-banner {{
    background: {DARK}; border-radius: 16px; padding: 2rem 2.5rem; color: white;
    overflow: hidden; box-shadow: 0 12px 32px rgba(30,41,59,0.3);
  }}
  .cta-banner h3 {{ font-size: 1.4rem; font-weight: 700; margin: 0 0 0.5rem 0; }}
  .cta-banner p  {{ font-size: 0.9rem; color: #94a3b8; margin: 0; line-height: 1.6; }}

  .app-header {{ display: flex; align-items: center; gap: 0.8rem; margin-bottom: 0.5rem; }}
  .app-header img {{ height: 44px; width: 44px; border-radius: 10px; }}
  .app-header .title {{ font-size: 1.3rem; font-weight: 700; color: {DARK}; }}
  .app-header .title span {{ color: {BLUE}; }}
</style>
""", unsafe_allow_html=True)


# ============================================================
# DATA PARSING HELPERS
# ============================================================

def parse_messy_table(df, start_keyword, end_condition_func, col_mapping=None):
    if df.empty:
        return pd.DataFrame()
    mask = df.apply(lambda row: row.astype(str).str.contains(start_keyword, case=False, na=False).any(), axis=1)
    start_idx = df[mask].index
    if len(start_idx) == 0:
        return pd.DataFrame()
    header_row_idx = start_idx[0] + 1
    if header_row_idx >= len(df):
        return pd.DataFrame()
    header_row = df.iloc[header_row_idx]
    data_rows = []
    for i in range(header_row_idx + 1, len(df)):
        row = df.iloc[i]
        if row.isna().all():
            continue
        if end_condition_func(row):
            break
        data_rows.append(row)
    if not data_rows:
        return pd.DataFrame()
    extracted_df = pd.DataFrame(data_rows)
    if col_mapping:
        actual_start_col = 0
        for col in range(header_row.shape[0]):
            if pd.notna(header_row.iloc[col]):
                actual_start_col = col
                break
        extracted_df = extracted_df.iloc[:, actual_start_col: actual_start_col + len(col_mapping)]
        if extracted_df.shape[1] == len(col_mapping):
            extracted_df.columns = col_mapping
    else:
        if extracted_df.shape[1] == len(header_row):
            extracted_df.columns = header_row
    return extracted_df


def normalize_departments(df, col_name):
    if df.empty or col_name not in df.columns:
        return df
    mapping = {
        'CUSTOMER SERVICE': 'Customer Service', 'CS': 'Customer Service',
        'PROJECT/PRODUCT': 'Product', 'Project/ Product': 'Product',
        'IT - DEVELOPER': 'Tech & IT', 'IT - BACKOFFICE': 'Tech & IT',
        'IT - UIUX': 'Tech & IT', 'IT - FRONT': 'Tech & IT',
        'IT ': 'Tech & IT', 'IT': 'Tech & IT',
        'HR-CORPORATE': 'HR', 'HR': 'HR',
        'Finance, Legal and Payments': 'Finance/Legal',
        'ACCOUNTING': 'Finance/Legal', 'TAX': 'Finance/Legal', 'PAYMENTS': 'Finance/Legal',
        'PAID MARKETING': 'Marketing', 'ORGANIC MARKETING': 'Marketing', 'SEO': 'Marketing',
        'DBI': 'Data & BI'
    }
    df['Dept_Unified'] = df[col_name].map(mapping).fillna('Other')
    return df


@st.cache_data
def load_and_process_data():
    result = {}
    try:
        hc_file = 'Headcount Evolution 2022-2026.xlsx'
        df_hc = pd.read_excel(hc_file, sheet_name='Hoja 1')
        df_hc['Fecha'] = pd.to_datetime(df_hc['Fecha'])
        df_hc = df_hc.sort_values('Fecha')
        for c in ['Leadtech', 'Randstad', 'Deel', 'Freelance']:
            if c in df_hc.columns:
                df_hc[c] = df_hc[c].fillna(0)
        result['hc'] = df_hc

        exits_file = '2025.xlsx'
        df_exits_raw = pd.read_excel(exits_file, sheet_name='Internal exits', header=None)
        df_vol = parse_messy_table(df_exits_raw, "Voluntary exit per Department",
                                   lambda r: pd.isna(r[0]) or str(r[0]).lower() == 'total',
                                   col_mapping=['Department', 'Count'])
        df_vol['Type'] = 'Voluntary'
        df_dis = parse_messy_table(df_exits_raw, "Disciplinary dismissal",
                                   lambda r: pd.isna(r[0]) or str(r[0]).lower() == 'total',
                                   col_mapping=['Department', 'Count'])
        df_dis['Type'] = 'Dismissal'
        df_exits = pd.concat([df_vol, df_dis])
        df_exits['Count'] = pd.to_numeric(df_exits['Count'], errors='coerce').fillna(0)
        result['exits_dept'] = normalize_departments(df_exits, 'Department')

        df_train_raw = pd.read_excel(exits_file, sheet_name='Training investment', header=None)
        df_train = parse_messy_table(df_train_raw, "Training investment by department",
                                     lambda r: pd.isna(r[0]) or str(r[0]).lower() == 'total',
                                     col_mapping=['Department', 'Investment', 'Hours'])
        df_train['Investment'] = pd.to_numeric(df_train['Investment'], errors='coerce').fillna(0)
        result['training'] = normalize_departments(df_train, 'Department')

        return result
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None


# ============================================================
# REFERENCE DATA (from presentation / HTML)
# ============================================================

HEADCOUNT_TREND = [
    {"date": "Mar 22", "Internal": 419, "Agency": 18, "Deel": 4},
    {"date": "Sep 22", "Internal": 522, "Agency": 44, "Deel": 2},
    {"date": "Mar 23", "Internal": 566, "Agency": 22, "Deel": 15},
    {"date": "Sep 23", "Internal": 588, "Agency": 36, "Deel": 25},
    {"date": "Jun 24", "Internal": 650, "Agency": 50, "Deel": 35},
    {"date": "Apr 25", "Internal": 707, "Agency": 64, "Deel": 33},
    {"date": "Oct 25", "Internal": 769, "Agency": 90, "Deel": 67},
    {"date": "Jan 26", "Internal": 684, "Agency": 53, "Deel": 50},
]

RISK_MATRIX = [
    {"name": "Customer Service", "investment": 11382, "voluntary": 29, "dismissal": 51, "totalExits": 80,  "headcount": 145, "color": PINK},
    {"name": "Product",          "investment": 10081, "voluntary": 12, "dismissal": 25, "totalExits": 37,  "headcount": 85,  "color": YELLOW},
    {"name": "Tech & IT",        "investment": 29500, "voluntary": 8,  "dismissal": 20, "totalExits": 28,  "headcount": 230, "color": GREEN},
    {"name": "Data & BI",        "investment": 6213,  "voluntary": 2,  "dismissal": 5,  "totalExits": 7,   "headcount": 45,  "color": PURPLE},
    {"name": "Marketing",        "investment": 6855,  "voluntary": 4,  "dismissal": 2,  "totalExits": 6,   "headcount": 55,  "color": BLUE},
]

EXIT_TYPE_DATA = [
    {"name": "Voluntary", "value": 55, "color": PURPLE},
    {"name": "Involuntary (Dismissal)", "value": 103, "color": PINK},
]

STRATEGY_CARDS = [
    {
        "title": "The Scaling Correction",
        "icon": "\u2696\ufe0f",
        "border_color": BLUE,
        "icon_bg": "#eff6ff",
        "insight": "We corrected the 2025 over-hiring (peak 941) down to <b>787</b>. The surge was a reactive response to ambitious targets without structural readiness.",
        "rec": "Formalize Q1 Headcount Planning linked strictly to CFO revenue forecasts. No req approval without P&amp;L justification.",
    },
    {
        "title": 'The "False Positive" Cost',
        "icon": "\u26a1",
        "border_color": PINK,
        "icon_bg": "#fff1f4",
        "insight": '59 "Disciplinary" exits are performance failures. Our assessments are ineffective, leading to "False Positive" hires.',
        "rec": "Replace subjective screening with objective technical assessments. Cap hiring volume to ensure quality validation.",
    },
    {
        "title": "The Governance Gap",
        "icon": "\U0001f4b0",
        "border_color": YELLOW,
        "icon_bg": "#fffbeb",
        "insight": "Lack of budgeting governance led to loose training spend (\u20ac87k). CS invests heavily in probationers subsequently fired for performance.",
        "rec": "Centralize training budget under HR. Freeze external training for &lt;6 months tenure until quality filter is fixed.",
    },
    {
        "title": "Delivery vs. Development",
        "icon": "\U0001f9e0",
        "border_color": PURPLE,
        "icon_bg": "#f5f3ff",
        "insight": "Culture prioritizes delivery over talent retention. Long-term employees were promoted on tenure without leadership assessment (Peter Principle risk).",
        "rec": "Audit all Team Leads with &gt;2 years tenure. Launch \"Manager Fundamentals\" to shift from output to team effectiveness.",
    },
    {
        "title": 'The "Partner" Illusion',
        "icon": "\U0001f310",
        "border_color": BLUE,
        "icon_bg": "#eff6ff",
        "insight": "Deel staff are effectively internal employees abroad, yet churn at ~40%. Treating them as \"external partners\" is damaging retention.",
        "rec": "Harmonize onboarding and feedback loops. Treat Deel staff as FTEs for all culture and performance programs.",
    },
    {
        "title": "Quantity vs. Quality",
        "icon": "\U0001f4a1",
        "border_color": GREEN,
        "icon_bg": "#f0fdf4",
        "insight": "Focus on delivery volume has overshadowed efficient retention. High churn in Product/IT signals burnout and lack of strategic direction.",
        "rec": "Executive roadshows to clarify 2026 Strategy. Shift measurement from \"Output Volume\" to \"Strategic Impact\".",
    },
]


# ============================================================
# HEADER (always visible)
# ============================================================
st.markdown("""
<div class="app-header">
  <img src="https://media.licdn.com/dms/image/v2/C4E0BAQGm6GIMqyYrbg/company-logo_200_200/company-logo_200_200/0/1656910905863/leadtech_group_logo?e=1770854400&v=beta&t=O6E2jtBpxrtCZWGFAQArQQkkipK_4MDLAUyEZftIGrY"
       alt="Leadtech" />
  <div class="title">Talent<span>Intel</span></div>
</div>
<div style="color:#64748b; font-size:0.9rem; margin-bottom:1.5rem;">
  2025 Workforce Intelligence Review &mdash; Strategic analysis of H1&ndash;H2 performance data
</div>
""", unsafe_allow_html=True)


# ============================================================
# LOAD DATA
# ============================================================
data = load_and_process_data()

if data:
    df_hc       = data['hc']
    df_exits    = data['exits_dept']
    df_training = data['training']

    # --------------------------------------------------------
    # SIDEBAR
    # --------------------------------------------------------
    st.sidebar.markdown("## \U0001f39b\ufe0f Controls")
    st.sidebar.subheader("Timeframe")
    min_date = df_hc['Fecha'].min().date()
    max_date = df_hc['Fecha'].max().date()
    start_date, end_date = st.sidebar.date_input("Select Range", [min_date, max_date])
    mask = (df_hc['Fecha'].dt.date >= start_date) & (df_hc['Fecha'].dt.date <= end_date)
    df_hc_filtered = df_hc.loc[mask]

    all_depts = sorted(list(set(df_training['Dept_Unified'].unique()) | set(df_exits['Dept_Unified'].unique())))
    selected_depts = st.sidebar.multiselect("Filter Departments", all_depts, default=all_depts)
    st.sidebar.divider()
    st.sidebar.caption("\U0001f4cc Data sourced from 2025.xlsx & Headcount Evolution 2022-2026.xlsx")

    # --------------------------------------------------------
    # KPI HEADER ROW
    # --------------------------------------------------------
    col_kpi_left, col_kpi_right = st.columns([1, 3])
    with col_kpi_left:
        st.markdown(f"""
        <div class="kpi-gradient">
          <div class="label">Total Active</div>
          <div class="value">787</div>
          <div class="badge">\u2193 -16% Rightsized</div>
        </div>
        """, unsafe_allow_html=True)

    with col_kpi_right:
        st.markdown(f"""
        <div class="narrative-card">
          <h3>\U0001f6e1\ufe0f Strategic Correction: Stability Achieved (941 &rarr; 787)</h3>
          <p>Following the unorganized scaling of 2025, we have successfully
          <strong>rightsized the organization by -16%</strong> (primarily Agency reduction).
          The focus for 2026 is strictly on <strong>Quality of Hire</strong>
          and stabilizing the core Deel &amp; Internal teams.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Four mini metric tiles
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"""<div class="metric-tile">
          <div class="mt-label">Dismissal Rate</div>
          <div class="mt-value" style="color:{PINK};">18.2%</div>
          <div class="mt-delta" style="color:{PINK};">\u26a0 Critical Risk</div>
        </div>""", unsafe_allow_html=True)
    with m2:
        st.markdown(f"""<div class="metric-tile">
          <div class="mt-label">eNPS Score</div>
          <div class="mt-value" style="color:{YELLOW};">11.8</div>
          <div class="mt-delta" style="color:{YELLOW};">\u26a1 Fragile / Watch</div>
        </div>""", unsafe_allow_html=True)
    with m3:
        st.markdown(f"""<div class="metric-tile">
          <div class="mt-label">Training Spend</div>
          <div class="mt-value">\u20ac87k</div>
          <div class="mt-delta" style="color:{MUTED};">Governance gap identified</div>
        </div>""", unsafe_allow_html=True)
    with m4:
        st.markdown(f"""<div class="metric-tile">
          <div class="mt-label">Agency Dependency</div>
          <div class="mt-value" style="color:{BLUE};">6.7%</div>
          <div class="mt-delta" style="color:{GREEN};">\u2713 Down from 9.6%</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br><hr>", unsafe_allow_html=True)

    # --------------------------------------------------------
    # TABS
    # --------------------------------------------------------
    tab1, tab2, tab3 = st.tabs([
        "\U0001f3af Executive Briefing",
        "\U0001f4c8 Growth & Velocity",
        "\u26a1 Efficiency & Risk"
    ])

    # --- TAB 1: EXECUTIVE BRIEFING ---
    with tab1:
        st.markdown("### Executive Briefing: The \"So What?\"")
        st.markdown(
            f"<div style='color:{MUTED}; margin-bottom:1.5rem; font-size:0.9rem;'>"
            "Six strategic insights distilled from 2025 data &mdash; each with a recommended action."
            "</div>",
            unsafe_allow_html=True
        )

        for row_start in range(0, len(STRATEGY_CARDS), 3):
            row_cards = STRATEGY_CARDS[row_start: row_start + 3]
            cols = st.columns(3)
            for col, card in zip(cols, row_cards):
                with col:
                    st.markdown(f"""
                    <div class="insight-card" style="border-top-color:{card['border_color']};">
                      <div class="ic-icon-wrap" style="background:{card['icon_bg']};">{card['icon']}</div>
                      <h4>{card['title']}</h4>
                      <p><strong>Insight:</strong> {card['insight']}</p>
                      <div class="rec-label">Recommendation</div>
                      <div class="rec-text">{card['rec']}</div>
                    </div>
                    """, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(f"""
        <div class="cta-banner">
          <h3>Ready to act?</h3>
          <p>The data suggests that <strong style="color:white;">slowing down</strong> hiring velocity
          to fix the quality filter will actually <strong style="color:white;">accelerate</strong>
          net productive headcount in 2026.</p>
        </div>
        """, unsafe_allow_html=True)

    # --- TAB 2: GROWTH & VELOCITY ---
    with tab2:
        col_g1, col_g2 = st.columns([2, 1])

        with col_g1:
            df_trend = pd.DataFrame(HEADCOUNT_TREND)
            fig_area = go.Figure()
            fig_area.add_trace(go.Scatter(
                x=df_trend['date'], y=df_trend['Internal'],
                name='FTEs (Internal)', mode='lines',
                line=dict(color=BLUE, width=3),
                fill='tozeroy', fillcolor='rgba(66,133,244,0.08)'
            ))
            fig_area.add_trace(go.Scatter(
                x=df_trend['date'], y=df_trend['Agency'],
                name='Contingent (Agency)', mode='lines',
                line=dict(color=YELLOW, width=2), fill='none'
            ))
            fig_area.add_trace(go.Scatter(
                x=df_trend['date'], y=df_trend['Deel'],
                name='Deel (Remote FTE)', mode='lines',
                line=dict(color=PURPLE, width=2, dash='dot'), fill='none'
            ))
            fig_area.add_vrect(
                x0="Oct 25", x1="Jan 26",
                fillcolor=PINK, opacity=0.07,
                annotation_text="Rightsizing", annotation_position="top left",
                annotation_font_color=PINK
            )
            fig_area.update_layout(
                title=dict(text="Workforce Velocity (2022\u20132026)", font=dict(size=15, color=DARK)),
                plot_bgcolor='white', paper_bgcolor='white',
                xaxis=dict(showgrid=False, showline=False, tickfont=dict(color=MUTED)),
                yaxis=dict(showgrid=True, gridcolor='#f1f5f9', showline=False, tickfont=dict(color=MUTED)),
                legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='left', x=0,
                            font=dict(size=11, color=MUTED)),
                hovermode='x unified',
                margin=dict(l=0, r=0, t=50, b=0)
            )
            st.plotly_chart(fig_area, use_container_width=True)

        with col_g2:
            df_exit_pie = pd.DataFrame(EXIT_TYPE_DATA)
            fig_donut = go.Figure(go.Pie(
                labels=df_exit_pie['name'],
                values=df_exit_pie['value'],
                hole=0.62,
                marker=dict(colors=[PURPLE, PINK]),
                textinfo='none',
                hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Share: %{percent}<extra></extra>'
            ))
            fig_donut.update_layout(
                title=dict(text="Exit Composition (2025)", font=dict(size=13, color=DARK)),
                showlegend=True,
                legend=dict(orientation='h', y=-0.1, font=dict(size=11, color=MUTED)),
                margin=dict(l=0, r=0, t=50, b=30),
                plot_bgcolor='white', paper_bgcolor='white',
                annotations=[dict(
                    text="<b>65%</b><br>Involuntary", x=0.5, y=0.5,
                    font=dict(size=13, color=DARK), showarrow=False
                )]
            )
            st.plotly_chart(fig_donut, use_container_width=True)

            st.markdown(f"""
            <div style="background:#f0fdf4; border:1px solid #bbf7d0; border-radius:10px;
                        padding:0.9rem 1rem; font-size:0.82rem; color:#15803d; margin-top:0.5rem;">
            \u2705 <strong>Stability signal:</strong> Workforce rightsized to 787.
            Agency dependency reduced from 90 &rarr; 53.
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("Churn Hotspots by Department")

        df_exits_filtered = df_exits[df_exits['Dept_Unified'].isin(selected_depts)]
        fig_bar = px.bar(
            df_exits_filtered,
            x='Dept_Unified', y='Count', color='Type',
            barmode='stack',
            color_discrete_map={'Voluntary': PURPLE, 'Dismissal': PINK},
            labels={'Dept_Unified': 'Department', 'Count': 'Exits'},
        )
        fig_bar.update_layout(
            plot_bgcolor='white', paper_bgcolor='white',
            xaxis=dict(showgrid=False, showline=False, tickfont=dict(color=MUTED)),
            yaxis=dict(showgrid=True, gridcolor='#f1f5f9', showline=False, tickfont=dict(color=MUTED)),
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='left', x=0,
                        title_text='', font=dict(size=11, color=MUTED)),
            margin=dict(l=0, r=0, t=30, b=0)
        )
        st.plotly_chart(fig_bar, use_container_width=True)

        st.markdown(f"""
        <div style="background:#fff1f4; border:1px solid #fecdd8; border-radius:10px;
                    padding:0.9rem 1rem; font-size:0.83rem; color:#9f1239;">
        \U0001f6a9 <strong>Critical Insight:</strong> The high volume of Dismissals in Product and CS suggests
        a breakdown in <strong>Recruitment Quality</strong> or <strong>Onboarding</strong>.
        </div>
        """, unsafe_allow_html=True)

    # --- TAB 3: EFFICIENCY & RISK ---
    with tab3:
        col_r1, col_r2 = st.columns([2, 1])

        with col_r1:
            df_rm = pd.DataFrame(RISK_MATRIX)
            fig_scatter = go.Figure()
            for _, row in df_rm.iterrows():
                fig_scatter.add_trace(go.Scatter(
                    x=[row['investment']], y=[row['totalExits']],
                    mode='markers+text',
                    name=row['name'],
                    text=[row['name']],
                    textposition='top center',
                    marker=dict(
                        size=row['headcount'] / 5,
                        color=row['color'],
                        opacity=0.85,
                        line=dict(width=2, color='white')
                    ),
                    hovertemplate=(
                        f"<b>{row['name']}</b><br>"
                        f"Training Spend: \u20ac{row['investment']:,}<br>"
                        f"Total Exits: {row['totalExits']}<br>"
                        f"Dismissals: {row['dismissal']}<br>"
                        f"Voluntary: {row['voluntary']}<extra></extra>"
                    )
                ))
            mean_invest = df_rm['investment'].mean()
            mean_exits  = df_rm['totalExits'].mean()
            fig_scatter.add_vline(x=mean_invest, line_dash="dash", line_color="#94a3b8",
                                  annotation_text="Avg Spend", annotation_font_color=MUTED)
            fig_scatter.add_hline(y=mean_exits, line_dash="dash", line_color="#94a3b8",
                                  annotation_text="Avg Churn", annotation_font_color=MUTED)
            fig_scatter.update_layout(
                title=dict(text="Efficiency Matrix: Training Investment vs. Total Exits",
                           font=dict(size=15, color=DARK)),
                xaxis=dict(title="Training Spend (\u20ac)", showgrid=True, gridcolor='#f1f5f9',
                           showline=False, tickfont=dict(color=MUTED)),
                yaxis=dict(title="Total Exits", showgrid=True, gridcolor='#f1f5f9',
                           showline=False, tickfont=dict(color=MUTED)),
                plot_bgcolor='white', paper_bgcolor='white',
                showlegend=False,
                margin=dict(l=0, r=0, t=50, b=0)
            )
            st.plotly_chart(fig_scatter, use_container_width=True)

        with col_r2:
            st.markdown("### Risk Diagnosis")
            st.markdown(f"""
            <div class="risk-critical" style="margin-bottom:0.8rem;">
              <span class="risk-badge critical">CRITICAL</span>
              <strong style="color:#9f1239;">Customer Service</strong>
              <p style="font-size:0.82rem; color:#be123c; margin:0.4rem 0 0.5rem 0;">
                Highest churn (80 exits) despite heavy training (\u20ac11k).
              </p>
              <div style="background:white; border:1px solid #fecdd8; border-radius:6px;
                          padding:0.4rem 0.6rem; font-family:monospace; font-size:0.75rem; color:#9f1239;">
                1 Dismissal per \u20ac223 spent
              </div>
            </div>
            <div class="risk-stable" style="margin-bottom:0.8rem;">
              <span class="risk-badge stable">STABLE</span>
              <strong style="color:#166534;">Tech &amp; IT</strong>
              <p style="font-size:0.82rem; color:#15803d; margin:0.4rem 0 0.5rem 0;">
                High investment (\u20ac29k) correlates with lower relative churn.
              </p>
              <div style="background:white; border:1px solid #bbf7d0; border-radius:6px;
                          padding:0.4rem 0.6rem; font-family:monospace; font-size:0.75rem; color:#166534;">
                1 Dismissal per \u20ac1,475 spent
              </div>
            </div>
            <div class="risk-medium" style="margin-bottom:0.8rem;">
              <span class="risk-badge medium">HIGH</span>
              <strong style="color:#92400e;">Product</strong>
              <p style="font-size:0.82rem; color:#b45309; margin:0.4rem 0 0;">
                High regrettable turnover (12 voluntary).
                Exit interviews cite &ldquo;Lack of Strategic Vision.&rdquo;
              </p>
            </div>
            <div class="risk-neutral">
              <strong style="color:{DARK};">Marketing / Data &amp; BI</strong>
              <p style="font-size:0.82rem; color:{MUTED}; margin:0.4rem 0 0;">
                Low churn, proportionate training. Monitor as org stabilises.
              </p>
            </div>
            """, unsafe_allow_html=True)

        # Live ROI from parsed Excel data
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("Live Data: Training ROI by Department")
        train_agg = df_training.groupby('Dept_Unified')['Investment'].sum().reset_index()
        exit_agg  = df_exits[df_exits['Type'] == 'Voluntary'].groupby('Dept_Unified')['Count'].sum().reset_index()
        df_roi    = pd.merge(train_agg, exit_agg, on='Dept_Unified', how='inner')
        df_roi    = df_roi[df_roi['Dept_Unified'].isin(selected_depts)]

        if not df_roi.empty:
            fig_roi = px.scatter(
                df_roi, x='Investment', y='Count',
                size='Count', color='Dept_Unified', text='Dept_Unified',
                labels={'Investment': 'Training Spend (\u20ac)', 'Count': 'Voluntary Exits',
                        'Dept_Unified': 'Department'},
                size_max=60,
                color_discrete_sequence=[PINK, PURPLE, BLUE, GREEN, YELLOW]
            )
            fig_roi.update_traces(textposition='top center')
            if len(df_roi) > 1:
                fig_roi.add_vline(x=df_roi['Investment'].mean(), line_dash="dash",
                                  line_color="#94a3b8", annotation_text="Avg Spend")
                fig_roi.add_hline(y=df_roi['Count'].mean(), line_dash="dash",
                                  line_color="#94a3b8", annotation_text="Avg Churn")
            fig_roi.update_layout(
                plot_bgcolor='white', paper_bgcolor='white', showlegend=False,
                xaxis=dict(showgrid=True, gridcolor='#f1f5f9', showline=False,
                           tickfont=dict(color=MUTED)),
                yaxis=dict(showgrid=True, gridcolor='#f1f5f9', showline=False,
                           tickfont=dict(color=MUTED)),
                margin=dict(l=0, r=0, t=20, b=0)
            )
            st.plotly_chart(fig_roi, use_container_width=True)
        else:
            st.info("No ROI data available for selected departments.")

else:
    st.info("\u23f3 Awaiting data... Please ensure the Excel files are in the app directory.")
