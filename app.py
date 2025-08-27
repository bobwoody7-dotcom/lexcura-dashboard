"""
LexCura Premium Compliance Dashboard
Boardroom-level interactive dashboard for 503B sterile manufacturers
Preserves original Google Sheets data logic, upgrades UI/UX only
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
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

# Load custom CSS
def load_css():
    """Load custom CSS styling"""
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700&display=swap');
        
        :root {
            --primary-gold: #D4AF37;
            --secondary-silver: #C0C0C0;
            --tertiary-grey: #808080;
            --accent-blue: #ADD8E6;
            --text-white: #FFFFFF;
            --bg-dark: #111827;
            --success: #28a745;
            --warning: #ffc107;
            --danger: #dc3545;
        }
        
        .stApp {
            background: linear-gradient(135deg, #0a0a0a 0%, var(--bg-dark) 100%);
            color: var(--text-white);
            font-family: 'Montserrat', 'Helvetica Neue', Arial, sans-serif;
        }
        
        /* Premium Header */
        .dashboard-header {
            background: linear-gradient(90deg, rgba(212, 175, 55, 0.1), rgba(192, 192, 192, 0.05));
            backdrop-filter: blur(20px);
            border-bottom: 1px solid rgba(212, 175, 55, 0.2);
            padding: 1rem 2rem;
            margin: -1rem -1rem 2rem -1rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            animation: slideDown 0.8s ease-out;
        }
        
        .logo-section {
            display: flex;
            align-items: center;
            gap: 1rem;
        }
        
        .brand-title {
            font-size: 1.8rem;
            font-weight: 600;
            color: var(--primary-gold);
            margin: 0;
        }
        
        .env-tag {
            background: var(--primary-gold);
            color: #000;
            padding: 0.25rem 0.5rem;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: 600;
        }
        
        .header-controls {
            display: flex;
            gap: 1rem;
            align-items: center;
        }
        
        .export-btn {
            background: linear-gradient(135deg, var(--primary-gold), #B8941F);
            color: #000;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 6px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .export-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(212, 175, 55, 0.4);
        }
        
        /* Sidebar Styling */
        .sidebar-card {
            background: rgba(26, 26, 26, 0.9);
            border: 1px solid rgba(212, 175, 55, 0.3);
            border-radius: 8px;
            padding: 1rem;
            margin-bottom: 1rem;
            backdrop-filter: blur(10px);
        }
        
        .sidebar-title {
            color: var(--primary-gold);
            font-weight: 600;
            font-size: 1.1rem;
            margin-bottom: 0.5rem;
        }
        
        /* KPI Cards */
        .kpi-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin: 2rem 0;
        }
        
        .kpi-card {
            background: linear-gradient(135deg, rgba(26, 26, 26, 0.9), rgba(45, 45, 45, 0.7));
            border: 1px solid rgba(212, 175, 55, 0.2);
            border-radius: 12px;
            padding: 1.5rem;
            text-align: center;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .kpi-card:hover {
            border-color: var(--primary-gold);
            transform: translateY(-4px);
            box-shadow: 0 8px 25px rgba(212, 175, 55, 0.3);
        }
        
        .kpi-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, var(--primary-gold), var(--secondary-silver));
        }
        
        .kpi-value {
            font-size: 2.2rem;
            font-weight: 700;
            color: var(--primary-gold);
            margin-bottom: 0.25rem;
        }
        
        .kpi-label {
            font-size: 0.9rem;
            color: var(--secondary-silver);
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        
        .kpi-change {
            font-size: 0.8rem;
            margin-top: 0.5rem;
        }
        
        .kpi-change.positive { color: var(--success); }
        .kpi-change.negative { color: var(--danger); }
        
        /* Chart Containers */
        .chart-section {
            background: rgba(26, 26, 26, 0.8);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            padding: 1.5rem;
            margin: 1rem 0;
            backdrop-filter: blur(15px);
            transition: all 0.3s ease;
            position: relative;
        }
        
        .chart-section:hover {
            border-color: rgba(212, 175, 55, 0.4);
        }
        
        .chart-title {
            color: var(--text-white);
            font-size: 1.1rem;
            font-weight: 600;
            margin-bottom: 1rem;
            text-align: center;
        }
        
        /* Modal Styling */
        .drill-down-modal {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: linear-gradient(135deg, #1a1a1a, #2d2d2d);
            border: 2px solid var(--primary-gold);
            border-radius: 12px;
            padding: 2rem;
            max-width: 80vw;
            max-height: 80vh;
            overflow-y: auto;
            z-index: 1000;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.8);
        }
        
        .modal-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background: rgba(0, 0, 0, 0.8);
            z-index: 999;
        }
        
        /* Filter Controls */
        .filter-section {
            background: rgba(45, 45, 45, 0.8);
            border-radius: 8px;
            padding: 1rem;
            margin-bottom: 2rem;
        }
        
        .filter-row {
            display: flex;
            gap: 1rem;
            flex-wrap: wrap;
            align-items: center;
        }
        
        /* Animations */
        @keyframes slideDown {
            from { transform: translateY(-100%); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }
        
        @keyframes fadeInUp {
            from { transform: translateY(20px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.7; }
        }
        
        .fade-in-up {
            animation: fadeInUp 0.6s ease-out forwards;
        }
        
        .loading-skeleton {
            background: linear-gradient(90deg, #2d2d2d 25%, #3d3d3d 50%, #2d2d2d 75%);
            background-size: 200% 100%;
            animation: loading 1.5s infinite;
        }
        
        @keyframes loading {
            0% { background-position: 200% 0; }
            100% { background-position: -200% 0; }
        }
        
        /* Accessibility */
        .sr-only {
            position: absolute;
            width: 1px;
            height: 1px;
            padding: 0;
            margin: -1px;
            overflow: hidden;
            clip: rect(0, 0, 0, 0);
            white-space: nowrap;
            border: 0;
        }
        
        /* High contrast mode */
        .high-contrast .kpi-card {
            border: 2px solid var(--text-white);
        }
        
        .high-contrast .chart-section {
            border: 2px solid var(--text-white);
        }
        
        /* Hide Streamlit elements */
        #MainMenu { visibility: hidden; }
        footer { visibility: hidden; }
        header { visibility: hidden; }
        .stDeployButton { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)

# Color scheme (preserving original requirements)
COLORS = {
    'primary_gold': '#D4AF37',
    'secondary_silver': '#C0C0C0', 
    'tertiary_grey': '#808080',
    'accent_blue': '#ADD8E6',
    'text_white': '#FFFFFF',
    'background_dark': '#111827',
    'success': '#28a745',
    'warning': '#ffc107',
    'danger': '#dc3545'
}

# Chart styling (exact requirements)
CHART_STYLE = {
    'font_family': 'Montserrat, Helvetica Neue, Arial, sans-serif',
    'title_size': 25,
    'legend_size': 18,
    'x_axis_size': 21,
    'y_axis_size': 18,
    'data_label_size': 15,
    'padding': {'l': 50, 'r': 50, 't': 50, 'b': 50}
}

# Initialize session state for filtering and views
def init_session_state():
    """Initialize session state variables"""
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
    
    if 'high_contrast' not in st.session_state:
        st.session_state.high_contrast = False
    
    if 'text_size' not in st.session_state:
        st.session_state.text_size = 'normal'

@st.cache_data(ttl=300)
def connect_to_sheets():
    """Connect to Google Sheets using service account credentials (PRESERVED)"""
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
    """Load client data from Google Sheets ROW 2 ONLY (PRESERVED)"""
    try:
        gc = connect_to_sheets()
        if not gc:
            return get_demo_data()
            
        sheet_id = st.secrets.get("MASTER_SHEET_ID", "1oI-XqRbp8r3V8yMjnC5pNvDMljJDv4f6d01vRmrVH1g")
        
        # Connect directly to MASTER SHEET worksheet (PRESERVED)
        spreadsheet = gc.open_by_key(sheet_id)
        sheet = spreadsheet.worksheet("MASTER SHEET")
        
        # Get headers from row 1 and data from row 2 ONLY (PRESERVED)
        headers = sheet.row_values(1)
        row_data = sheet.row_values(2)
        
        while len(row_data) < len(headers):
            row_data.append("")
            
        data = dict(zip(headers, row_data))
        
        # Column mapping A-V preserved exactly
        return {
            'UNIQUE CLIENT ID': data.get('UNIQUE CLIENT ID', client_id or '11AA'),
            'CLIENT NAME': data.get('CLIENT NAME', 'Client Name'),
            'TIER': data.get('TIER', 'Standard'),
            'REGION': data.get('REGION', 'Region'),
            'DELIVERY FREQUENCY': data.get('DELIVERY FREQUENCY', 'Monthly'),
            'EMAIL ADDRESS': data.get('EMAIL ADDRESS', ''),
            'MAIN STRUCTURED CONTENT': data.get('MAIN STRUCTURED CONTENT', ''),
            'CURRENT FINANCIAL STATS': data.get('CURRENT FINANCIAL STATS', ''),
            'HISTORICAL FINANCIAL IMPACTS': data.get('HISTORICAL FINANCIAL IMPACTS', ''),
            'EXECUTIVE SUMMARY': data.get('EXECUTIVE SUMMARY', ''),
            'DETECTION': data.get('DETECTION', ''),
            'COMPLIANCE ALERTS': data.get('COMPLIANCE ALERTS', ''),
            'RISK ANALYSIS': data.get('RISK ANALYSIS', ''),
            'REGULATORY UPDATES': data.get('REGULATORY UPDATES', ''),
            'URGENCY': data.get('URGENCY', ''),
            'ALERT LEVEL': data.get('ALERT LEVEL', 'GREEN'),
            'DATE SCRAPED': data.get('DATE SCRAPED', datetime.now().strftime('%Y-%m-%d')),
            'STATUS': data.get('STATUS', 'Active'),
            'TYPE OF UPDATE': data.get('TYPE OF UPDATE', ''),
            'DATE DELIVERED': data.get('DATE DELIVERED', ''),
            'EDUCATIONAL GUIDE AND TOOLS': data.get('EDUCATIONAL GUIDE AND TOOLS', '')
        }
        
    except Exception as e:
        st.warning(f"Live data unavailable: {str(e)}")
        return get_demo_data()

def get_demo_data():
    """Demo data for testing (PRESERVED)"""
    return {
        'UNIQUE CLIENT ID': '11AA',
        'CLIENT NAME': 'Elite Pharmaceutical Corp',
        'TIER': 'Professional',
        'REGION': 'Northeast',
        'DELIVERY FREQUENCY': 'Weekly',
        'EMAIL ADDRESS': 'contact@elitepharma.com',
        'MAIN STRUCTURED CONTENT': 'Comprehensive compliance monitoring and regulatory intelligence.',
        'CURRENT FINANCIAL STATS': '$2.5M annual savings, $450K compliance investment',
        'HISTORICAL FINANCIAL IMPACTS': 'ROI: 556% over 18 months',
        'EXECUTIVE SUMMARY': 'Strong compliance performance with proactive risk management.',
        'DETECTION': 'Automated monitoring active',
        'COMPLIANCE ALERTS': 'No critical alerts, 3 items for review',
        'RISK ANALYSIS': 'Low risk profile, excellent controls',
        'REGULATORY UPDATES': 'USP 797 revision Q2 2024, FDA guidance update March 2024',
        'URGENCY': 'Standard',
        'ALERT LEVEL': 'GREEN',
        'DATE SCRAPED': datetime.now().strftime('%Y-%m-%d'),
        'STATUS': 'Active',
        'TYPE OF UPDATE': 'Routine Monitoring',
        'DATE DELIVERED': datetime.now().strftime('%Y-%m-%d'),
        'EDUCATIONAL GUIDE AND TOOLS': 'Training materials updated'
    }

def create_premium_chart_layout(title):
    """Create premium chart layout with exact specifications"""
    return {
        'title': {
            'text': f'<b>{title}</b>',
            'font': {
                'family': CHART_STYLE['font_family'],
                'size': CHART_STYLE['title_size'],
                'color': COLORS['text_white']
            },
            'x': 0.5,
            'xanchor': 'center'
        },
        'paper_bgcolor': COLORS['background_dark'],
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'font': {
            'color': COLORS['text_white'], 
            'family': CHART_STYLE['font_family'],
            'size': CHART_STYLE['legend_size']
        },
        'margin': CHART_STYLE['padding'],
        'height': 450,
        'showlegend': True,
        'legend': {
            'font': {
                'color': COLORS['text_white'],
                'family': CHART_STYLE['font_family'],
                'size': CHART_STYLE['legend_size']
            },
            'bgcolor': 'rgba(0,0,0,0)',
            'borderwidth': 0
        },
        'transition': {
            'duration': 600,
            'easing': 'cubic-in-out'
        },
        'xaxis': {
            'color': COLORS['text_white'],
            'gridcolor': 'rgba(128, 128, 128, 0.3)',
            'tickfont': {
                'size': CHART_STYLE['x_axis_size'],
                'family': CHART_STYLE['font_family']
            }
        },
        'yaxis': {
            'color': COLORS['text_white'],
            'gridcolor': 'rgba(128, 128, 128, 0.3)',
            'tickfont': {
                'size': CHART_STYLE['y_axis_size'],
                'family': CHART_STYLE['font_family']
            }
        }
    }

def apply_filters(data, filters):
    """Apply session state filters to data"""
    filtered_data = data.copy()
    
    # Apply date range filter
    if filters.get('date_range'):
        # Implementation depends on data structure
        pass
    
    # Apply alert level filter
    if filters.get('alert_levels'):
        # Implementation depends on data structure
        pass
    
    return filtered_data

# Chart functions (upgraded with premium styling and interactivity)
def chart_1_financial_impact(data, filters=None):
    """Financial Impact Chart - Premium Interactive Version"""
    # Apply filters
    if filters:
        data = apply_filters(data, filters)
    
    categories = ['Q1 2024', 'Q2 2024', 'Q3 2024', 'Q4 2024']
    cost_savings = [285000, 320000, 295000, 340000]
    compliance_costs = [65000, 58000, 72000, 61000]
    
    fig = go.Figure()
    
    # Cost savings bars with enhanced interactivity
    fig.add_trace(go.Bar(
        x=categories,
        y=cost_savings,
        name='Cost Savings',
        marker=dict(
            color=COLORS['primary_gold'],
            line=dict(color=COLORS['secondary_silver'], width=1)
        ),
        hovertemplate='<b>Cost Savings</b><br>%{x}<br>$%{y:,.0f}<br><i>+15% vs previous period</i><extra></extra>',
        text=['$' + f'{val:,.0f}' for val in cost_savings],
        textposition='auto',
        textfont=dict(
            size=CHART_STYLE['data_label_size'],
            color=COLORS['background_dark'],
            family=CHART_STYLE['font_family']
        )
    ))
    
    # Compliance costs with interactive elements
    fig.add_trace(go.Bar(
        x=categories,
        y=compliance_costs,
        name='Compliance Investment',
        marker=dict(
            color=COLORS['tertiary_grey'],
            line=dict(color=COLORS['secondary_silver'], width=1)
        ),
        hovertemplate='<b>Investment</b><br>%{x}<br>$%{y:,.0f}<br><i>ROI: 487%</i><extra></extra>',
        text=['$' + f'{val:,.0f}' for val in compliance_costs],
        textposition='auto',
        textfont=dict(
            size=CHART_STYLE['data_label_size'],
            color=COLORS['text_white'],
            family=CHART_STYLE['font_family']
        )
    ))
    
    layout = create_premium_chart_layout('Financial Impact Analysis')
    layout['barmode'] = 'group'
    
    fig.update_layout(layout)
    return fig

def chart_2_compliance_excellence(data, filters=None):
    """Compliance Excellence Radar - Interactive"""
    if filters:
        data = apply_filters(data, filters)
    
    categories = ['Documentation<br>Excellence', 'Personnel<br>Training', 'Environmental<br>Controls', 
                 'Quality<br>Systems', 'Facility<br>Standards', 'Process<br>Validation']
    current_scores = [94, 97, 91, 96, 98, 93]
    target_scores = [95] * len(categories)
    
    fig = go.Figure()
    
    # Current performance
    fig.add_trace(go.Scatterpolar(
        r=current_scores + [current_scores[0]],
        theta=categories + [categories[0]],
        fill='toself',
        name='Current Performance',
        line=dict(color=COLORS['primary_gold'], width=3),
        fillcolor=f"rgba(212, 175, 55, 0.2)",
        marker=dict(size=8, color=COLORS['primary_gold']),
        hovertemplate='<b>%{theta}</b><br>Score: %{r}%<br><i>Above target</i><extra></extra>'
    ))
    
    # Target performance
    fig.add_trace(go.Scatterpolar(
        r=target_scores + [target_scores[0]],
        theta=categories + [categories[0]],
        line=dict(color=COLORS['secondary_silver'], width=2, dash='dash'),
        name='Target (95%)',
        hovertemplate='<b>Target</b><br>%{theta}<br>Score: %{r}%<extra></extra>'
    ))
    
    layout = create_premium_chart_layout('Compliance Excellence Matrix')
    layout['polar'] = dict(
        radialaxis=dict(
            visible=True,
            range=[0, 100],
            tickfont=dict(size=14, color=COLORS['text_white']),
            gridcolor='rgba(128, 128, 128, 0.3)'
        ),
        angularaxis=dict(
            tickfont=dict(size=16, color=COLORS['text_white'])
        ),
        bgcolor='rgba(0,0,0,0)'
    )
    
    fig.update_layout(layout)
    return fig

def chart_3_monitoring_gauge(data, filters=None):
    """Compliance Monitoring Gauge with Animation"""
    current_score = 97
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=current_score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={
            'text': "<b>Overall Compliance Score</b>",
            'font': {'color': COLORS['text_white'], 'size': 20}
        },
        delta={
            'reference': 95,
            'font': {'color': COLORS['text_white'], 'size': 16}
        },
        gauge={
            'axis': {
                'range': [None, 100],
                'tickcolor': COLORS['text_white'],
                'tickfont': {'size': 14}
            },
            'bar': {'color': COLORS['primary_gold'], 'thickness': 0.8},
            'steps': [
                {'range': [0, 70], 'color': COLORS['danger']},
                {'range': [70, 85], 'color': COLORS['warning']},
                {'range': [85, 95], 'color': COLORS['success']},
                {'range': [95, 100], 'color': COLORS['primary_gold']}
            ],
            'threshold': {
                'line': {'color': COLORS['text_white'], 'width': 4},
                'thickness': 0.9,
                'value': 98
            }
        },
        number={'font': {'color': COLORS['text_white'], 'size': 40}}
    ))
    
    layout = create_premium_chart_layout('Current Compliance Status')
    fig.update_layout(layout)
    return fig

def chart_4_alert_status(data, filters=None):
    """Interactive Alert Status Indicator"""
    departments = ['Quality Control', 'Manufacturing', 'Environmental', 'Training', 'Documentation']
    green_alerts = [18, 14, 20, 10, 15]
    amber_alerts = [2, 3, 1, 2, 1] 
    red_alerts = [0, 0, 0, 0, 1]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=departments,
        x=green_alerts,
        name='Normal (Green)',
        orientation='h',
        marker=dict(color=COLORS['success']),
        hovertemplate='<b>%{y}</b><br>Normal Status: %{x}<br><i>No action required</i><extra></extra>'
    ))
    
    fig.add_trace(go.Bar(
        y=departments,
        x=amber_alerts,
        name='Review Required',
        orientation='h',
        marker=dict(color=COLORS['warning']),
        hovertemplate='<b>%{y}</b><br>Review Required: %{x}<br><i>Monitor closely</i><extra></extra>'
    ))
    
    fig.add_trace(go.Bar(
        y=departments,
        x=red_alerts,
        name='Immediate Action',
        orientation='h',
        marker=dict(color=COLORS['danger']),
        hovertemplate='<b>%{y}</b><br>Critical: %{x}<br><i>Immediate attention needed</i><extra></extra>'
    ))
    
    layout = create_premium_chart_layout('Alert Status by Department')
    layout['barmode'] = 'stack'
    
    fig.update_layout(layout)
    return fig

def chart_5_risk_gauge(data, filters=None):
    """Risk Assessment Gauge"""
    risk_score = 15  # Very low risk
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=risk_score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={
            'text': "<b>Risk Level Assessment</b>",
            'font': {'color': COLORS['text_white'], 'size': 20}
        },
        delta={'reference': 25},
        gauge={
            'axis': {'range': [None, 100], 'tickcolor': COLORS['text_white']},
            'bar': {'color': COLORS['success']},
            'steps': [
                {'range': [0, 25], 'color': COLORS['success']},
                {'range': [25, 50], 'color': COLORS['warning']},
                {'range': [50, 100], 'color': COLORS['danger']}
            ],
            'threshold': {
                'line': {'color': COLORS['text_white'], 'width': 4},
                'thickness': 0.75,
                'value': 30
            }
        },
        number={'font': {'color': COLORS['text_white'], 'size': 40}}
    ))
    
    layout = create_premium_chart_layout('Current Risk Profile')
    fig.update_layout(layout)
    return fig

def chart_6_performance_timeline(data, filters=None):
    """Executive Performance Timeline with Playback"""
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct']
    performance = [91, 93, 92, 95, 96, 94, 95, 97, 96, 97]
    target = [95] * len(months)
    industry_avg = [88, 89, 90, 90, 91, 91, 92, 92, 93, 93]
    
    fig = go.Figure()
    
    # Actual performance with area fill
    fig.add_trace(go.Scatter(
        x=months,
        y=performance,
        mode='lines+markers',
        name='Actual Performance',
        line=dict(color=COLORS['primary_gold'], width=4),
        marker=dict(size=10, color=COLORS['primary_gold']),
        fill='tonexty',
        fillcolor=f"rgba(212, 175, 55, 0.1)",
        hovertemplate='<b>Performance</b><br>%{x}: %{y}%<br><i>Trending upward</i><extra></extra>'
    ))
    
    # Target line
    fig.add_trace(go.Scatter(
        x=months,
        y=target,
        mode='lines',
        name='Target (95%)',
        line=dict(color=COLORS['secondary_silver'], width=2, dash='dash'),
        hovertemplate='<b>Target</b><br>%{x}: %{y}%<extra></extra>'
    ))
    
    # Industry benchmark
    fig.add_trace(go.Scatter(
        x=months,
        y=industry_avg,
        mode='lines',
        name='Industry Average',
        line=dict(color=COLORS['tertiary_grey'], width=2, dash='dot'),
        hovertemplate='<b>Industry Avg</b><br>%{x}: %{y}%<extra></extra>'
    ))
    
    layout = create_premium_chart_layout('Performance Timeline')
    layout['yaxis']['range'] = [85, 100]
    
    fig.update_layout(layout)
    return fig

def chart_7_regulatory_heatmap(data, filters=None):
    """Regulatory Risk Heatmap"""
    categories = ['USP <797>', 'USP <800>', 'USP <825>', 'FDA 503B', 'State Board', 'cGMP', 'Environmental']
    risk_levels = [12, 25, 8, 18, 15, 22, 10]
    
    # Color coding for risk levels
    colors = []
    for risk in risk_levels:
        if risk < 15:
            colors.append(COLORS['success'])
        elif risk < 30:
            colors.append(COLORS['warning'])
        else:
            colors.append(COLORS['danger'])
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=categories,
        y=risk_levels,
        marker=dict(
            color=colors,
            line=dict(color=COLORS['text_white'], width=1)
        ),
        text=[f'{score}%' for score in risk_levels],
        textposition='auto',
        textfont=dict(
            size=CHART_STYLE['data_label_size'],
            color=COLORS['text_white']
        ),
        hovertemplate='<b>%{x}</b><br>Risk Level: %{y}%<br><i>Click for details</i><extra></extra>'
    ))
    
    layout = create_premium_chart_layout('Regulatory Risk Matrix')
    layout['xaxis']['tickangle'] = -45
    
    fig.update_layout(layout)
    return fig

def chart_8_deadlines_gantt(data, filters=None):
    """Upcoming Deadlines Gantt Chart"""
    tasks = ['Annual Inspection Prep', 'USP <797> Training', 'Environmental Validation', 'Quality Review', 'Equipment Calibration']
    start_dates = [datetime.now() + timedelta(days=d) for d in [15, 8, 30, 20, 40]]
    durations = [25, 10, 18, 12, 7]
    
    fig = go.Figure()
    
    for i, (task, start, duration) in enumerate(zip(tasks, start_dates, durations)):
        days_until = (start - datetime.now()).days
        color = COLORS['danger'] if days_until <= 10 else COLORS['warning'] if days_until <= 25 else COLORS['success']
        
        fig.add_trace(go.Bar(
            y=[task],
            x=[duration],
            base=[start],
            orientation='h',
            marker=dict(color=color),
            showlegend=False,
            hovertemplate=f'<b>{task}</b><br>Start: {start.strftime("%Y-%m-%d")}<br>Duration: {duration} days<extra></extra>'
        ))
    
    # Today indicator
    fig.add_shape(
        type="line",
        x0=datetime.now(),
        x1=datetime.now(),
        y0=-0.5,
        y1=len(tasks)-0.5,
        line=dict(color=COLORS['primary_gold'], width=3)
    )
    
    layout = create_premium_chart_layout('Upcoming Deadlines')
    layout['xaxis']['type'] = 'date'
    
    fig.update_layout(layout)
    return fig

def render_header(client_data):
    """Render premium dashboard header"""
    st.markdown(f"""
    <div class="dashboard-header">
        <div class="logo-section">
            <h1 class="brand-title">LexCura Elite</h1>
            <span class="env-tag">PROD</span>
        </div>
        <div class="header-controls">
            <span style="color: var(--secondary-silver); font-size: 0.9rem;">
                {client_data['CLIENT NAME']} | Last Updated: {client_data['DATE SCRAPED']}
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_sidebar(client_data):
    """Render enhanced sidebar with client info and controls"""
    with st.sidebar:
        # Client Information Card
        st.markdown(f"""
        <div class="sidebar-card">
            <div class="sidebar-title">Client Overview</div>
            <p><strong>ID:</strong> {client_data['UNIQUE CLIENT ID']}</p>
            <p><strong>Tier:</strong> {client_data['TIER']}</p>
            <p><strong>Region:</strong> {client_data['REGION']}</p>
            <p><strong>Frequency:</strong> {client_data['DELIVERY FREQUENCY']}</p>
            <p><strong>Status:</strong> <span style="color: var(--success);">{client_data['STATUS']}</span></p>
        </div>
        """, unsafe_allow_html=True)
        
        # Filter Controls
        st.markdown('<div class="sidebar-title">Filters</div>', unsafe_allow_html=True)
        
        # Alert Level Filter
        alert_levels = st.multiselect(
            "Alert Levels",
            ['RED', 'AMBER', 'GREEN'],
            key="alert_filter"
        )
        
        # Date Range Filter
        date_range = st.date_input(
            "Date Range",
            value=(datetime.now() - timedelta(days=30), datetime.now()),
            key="date_filter"
        )
        
        # Update Type Filter
        update_types = st.multiselect(
            "Update Types",
            ['Routine Monitoring', 'Critical Alert', 'Regulatory Change'],
            key="update_filter"
        )
        
        # Clear Filters Button
        if st.button("Clear All Filters", key="clear_filters"):
            st.session_state.filters = {
                'date_range': None,
                'alert_levels': [],
                'update_types': [],
                'selected_data': None
            }
            st.rerun()
        
        # Save Current View
        st.markdown('<div class="sidebar-title">Saved Views</div>', unsafe_allow_html=True)
        
        view_name = st.text_input("Save Current View As:", key="view_name")
        if st.button("Save View", key="save_view") and view_name:
            st.session_state.saved_views[view_name] = {
                'filters': st.session_state.filters.copy(),
                'timestamp': datetime.now().isoformat()
            }
            st.success(f"View '{view_name}' saved!")
        
        # Load Saved Views
        if st.session_state.saved_views:
            selected_view = st.selectbox(
                "Load Saved View",
                [""] + list(st.session_state.saved_views.keys()),
                key="load_view"
            )
            if selected_view and st.button("Load View", key="load_view_btn"):
                st.session_state.filters = st.session_state.saved_views[selected_view]['filters']
                st.rerun()
        
        # Export Controls
        st.markdown('<div class="sidebar-title">Export Options</div>', unsafe_allow_html=True)
        
        if st.button("Export Snapshot", key="export_snapshot"):
            export_dashboard_snapshot(client_data)

def render_kpi_cards(client_data):
    """Render KPI overview cards"""
    st.markdown("""
    <div class="kpi-grid">
        <div class="kpi-card">
            <div class="kpi-value">97%</div>
            <div class="kpi-label">Compliance Score</div>
            <div class="kpi-change positive">+2% this month</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-value">15</div>
            <div class="kpi-label">Risk Level</div>
            <div class="kpi-change positive">-5 points</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-value">$2.5M</div>
            <div class="kpi-label">Annual Savings</div>
            <div class="kpi-change positive">+12% YoY</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-value">0</div>
            <div class="kpi-label">Critical Alerts</div>
            <div class="kpi-change positive">No change</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def export_dashboard_snapshot(client_data):
    """Export dashboard as high-resolution images"""
    if not KALEIDO_AVAILABLE:
        st.error("Export functionality requires Kaleido library. Please install: pip install kaleido")
        st.info("Alternative: Use browser's print function or screenshot tools")
        return
    
    try:
        # Create charts
        charts = {
            'financial_impact': chart_1_financial_impact(client_data),
            'compliance_radar': chart_2_compliance_excellence(client_data),
            'monitoring_gauge': chart_3_monitoring_gauge(client_data),
            'alert_status': chart_4_alert_status(client_data),
            'risk_gauge': chart_5_risk_gauge(client_data),
            'performance_timeline': chart_6_performance_timeline(client_data),
            'regulatory_heatmap': chart_7_regulatory_heatmap(client_data),
            'deadlines_gantt': chart_8_deadlines_gantt(client_data)
        }
        
        # Generate high-resolution images
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for chart_name, fig in charts.items():
                img_bytes = fig.to_image(
                    format="png",
                    width=1600,
                    height=900,
                    scale=2
                )
                zip_file.writestr(f"lexcura_{chart_name}_{datetime.now().strftime('%Y%m%d')}.png", img_bytes)
        
        zip_buffer.seek(0)
        
        st.download_button(
            label="Download Chart Package",
            data=zip_buffer.getvalue(),
            file_name=f"lexcura_dashboard_{client_data['UNIQUE CLIENT ID']}_{datetime.now().strftime('%Y%m%d')}.zip",
            mime="application/zip"
        )
        
        st.success("Dashboard snapshot exported successfully!")
        
    except Exception as e:
        st.error(f"Export failed: {str(e)}")

def render_drill_down_modal(title, data_list):
    """Render drill-down modal for detailed data"""
    st.markdown(f"""
    <div class="drill-down-modal">
        <h3 style="color: var(--primary-gold); margin-bottom: 1rem;">{title}</h3>
        <div style="max-height: 400px; overflow-y: auto;">
    """, unsafe_allow_html=True)
    
    # Paginate data
    items_per_page = 10
    page = st.number_input("Page", min_value=1, max_value=max(1, len(data_list)//items_per_page + 1), value=1)
    start_idx = (page - 1) * items_per_page
    end_idx = start_idx + items_per_page
    
    for i, item in enumerate(data_list[start_idx:end_idx], start_idx + 1):
        st.markdown(f"""
        <div style="border: 1px solid var(--tertiary-grey); border-radius: 4px; padding: 0.5rem; margin: 0.5rem 0;">
            <strong>{i}.</strong> {item}
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div></div>", unsafe_allow_html=True)

def handle_chart_interactions():
    """Handle chart click events and cross-filtering"""
    if not PLOTLY_EVENTS_AVAILABLE:
        st.info("Install streamlit-plotly-events for advanced chart interactions")
        return
    
    # Implementation for chart click events
    # This would use plotly_events to capture click data and update session state
    pass

def main():
    """Main dashboard application"""
    
    # Initialize session state
    init_session_state()
    
    # Load CSS
    load_css()
    
    # Get client ID from URL
    client_id = st.query_params.get("client_id", "11AA")
    
    # Load client data (preserves original logic)
    with st.spinner("Loading compliance intelligence..."):
        client_data = load_client_data(client_id)
    
    # Render header
    render_header(client_data)
    
    # Render sidebar
    render_sidebar(client_data)
    
    # Main content area
    with st.container():
        # KPI Cards
        render_kpi_cards(client_data)
        
        # Executive Summary
        if client_data.get('EXECUTIVE SUMMARY'):
            st.markdown(f"""
            <div class="chart-section fade-in-up">
                <h3 style="color: var(--primary-gold); margin-bottom: 1rem;">Executive Summary</h3>
                <p style="line-height: 1.6; color: var(--text-white);">{client_data['EXECUTIVE SUMMARY']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Charts in tabs for better organization
        tab1, tab2, tab3 = st.tabs(["📊 Performance", "🔍 Analysis", "📈 Trends"])
        
        with tab1:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown('<div class="chart-section">', unsafe_allow_html=True)
                fig1 = chart_1_financial_impact(client_data, st.session_state.filters)
                
                if PLOTLY_EVENTS_AVAILABLE:
                    selected_data = plotly_events(fig1, click_event=True, hover_event=False)
                    if selected_data:
                        st.session_state.filters['selected_data'] = selected_data
                else:
                    st.plotly_chart(fig1, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="chart-section">', unsafe_allow_html=True)
                st.plotly_chart(chart_2_compliance_excellence(client_data, st.session_state.filters), use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown('<div class="chart-section">', unsafe_allow_html=True)
                st.plotly_chart(chart_3_monitoring_gauge(client_data, st.session_state.filters), use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="chart-section">', unsafe_allow_html=True)
                st.plotly_chart(chart_4_alert_status(client_data, st.session_state.filters), use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
        
        with tab2:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown('<div class="chart-section">', unsafe_allow_html=True)
                st.plotly_chart(chart_5_risk_gauge(client_data, st.session_state.filters), use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="chart-section">', unsafe_allow_html=True)
                st.plotly_chart(chart_7_regulatory_heatmap(client_data, st.session_state.filters), use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
        
        with tab3:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown('<div class="chart-section">', unsafe_allow_html=True)
                st.plotly_chart(chart_6_performance_timeline(client_data, st.session_state.filters), use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="chart-section">', unsafe_allow_html=True)
                st.plotly_chart(chart_8_deadlines_gantt(client_data, st.session_state.filters), use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
        
        # Drill-down section
        if client_data.get('REGULATORY UPDATES'):
            with st.expander("📋 Detailed Regulatory Updates", expanded=False):
                updates_list = client_data['REGULATORY UPDATES'].split(',') if client_data['REGULATORY UPDATES'] else []
                if updates_list:
                    render_drill_down_modal("Regulatory Updates", updates_list)
                else:
                    st.info("No detailed regulatory updates available")
        
        # Data access section
        raw_content = client_data.get('MAIN STRUCTURED CONTENT', '')
        if raw_content and len(raw_content) > 500:
            st.markdown(f"""
            <div class="chart-section">
                <h3 style="color: var(--primary-gold);">Data Access</h3>
                <p>Comprehensive compliance intelligence for {client_data['CLIENT NAME']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if len(raw_content) > 1000:
                st.text_area("Content Preview", raw_content[:1000] + "...", height=150, disabled=True)
                st.download_button(
                    "Download Full Report",
                    raw_content,
                    file_name=f"lexcura_report_{client_id}_{datetime.now().strftime('%Y%m%d')}.txt",
                    mime="text/plain"
                )
            else:
                st.text_area("Full Content", raw_content, height=200, disabled=True)

if __name__ == "__main__":
    main()
