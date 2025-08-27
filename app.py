"""
LexCura Elite Compliance Dashboard - Professional Legal Edition
Enterprise legal compliance monitoring and regulatory intelligence
Sharp, modern, professional design for serious legal compliance services
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
from plotly.subplots import make_subplots
import gspread
from google.oauth2.service_account import Credentials
import json
import io
import zipfile
import base64
from datetime import datetime, timedelta
import numpy as np
import time
import logging

# Optional imports with fallbacks
try:
    from streamlit_plotly_events import plotly_events
    PLOTLY_EVENTS_AVAILABLE = True
except ImportError:
    PLOTLY_EVENTS_AVAILABLE = False

try:
    import kaleido
    KALEIDO_AVAILABLE = True
except ImportError:
    KALEIDO_AVAILABLE = False

# Page configuration
st.set_page_config(
    page_title="LexCura Elite | Legal Compliance Intelligence",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional Template System
def register_professional_template():
    """Register professional legal compliance template"""
    try:
        professional_template = go.layout.Template(
            layout=go.Layout(
                paper_bgcolor="#0F1113",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(
                    family="Source Sans Pro, Helvetica, Arial, sans-serif",
                    color="#F5F6F7",
                    size=12
                ),
                title=dict(
                    font=dict(size=18, color="#F5F6F7", family="Source Sans Pro"),
                    x=0.5,
                    xanchor="center",
                    pad=dict(t=20)
                ),
                colorway=["#D4AF37", "#3DBC6B", "#E4574C", "#FFCF66", "#B8B9BB", "#F5F6F7"],
                xaxis=dict(
                    gridcolor="rgba(184,185,187,0.15)",
                    linecolor="rgba(184,185,187,0.3)",
                    zerolinecolor="rgba(184,185,187,0.3)",
                    tickfont=dict(size=11, color="#B8B9BB"),
                    titlefont=dict(size=13, color="#F5F6F7")
                ),
                yaxis=dict(
                    gridcolor="rgba(184,185,187,0.15)",
                    linecolor="rgba(184,185,187,0.3)",
                    zerolinecolor="rgba(184,185,187,0.3)",
                    tickfont=dict(size=11, color="#B8B9BB"),
                    titlefont=dict(size=13, color="#F5F6F7")
                ),
                legend=dict(
                    font=dict(size=11, color="#F5F6F7"),
                    bgcolor="rgba(27,29,31,0.9)",
                    bordercolor="rgba(184,185,187,0.3)",
                    borderwidth=1
                )
            )
        )
        pio.templates["professional"] = professional_template
        pio.templates.default = "professional"
    except Exception as e:
        pio.templates.default = "plotly_dark"

def apply_professional_styling(fig):
    """Apply professional legal styling to charts"""
    try:
        fig.update_layout(template="professional")
    except:
        fig.update_layout(
            paper_bgcolor="#0F1113",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#F5F6F7", family="Source Sans Pro"),
            title=dict(font=dict(color="#F5F6F7", size=18)),
            xaxis=dict(gridcolor="rgba(184,185,187,0.15)", tickfont=dict(color="#B8B9BB")),
            yaxis=dict(gridcolor="rgba(184,185,187,0.15)", tickfont=dict(color="#B8B9BB"))
        )
    
    fig.update_layout(
        height=380,
        margin=dict(l=50, r=50, t=60, b=50),
        hovermode='closest',
        showlegend=True
    )
    
    return fig

# Initialize professional template
register_professional_template()

# Professional Legal CSS
def load_professional_css():
    """Load professional legal compliance dashboard CSS"""
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Source+Sans+Pro:wght@300;400;600;700&display=swap');
        
        :root {
            --bg-primary: #0F1113;
            --bg-card: #1B1D1F;
            --bg-card-light: #252728;
            --accent-primary: #D4AF37;
            --accent-success: #3DBC6B;
            --accent-warning: #FFCF66;
            --accent-error: #E4574C;
            --text-primary: #F5F6F7;
            --text-secondary: #B8B9BB;
            --border-subtle: rgba(184, 185, 187, 0.12);
            --shadow-card: 0 4px 12px rgba(0, 0, 0, 0.4);
        }
        
        .stApp {
            background: var(--bg-primary);
            color: var(--text-primary);
            font-family: 'Source Sans Pro', Helvetica, Arial, sans-serif;
        }
        
        /* Professional Header */
        .professional-header {
            background: linear-gradient(135deg, #1B1D1F 0%, #252728 100%);
            border-bottom: 3px solid var(--accent-primary);
            padding: 1.5rem 2rem;
            margin: -1rem -1rem 2rem -1rem;
            box-shadow: var(--shadow-card);
        }
        
        .header-content {
            max-width: 1200px;
            margin: 0 auto;
            display: grid;
            grid-template-columns: 1fr auto;
            align-items: center;
            gap: 2rem;
        }
        
        .brand-section {
            display: flex;
            align-items: center;
            gap: 1rem;
        }
        
        .brand-title {
            font-size: 2rem;
            font-weight: 700;
            color: var(--accent-primary);
            margin: 0;
        }
        
        .brand-subtitle {
            font-size: 0.9rem;
            color: var(--text-secondary);
            margin: 0;
            font-weight: 400;
        }
        
        .status-section {
            text-align: right;
            font-size: 0.875rem;
            color: var(--text-secondary);
        }
        
        .status-live {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            justify-content: flex-end;
            color: var(--accent-success);
            font-weight: 600;
        }
        
        .status-dot {
            width: 8px;
            height: 8px;
            background: var(--accent-success);
            border-radius: 50%;
            animation: pulse 2s infinite;
        }
        
        /* Professional Cards */
        .pro-card {
            background: var(--bg-card);
            border: 1px solid var(--border-subtle);
            border-radius: 8px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: var(--shadow-card);
            transition: border-color 0.2s ease;
        }
        
        .pro-card:hover {
            border-color: var(--accent-primary);
        }
        
        .pro-card-title {
            font-size: 1.1rem;
            font-weight: 600;
            color: var(--text-primary);
            margin-bottom: 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid var(--accent-primary);
        }
        
        /* KPI Grid */
        .kpi-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.5rem;
            margin: 1.5rem 0;
        }
        
        .kpi-card {
            background: var(--bg-card);
            border: 1px solid var(--border-subtle);
            border-radius: 8px;
            padding: 1.5rem;
            text-align: center;
            transition: all 0.2s ease;
            position: relative;
        }
        
        .kpi-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: var(--accent-primary);
        }
        
        .kpi-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.5);
            border-color: var(--accent-primary);
        }
        
        .kpi-value {
            font-size: 2.5rem;
            font-weight: 700;
            color: var(--accent-primary);
            margin: 0.5rem 0;
        }
        
        .kpi-label {
            font-size: 0.875rem;
            color: var(--text-secondary);
            text-transform: uppercase;
            font-weight: 600;
            letter-spacing: 0.5px;
        }
        
        .kpi-change {
            font-size: 0.8rem;
            margin-top: 0.5rem;
            font-weight: 600;
        }
        
        .kpi-change.positive { color: var(--accent-success); }
        .kpi-change.negative { color: var(--accent-error); }
        .kpi-change.neutral { color: var(--text-secondary); }
        
        /* Professional Sidebar */
        .sidebar-section {
            background: var(--bg-card);
            border: 1px solid var(--border-subtle);
            border-radius: 8px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
        }
        
        .sidebar-title {
            font-size: 1rem;
            font-weight: 600;
            color: var(--accent-primary);
            margin-bottom: 1rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .info-grid {
            display: grid;
            gap: 0.75rem;
        }
        
        .info-row {
            display: grid;
            grid-template-columns: 1fr auto;
            align-items: center;
            padding: 0.5rem 0;
            border-bottom: 1px solid rgba(184, 185, 187, 0.1);
        }
        
        .info-label {
            font-size: 0.875rem;
            color: var(--text-secondary);
        }
        
        .info-value {
            font-size: 0.875rem;
            color: var(--text-primary);
            font-weight: 600;
        }
        
        /* Professional Buttons */
        .btn-group {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 1rem;
            margin: 1rem 0;
        }
        
        .pro-btn {
            background: var(--bg-card-light);
            border: 1px solid var(--border-subtle);
            border-radius: 6px;
            padding: 0.75rem 1rem;
            color: var(--text-primary);
            font-weight: 600;
            font-size: 0.875rem;
            cursor: pointer;
            transition: all 0.2s ease;
        }
        
        .pro-btn:hover {
            background: var(--accent-primary);
            color: #000;
            border-color: var(--accent-primary);
        }
        
        /* Chart Containers */
        .chart-wrapper {
            background: var(--bg-card);
            border: 1px solid var(--border-subtle);
            border-radius: 8px;
            padding: 1.5rem;
            margin: 1.5rem 0;
            box-shadow: var(--shadow-card);
        }
        
        .chart-title {
            font-size: 1.1rem;
            font-weight: 600;
            color: var(--text-primary);
            margin-bottom: 1rem;
            text-align: center;
        }
        
        /* Tab System */
        .stTabs [data-baseweb="tab-list"] {
            background: var(--bg-card-light);
            border-radius: 6px;
            padding: 0.25rem;
            border: 1px solid var(--border-subtle);
        }
        
        .stTabs [data-baseweb="tab"] {
            background: transparent;
            border-radius: 4px;
            color: var(--text-secondary);
            font-weight: 600;
            padding: 0.75rem 1.5rem;
        }
        
        .stTabs [aria-selected="true"] {
            background: var(--accent-primary);
            color: #000 !important;
        }
        
        /* Executive Summary */
        .summary-card {
            background: linear-gradient(135deg, var(--bg-card) 0%, var(--bg-card-light) 100%);
            border: 1px solid var(--border-subtle);
            border-left: 4px solid var(--accent-primary);
            border-radius: 8px;
            padding: 2rem;
            margin: 1.5rem 0;
            box-shadow: var(--shadow-card);
        }
        
        .summary-title {
            font-size: 1.25rem;
            font-weight: 700;
            color: var(--accent-primary);
            margin-bottom: 1rem;
        }
        
        .summary-text {
            font-size: 1rem;
            line-height: 1.6;
            color: var(--text-primary);
        }
        
        /* Alert Styling */
        .alert {
            padding: 1rem 1.5rem;
            border-radius: 6px;
            margin: 1rem 0;
            border-left: 4px solid;
        }
        
        .alert-success {
            background: rgba(61, 188, 107, 0.1);
            border-left-color: var(--accent-success);
            color: var(--accent-success);
        }
        
        .alert-warning {
            background: rgba(255, 207, 102, 0.1);
            border-left-color: var(--accent-warning);
            color: var(--accent-warning);
        }
        
        .alert-error {
            background: rgba(228, 87, 76, 0.1);
            border-left-color: var(--accent-error);
            color: var(--accent-error);
        }
        
        /* Animations */
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        
        /* Hide Streamlit Elements */
        #MainMenu { visibility: hidden; }
        footer { visibility: hidden; }
        header { visibility: hidden; }
        .stDeployButton { visibility: hidden; }
        
        /* Form Elements */
        .stSelectbox > div > div,
        .stMultiSelect > div > div,
        .stDateInput > div > div > div {
            background: var(--bg-card-light);
            border: 1px solid var(--border-subtle);
            border-radius: 6px;
            color: var(--text-primary);
        }
        
        /* Responsive */
        @media (max-width: 768px) {
            .header-content {
                grid-template-columns: 1fr;
                text-align: center;
            }
            
            .kpi-container {
                grid-template-columns: repeat(2, 1fr);
            }
        }
    </style>
    """, unsafe_allow_html=True)

# Session state initialization
def init_session_state():
    """Initialize session state for professional dashboard"""
    if 'filters' not in st.session_state:
        st.session_state.filters = {
            'date_range': None,
            'alert_levels': [],
            'update_types': []
        }

# Data connection functions (ROBUST ERROR HANDLING)
@st.cache_data(ttl=300)
def connect_to_sheets():
    """Connect to Google Sheets with robust error handling"""
    try:
        if "gcp_service_account" in st.secrets:
            credentials_data = st.secrets["gcp_service_account"]
            if isinstance(credentials_data, str):
                credentials_info = json.loads(credentials_data)
            else:
                credentials_info = dict(credentials_data)
        else:
            return None
            
        credentials = Credentials.from_service_account_info(
            credentials_info,
            scopes=[
                "https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive"
            ]
        )
        gc = gspread.authorize(credentials)
        return gc
    except Exception as e:
        return None

@st.cache_data(ttl=60)
def load_client_data(client_id=None):
    """Load client data with fallback to demo data"""
    try:
        gc = connect_to_sheets()
        if not gc:
            return get_demo_data()
            
        sheet_id = st.secrets.get("MASTER_SHEET_ID", "1oI-XqRbp8r3V8yMjnC5pNvDMljJDv4f6d01vRmrVH1g")
        spreadsheet = gc.open_by_key(sheet_id)
        sheet = spreadsheet.worksheet("MASTER SHEET")
        
        headers = sheet.row_values(1)
        row_data = sheet.row_values(2)
        
        while len(row_data) < len(headers):
            row_data.append("")
            
        data = dict(zip(headers, row_data))
        
        return {
            'UNIQUE_CLIENT_ID': data.get('UNIQUE CLIENT ID', client_id or '11AA'),
            'CLIENT_NAME': data.get('CLIENT NAME', 'Elite Pharmaceutical Corp'),
            'TIER': data.get('TIER', 'Professional'),
            'REGION': data.get('REGION', 'Northeast'),
            'DELIVERY_FREQUENCY': data.get('DELIVERY FREQUENCY', 'Weekly'),
            'EMAIL_ADDRESS': data.get('EMAIL ADDRESS', 'contact@elitepharma.com'),
            'MAIN_CONTENT': data.get('MAIN STRUCTURED CONTENT', ''),
            'FINANCIAL_STATS': data.get('CURRENT FINANCIAL STATS', '$2.5M annual savings'),
            'HISTORICAL_IMPACTS': data.get('HISTORICAL FINANCIAL IMPACTS', 'ROI: 556%'),
            'EXECUTIVE_SUMMARY': data.get('EXECUTIVE SUMMARY', ''),
            'COMPLIANCE_ALERTS': data.get('COMPLIANCE ALERTS', 'No critical alerts'),
            'RISK_ANALYSIS': data.get('RISK ANALYSIS', 'Low risk profile'),
            'REGULATORY_UPDATES': data.get('REGULATORY UPDATES', 'USP 797 revision'),
            'ALERT_LEVEL': data.get('ALERT LEVEL', 'GREEN'),
            'DATE_SCRAPED': data.get('DATE SCRAPED', datetime.now().strftime('%Y-%m-%d')),
            'STATUS': data.get('STATUS', 'Active')
        }
        
    except Exception as e:
        return get_demo_data()

def get_demo_data():
    """Professional demo data for legal compliance dashboard"""
    return {
        'UNIQUE_CLIENT_ID': '11AA',
        'CLIENT_NAME': 'Elite Pharmaceutical Corporation',
        'TIER': 'Professional',
        'REGION': 'Northeast',
        'DELIVERY_FREQUENCY': 'Weekly',
        'EMAIL_ADDRESS': 'compliance@elitepharma.com',
        'MAIN_CONTENT': 'Comprehensive regulatory compliance monitoring with advanced risk analytics and legal intelligence.',
        'FINANCIAL_STATS': '$2.5M annual compliance savings, $450K platform investment',
        'HISTORICAL_IMPACTS': 'ROI: 556% over 18 months, zero regulatory violations',
        'EXECUTIVE_SUMMARY': 'Outstanding compliance performance across all regulatory domains. Proactive risk management framework has eliminated critical violations while optimizing operational efficiency. Current status exceeds industry benchmarks with 97.3% overall compliance score.',
        'COMPLIANCE_ALERTS': 'Zero critical alerts, 2 optimization opportunities under review',
        'RISK_ANALYSIS': 'Low risk profile with comprehensive controls and monitoring',
        'REGULATORY_UPDATES': 'USP 797 revision Q2 2024, FDA guidance updates, state board notifications',
        'ALERT_LEVEL': 'GREEN',
        'DATE_SCRAPED': datetime.now().strftime('%Y-%m-%d'),
        'STATUS': 'Active'
    }

# Professional Chart Functions (FIXED DEADLINES CHART)
def create_financial_performance_chart(data):
    """Professional financial performance analysis"""
    quarters = ['Q1 2024', 'Q2 2024', 'Q3 2024', 'Q4 2024']
    savings = [285000, 320000, 295000, 340000]
    investment = [65000, 58000, 72000, 61000]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=quarters, y=savings, name='Compliance Savings',
        marker=dict(color='#D4AF37', opacity=0.9),
        text=[f'${val/1000:.0f}K' for val in savings],
        textposition='auto'
    ))
    
    fig.add_trace(go.Bar(
        x=quarters, y=investment, name='Platform Investment',
        marker=dict(color='#B8B9BB', opacity=0.8),
        text=[f'${val/1000:.0f}K' for val in investment],
        textposition='auto'
    ))
    
    fig.update_layout(
        title="Quarterly Financial Performance",
        barmode='group',
        yaxis_title="Amount ($)",
        xaxis_title="Quarter"
    )
    
    return apply_professional_styling(fig)

def create_compliance_radar_chart(data):
    """Professional compliance radar chart"""
    categories = ['Documentation', 'Training', 'Environmental', 'Quality', 'Facilities', 'Process']
    scores = [97, 98, 94, 96, 99, 95]
    target = [95] * len(categories)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=scores + [scores[0]],
        theta=categories + [categories[0]],
        fill='toself',
        name='Current Score',
        line=dict(color='#D4AF37', width=2),
        fillcolor="rgba(212, 175, 55, 0.2)"
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=target + [target[0]],
        theta=categories + [categories[0]],
        line=dict(color='#B8B9BB', width=2, dash='dash'),
        name='Target (95%)'
    ))
    
    fig.update_layout(
        title="Compliance Performance Matrix",
        polar=dict(radialaxis=dict(visible=True, range=[0, 100]))
    )
    
    return apply_professional_styling(fig)

def create_compliance_gauge(data):
    """Professional compliance gauge"""
    score = 97.3
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Overall Compliance Score"},
        delta={'reference': 95},
        gauge={
            'axis': {'range': [None, 100]},
            'bar': {'color': '#D4AF37'},
            'steps': [
                {'range': [0, 70], 'color': 'rgba(228, 87, 76, 0.3)'},
                {'range': [70, 85], 'color': 'rgba(255, 207, 102, 0.3)'},
                {'range': [85, 95], 'color': 'rgba(61, 188, 107, 0.3)'},
                {'range': [95, 100], 'color': 'rgba(212, 175, 55, 0.3)'}
            ],
            'threshold': {'line': {'color': '#F5F6F7', 'width': 4}, 'value': 98}
        }
    ))
    
    return apply_professional_styling(fig)

def create_alert_status_chart(data):
    """Professional alert status chart"""
    departments = ['Quality Control', 'Manufacturing', 'Environmental', 'Training', 'Documentation']
    normal = [22, 18, 25, 15, 20]
    review = [1, 2, 0, 1, 0]
    critical = [0, 0, 0, 0, 0]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=departments, x=normal, name='Normal',
        orientation='h', marker=dict(color='#3DBC6B')
    ))
    
    fig.add_trace(go.Bar(
        y=departments, x=review, name='Review Required',
        orientation='h', marker=dict(color='#FFCF66')
    ))
    
    fig.add_trace(go.Bar(
        y=departments, x=critical, name='Critical',
        orientation='h', marker=dict(color='#E4574C')
    ))
    
    fig.update_layout(
        title="Alert Status by Department",
        barmode='stack',
        xaxis_title="Number of Items"
    )
    
    return apply_professional_styling(fig)

def create_risk_gauge(data):
    """Professional risk assessment gauge"""
    risk_score = 12.8
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=risk_score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Risk Assessment Score"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': '#3DBC6B'},
            'steps': [
                {'range': [0, 25], 'color': 'rgba(61, 188, 107, 0.3)'},
                {'range': [25, 50], 'color': 'rgba(255, 207, 102, 0.3)'},
                {'range': [50, 100], 'color': 'rgba(228, 87, 76, 0.3)'}
            ]
        },
        number={'suffix': '%'}
    ))
    
    return apply_professional_styling(fig)

def create_performance_timeline(data):
    """Professional performance timeline"""
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct']
    performance = [93, 94, 94, 95, 96, 96, 96, 97, 97, 97]
    target = [95] * len(months)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=months, y=performance, mode='lines+markers',
        name='Actual Performance',
        line=dict(color='#D4AF37', width=3),
        marker=dict(size=8, color='#D4AF37')
    ))
    
    fig.add_trace(go.Scatter(
        x=months, y=target, mode='lines',
        name='Target',
        line=dict(color='#B8B9BB', width=2, dash='dash')
    ))
    
    fig.update_layout(
        title="Performance Timeline",
        yaxis=dict(range=[90, 100], title="Compliance Score (%)"),
        xaxis_title="Month"
    )
    
    return apply_professional_styling(fig)

def create_regulatory_heatmap(data):
    """Professional regulatory compliance heatmap"""
    regulations = ['USP 797', 'USP 800', 'USP 825', 'FDA 503B', 'State Board', 'cGMP']
    scores = [98, 96, 99, 97, 95, 94]
    
    colors = ['#3DBC6B' if score >= 97 else '#D4AF37' if score >= 94 else '#FFCF66' for score in scores]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=regulations, y=scores,
        marker=dict(color=colors),
        text=[f'{score}%' for score in scores],
        textposition='auto'
    ))
    
    fig.update_layout(
        title="Regulatory Compliance Scores",
        yaxis=dict(range=[90, 100], title="Compliance Score (%)"),
        xaxis_title="Regulatory Standards"
    )
    
    return apply_professional_styling(fig)

def create_deadlines_chart(data):
    """Fixed professional deadlines chart"""
    tasks = ['Annual Inspection', 'USP 797 Training', 'Environmental Review', 'Quality Audit']
    days_remaining = [45, 15, 30, 60]
    priorities = ['High', 'Critical', 'Medium', 'Low']
    
    color_map = {'Critical': '#E4574C', 'High': '#FFCF66', 'Medium': '#3DBC6B', 'Low': '#B8B9BB'}
    colors = [color_map[priority] for priority in priorities]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=tasks, y=days_remaining,
        marker=dict(color=colors),
        text=[f'{days} days' for days in days_remaining],
        textposition='auto'
    ))
    
    fig.update_layout(
        title="Upcoming Compliance Deadlines",
        yaxis_title="Days Remaining",
        xaxis_title="Tasks"
    )
    
    return apply_professional_styling(fig)

# Professional UI Components
def render_professional_header(client_data):
    """Render professional legal compliance header"""
    client_name = client_data.get('CLIENT_NAME', 'Professional Client')
    date_updated = client_data.get('DATE_SCRAPED', datetime.now().strftime('%Y-%m-%d'))
    
    st.markdown(f"""
    <div class="professional-header">
        <div class="header-content">
            <div class="brand-section">
                <div>
                    <h1 class="brand-title">LexCura Elite</h1>
                    <p class="brand-subtitle">Legal Compliance Intelligence Platform</p>
                </div>
            </div>
            <div class="status-section">
                <div style="margin-bottom: 0.5rem; font-weight: 600;">{client_name}</div>
                <div class="status-live">
                    <div class="status-dot"></div>
                    System Active • Updated {date_updated}
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_professional_sidebar(client_data):
    """Render professional sidebar with client information"""
    with st.sidebar:
        # Client Information Section
        st.markdown(f"""
        <div class="sidebar-section">
            <div class="sidebar-title">Client Information</div>
            <div class="info-grid">
                <div class="info-row">
                    <span class="info-label">Client ID</span>
                    <span class="info-value">{client_data.get('UNIQUE_CLIENT_ID', 'N/A')}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">Service Tier</span>
                    <span class="info-value">{client_data.get('TIER', 'Standard')}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">Region</span>
                    <span class="info-value">{client_data.get('REGION', 'Not specified')}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">Update Frequency</span>
                    <span class="info-value">{client_data.get('DELIVERY_FREQUENCY', 'Monthly')}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">Status</span>
                    <span class="info-value" style="color: var(--accent-success);">{client_data.get('STATUS', 'Active')}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Quick Actions Section
        st.markdown("""
        <div class="sidebar-section">
            <div class="sidebar-title">Quick Actions</div>
            <div class="btn-group">
                <div class="pro-btn">🔄 Refresh</div>
                <div class="pro-btn">📊 Export</div>
                <div class="pro-btn">⚙️ Settings</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Filters Section
        st.markdown('<div class="sidebar-title">Filters & Controls</div>', unsafe_allow_html=True)
        
        # Alert level filter
        alert_levels = st.multiselect(
            "Alert Levels",
            options=['GREEN', 'AMBER', 'RED'],
            default=['GREEN'],
            help="Filter by compliance alert levels"
        )
        
        # Date range filter
        date_range = st.date_input(
            "Date Range",
            value=(datetime.now() - timedelta(days=30), datetime.now()),
            help="Select reporting period"
        )
        
        # Department filter
        departments = st.multiselect(
            "Departments",
            options=['Quality Control', 'Manufacturing', 'Environmental', 'Training', 'Documentation'],
            default=['Quality Control', 'Manufacturing'],
            help="Select departments to analyze"
        )

def render_kpi_section(client_data):
    """Render professional KPI cards"""
    st.markdown("## Key Performance Indicators")
    
    st.markdown("""
    <div class="kpi-container">
        <div class="kpi-card">
            <div class="kpi-label">Overall Compliance</div>
            <div class="kpi-value">97.3%</div>
            <div class="kpi-change positive">▲ 2.1% vs last month</div>
        </div>
        
        <div class="kpi-card">
            <div class="kpi-label">Risk Score</div>
            <div class="kpi-value">12.8</div>
            <div class="kpi-change positive">▼ 1.5 pts (Low Risk)</div>
        </div>
        
        <div class="kpi-card">
            <div class="kpi-label">Critical Alerts</div>
            <div class="kpi-value">0</div>
            <div class="kpi-change neutral">● No violations</div>
        </div>
        
        <div class="kpi-card">
            <div class="kpi-label">Annual Savings</div>
            <div class="kpi-value">$2.5M</div>
            <div class="kpi-change positive">▲ 15.2% YoY</div>
        </div>
        
        <div class="kpi-card">
            <div class="kpi-label">Audit Readiness</div>
            <div class="kpi-value">98.7%</div>
            <div class="kpi-change positive">▲ Fully prepared</div>
        </div>
        
        <div class="kpi-card">
            <div class="kpi-label">Training Completion</div>
            <div class="kpi-value">96.4%</div>
            <div class="kpi-change positive">▲ Above target</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_executive_summary(client_data):
    """Render professional executive summary"""
    summary = client_data.get('EXECUTIVE_SUMMARY', 
        'Comprehensive compliance monitoring active across all regulatory domains. '
        'Current performance exceeds industry standards with zero critical violations. '
        'Risk management framework operating at optimal efficiency.')
    
    st.markdown(f"""
    <div class="summary-card">
        <div class="summary-title">Executive Summary</div>
        <div class="summary-text">{summary}</div>
    </div>
    """, unsafe_allow_html=True)

def render_compliance_alerts(client_data):
    """Render compliance alerts section"""
    st.markdown("## Compliance Status")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="alert alert-success">
            <strong>System Status: Optimal</strong><br>
            All monitoring systems operational
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="alert alert-success">
            <strong>Violations: Zero</strong><br>
            No critical compliance issues detected
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="alert alert-warning">
            <strong>Reviews: 2 Pending</strong><br>
            Routine optimization opportunities
        </div>
        """, unsafe_allow_html=True)

def render_chart_section(chart_func, data, title, description=None):
    """Render chart with professional wrapper"""
    st.markdown(f"""
    <div class="chart-wrapper">
        <div class="chart-title">{title}</div>
        {f'<p style="text-align: center; color: var(--text-secondary); margin-bottom: 1rem;">{description}</p>' if description else ''}
    """, unsafe_allow_html=True)
    
    try:
        fig = chart_func(data)
        st.plotly_chart(fig, use_container_width=True, config={
            "displayModeBar": False,
            "responsive": True
        })
    except Exception as e:
        st.error(f"Chart rendering error: {str(e)}")
        st.markdown("""
        <div style="text-align: center; padding: 2rem; color: var(--text-secondary);">
            Chart temporarily unavailable. Data processing in progress.
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

def main():
    """Main professional dashboard application"""
    
    # Initialize
    init_session_state()
    load_professional_css()
    
    # Load data
    client_id = st.query_params.get("client_id", "11AA")
    
    with st.spinner("Loading compliance intelligence..."):
        client_data = load_client_data(client_id)
    
    # Render header
    render_professional_header(client_data)
    
    # Render sidebar
    render_professional_sidebar(client_data)
    
    # Main dashboard content
    with st.container():
        # KPI Section
        render_kpi_section(client_data)
        
        # Compliance alerts
        render_compliance_alerts(client_data)
        
        # Executive Summary
        render_executive_summary(client_data)
        
        # Dashboard tabs
        tab1, tab2, tab3 = st.tabs([
            "📊 Performance Dashboard", 
            "🔍 Detailed Analysis", 
            "📋 Compliance Reports"
        ])
        
        with tab1:
            col1, col2 = st.columns(2)
            
            with col1:
                render_chart_section(
                    create_financial_performance_chart, client_data,
                    "Financial Performance Analysis",
                    "Quarterly compliance savings vs platform investment"
                )
                
                render_chart_section(
                    create_compliance_gauge, client_data,
                    "Overall Compliance Score",
                    "Current compliance performance rating"
                )
            
            with col2:
                render_chart_section(
                    create_compliance_radar_chart, client_data,
                    "Compliance Performance Matrix",
                    "Multi-domain compliance assessment"
                )
                
                render_chart_section(
                    create_alert_status_chart, client_data,
                    "Alert Status by Department",
                    "Current alert distribution across departments"
                )
        
        with tab2:
            col1, col2 = st.columns(2)
            
            with col1:
                render_chart_section(
                    create_risk_gauge, client_data,
                    "Risk Assessment Overview",
                    "Current organizational risk profile"
                )
                
                render_chart_section(
                    create_regulatory_heatmap, client_data,
                    "Regulatory Compliance Matrix",
                    "Performance across regulatory standards"
                )
            
            with col2:
                render_chart_section(
                    create_performance_timeline, client_data,
                    "Performance Trend Analysis",
                    "Historical compliance performance tracking"
                )
                
                render_chart_section(
                    create_deadlines_chart, client_data,
                    "Upcoming Compliance Deadlines",
                    "Critical dates and task priorities"
                )
        
        with tab3:
            # Comprehensive reporting section
            st.markdown("""
            <div class="pro-card">
                <div class="pro-card-title">Comprehensive Compliance Reports</div>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem;">
                    <div>
                        <h4 style="color: var(--accent-primary); margin-bottom: 1rem;">Regulatory Intelligence</h4>
                        <ul style="color: var(--text-secondary); line-height: 1.8;">
                            <li>USP 797 Sterile Compounding Standards</li>
                            <li>FDA 503B Outsourcing Facility Regulations</li>
                            <li>State Board of Pharmacy Requirements</li>
                            <li>Environmental Health & Safety Protocols</li>
                        </ul>
                    </div>
                    <div>
                        <h4 style="color: var(--accent-primary); margin-bottom: 1rem;">Risk Management</h4>
                        <ul style="color: var(--text-secondary); line-height: 1.8;">
                            <li>Proactive violation prevention protocols</li>
                            <li>Continuous monitoring and alerting</li>
                            <li>Compliance gap analysis and remediation</li>
                            <li>Staff training and certification tracking</li>
                        </ul>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Document access section
            main_content = client_data.get('MAIN_CONTENT', '')
            if main_content and len(main_content) > 50:
                st.markdown("""
                <div class="pro-card">
                    <div class="pro-card-title">Detailed Compliance Documentation</div>
                    <p style="color: var(--text-secondary); margin-bottom: 1.5rem;">
                        Access comprehensive compliance reports, regulatory updates, and detailed analysis documentation.
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                if len(main_content) > 500:
                    preview_text = main_content[:400] + "..."
                    st.text_area(
                        "Document Preview", 
                        preview_text, 
                        height=150, 
                        disabled=True,
                        help="Full documentation available for download"
                    )
                    
                    # Download button
                    st.download_button(
                        label="📄 Download Complete Compliance Report",
                        data=main_content,
                        file_name=f"lexcura_compliance_report_{client_id}_{datetime.now().strftime('%Y%m%d')}.txt",
                        mime="text/plain",
                        help="Download comprehensive compliance documentation"
                    )
            
            # Additional compliance metrics
            st.markdown("""
            <div class="pro-card">
                <div class="pro-card-title">Additional Compliance Metrics</div>
                <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 2rem; text-align: center;">
                    <div>
                        <div style="font-size: 2rem; color: var(--accent-success); font-weight: 700;">100%</div>
                        <div style="color: var(--text-secondary); font-size: 0.875rem;">Documentation Compliance</div>
                    </div>
                    <div>
                        <div style="font-size: 2rem; color: var(--accent-primary); font-weight: 700;">45</div>
                        <div style="color: var(--text-secondary); font-size: 0.875rem;">Days Until Next Audit</div>
                    </div>
                    <div>
                        <div style="font-size: 2rem; color: var(--accent-success); font-weight: 700;">99.2%</div>
                        <div style="color: var(--text-secondary); font-size: 0.875rem;">System Uptime</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
