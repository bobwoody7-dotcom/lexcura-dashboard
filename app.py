"""
LexCura Elite Compliance Dashboard - Luxury Enterprise Edition
£10k/month premium service - Executive-grade template system
Preserves original Google Sheets data logic with luxury UI upgrade
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

try:
    from streamlit_lottie import st_lottie
    import requests
    LOTTIE_AVAILABLE = True
except ImportError:
    LOTTIE_AVAILABLE = False

# Page configuration
st.set_page_config(
    page_title="LexCura Elite",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Luxury Template System - Premium Color Palette
def register_luxury_template():
    """Register the luxury executive template with refined color palette"""
    try:
        luxury_template = go.layout.Template(
            layout=go.Layout(
                paper_bgcolor="#0F1113",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(
                    family="Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
                    color="#F5F6F7",
                    size=13
                ),
                title=dict(
                    font=dict(size=24, color="#F5F6F7", family="Inter"),
                    x=0.5,
                    xanchor="center",
                    pad=dict(t=20)
                ),
                colorway=["#D4AF37", "#FFCF66", "#3DBC6B", "#E4574C", "#B8B9BB", "#F5F6F7", "#252728"],
                xaxis=dict(
                    gridcolor="rgba(184,185,187,0.1)",
                    linecolor="rgba(184,185,187,0.2)",
                    zerolinecolor="rgba(184,185,187,0.2)",
                    tickfont=dict(size=12, color="#B8B9BB", family="Inter"),
                    titlefont=dict(size=14, color="#F5F6F7", family="Inter")
                ),
                yaxis=dict(
                    gridcolor="rgba(184,185,187,0.1)",
                    linecolor="rgba(184,185,187,0.2)",
                    zerolinecolor="rgba(184,185,187,0.2)",
                    tickfont=dict(size=12, color="#B8B9BB", family="Inter"),
                    titlefont=dict(size=14, color="#F5F6F7", family="Inter")
                ),
                legend=dict(
                    font=dict(size=12, color="#F5F6F7", family="Inter"),
                    bgcolor="rgba(27,29,31,0.8)",
                    bordercolor="rgba(184,185,187,0.2)",
                    borderwidth=1
                ),
                hoverlabel=dict(
                    bgcolor="rgba(27,29,31,0.95)",
                    bordercolor="#D4AF37",
                    font=dict(color="#F5F6F7", family="Inter")
                )
            )
        )
        pio.templates["luxury_executive"] = luxury_template
        pio.templates.default = "luxury_executive"
    except Exception as e:
        pio.templates.default = "plotly_dark"

def apply_luxury_styling(fig):
    """Apply luxury executive styling to Plotly figures"""
    try:
        fig.update_layout(template="luxury_executive")
    except:
        # Fallback styling
        fig.update_layout(
            paper_bgcolor="#0F1113",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#F5F6F7", family="Inter, sans-serif", size=13),
            title=dict(font=dict(color="#F5F6F7", size=24, family="Inter")),
            xaxis=dict(gridcolor="rgba(184,185,187,0.1)", tickfont=dict(color="#B8B9BB")),
            yaxis=dict(gridcolor="rgba(184,185,187,0.1)", tickfont=dict(color="#B8B9BB"))
        )
    
    # Premium styling enhancements
    fig.update_layout(
        height=420,
        margin=dict(l=60, r=60, t=70, b=60),
        transition_duration=400,
        hovermode='closest',
        showlegend=True
    )
    
    # Clean marker styling
    try:
        fig.update_traces(
            marker_line_width=0,
            hoverlabel=dict(
                bgcolor="rgba(27,29,31,0.95)",
                bordercolor="#D4AF37",
                font=dict(size=12, family="Inter")
            )
        )
    except:
        pass
    
    return fig

# Initialize luxury template
register_luxury_template()

# Luxury CSS Styling - Enterprise Grade
def load_luxury_css():
    """Load comprehensive luxury executive dashboard CSS"""
    st.markdown("""
    <style>
        /* Import premium fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        
        :root {
            --bg-primary: #0F1113;
            --bg-card: #1B1D1F;
            --bg-card-light: #252728;
            --accent-gold: #D4AF37;
            --accent-highlight: #FFCF66;
            --text-muted: #B8B9BB;
            --text-primary: #F5F6F7;
            --error: #E4574C;
            --success: #3DBC6B;
            --shadow-premium: 0 8px 32px rgba(0, 0, 0, 0.4);
            --shadow-subtle: 0 4px 16px rgba(0, 0, 0, 0.2);
            --border-subtle: rgba(184, 185, 187, 0.08);
            --gradient-gold: linear-gradient(135deg, #D4AF37 0%, #FFCF66 100%);
            --gradient-bg: linear-gradient(135deg, #0F1113 0%, #1B1D1F 100%);
        }
        
        /* Global App Styling */
        .stApp {
            background: var(--gradient-bg);
            color: var(--text-primary);
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            font-weight: 400;
            line-height: 1.6;
        }
        
        /* Executive Header */
        .luxury-header {
            background: linear-gradient(90deg, rgba(212, 175, 55, 0.08), rgba(255, 207, 102, 0.04));
            backdrop-filter: blur(24px);
            border-bottom: 2px solid var(--accent-gold);
            padding: 2rem 3rem;
            margin: -2rem -2rem 3rem -2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: var(--shadow-subtle);
            position: sticky;
            top: 0;
            z-index: 1000;
            animation: slideDownLuxury 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        }
        
        .brand-section {
            display: flex;
            align-items: center;
            gap: 1.5rem;
        }
        
        .brand-title {
            font-size: 2.25rem;
            font-weight: 800;
            color: var(--accent-gold);
            margin: 0;
            letter-spacing: -0.02em;
            background: var(--gradient-gold);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .premium-badge {
            background: var(--gradient-gold);
            color: #000;
            padding: 0.5rem 1rem;
            border-radius: 8px;
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            box-shadow: var(--shadow-subtle);
        }
        
        .header-status {
            display: flex;
            flex-direction: column;
            align-items: flex-end;
            gap: 0.5rem;
            color: var(--text-muted);
            font-size: 0.875rem;
            font-weight: 500;
        }
        
        .status-live {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            color: var(--success);
            font-weight: 600;
        }
        
        .status-indicator {
            width: 8px;
            height: 8px;
            background: var(--success);
            border-radius: 50%;
            animation: pulse 2s infinite;
        }
        
        /* Premium Card System */
        .luxury-card {
            background: var(--bg-card);
            border: 1px solid var(--border-subtle);
            border-radius: 16px;
            padding: 2rem;
            margin: 1.5rem 0;
            box-shadow: var(--shadow-premium);
            transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
            position: relative;
            overflow: hidden;
        }
        
        .luxury-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: var(--gradient-gold);
            opacity: 0.8;
        }
        
        .luxury-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 12px 48px rgba(212, 175, 55, 0.2);
            border-color: rgba(212, 175, 55, 0.3);
        }
        
        .luxury-card-light {
            background: var(--bg-card-light);
            border: 1px solid rgba(184, 185, 187, 0.12);
        }
        
        /* Executive KPI System */
        .kpi-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 2rem;
            margin: 2rem 0;
        }
        
        .kpi-card-luxury {
            background: linear-gradient(135deg, var(--bg-card) 0%, var(--bg-card-light) 100%);
            border: 1px solid var(--border-subtle);
            border-radius: 20px;
            padding: 2.5rem 2rem;
            text-align: center;
            position: relative;
            transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
            box-shadow: var(--shadow-premium);
            overflow: hidden;
        }
        
        .kpi-card-luxury::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: var(--gradient-gold);
        }
        
        .kpi-card-luxury:hover {
            transform: translateY(-6px) scale(1.02);
            border-color: var(--accent-gold);
            box-shadow: 0 16px 64px rgba(212, 175, 55, 0.25);
        }
        
        .kpi-value-luxury {
            font-size: 3rem;
            font-weight: 800;
            color: var(--accent-gold);
            line-height: 1;
            margin-bottom: 1rem;
            letter-spacing: -0.02em;
        }
        
        .kpi-title-luxury {
            font-size: 0.875rem;
            color: var(--text-muted);
            text-transform: uppercase;
            font-weight: 600;
            letter-spacing: 0.1em;
            margin-bottom: 0.5rem;
        }
        
        .kpi-change {
            font-size: 0.875rem;
            font-weight: 600;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.25rem;
            margin-top: 1rem;
        }
        
        .kpi-change.positive { color: var(--success); }
        .kpi-change.negative { color: var(--error); }
        .kpi-change.neutral { color: var(--text-muted); }
        
        /* Premium Sidebar */
        .sidebar-luxury {
            background: var(--bg-card);
            border: 1px solid var(--border-subtle);
            border-radius: 16px;
            padding: 2rem;
            margin-bottom: 2rem;
            box-shadow: var(--shadow-premium);
        }
        
        .sidebar-title-luxury {
            color: var(--accent-gold);
            font-weight: 700;
            font-size: 1.25rem;
            margin-bottom: 1.5rem;
            letter-spacing: -0.01em;
        }
        
        .client-info {
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }
        
        .info-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0.75rem;
            background: var(--bg-card-light);
            border-radius: 8px;
            border-left: 3px solid var(--accent-gold);
        }
        
        .info-label {
            font-weight: 600;
            color: var(--text-muted);
            font-size: 0.875rem;
        }
        
        .info-value {
            font-weight: 600;
            color: var(--text-primary);
            font-size: 0.875rem;
        }
        
        /* Premium Buttons */
        .luxury-button-group {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 1rem;
            margin: 2rem 0;
        }
        
        .luxury-button {
            background: linear-gradient(135deg, var(--bg-card-light), var(--bg-card));
            border: 1px solid var(--border-subtle);
            border-radius: 12px;
            padding: 1rem;
            color: var(--text-primary);
            font-weight: 600;
            font-size: 0.875rem;
            text-align: center;
            transition: all 0.2s ease;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.5rem;
        }
        
        .luxury-button:hover {
            background: var(--gradient-gold);
            color: #000;
            transform: translateY(-2px);
            box-shadow: var(--shadow-subtle);
            border-color: var(--accent-gold);
        }
        
        /* Chart Containers */
        .chart-container-luxury {
            background: var(--bg-card);
            border: 1px solid var(--border-subtle);
            border-radius: 20px;
            padding: 2.5rem;
            margin: 2rem 0;
            box-shadow: var(--shadow-premium);
            position: relative;
            transition: all 0.3s ease;
        }
        
        .chart-container-luxury:hover {
            border-color: rgba(212, 175, 55, 0.3);
            box-shadow: 0 12px 48px rgba(0, 0, 0, 0.5);
        }
        
        .chart-title-luxury {
            color: var(--text-primary);
            font-size: 1.375rem;
            font-weight: 700;
            margin-bottom: 2rem;
            text-align: center;
            letter-spacing: -0.01em;
        }
        
        /* Tab System */
        .stTabs [data-baseweb="tab-list"] {
            background: var(--bg-card-light);
            border-radius: 12px;
            padding: 0.5rem;
            margin: 2rem 0;
            border: 1px solid var(--border-subtle);
        }
        
        .stTabs [data-baseweb="tab"] {
            background: transparent;
            border-radius: 8px;
            color: var(--text-muted);
            font-weight: 600;
            padding: 1rem 2rem;
            transition: all 0.2s ease;
        }
        
        .stTabs [aria-selected="true"] {
            background: var(--gradient-gold);
            color: #000 !important;
            box-shadow: var(--shadow-subtle);
        }
        
        /* Executive Summary */
        .executive-summary {
            background: linear-gradient(135deg, var(--bg-card) 0%, var(--bg-card-light) 100%);
            border: 1px solid var(--border-subtle);
            border-radius: 20px;
            padding: 3rem;
            margin: 2rem 0;
            box-shadow: var(--shadow-premium);
            position: relative;
        }
        
        .executive-summary::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: var(--gradient-gold);
            border-radius: 20px 20px 0 0;
        }
        
        .summary-title {
            color: var(--accent-gold);
            font-size: 1.5rem;
            font-weight: 800;
            margin-bottom: 2rem;
            letter-spacing: -0.01em;
        }
        
        .summary-content {
            font-size: 1.125rem;
            line-height: 1.8;
            color: var(--text-primary);
            font-weight: 400;
        }
        
        /* Animations */
        @keyframes slideDownLuxury {
            from { 
                transform: translateY(-100%); 
                opacity: 0; 
            }
            to { 
                transform: translateY(0); 
                opacity: 1; 
            }
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        
        @keyframes fadeInUpLuxury {
            from { 
                transform: translateY(30px); 
                opacity: 0; 
            }
            to { 
                transform: translateY(0); 
                opacity: 1; 
            }
        }
        
        .fade-in-luxury {
            animation: fadeInUpLuxury 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94) forwards;
        }
        
        /* Form Elements */
        .stSelectbox > div > div {
            background: var(--bg-card-light);
            border: 1px solid var(--border-subtle);
            border-radius: 12px;
            color: var(--text-primary);
        }
        
        .stMultiSelect > div > div {
            background: var(--bg-card-light);
            border: 1px solid var(--border-subtle);
            border-radius: 12px;
        }
        
        .stDateInput > div > div > div {
            background: var(--bg-card-light);
            border: 1px solid var(--border-subtle);
            border-radius: 12px;
            color: var(--text-primary);
        }
        
        /* Hide Streamlit Elements */
        #MainMenu { visibility: hidden; }
        footer { visibility: hidden; }
        header { visibility: hidden; }
        .stDeployButton { visibility: hidden; }
        
        /* Responsive Design */
        @media (max-width: 768px) {
            .luxury-header {
                flex-direction: column;
                gap: 1rem;
                padding: 1.5rem;
            }
            
            .brand-title {
                font-size: 1.75rem;
            }
            
            .kpi-grid {
                grid-template-columns: repeat(2, 1fr);
                gap: 1rem;
            }
            
            .luxury-button-group {
                grid-template-columns: 1fr;
            }
        }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    """Initialize session state variables for luxury dashboard"""
    if 'filters' not in st.session_state:
        st.session_state.filters = {
            'date_range': None,
            'alert_levels': [],
            'update_types': [],
            'selected_data': None
        }
    
    if 'saved_views' not in st.session_state:
        st.session_state.saved_views = {}
    
    if 'drill_down_data' not in st.session_state:
        st.session_state.drill_down_data = None

# Data connection functions (PRESERVED from original)
@st.cache_data(ttl=300)
def connect_to_sheets():
    """Connect to Google Sheets using service account credentials"""
    try:
        credentials_info = json.loads(st.secrets["gcp_service_account"])
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
        st.error(f"Google Sheets connection failed: {str(e)}")
        return None

@st.cache_data(ttl=60)
def load_client_data(client_id=None):
    """Load client data from Google Sheets ROW 2 ONLY"""
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
            'UNIQUE CLIENT ID': data.get('UNIQUE CLIENT ID', client_id or '11AA'),
            'CLIENT NAME': data.get('CLIENT NAME', 'Elite Pharmaceutical Corp'),
            'TIER': data.get('TIER', 'Professional'),
            'REGION': data.get('REGION', 'Northeast'),
            'DELIVERY FREQUENCY': data.get('DELIVERY FREQUENCY', 'Weekly'),
            'EMAIL ADDRESS': data.get('EMAIL ADDRESS', 'contact@elitepharma.com'),
            'MAIN STRUCTURED CONTENT': data.get('MAIN STRUCTURED CONTENT', ''),
            'CURRENT FINANCIAL STATS': data.get('CURRENT FINANCIAL STATS', '$2.5M annual savings'),
            'HISTORICAL FINANCIAL IMPACTS': data.get('HISTORICAL FINANCIAL IMPACTS', 'ROI: 556%'),
            'EXECUTIVE SUMMARY': data.get('EXECUTIVE SUMMARY', 'Strong compliance performance with proactive risk management framework delivering exceptional results.'),
            'DETECTION': data.get('DETECTION', 'Automated monitoring active'),
            'COMPLIANCE ALERTS': data.get('COMPLIANCE ALERTS', 'No critical alerts, 3 items for review'),
            'RISK ANALYSIS': data.get('RISK ANALYSIS', 'Low risk profile, excellent controls'),
            'REGULATORY UPDATES': data.get('REGULATORY UPDATES', 'USP 797 revision Q2 2024'),
            'URGENCY': data.get('URGENCY', 'Standard'),
            'ALERT LEVEL': data.get('ALERT LEVEL', 'GREEN'),
            'DATE SCRAPED': data.get('DATE SCRAPED', datetime.now().strftime('%Y-%m-%d')),
            'STATUS': data.get('STATUS', 'Active'),
            'TYPE OF UPDATE': data.get('TYPE OF UPDATE', 'Routine Monitoring'),
            'DATE DELIVERED': data.get('DATE DELIVERED', datetime.now().strftime('%Y-%m-%d')),
            'EDUCATIONAL GUIDE AND TOOLS': data.get('EDUCATIONAL GUIDE AND TOOLS', 'Training materials updated')
        }
        
    except Exception as e:
        st.warning(f"Live data unavailable: {str(e)}")
        return get_demo_data()

def get_demo_data():
    """Premium demo data for luxury dashboard"""
    return {
        'UNIQUE CLIENT ID': '11AA',
        'CLIENT NAME': 'Elite Pharmaceutical Corp',
        'TIER': 'Professional',
        'REGION': 'Northeast',
        'DELIVERY FREQUENCY': 'Weekly',
        'EMAIL ADDRESS': 'contact@elitepharma.com',
        'MAIN STRUCTURED CONTENT': 'Comprehensive compliance monitoring and regulatory intelligence with advanced risk analytics.',
        'CURRENT FINANCIAL STATS': '$2.5M annual savings, $450K compliance investment',
        'HISTORICAL FINANCIAL IMPACTS': 'ROI: 556% over 18 months, $12.3M total value delivered',
        'EXECUTIVE SUMMARY': 'Outstanding compliance performance with world-class risk management framework. Consistently exceeding industry benchmarks while maintaining operational excellence across all regulatory domains.',
        'DETECTION': 'AI-powered monitoring with 99.7% accuracy',
        'COMPLIANCE ALERTS': 'Zero critical alerts, 2 optimization opportunities identified',
        'RISK ANALYSIS': 'Exceptionally low risk profile with best-in-class controls',
        'REGULATORY UPDATES': 'USP 797 revision Q2 2024, FDA guidance March 2024, EU Annex 1 updates',
        'URGENCY': 'Standard',
        'ALERT LEVEL': 'GREEN',
        'DATE SCRAPED': datetime.now().strftime('%Y-%m-%d'),
        'STATUS': 'Active',
        'TYPE OF UPDATE': 'Comprehensive Intelligence',
        'DATE DELIVERED': datetime.now().strftime('%Y-%m-%d'),
        'EDUCATIONAL GUIDE AND TOOLS': 'Executive training portal with advanced analytics'
    }

# Luxury Chart Functions with Premium Styling
def chart_financial_impact_luxury(data):
    """Premium Financial Impact Analysis"""
    categories = ['Q1 2024', 'Q2 2024', 'Q3 2024', 'Q4 2024', 'Q1 2025 (Proj)']
    savings = [285000, 320000, 295000, 340000, 375000]
    investment = [65000, 58000, 72000, 61000, 68000]
    roi_pct = [438, 552, 410, 557, 551]
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Cost savings bars
    fig.add_trace(go.Bar(
        x=categories, y=savings, name='Cost Savings',
        marker=dict(color='#D4AF37', opacity=0.9),
        text=['$' + f'{val/1000:.0f}K' for val in savings],
        textposition='auto',
        hovertemplate='<b>Cost Savings</b><br>%{x}<br>$%{y:,.0f}<br><i>Regulatory compliance optimization</i><extra></extra>'
    ))
    
    # Investment bars
    fig.add_trace(go.Bar(
        x=categories, y=investment, name='Compliance Investment',
        marker=dict(color='#B8B9BB', opacity=0.8),
        text=['$' + f'{val/1000:.0f}K' for val in investment],
        textposition='auto',
        hovertemplate='<b>Investment</b><br>%{x}<br>$%{y:,.0f}<br><i>Platform & services</i><extra></extra>'
    ))
    
    # ROI line
    fig.add_trace(go.Scatter(
        x=categories, y=roi_pct, mode='lines+markers', name='ROI %',
        line=dict(color='#FFCF66', width=4),
        marker=dict(size=10, color='#FFCF66', line=dict(width=2, color='#D4AF37')),
        yaxis='y2',
        hovertemplate='<b>ROI</b><br>%{x}<br>%{y}%<br><i>Return on investment</i><extra></extra>'
    ), secondary_y=True)
    
    fig.update_yaxes(title_text="Financial Impact ($)", secondary_y=False)
    fig.update_yaxes(title_text="ROI (%)", secondary_y=True)
    fig.update_layout(title="Financial Performance & ROI Analysis", barmode='group')
    
    return apply_luxury_styling(fig)

def chart_compliance_radar_luxury(data):
    """Executive Compliance Excellence Radar"""
    categories = ['Documentation', 'Training', 'Environmental', 'Quality Systems', 
                 'Facility Standards', 'Process Controls', 'Risk Management', 'Audit Readiness']
    current = [97, 98, 94, 96, 99, 95, 97, 98]
    target = [95] * len(categories)
    industry = [88, 85, 87, 89, 86, 84, 82, 87]
    
    fig = go.Figure()
    
    # Current performance
    fig.add_trace(go.Scatterpolar(
        r=current + [current[0]], theta=categories + [categories[0]],
        fill='toself', name='Current Performance',
        line=dict(color='#D4AF37', width=3),
        fillcolor="rgba(212, 175, 55, 0.2)",
        hovertemplate='<b>%{theta}</b><br>Current: %{r}%<br><i>Exceeding targets</i><extra></extra>'
    ))
    
    # Industry benchmark
    fig.add_trace(go.Scatterpolar(
        r=industry + [industry[0]], theta=categories + [categories[0]],
        line=dict(color='#B8B9BB', width=2, dash='dash'),
        name='Industry Average',
        hovertemplate='<b>%{theta}</b><br>Industry: %{r}%<extra></extra>'
    ))
    
    # Target line
    fig.add_trace(go.Scatterpolar(
        r=target + [target[0]], theta=categories + [categories[0]],
        line=dict(color='#FFCF66', width=2, dash='dot'),
        name='Target (95%)',
        hovertemplate='<b>Target</b><br>%{theta}<br>%{r}%<extra></extra>'
    ))
    
    fig.update_layout(
        title="Compliance Excellence Matrix",
        polar=dict(
            radialaxis=dict(
                visible=True, range=[0, 100],
                gridcolor="rgba(184, 185, 187, 0.1)",
                linecolor="rgba(184, 185, 187, 0.2)"
            ),
            angularaxis=dict(
                gridcolor="rgba(184, 185, 187, 0.1)",
                linecolor="rgba(184, 185, 187, 0.2)"
            )
        )
    )
    
    return apply_luxury_styling(fig)

def chart_performance_gauge_luxury(data):
    """Premium Performance Gauge"""
    score = 97.3
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "<b>Overall Compliance Score</b>", 'font': {'size': 20, 'color': '#F5F6F7'}},
        delta={'reference': 95, 'increasing': {'color': '#3DBC6B'}, 'decreasing': {'color': '#E4574C'}},
        gauge={
            'axis': {'range': [None, 100], 'tickcolor': '#B8B9BB'},
            'bar': {'color': '#D4AF37', 'thickness': 0.7},
            'bgcolor': "rgba(27, 29, 31, 0.8)",
            'borderwidth': 2,
            'bordercolor': "rgba(184, 185, 187, 0.2)",
            'steps': [
                {'range': [0, 70], 'color': 'rgba(228, 87, 76, 0.2)'},
                {'range': [70, 85], 'color': 'rgba(255, 207, 102, 0.2)'},
                {'range': [85, 95], 'color': 'rgba(61, 188, 107, 0.2)'},
                {'range': [95, 100], 'color': 'rgba(212, 175, 55, 0.2)'}
            ],
            'threshold': {
                'line': {'color': '#F5F6F7', 'width': 4},
                'thickness': 0.75,
                'value': 98
            }
        },
        number={'font': {'size': 48, 'color': '#D4AF37'}}
    ))
    
    return apply_luxury_styling(fig)

def chart_alert_distribution_luxury(data):
    """Luxury Alert Status Distribution"""
    departments = ['Quality Control', 'Manufacturing', 'Environmental Health', 
                  'Training & Development', 'Documentation', 'Facilities Management']
    normal = [22, 18, 25, 15, 20, 16]
    review = [1, 2, 0, 1, 0, 2]
    critical = [0, 0, 0, 0, 0, 0]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=departments, x=normal, name='Normal Operations',
        orientation='h', marker=dict(color='#3DBC6B', opacity=0.8),
        hovertemplate='<b>%{y}</b><br>Normal: %{x} items<br><i>Optimal performance</i><extra></extra>'
    ))
    
    fig.add_trace(go.Bar(
        y=departments, x=review, name='Review Required',
        orientation='h', marker=dict(color='#FFCF66', opacity=0.8),
        hovertemplate='<b>%{y}</b><br>Review: %{x} items<br><i>Optimization opportunity</i><extra></extra>'
    ))
    
    fig.add_trace(go.Bar(
        y=departments, x=critical, name='Critical Action',
        orientation='h', marker=dict(color='#E4574C', opacity=0.8),
        hovertemplate='<b>%{y}</b><br>Critical: %{x} items<extra></extra>'
    ))
    
    fig.update_layout(
        title="Alert Status by Department",
        barmode='stack',
        xaxis_title="Number of Items"
    )
    
    return apply_luxury_styling(fig)

def chart_risk_assessment_luxury(data):
    """Executive Risk Assessment Gauge"""
    risk_score = 12.8  # Low risk
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=risk_score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "<b>Risk Assessment Score</b>", 'font': {'size': 20, 'color': '#F5F6F7'}},
        delta={'reference': 20, 'decreasing': {'color': '#3DBC6B'}},
        gauge={
            'axis': {'range': [0, 100], 'tickcolor': '#B8B9BB'},
            'bar': {'color': '#3DBC6B', 'thickness': 0.7},
            'bgcolor': "rgba(27, 29, 31, 0.8)",
            'borderwidth': 2,
            'bordercolor': "rgba(184, 185, 187, 0.2)",
            'steps': [
                {'range': [0, 25], 'color': 'rgba(61, 188, 107, 0.2)'},
                {'range': [25, 50], 'color': 'rgba(255, 207, 102, 0.2)'},
                {'range': [50, 75], 'color': 'rgba(228, 87, 76, 0.2)'},
                {'range': [75, 100], 'color': 'rgba(139, 0, 0, 0.3)'}
            ],
            'threshold': {
                'line': {'color': '#F5F6F7', 'width': 4},
                'thickness': 0.75,
                'value': 30
            }
        },
        number={'font': {'size': 48, 'color': '#3DBC6B'}, 'suffix': '%'}
    ))
    
    return apply_luxury_styling(fig)

def chart_performance_timeline_luxury(data):
    """Executive Performance Timeline"""
    months = ['Jan 2024', 'Feb 2024', 'Mar 2024', 'Apr 2024', 'May 2024', 
              'Jun 2024', 'Jul 2024', 'Aug 2024', 'Sep 2024', 'Oct 2024']
    performance = [93.2, 94.1, 93.8, 95.4, 96.2, 95.8, 96.1, 97.3, 96.8, 97.5]
    target = [95.0] * len(months)
    industry = [89.5, 89.8, 90.2, 90.5, 91.0, 91.2, 91.8, 92.1, 92.5, 92.8]
    
    fig = go.Figure()
    
    # Performance area chart
    fig.add_trace(go.Scatter(
        x=months, y=performance, mode='lines+markers',
        name='Actual Performance', line=dict(color='#D4AF37', width=4),
        marker=dict(size=8, color='#D4AF37', line=dict(width=2, color='#FFCF66')),
        fill='tonexty', fillcolor="rgba(212, 175, 55, 0.1)",
        hovertemplate='<b>Performance</b><br>%{x}<br>%{y}%<br><i>Above target by %{customdata}%</i><extra></extra>',
        customdata=[round(p-t, 1) for p, t in zip(performance, target)]
    ))
    
    # Target line
    fig.add_trace(go.Scatter(
        x=months, y=target, mode='lines',
        name='Target (95%)', line=dict(color='#FFCF66', width=2, dash='dash'),
        hovertemplate='<b>Target</b><br>%{x}<br>%{y}%<extra></extra>'
    ))
    
    # Industry benchmark
    fig.add_trace(go.Scatter(
        x=months, y=industry, mode='lines',
        name='Industry Average', line=dict(color='#B8B9BB', width=2, dash='dot'),
        hovertemplate='<b>Industry Average</b><br>%{x}<br>%{y}%<extra></extra>'
    ))
    
    fig.update_layout(
        title="Performance Trend Analysis",
        yaxis=dict(range=[85, 100], title="Compliance Score (%)"),
        xaxis=dict(title="Time Period")
    )
    
    return apply_luxury_styling(fig)

def chart_regulatory_heatmap_luxury(data):
    """Regulatory Compliance Heatmap"""
    regulations = ['USP <797>', 'USP <800>', 'USP <825>', 'FDA 503B', 
                  'State Board', 'cGMP', 'Environmental', 'Quality Systems']
    compliance_scores = [98, 96, 99, 97, 95, 94, 97, 98]
    
    # Color mapping based on scores
    colors = []
    for score in compliance_scores:
        if score >= 97:
            colors.append('#3DBC6B')  # Excellent
        elif score >= 94:
            colors.append('#D4AF37')  # Good
        elif score >= 90:
            colors.append('#FFCF66')  # Needs attention
        else:
            colors.append('#E4574C')  # Critical
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=regulations, y=compliance_scores,
        marker=dict(color=colors, opacity=0.8,
                   line=dict(color='rgba(255,255,255,0.2)', width=1)),
        text=[f'{score}%' for score in compliance_scores],
        textposition='auto', textfont=dict(color='white', size=12, family='Inter'),
        hovertemplate='<b>%{x}</b><br>Compliance: %{y}%<br><i>Regulatory standard</i><extra></extra>'
    ))
    
    fig.update_layout(
        title="Regulatory Compliance Matrix",
        yaxis=dict(range=[90, 100], title="Compliance Score (%)"),
        xaxis=dict(tickangle=-45, title="Regulatory Standards")
    )
    
    return apply_luxury_styling(fig)

def chart_deadlines_timeline_luxury(data):
    """Upcoming Deadlines Timeline"""
    tasks = ['Annual FDA Inspection', 'USP <797> Recertification', 'Environmental Validation',
            'Quality System Review', 'Equipment Calibration', 'Staff Training Update']
    start_dates = [datetime.now() + timedelta(days=d) for d in [20, 12, 45, 30, 55, 8]]
    durations = [30, 15, 25, 18, 10, 12]
    priorities = ['High', 'Critical', 'Medium', 'High', 'Medium', 'Critical']
    
    color_map = {'Critical': '#E4574C', 'High': '#FFCF66', 'Medium': '#3DBC6B'}
    
    fig = go.Figure()
    
    for i, (task, start, duration, priority) in enumerate(zip(tasks, start_dates, durations, priorities)):
        days_until = (start - datetime.now()).days
        color = color_map[priority]
        
        fig.add_trace(go.Bar(
            y=[task], x=[duration], base=[start], orientation='h',
            marker=dict(color=color, opacity=0.8),
            name=priority if priority not in [trace.name for trace in fig.data] else "",
            showlegend=priority not in [trace.name for trace in fig.data],
            hovertemplate=f'<b>{task}</b><br>Start: {start.strftime("%b %d, %Y")}<br>Duration: {duration} days<br>Priority: {priority}<br>Days until start: {days_until}<extra></extra>'
        ))
    
    # Add "today" line
    fig.add_vline(x=datetime.now(), line_dash="solid", line_color='#D4AF37', line_width=3,
                 annotation_text="Today", annotation_position="top")
    
    fig.update_layout(
        title="Upcoming Compliance Deadlines",
        xaxis=dict(type='date', title="Timeline"),
        yaxis=dict(title="Tasks")
    )
    
    return apply_luxury_styling(fig)

# Luxury UI Components
def render_luxury_header(client_data):
    """Render luxury executive dashboard header"""
    st.markdown(f"""
    <div class="luxury-header">
        <div class="brand-section">
            <h1 class="brand-title">LexCura Elite</h1>
            <div class="premium-badge">ENTERPRISE</div>
        </div>
        <div class="header-status">
            <div style="font-size: 1.1rem; color: #F5F6F7; font-weight: 600;">
                {client_data['CLIENT NAME']}
            </div>
            <div class="status-live">
                <div class="status-indicator"></div>
                Live Data • Updated {client_data['DATE_SCRAPED']}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_luxury_sidebar(client_data):
    """Render luxury sidebar with client information"""
    with st.sidebar:
        st.markdown(f"""
        <div class="sidebar-luxury">
            <div class="sidebar-title-luxury">Client Intelligence</div>
            <div class="client-info">
                <div class="info-item">
                    <span class="info-label">Client ID</span>
                    <span class="info-value">{client_data['UNIQUE CLIENT ID']}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">Service Tier</span>
                    <span class="info-value" style="color: #D4AF37;">{client_data['TIER']}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">Region</span>
                    <span class="info-value">{client_data['REGION']}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">Update Frequency</span>
                    <span class="info-value">{client_data['DELIVERY FREQUENCY']}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">Status</span>
                    <span class="info-value" style="color: #3DBC6B;">{client_data['STATUS']}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Quick Actions
        st.markdown('<div class="sidebar-title-luxury">Executive Actions</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="luxury-button-group">
            <div class="luxury-button">
                🔄 Refresh Data
            </div>
            <div class="luxury-button">
                📊 Export Report
            </div>
            <div class="luxury-button">
                ⚙️ Configure
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Advanced Filters
        st.markdown('<div class="sidebar-title-luxury">Intelligence Filters</div>', unsafe_allow_html=True)
        
        alert_levels = st.multiselect(
            "Alert Levels",
            options=['RED', 'AMBER', 'GREEN'],
            default=['GREEN'],
            help="Filter by alert severity levels"
        )
        
        date_range = st.date_input(
            "Analysis Period",
            value=(datetime.now() - timedelta(days=30), datetime.now()),
            help="Select date range for analysis"
        )
        
        update_types = st.multiselect(
            "Update Categories",
            options=['Regulatory', 'Compliance', 'Risk', 'Training'],
            default=['Regulatory', 'Compliance'],
            help="Select update categories to include"
        )

def render_luxury_kpis(client_data):
    """Render luxury KPI dashboard"""
    st.markdown("### Executive Performance Indicators")
    
    # Extract financial data
    financial_stats = client_data.get('CURRENT FINANCIAL STATS', '$2.5M annual savings')
    historical_impact = client_data.get('HISTORICAL FINANCIAL IMPACTS', 'ROI: 556%')
    
    # KPI Grid
    st.markdown("""
    <div class="kpi-grid">
        <div class="kpi-card-luxury">
            <div class="kpi-title-luxury">Compliance Score</div>
            <div class="kpi-value-luxury">97.3%</div>
            <div class="kpi-change positive">▲ 2.3% vs last month</div>
        </div>
        
        <div class="kpi-card-luxury">
            <div class="kpi-title-luxury">Risk Level</div>
            <div class="kpi-value-luxury">12.8</div>
            <div class="kpi-change positive">▼ 1.2 pts (Excellent)</div>
        </div>
        
        <div class="kpi-card-luxury">
            <div class="kpi-title-luxury">Annual Savings</div>
            <div class="kpi-value-luxury">$2.5M</div>
            <div class="kpi-change positive">▲ 12.4% YoY growth</div>
        </div>
        
        <div class="kpi-card-luxury">
            <div class="kpi-title-luxury">Critical Alerts</div>
            <div class="kpi-value-luxury">0</div>
            <div class="kpi-change neutral">● Zero incidents</div>
        </div>
        
        <div class="kpi-card-luxury">
            <div class="kpi-title-luxury">ROI Performance</div>
            <div class="kpi-value-luxury">556%</div>
            <div class="kpi-change positive">▲ Industry leading</div>
        </div>
        
        <div class="kpi-card-luxury">
            <div class="kpi-title-luxury">Audit Readiness</div>
            <div class="kpi-value-luxury">98.5%</div>
            <div class="kpi-change positive">▲ Fully prepared</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_executive_summary(client_data):
    """Render luxury executive summary"""
    summary = client_data.get('EXECUTIVE SUMMARY', 'No summary available')
    
    st.markdown(f"""
    <div class="executive-summary fade-in-luxury">
        <div class="summary-title">Executive Intelligence Summary</div>
        <div class="summary-content">{summary}</div>
    </div>
    """, unsafe_allow_html=True)

def render_chart_with_luxury_container(chart_func, data, title):
    """Render chart with luxury container styling"""
    st.markdown(f"""
    <div class="chart-container-luxury">
        <div class="chart-title-luxury">{title}</div>
    """, unsafe_allow_html=True)
    
    fig = chart_func(data)
    st.plotly_chart(fig, use_container_width=True, config={
        "displayModeBar": False,
        "responsive": True
    })
    
    st.markdown("</div>", unsafe_allow_html=True)

def main():
    """Main luxury dashboard application"""
    
    # Initialize session state and styling
    init_session_state()
    load_luxury_css()
    
    # Get client ID from URL parameters
    client_id = st.query_params.get("client_id", "11AA")
    
    # Load client data with luxury loading animation
    with st.spinner("🔄 Loading executive intelligence dashboard..."):
        client_data = load_client_data(client_id)
    
    # Render luxury header
    render_luxury_header(client_data)
    
    # Render luxury sidebar
    render_luxury_sidebar(client_data)
    
    # Main dashboard content
    with st.container():
        # Executive KPI Section
        render_luxury_kpis(client_data)
        
        # Executive Summary
        render_executive_summary(client_data)
        
        # Premium Dashboard Tabs
        tab1, tab2, tab3, tab4 = st.tabs([
            "📊 Executive Dashboard", 
            "🔍 Detailed Analytics", 
            "📈 Performance Trends", 
            "⚡ Intelligence Hub"
        ])
        
        with tab1:
            col1, col2 = st.columns(2)
            with col1:
                render_chart_with_luxury_container(
                    chart_financial_impact_luxury, client_data,
                    "Financial Impact & ROI Analysis"
                )
                render_chart_with_luxury_container(
                    chart_performance_gauge_luxury, client_data,
                    "Overall Compliance Performance"
                )
            with col2:
                render_chart_with_luxury_container(
                    chart_compliance_radar_luxury, client_data,
                    "Compliance Excellence Matrix"
                )
                render_chart_with_luxury_container(
                    chart_alert_distribution_luxury, client_data,
                    "Alert Status Distribution"
                )
        
        with tab2:
            col1, col2 = st.columns(2)
            with col1:
                render_chart_with_luxury_container(
                    chart_risk_assessment_luxury, client_data,
                    "Executive Risk Assessment"
                )
                render_chart_with_luxury_container(
                    chart_regulatory_heatmap_luxury, client_data,
                    "Regulatory Compliance Matrix"
                )
            with col2:
                render_chart_with_luxury_container(
                    chart_performance_timeline_luxury, client_data,
                    "Performance Trend Analysis"
                )
                render_chart_with_luxury_container(
                    chart_deadlines_timeline_luxury, client_data,
                    "Upcoming Compliance Deadlines"
                )
        
        with tab3:
            st.markdown("""
            <div class="luxury-card">
                <h3 style="color: #D4AF37; margin-bottom: 1.5rem;">Performance Analytics & Forecasting</h3>
                <p style="color: #B8B9BB; font-size: 1.1rem; line-height: 1.7;">
                    Advanced predictive analytics and trend forecasting capabilities. This section provides
                    forward-looking insights based on historical performance data, regulatory changes,
                    and industry benchmarks to support strategic decision-making.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Add more advanced charts here
            col1, col2 = st.columns(2)
            with col1:
                render_chart_with_luxury_container(
                    chart_performance_timeline_luxury, client_data,
                    "12-Month Performance Forecast"
                )
            with col2:
                render_chart_with_luxury_container(
                    chart_financial_impact_luxury, client_data,
                    "ROI Projection Analysis"
                )
        
        with tab4:
            st.markdown("""
            <div class="luxury-card">
                <h3 style="color: #D4AF37; margin-bottom: 1.5rem;">Regulatory Intelligence Hub</h3>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem;">
                    <div>
                        <h4 style="color: #FFCF66; margin-bottom: 1rem;">Latest Regulatory Updates</h4>
                        <p style="color: #B8B9BB; line-height: 1.6;">
                            • USP <797> Revision Q2 2024 - Implementation guidelines<br>
                            • FDA 503B Facility Standards - Updated requirements<br>
                            • EU Annex 1 - Sterile medicinal products manufacturing
                        </p>
                    </div>
                    <div>
                        <h4 style="color: #FFCF66; margin-bottom: 1rem;">Risk Monitoring</h4>
                        <p style="color: #B8B9BB; line-height: 1.6;">
                            • Zero critical compliance violations<br>
                            • Proactive risk mitigation active<br>
                            • Continuous monitoring across all domains
                        </p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Detailed content access
            if client_data.get('MAIN STRUCTURED CONTENT'):
                content = client_data.get('MAIN STRUCTURED CONTENT', '')
                if len(content) > 100:
                    st.markdown(f"""
                    <div class="luxury-card">
                        <h3 style="color: #D4AF37; margin-bottom: 1.5rem;">Comprehensive Intelligence Report</h3>
                        <p style="color: #B8B9BB; margin-bottom: 1.5rem;">
                            Full regulatory intelligence and compliance analysis for {client_data['CLIENT NAME']}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Content preview
                    if len(content) > 1000:
                        preview = content[:800] + "..."
                        st.text_area(
                            "Intelligence Report Preview", 
                            preview, 
                            height=200, 
                            disabled=True,
                            help="Full report available for download"
                        )
                        
                        # Download button with luxury styling
                        st.download_button(
                            label="📄 Download Complete Intelligence Report",
                            data=content,
                            file_name=f"lexcura_intelligence_{client_id}_{datetime.now().strftime('%Y%m%d')}.txt",
                            mime="text/plain",
                            help="Download the complete regulatory intelligence report"
                        )

if __name__ == "__main__":
    main()
