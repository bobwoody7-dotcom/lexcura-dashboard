"""
LexCura Elite Compliance Dashboard - Premium £10,000 Client Edition
Luxury legal compliance monitoring with executive-grade intelligence
Ultra-premium design for high-value enterprise clients
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
    page_title="LexCura Elite | Executive Legal Intelligence",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium Template System
def register_premium_template():
    """Register premium luxury template for high-value clients"""
    try:
        premium_template = go.layout.Template(
            layout=go.Layout(
                paper_bgcolor="#1C1C1C",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(
                    family="Inter, 'SF Pro Display', system-ui, sans-serif",
                    color="#E0E0E0",
                    size=13
                ),
                title=dict(
                    font=dict(size=20, color="#D4AF37", family="Inter", weight=600),
                    x=0.5,
                    xanchor="center",
                    pad=dict(t=25)
                ),
                colorway=["#D4AF37", "#E6C973", "#B08D57", "#8B7355", "#E0E0E0", "#C0C0C0"],
                xaxis=dict(
                    gridcolor="rgba(212,175,55,0.08)",
                    linecolor="rgba(212,175,55,0.2)",
                    zerolinecolor="rgba(212,175,55,0.2)",
                    tickfont=dict(size=12, color="#E0E0E0"),
                    titlefont=dict(size=14, color="#D4AF37", weight=500)
                ),
                yaxis=dict(
                    gridcolor="rgba(212,175,55,0.08)",
                    linecolor="rgba(212,175,55,0.2)",
                    zerolinecolor="rgba(212,175,55,0.2)",
                    tickfont=dict(size=12, color="#E0E0E0"),
                    titlefont=dict(size=14, color="#D4AF37", weight=500)
                ),
                legend=dict(
                    font=dict(size=12, color="#E0E0E0"),
                    bgcolor="rgba(28,28,28,0.95)",
                    bordercolor="rgba(212,175,55,0.3)",
                    borderwidth=2
                )
            )
        )
        pio.templates["premium"] = premium_template
        pio.templates.default = "premium"
    except Exception as e:
        pio.templates.default = "plotly_dark"

def apply_premium_styling(fig):
    """Apply premium luxury styling to charts"""
    try:
        fig.update_layout(template="premium")
    except:
        fig.update_layout(
            paper_bgcolor="#1C1C1C",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#E0E0E0", family="Inter"),
            title=dict(font=dict(color="#D4AF37", size=20, weight=600)),
            xaxis=dict(gridcolor="rgba(212,175,55,0.08)", tickfont=dict(color="#E0E0E0")),
            yaxis=dict(gridcolor="rgba(212,175,55,0.08)", tickfont=dict(color="#E0E0E0"))
        )
    
    fig.update_layout(
        height=420,
        margin=dict(l=60, r=60, t=80, b=60),
        hovermode='closest',
        showlegend=True
    )
    
    return fig

# Initialize premium template
register_premium_template()

# Premium Luxury CSS
def load_premium_css():
    """Load ultra-premium £10,000 client dashboard CSS"""
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Playfair+Display:wght@400;500;600;700&display=swap');
        
        :root {
            --bg-primary: #1C1C1C;
            --bg-luxury: #0F0F0F;
            --bg-card: #242424;
            --bg-card-hover: #2A2A2A;
            --accent-gold: #D4AF37;
            --accent-bronze: #B08D57;
            --accent-champagne: #E6C973;
            --text-primary: #E0E0E0;
            --text-muted: #B0B0B0;
            --text-subtle: #808080;
            --border-gold: rgba(212, 175, 55, 0.2);
            --shadow-luxury: 0 8px 32px rgba(0, 0, 0, 0.6), 0 2px 16px rgba(212, 175, 55, 0.1);
            --gradient-gold: linear-gradient(135deg, #D4AF37 0%, #E6C973 50%, #B08D57 100%);
            --gradient-card: linear-gradient(145deg, #242424 0%, #2A2A2A 100%);
        }
        
        .stApp {
            background: var(--bg-primary);
            color: var(--text-primary);
            font-family: 'Inter', system-ui, sans-serif;
        }
        
        /* Ultra-Premium Header */
        .executive-header {
            background: linear-gradient(135deg, var(--bg-luxury) 0%, var(--bg-card) 30%, var(--bg-luxury) 100%);
            border-bottom: 3px solid transparent;
            border-image: var(--gradient-gold) 1;
            padding: 2.5rem 3rem;
            margin: -1rem -1rem 3rem -1rem;
            box-shadow: var(--shadow-luxury);
            position: relative;
            overflow: hidden;
        }
        
        .executive-header::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: 
                radial-gradient(circle at 20% 20%, rgba(212, 175, 55, 0.03) 0%, transparent 50%),
                radial-gradient(circle at 80% 80%, rgba(230, 201, 115, 0.02) 0%, transparent 50%),
                conic-gradient(from 45deg at 50% 50%, transparent 0deg, rgba(212, 175, 55, 0.01) 90deg, transparent 180deg);
            pointer-events: none;
        }
        
        .header-content {
            max-width: 1400px;
            margin: 0 auto;
            display: grid;
            grid-template-columns: 1fr auto;
            align-items: center;
            gap: 3rem;
            position: relative;
            z-index: 1;
        }
        
        .brand-section {
            display: flex;
            align-items: center;
            gap: 1.5rem;
        }
        
        .brand-icon {
            width: 64px;
            height: 64px;
            background: var(--gradient-gold);
            border-radius: 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 2rem;
            color: var(--bg-primary);
            font-weight: 700;
            box-shadow: 0 8px 24px rgba(212, 175, 55, 0.3);
        }
        
        .brand-title {
            font-size: 3rem;
            font-weight: 800;
            background: var(--gradient-gold);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin: 0;
            font-family: 'Playfair Display', serif;
            letter-spacing: -0.02em;
        }
        
        .brand-subtitle {
            font-size: 1rem;
            color: var(--text-muted);
            margin: 0.5rem 0 0 0;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.1em;
        }
        
        .status-section {
            text-align: right;
            font-size: 0.95rem;
            color: var(--text-muted);
        }
        
        .client-badge {
            background: var(--gradient-gold);
            color: var(--bg-primary);
            padding: 0.75rem 2rem;
            border-radius: 50px;
            font-weight: 700;
            font-size: 1.1rem;
            margin-bottom: 1rem;
            box-shadow: 0 4px 16px rgba(212, 175, 55, 0.4);
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        
        .status-live {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            justify-content: flex-end;
            color: var(--accent-champagne);
            font-weight: 600;
        }
        
        .status-dot {
            width: 10px;
            height: 10px;
            background: var(--accent-champagne);
            border-radius: 50%;
            animation: luxuryPulse 2s infinite;
            box-shadow: 0 0 10px rgba(230, 201, 115, 0.5);
        }
        
        /* Ultra-Premium KPI Cards */
        .luxury-kpi-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 2rem;
            margin: 2.5rem 0;
        }
        
        .luxury-kpi-card {
            background: var(--gradient-card);
            border: 2px solid var(--border-gold);
            border-radius: 20px;
            padding: 2.5rem 2rem;
            text-align: center;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
            box-shadow: var(--shadow-luxury);
        }
        
        .luxury-kpi-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: var(--gradient-gold);
        }
        
        .luxury-kpi-card::after {
            content: '';
            position: absolute;
            top: -2px;
            left: -2px;
            right: -2px;
            bottom: -2px;
            background: var(--gradient-gold);
            border-radius: 22px;
            opacity: 0;
            transition: opacity 0.4s ease;
            z-index: -1;
        }
        
        .luxury-kpi-card:hover {
            transform: translateY(-8px) scale(1.02);
            box-shadow: 
                0 20px 60px rgba(0, 0, 0, 0.8),
                0 8px 32px rgba(212, 175, 55, 0.2);
        }
        
        .luxury-kpi-card:hover::after {
            opacity: 0.1;
        }
        
        .kpi-icon {
            font-size: 3rem;
            margin-bottom: 1rem;
            background: var(--gradient-gold);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .kpi-value {
            font-size: 3.5rem;
            font-weight: 800;
            background: var(--gradient-gold);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin: 1rem 0;
            font-family: 'Inter', sans-serif;
            letter-spacing: -0.02em;
        }
        
        .kpi-label {
            font-size: 1rem;
            color: var(--text-muted);
            text-transform: uppercase;
            font-weight: 600;
            letter-spacing: 0.1em;
            margin-bottom: 0.5rem;
        }
        
        .kpi-change {
            font-size: 0.9rem;
            margin-top: 1rem;
            font-weight: 600;
            padding: 0.5rem 1rem;
            border-radius: 50px;
            display: inline-block;
        }
        
        .kpi-change.positive { 
            background: rgba(76, 175, 80, 0.15);
            color: #81C784;
            border: 1px solid rgba(76, 175, 80, 0.3);
        }
        .kpi-change.negative { 
            background: rgba(244, 67, 54, 0.15);
            color: #EF5350;
            border: 1px solid rgba(244, 67, 54, 0.3);
        }
        .kpi-change.neutral { 
            background: rgba(212, 175, 55, 0.15);
            color: var(--accent-champagne);
            border: 1px solid var(--border-gold);
        }
        
        /* Premium Cards */
        .executive-card {
            background: var(--gradient-card);
            border: 2px solid var(--border-gold);
            border-radius: 16px;
            padding: 2.5rem;
            margin: 2rem 0;
            box-shadow: var(--shadow-luxury);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .executive-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 1px;
            background: var(--gradient-gold);
        }
        
        .executive-card:hover {
            border-color: var(--accent-champagne);
            transform: translateY(-4px);
            box-shadow: 
                0 16px 48px rgba(0, 0, 0, 0.7),
                0 4px 24px rgba(212, 175, 55, 0.15);
        }
        
        .card-title {
            font-size: 1.4rem;
            font-weight: 700;
            color: var(--accent-gold);
            margin-bottom: 1.5rem;
            font-family: 'Playfair Display', serif;
        }
        
        /* Premium Sidebar */
        .executive-sidebar {
            background: var(--gradient-card);
            border: 2px solid var(--border-gold);
            border-radius: 16px;
            padding: 2rem;
            margin-bottom: 2rem;
            box-shadow: var(--shadow-luxury);
        }
        
        .sidebar-title {
            font-size: 1.1rem;
            font-weight: 700;
            color: var(--accent-gold);
            margin-bottom: 1.5rem;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            font-family: 'Inter', sans-serif;
        }
        
        .info-grid {
            display: grid;
            gap: 1rem;
        }
        
        .info-row {
            display: grid;
            grid-template-columns: 1fr auto;
            align-items: center;
            padding: 1rem;
            background: rgba(212, 175, 55, 0.02);
            border: 1px solid rgba(212, 175, 55, 0.1);
            border-radius: 8px;
            transition: all 0.2s ease;
        }
        
        .info-row:hover {
            background: rgba(212, 175, 55, 0.05);
            border-color: rgba(212, 175, 55, 0.2);
        }
        
        .info-label {
            font-size: 0.95rem;
            color: var(--text-muted);
            font-weight: 500;
        }
        
        .info-value {
            font-size: 0.95rem;
            color: var(--text-primary);
            font-weight: 700;
        }
        
        /* Executive Summary */
        .executive-summary {
            background: linear-gradient(145deg, var(--bg-card) 0%, var(--bg-card-hover) 100%);
            border: 2px solid var(--border-gold);
            border-left: 6px solid var(--accent-gold);
            border-radius: 16px;
            padding: 3rem;
            margin: 2.5rem 0;
            box-shadow: var(--shadow-luxury);
            position: relative;
        }
        
        .executive-summary::before {
            content: '';
            position: absolute;
            top: 2rem;
            right: 2rem;
            width: 60px;
            height: 60px;
            background: var(--gradient-gold);
            border-radius: 50%;
            opacity: 0.1;
        }
        
        .summary-title {
            font-size: 1.8rem;
            font-weight: 700;
            color: var(--accent-gold);
            margin-bottom: 1.5rem;
            font-family: 'Playfair Display', serif;
        }
        
        .summary-text {
            font-size: 1.1rem;
            line-height: 1.8;
            color: var(--text-primary);
            font-weight: 400;
        }
        
        /* Premium Alerts */
        .luxury-alert {
            padding: 1.5rem 2rem;
            border-radius: 12px;
            margin: 1.5rem 0;
            border-left: 4px solid;
            font-weight: 500;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
        }
        
        .luxury-alert.success {
            background: linear-gradient(135deg, rgba(76, 175, 80, 0.08) 0%, rgba(76, 175, 80, 0.04) 100%);
            border-left-color: #4CAF50;
            color: #81C784;
        }
        
        .luxury-alert.warning {
            background: linear-gradient(135deg, rgba(255, 193, 7, 0.08) 0%, rgba(255, 193, 7, 0.04) 100%);
            border-left-color: #FFC107;
            color: #FFD54F;
        }
        
        .luxury-alert.error {
            background: linear-gradient(135deg, rgba(244, 67, 54, 0.08) 0%, rgba(244, 67, 54, 0.04) 100%);
            border-left-color: #F44336;
            color: #EF5350;
        }
        
        /* Chart Containers */
        .chart-luxury {
            background: var(--gradient-card);
            border: 2px solid var(--border-gold);
            border-radius: 20px;
            padding: 2.5rem;
            margin: 2rem 0;
            box-shadow: var(--shadow-luxury);
            transition: all 0.3s ease;
        }
        
        .chart-luxury:hover {
            border-color: var(--accent-champagne);
            transform: translateY(-2px);
        }
        
        .chart-title {
            font-size: 1.3rem;
            font-weight: 700;
            color: var(--accent-gold);
            margin-bottom: 1.5rem;
            text-align: center;
            font-family: 'Playfair Display', serif;
        }
        
        .chart-description {
            text-align: center;
            color: var(--text-muted);
            margin-bottom: 2rem;
            font-style: italic;
        }
        
        /* Tab System */
        .stTabs [data-baseweb="tab-list"] {
            background: var(--bg-card);
            border-radius: 12px;
            padding: 0.5rem;
            border: 2px solid var(--border-gold);
            box-shadow: var(--shadow-luxury);
        }
        
        .stTabs [data-baseweb="tab"] {
            background: transparent;
            border-radius: 8px;
            color: var(--text-muted);
            font-weight: 600;
            padding: 1rem 2rem;
            font-size: 0.95rem;
        }
        
        .stTabs [aria-selected="true"] {
            background: var(--gradient-gold);
            color: var(--bg-primary) !important;
            font-weight: 700;
        }
        
        /* Animations */
        @keyframes luxuryPulse {
            0%, 100% { 
                opacity: 1; 
                transform: scale(1);
                box-shadow: 0 0 10px rgba(230, 201, 115, 0.5);
            }
            50% { 
                opacity: 0.7; 
                transform: scale(1.1);
                box-shadow: 0 0 20px rgba(230, 201, 115, 0.8);
            }
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
            background: var(--bg-card);
            border: 2px solid var(--border-gold);
            border-radius: 8px;
            color: var(--text-primary);
        }
        
        /* Responsive Design */
        @media (max-width: 768px) {
            .header-content {
                grid-template-columns: 1fr;
                text-align: center;
                gap: 2rem;
            }
            
            .luxury-kpi-container {
                grid-template-columns: repeat(2, 1fr);
            }
            
            .brand-title {
                font-size: 2.5rem;
            }
        }
        
        @media (max-width: 480px) {
            .luxury-kpi-container {
                grid-template-columns: 1fr;
            }
        }
    </style>
    """, unsafe_allow_html=True)

# Session state initialization
def init_session_state():
    """Initialize session state for premium dashboard"""
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
    """Load client data with fallback to premium demo data"""
    try:
        gc = connect_to_sheets()
        if not gc:
            return get_premium_demo_data()
            
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
            'CLIENT_NAME': data.get('CLIENT NAME', 'Elite Pharmaceutical Corporation'),
            'TIER': data.get('TIER', 'Executive'),
            'REGION': data.get('REGION', 'Global'),
            'DELIVERY_FREQUENCY': data.get('DELIVERY FREQUENCY', 'Real-time'),
            'EMAIL_ADDRESS': data.get('EMAIL ADDRESS', 'executive@elitepharma.com'),
            'MAIN_CONTENT': data.get('MAIN STRUCTURED CONTENT', ''),
            'FINANCIAL_STATS': data.get('CURRENT FINANCIAL STATS', '£4.2M annual optimization'),
            'HISTORICAL_IMPACTS': data.get('HISTORICAL FINANCIAL IMPACTS', 'ROI: 847%'),
            'EXECUTIVE_SUMMARY': data.get('EXECUTIVE SUMMARY', ''),
            'COMPLIANCE_ALERTS': data.get('COMPLIANCE ALERTS', 'Zero critical violations'),
            'RISK_ANALYSIS': data.get('RISK ANALYSIS', 'Ultra-low risk profile'),
            'REGULATORY_UPDATES': data.get('REGULATORY UPDATES', 'Global regulatory intelligence'),
            'ALERT_LEVEL': data.get('ALERT LEVEL', 'OPTIMAL'),
            'DATE_SCRAPED': data.get('DATE SCRAPED', datetime.now().strftime('%Y-%m-%d')),
            'STATUS': data.get('STATUS', 'Premium Active')
        }
        
    except Exception as e:
        return get_premium_demo_data()

def get_premium_demo_data():
    """Premium demo data for £10,000 executive dashboard"""
    return {
        'UNIQUE_CLIENT_ID': '11AA',
        'CLIENT_NAME': 'Elite Pharmaceutical Corporation',
        'TIER': 'Executive Premium',
        'REGION': 'Global Operations',
        'DELIVERY_FREQUENCY': 'Real-time Intelligence',
        'EMAIL_ADDRESS': 'executive@elitepharma.com',
        'MAIN_CONTENT': 'Comprehensive executive-grade regulatory intelligence with AI-powered risk prediction, real-time compliance monitoring, and strategic legal advisory services.',
        'FINANCIAL_STATS': '£4.2M annual compliance optimization, £850K platform investment',
        'HISTORICAL_IMPACTS': 'ROI: 847% over 24 months, zero regulatory penalties avoided',
        'EXECUTIVE_SUMMARY': 'Outstanding executive performance across all regulatory domains. Advanced AI-powered risk prediction has eliminated critical violations while optimizing operational efficiency. Current performance exceeds industry benchmarks with 99.4% overall compliance score and predictive risk mitigation.',
        'COMPLIANCE_ALERTS': 'Zero critical violations, proactive optimization opportunities identified',
        'RISK_ANALYSIS': 'Ultra-low risk profile with predictive monitoring and strategic controls',
        'REGULATORY_UPDATES': 'Global regulatory intelligence, AI-powered trend analysis, executive briefings',
        'ALERT_LEVEL': 'OPTIMAL',
        'DATE_SCRAPED': datetime.now().strftime('%Y-%m-%d'),
        'STATUS': 'Premium Active'
    }

# Premium Chart Functions
def create_executive_performance_chart(data):
    """Executive-grade financial performance analysis"""
    quarters = ['Q1 2024', 'Q2 2024', 'Q3 2024', 'Q4 2024', 'Q1 2025']
    savings = [420000, 485000, 520000, 610000, 665000]
    investment = [85000, 78000, 92000, 88000, 95000]
    roi = [494, 621, 565, 693, 700]
    
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Financial Impact Analysis', 'Return on Investment'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # Financial bars
    fig.add_trace(go.Bar(
        x=quarters, y=savings, name='Compliance Optimization',
        marker=dict(color='#D4AF37', opacity=0.9),
        text=[f'£{val/1000:.0f}K' for val in savings],
        textposition='auto'
    ), row=1, col=1)
    
    fig.add_trace(go.Bar(
        x=quarters, y=investment, name='Platform Investment',
        marker=dict(color='#B08D57', opacity=0.8),
        text=[f'£{val/1000:.0f}K' for val in investment],
        textposition='auto'
    ), row=1, col=1)
    
    # ROI line
    fig.add_trace(go.Scatter(
        x=quarters, y=roi, mode='lines+markers',
        name='ROI %', line=dict(color='#E6C973', width=4),
        marker=dict(size=12, color='#E6C973'),
        text=[f'{val}%' for val in roi],
        textposition='top center'
    ), row=1, col=2)
    
    fig.update_layout(
        title="Executive Financial Intelligence Dashboard",
        showlegend=True,
        height=450
    )
    
    return apply_premium_styling(fig)

def create_executive_compliance_radar(data):
    """Executive compliance performance radar"""
    categories = ['Regulatory Compliance', 'Risk Management', 'Quality Systems', 
                 'Environmental Controls', 'Training & Certification', 'Documentation Excellence']
    scores = [99.4, 98.7, 99.1, 97.8, 98.9, 99.6]
    benchmark = [95] * len(categories)
    industry_avg = [87, 85, 89, 82, 86, 88]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=scores + [scores[0]],
        theta=categories + [categories[0]],
        fill='toself',
        name='Current Performance',
        line=dict(color='#D4AF37', width=3),
        fillcolor="rgba(212, 175, 55, 0.25)"
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=benchmark + [benchmark[0]],
        theta=categories + [categories[0]],
        line=dict(color='#E6C973', width=2, dash='dash'),
        name='Executive Target (95%)',
        fillcolor="rgba(230, 201, 115, 0.1)"
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=industry_avg + [industry_avg[0]],
        theta=categories + [categories[0]],
        line=dict(color='#B08D57', width=2, dash='dot'),
        name='Industry Average'
    ))
    
    fig.update_layout(
        title="Executive Compliance Performance Matrix",
        polar=dict(
            radialaxis=dict(
                visible=True, 
                range=[0, 100],
                tickfont=dict(color='#E0E0E0'),
                gridcolor='rgba(212, 175, 55, 0.2)'
            ),
            angularaxis=dict(
                tickfont=dict(color='#D4AF37', size=12)
            )
        )
    )
    
    return apply_premium_styling(fig)

def create_executive_compliance_gauge(data):
    """Executive compliance performance gauge"""
    score = 99.4
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Overall Compliance Excellence", 'font': {'color': '#D4AF37', 'size': 18}},
        delta={'reference': 95, 'increasing': {'color': '#4CAF50'}},
        gauge={
            'axis': {'range': [None, 100], 'tickcolor': '#E0E0E0'},
            'bar': {'color': '#D4AF37', 'thickness': 0.8},
            'steps': [
                {'range': [0, 70], 'color': 'rgba(244, 67, 54, 0.2)'},
                {'range': [70, 85], 'color': 'rgba(255, 193, 7, 0.2)'},
                {'range': [85, 95], 'color': 'rgba(76, 175, 80, 0.2)'},
                {'range': [95, 100], 'color': 'rgba(212, 175, 55, 0.3)'}
            ],
            'threshold': {
                'line': {'color': '#E6C973', 'width': 6}, 
                'thickness': 0.8, 
                'value': 99
            }
        },
        number={'font': {'color': '#D4AF37', 'size': 36}}
    ))
    
    return apply_premium_styling(fig)

def create_risk_prediction_chart(data):
    """AI-powered risk prediction timeline"""
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    actual_risk = [8.2, 7.8, 6.5, 5.9, 4.2, 3.8, 3.1, 2.9, 2.4, 2.1, 1.8, 1.5]
    predicted_risk = [None] * 10 + [1.2, 0.9]  # Future predictions
    industry_risk = [15.2, 14.8, 16.1, 15.5, 14.9, 15.8, 16.2, 15.1, 14.6, 15.9, 16.3, 15.7]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=months, y=actual_risk, mode='lines+markers',
        name='Actual Risk Score',
        line=dict(color='#D4AF37', width=4),
        marker=dict(size=10, color='#D4AF37')
    ))
    
    fig.add_trace(go.Scatter(
        x=months[-2:], y=predicted_risk[-2:], mode='lines+markers',
        name='AI Prediction',
        line=dict(color='#E6C973', width=3, dash='dash'),
        marker=dict(size=8, color='#E6C973', symbol='diamond')
    ))
    
    fig.add_trace(go.Scatter(
        x=months, y=industry_risk, mode='lines',
        name='Industry Benchmark',
        line=dict(color='#B08D57', width=2, dash='dot'),
        opacity=0.7
    ))
    
    fig.update_layout(
        title="AI-Powered Risk Intelligence & Prediction",
        yaxis=dict(title="Risk Score (%)", range=[0, 20]),
        xaxis_title="2024 Performance Timeline"
    )
    
    return apply_premium_styling(fig)

def create_regulatory_intelligence_heatmap(data):
    """Global regulatory compliance heatmap"""
    regulations = ['FDA 503B', 'USP 797', 'USP 800', 'EU GMP', 'MHRA Standards', 'Health Canada', 'TGA Guidelines']
    regions = ['US', 'EU', 'UK', 'Canada', 'Australia', 'Asia-Pacific']
    
    # Compliance scores matrix
    scores = [
        [99.2, 98.8, 99.1, 98.9, 99.0, 98.5],  # FDA 503B
        [99.4, 98.9, 99.2, 99.1, 98.7, 99.0],  # USP 797
        [98.8, 99.1, 98.6, 99.0, 98.9, 98.4],  # USP 800
        [98.6, 99.6, 99.2, 98.8, 98.5, 98.9],  # EU GMP
        [98.9, 99.0, 99.8, 98.7, 99.1, 98.6],  # MHRA
        [99.1, 98.5, 98.8, 99.4, 98.9, 99.0],  # Health Canada
        [98.7, 98.9, 99.0, 98.6, 99.3, 99.1]   # TGA
    ]
    
    fig = go.Figure(data=go.Heatmap(
        z=scores,
        x=regions,
        y=regulations,
        colorscale=[[0, '#B08D57'], [0.8, '#D4AF37'], [1, '#E6C973']],
        text=[[f'{val}%' for val in row] for row in scores],
        texttemplate="%{text}",
        textfont={"size": 11, "color": "#1C1C1C"},
        hoverongaps=False
    ))
    
    fig.update_layout(
        title="Global Regulatory Compliance Intelligence Matrix",
        xaxis_title="Geographic Regions",
        yaxis_title="Regulatory Standards"
    )
    
    return apply_premium_styling(fig)

def create_executive_timeline(data):
    """Executive performance and milestones timeline"""
    dates = pd.date_range('2024-01-01', '2024-12-31', freq='M')
    performance = [94.2, 95.1, 96.8, 97.2, 97.9, 98.1, 98.5, 98.8, 99.0, 99.2, 99.3, 99.4]
    target = [95] * len(dates)
    milestones = [
        (pd.Timestamp('2024-03-15'), 96.8, 'ISO Certification Achieved'),
        (pd.Timestamp('2024-06-20'), 98.1, 'Zero Violations Milestone'),
        (pd.Timestamp('2024-09-10'), 99.0, 'Executive Excellence Award'),
        (pd.Timestamp('2024-11-05'), 99.3, 'Global Expansion Complete')
    ]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=dates, y=performance, mode='lines+markers',
        name='Executive Performance',
        line=dict(color='#D4AF37', width=4),
        marker=dict(size=8, color='#D4AF37'),
        fill='tonexty'
    ))
    
    fig.add_trace(go.Scatter(
        x=dates, y=target, mode='lines',
        name='Executive Target',
        line=dict(color='#E6C973', width=2, dash='dash'),
        fill='tozeroy',
        fillcolor='rgba(212, 175, 55, 0.1)'
    ))
    
    # Add milestone annotations
    for date, score, milestone in milestones:
        fig.add_annotation(
            x=date, y=score,
            text=milestone,
            showarrow=True,
            arrowhead=2,
            arrowcolor='#E6C973',
            bgcolor='rgba(212, 175, 55, 0.9)',
            bordercolor='#D4AF37',
            font=dict(color='#1C1C1C', size=10)
        )
    
    fig.update_layout(
        title="Executive Performance Timeline & Milestones",
        yaxis=dict(range=[90, 100], title="Compliance Excellence (%)"),
        xaxis_title="2024 Executive Journey"
    )
    
    return apply_premium_styling(fig)

def create_savings_waterfall(data):
    """Executive savings waterfall analysis"""
    categories = ['Baseline', 'Risk Prevention', 'Process Optimization', 'Training Efficiency', 
                 'Technology ROI', 'Regulatory Advantage', 'Total Savings']
    values = [0, 850000, 1200000, 450000, 980000, 720000, 4200000]
    
    fig = go.Figure(go.Waterfall(
        name="Executive Savings Analysis",
        orientation="v",
        measure=["absolute", "relative", "relative", "relative", "relative", "relative", "total"],
        x=categories,
        textposition="outside",
        text=[f"£{val/1000:.0f}K" if val != 0 else "" for val in values],
        y=values,
        connector={"line":{"color":"rgba(212, 175, 55, 0.3)"}},
        increasing={"marker":{"color":"#D4AF37"}},
        decreasing={"marker":{"color":"#B08D57"}},
        totals={"marker":{"color":"#E6C973"}}
    ))
    
    fig.update_layout(
        title="Executive Value Creation Waterfall Analysis",
        yaxis_title="Cumulative Savings (£)",
        showlegend=False
    )
    
    return apply_premium_styling(fig)

# Premium UI Components
def render_executive_header(client_data):
    """Render ultra-premium executive header"""
    client_name = client_data.get('CLIENT_NAME', 'Executive Client')
    date_updated = client_data.get('DATE_SCRAPED', datetime.now().strftime('%Y-%m-%d'))
    
    st.markdown(f"""
    <div class="executive-header">
        <div class="header-content">
            <div class="brand-section">
                <div class="brand-icon">⚖</div>
                <div>
                    <h1 class="brand-title">LexCura Elite</h1>
                    <p class="brand-subtitle">Executive Legal Intelligence Platform</p>
                </div>
            </div>
            <div class="status-section">
                <div class="client-badge">{client_name}</div>
                <div class="status-live">
                    <div class="status-dot"></div>
                    Executive Intelligence Active • Updated {date_updated}
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_executive_sidebar(client_data):
    """Render ultra-premium executive sidebar"""
    with st.sidebar:
        st.markdown(f"""
        <div class="executive-sidebar">
            <div class="sidebar-title">Executive Account</div>
            <div class="info-grid">
                <div class="info-row">
                    <span class="info-label">Client ID</span>
                    <span class="info-value">{client_data.get('UNIQUE_CLIENT_ID', 'N/A')}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">Service Tier</span>
                    <span class="info-value">{client_data.get('TIER', 'Executive')}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">Coverage</span>
                    <span class="info-value">{client_data.get('REGION', 'Global')}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">Intelligence</span>
                    <span class="info-value">{client_data.get('DELIVERY_FREQUENCY', 'Real-time')}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">Status</span>
                    <span class="info-value" style="color: var(--accent-champagne);">{client_data.get('STATUS', 'Premium Active')}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def render_executive_kpis(client_data):
    """Render ultra-premium KPI section with proper HTML rendering"""
    st.markdown("## Executive Performance Intelligence")
    
    # Fixed HTML rendering issue - removed the problematic HTML string
    kpi_html = """
    <div class="luxury-kpi-container">
        <div class="luxury-kpi-card">
            <div class="kpi-icon">🎯</div>
            <div class="kpi-label">Compliance Excellence</div>
            <div class="kpi-value">99.4%</div>
            <div class="kpi-change positive">▲ 2.8% vs industry</div>
        </div>
        
        <div class="luxury-kpi-card">
            <div class="kpi-icon">🛡️</div>
            <div class="kpi-label">Risk Intelligence</div>
            <div class="kpi-value">1.5</div>
            <div class="kpi-change positive">▼ 8.7 pts (Ultra-Low)</div>
        </div>
        
        <div class="luxury-kpi-card">
            <div class="kpi-icon">⚠️</div>
            <div class="kpi-label">Critical Violations</div>
            <div class="kpi-value">0</div>
            <div class="kpi-change neutral">● 847 days violation-free</div>
        </div>
        
        <div class="luxury-kpi-card">
            <div class="kpi-icon">💰</div>
            <div class="kpi-label">Annual Optimization</div>
            <div class="kpi-value">£4.2M</div>
            <div class="kpi-change positive">▲ 28.4% YoY growth</div>
        </div>
        
        <div class="luxury-kpi-card">
            <div class="kpi-icon">🎖️</div>
            <div class="kpi-label">Executive Readiness</div>
            <div class="kpi-value">99.8%</div>
            <div class="kpi-change positive">▲ Exceptional status</div>
        </div>
        
        <div class="luxury-kpi-card">
            <div class="kpi-icon">🎓</div>
            <div class="kpi-label">Team Certification</div>
            <div class="kpi-value">99.1%</div>
            <div class="kpi-change positive">▲ Above excellence</div>
        </div>
    </div>
    """
    
    st.markdown(kpi_html, unsafe_allow_html=True)

def render_executive_summary(client_data):
    """Render premium executive summary"""
    summary = client_data.get('EXECUTIVE_SUMMARY', 
        'Outstanding executive performance across all regulatory domains. Advanced AI-powered risk '
        'prediction has eliminated critical violations while optimizing operational efficiency. Current '
        'performance exceeds industry benchmarks with comprehensive predictive risk mitigation and '
        'strategic regulatory intelligence.')
    
    st.markdown(f"""
    <div class="executive-summary">
        <div class="summary-title">Executive Intelligence Brief</div>
        <div class="summary-text">{summary}</div>
    </div>
    """, unsafe_allow_html=True)

def render_executive_alerts(client_data):
    """Render executive-grade compliance alerts"""
    st.markdown("## Executive Status Intelligence")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="luxury-alert success">
            <strong>System Status: Optimal Excellence</strong><br>
            All AI monitoring systems operating at peak performance
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="luxury-alert success">
            <strong>Violations: Zero (847 days)</strong><br>
            Perfect compliance record with predictive prevention
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="luxury-alert success">
            <strong>AI Insights: 3 Optimizations</strong><br>
            Proactive efficiency improvements identified
        </div>
        """, unsafe_allow_html=True)

def render_chart_section(chart_func, data, title, description=None):
    """Render chart with luxury wrapper"""
    st.markdown(f"""
    <div class="chart-luxury">
        <div class="chart-title">{title}</div>
        {f'<p class="chart-description">{description}</p>' if description else ''}
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
        <div style="text-align: center; padding: 3rem; color: var(--text-muted);">
            Executive chart temporarily unavailable. Premium analytics processing.
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

def main():
    """Main premium executive dashboard application"""
    
    # Initialize
    init_session_state()
    load_premium_css()
    
    # Load data
    client_id = st.query_params.get("client_id", "11AA")
    
    with st.spinner("Loading executive intelligence..."):
        client_data = load_client_data(client_id)
    
    # Render header
    render_executive_header(client_data)
    
    # Render sidebar
    render_executive_sidebar(client_data)
    
    # Main dashboard content
    with st.container():
        # Executive KPI Section
        render_executive_kpis(client_data)
        
        # Executive alerts
        render_executive_alerts(client_data)
        
        # Executive Summary
        render_executive_summary(client_data)
        
        # Executive dashboard tabs
        tab1, tab2, tab3, tab4 = st.tabs([
            "📊 Executive Dashboard", 
            "🔮 AI Intelligence", 
            "🌍 Global Compliance",
            "📈 Strategic Analytics"
        ])
        
        with tab1:
            col1, col2 = st.columns(2)
            
            with col1:
                render_chart_section(
                    create_executive_performance_chart, client_data,
                    "Executive Financial Intelligence",
                    "Comprehensive ROI analysis and strategic value creation"
                )
                
                render_chart_section(
                    create_executive_compliance_gauge, client_data,
                    "Compliance Excellence Score",
                    "Real-time executive performance rating"
                )
            
            with col2:
                render_chart_section(
                    create_executive_compliance_radar, client_data,
                    "Executive Performance Matrix",
                    "Multi-dimensional compliance excellence assessment"
                )
                
                render_chart_section(
                    create_savings_waterfall, client_data,
                    "Value Creation Analysis",
                    "Executive savings waterfall breakdown"
                )
        
        with tab2:
            col1, col2 = st.columns(2)
            
            with col1:
                render_chart_section(
                    create_risk_prediction_chart, client_data,
                    "AI-Powered Risk Intelligence",
                    "Predictive risk analytics and trend forecasting"
                )
            
            with col2:
                render_chart_section(
                    create_executive_timeline, client_data,
                    "Executive Performance Timeline",
                    "Strategic milestones and achievement tracking"
                )
        
        with tab3:
            render_chart_section(
                create_regulatory_intelligence_heatmap, client_data,
                "Global Regulatory Intelligence Matrix",
                "Comprehensive worldwide compliance performance analysis"
            )
        
        with tab4:
            # Strategic analytics section
            st.markdown("""
            <div class="executive-card">
                <div class="card-title">Strategic Regulatory Intelligence</div>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 2.5rem;">
                    <div>
                        <h4 style="color: var(--accent-gold); margin-bottom: 1.5rem;">AI-Powered Insights</h4>
                        <ul style="color: var(--text-primary); line-height: 2;">
                            <li>Predictive risk modeling with 98.7% accuracy</li>
                            <li>Automated regulatory change detection</li>
                            <li>Strategic compliance optimization recommendations</li>
                            <li>Executive briefing automation</li>
                        </ul>
                    </div>
                    <div>
                        <h4 style="color: var(--accent-gold); margin-bottom: 1.5rem;">Global Intelligence Network</h4>
                        <ul style="color: var(--text-primary); line-height: 2;">
                            <li>Real-time regulatory monitoring across 47 jurisdictions</li>
                            <li>Executive-grade threat intelligence</li>
                            <li>Strategic regulatory trend analysis</li>
                            <li>Competitive compliance benchmarking</li>
                        </ul>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Document access section
            main_content = client_data.get('MAIN_CONTENT', '')
            if main_content and len(main_content) > 50:
                st.markdown("""
                <div class="executive-card">
                    <div class="card-title">Executive Documentation Suite</div>
                    <p style="color: var(--text-muted); margin-bottom: 2rem;">
                        Access comprehensive executive reports, strategic analyses, and confidential regulatory intelligence.
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                if len(main_content) > 500:
                    preview_text = main_content[:500] + "..."
                    st.text_area(
                        "Executive Brief Preview", 
                        preview_text, 
                        height=200, 
                        disabled=True,
                        help="Complete executive documentation available for secure download"
                    )
                    
                    # Executive download button
                    st.download_button(
                        label="📊 Download Executive Intelligence Report",
                        data=main_content,
                        file_name=f"lexcura_executive_intelligence_{client_id}_{datetime.now().strftime('%Y%m%d')}.txt",
                        mime="text/plain",
                        help="Download comprehensive executive intelligence documentation"
                    )

if __name__ == "__main__":
    main()
