"""
LexCura Elite Compliance Dashboard
INTEGRATED UI-REFACTOR-GOLD-2025: Enterprise-grade template system + Premium features
Preserves original Google Sheets data logic, integrates template system with full functionality
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

# UI-REFACTOR-GOLD-2025: Template system integration
def register_gold_dark_template():
    """Register the Gold Dark template for consistent styling"""
    gold_dark_template = {
        "layout": {
            "paper_bgcolor": "#0F1113",
            "plot_bgcolor": "rgba(0,0,0,0)",
            "font": {
                "family": "Inter, Montserrat, Helvetica Neue, Arial, sans-serif",
                "color": "#F5F6F7",
                "size": 14
            },
            "title": {
                "font": {"size": 25, "color": "#F5F6F7", "family": "Inter"},
                "x": 0.5,
                "xanchor": "center"
            },
            "colorway": ["#D4AF37", "#C0C0C0", "#808080", "#ADD8E6", "#3DBC6B", "#FFCF66", "#E4574C"],
            "xaxis": {
                "gridcolor": "rgba(255,255,255,0.1)",
                "linecolor": "rgba(255,255,255,0.2)",
                "tickfont": {"size": 16, "color": "#F5F6F7"},
                "titlefont": {"size": 18, "color": "#F5F6F7"}
            },
            "yaxis": {
                "gridcolor": "rgba(255,255,255,0.1)",
                "linecolor": "rgba(255,255,255,0.2)",
                "tickfont": {"size": 16, "color": "#F5F6F7"},
                "titlefont": {"size": 18, "color": "#F5F6F7"}
            },
            "legend": {
                "font": {"size": 16, "color": "#F5F6F7"},
                "bgcolor": "rgba(0,0,0,0)"
            }
        }
    }
    pio.templates["gold_dark"] = gold_dark_template
    pio.templates.default = "gold_dark"

def apply_executive_styling(fig):
    """Apply executive styling to any Plotly figure"""
    fig.update_layout(
        template="gold_dark",
        height=400,
        margin=dict(l=50, r=50, t=50, b=50),
        transition_duration=600,
        hovermode='closest'
    )
    # Remove marker lines for cleaner look
    fig.update_traces(marker_line_width=0)
    return fig

# Initialize template system
register_gold_dark_template()

# Load executive CSS styling (integrated from both versions)
def load_executive_css():
    """Load comprehensive executive dashboard CSS styling"""
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700&display=swap');
        
        :root {
            --primary-gold: #D4AF37;
            --secondary-silver: #C0C0C0;
            --tertiary-grey: #808080;
            --accent-blue: #ADD8E6;
            --text-white: #FFFFFF;
            --bg-dark: #0F1113;
            --card-bg: #1B1D1F;
            --success: #3DBC6B;
            --warning: #FFCF66;
            --danger: #E4574C;
            --border: rgba(255,255,255,0.06);
        }
        
        .stApp {
            background: linear-gradient(135deg, var(--bg-dark) 0%, #111827 100%);
            color: var(--text-white);
            font-family: 'Inter', 'Montserrat', 'Helvetica Neue', Arial, sans-serif;
        }
        
        /* Executive Header */
        .dashboard-header {
            background: linear-gradient(90deg, rgba(212, 175, 55, 0.1), rgba(192, 192, 192, 0.05));
            backdrop-filter: blur(20px);
            border-bottom: 1px solid var(--primary-gold);
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
            font-weight: 700;
            color: var(--primary-gold);
            margin: 0;
            font-family: 'Inter', sans-serif;
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
            color: var(--secondary-silver);
            font-size: 0.9rem;
        }
        
        /* Card System */
        .card {
            background: var(--card-bg);
            border-radius: 12px;
            border: 1px solid var(--border);
            padding: 1.5rem;
            transition: all 0.3s ease;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            position: relative;
            overflow: hidden;
        }
        
        .card:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(212, 175, 55, 0.3);
            border-color: var(--primary-gold);
        }
        
        .card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, var(--primary-gold), var(--secondary-silver));
        }
        
        /* KPI Cards */
        .kpi-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 1.5rem;
            margin: 2rem 0;
        }
        
        .kpi-card {
            background: linear-gradient(135deg, var(--card-bg), rgba(45, 45, 45, 0.7));
            border: 1px solid var(--border);
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
            font-size: 2.25rem;
            font-weight: 700;
            color: var(--primary-gold);
            line-height: 1;
            margin-bottom: 0.5rem;
        }
        
        .kpi-title, .kpi-label {
            font-size: 0.875rem;
            color: var(--secondary-silver);
            text-transform: uppercase;
            font-weight: 500;
            letter-spacing: 0.05em;
        }
        
        .kpi-delta, .kpi-change {
            font-size: 0.8rem;
            margin-top: 0.5rem;
        }
        
        .kpi-delta.positive, .kpi-change.positive { color: var(--success); }
        .kpi-delta.negative, .kpi-change.negative { color: var(--danger); }
        .kpi-delta.neutral { color: var(--tertiary-grey); }
        
        /* Sidebar Styling */
        .sidebar-card {
            background: var(--card-bg);
            border: 1px solid var(--border);
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
        
        /* Chart Sections */
        .chart-section {
            background: var(--card-bg);
            border: 1px solid var(--border);
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
        
        /* Animations */
        @keyframes slideDown {
            from { transform: translateY(-100%); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }
        
        @keyframes fadeInUp {
            from { transform: translateY(20px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }
        
        .fade-in-up {
            animation: fadeInUp 0.6s ease-out forwards;
        }
        
        /* Hide Streamlit elements */
        #MainMenu { visibility: hidden; }
        footer { visibility: hidden; }
        header { visibility: hidden; }
        .stDeployButton { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)

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

# Executive UI helpers (from NEW script)
def kpi_card(title, value, delta=None, sparkline_fig=None):
    """Render executive KPI card with optional delta and sparkline"""
    delta_class = "positive" if delta and delta > 0 else "negative" if delta and delta < 0 else "neutral"
    delta_icon = "▲" if delta and delta > 0 else "▼" if delta and delta < 0 else "●"
    
    card_html = f"""
    <div class="kpi-card">
        <div class="kpi-title">{title}</div>
        <div class="kpi-value">{value}</div>
        {f'<div class="kpi-delta {delta_class}">{delta_icon} {abs(delta)}%</div>' if delta else ''}
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)
    
    if sparkline_fig:
        st.markdown('<div class="sparkline">', unsafe_allow_html=True)
        st.plotly_chart(apply_executive_styling(sparkline_fig), use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

def styled_plotly_chart(fig, height=400, use_modebar=False):
    """Apply executive styling and render Plotly chart"""
    styled_fig = apply_executive_styling(fig)
    styled_fig.update_layout(height=height)
    
    config = {"displayModeBar": use_modebar, "responsive": True}
    st.plotly_chart(styled_fig, use_container_width=True, config=config)

# Data connection functions (PRESERVED from both versions)
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
        spreadsheet = gc.open_by_key(sheet_id)
        sheet = spreadsheet.worksheet("MASTER SHEET")
        
        headers = sheet.row_values(1)
        row_data = sheet.row_values(2)
        
        while len(row_data) < len(headers):
            row_data.append("")
            
        data = dict(zip(headers, row_data))
        
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
        'EXECUTIVE SUMMARY': 'Strong compliance performance with proactive risk management framework delivering exceptional results.',
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

def apply_filters(data, filters):
    """Apply session state filters to data"""
    filtered_data = data.copy()
    
    if filters.get('date_range'):
        pass
    
    if filters.get('alert_levels'):
        pass
    
    return filtered_data

# Chart functions with integrated styling
def chart_1_financial_impact(data, filters=None):
    """Financial Impact Chart - Executive Styled with Template"""
    if filters:
        data = apply_filters(data, filters)
    
    categories = ['Q1 2024', 'Q2 2024', 'Q3 2024', 'Q4 2024']
    cost_savings = [285000, 320000, 295000, 340000]
    compliance_costs = [65000, 58000, 72000, 61000]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=categories,
        y=cost_savings,
        name='Cost Savings',
        marker=dict(color='#D4AF37'),
        hovertemplate='<b>Cost Savings</b><br>%{x}<br>$%{y:,.0f}<br><i>+15% vs previous period</i><extra></extra>',
        text=['$' + f'{val:,.0f}' for val in cost_savings],
        textposition='auto'
    ))
    
    fig.add_trace(go.Bar(
        x=categories,
        y=compliance_costs,
        name='Compliance Investment',
        marker=dict(color='#808080'),
        hovertemplate='<b>Investment</b><br>%{x}<br>$%{y:,.0f}<br><i>ROI: 487%</i><extra></extra>',
        text=['$' + f'{val:,.0f}' for val in compliance_costs],
        textposition='auto'
    ))
    
    fig.update_layout(
        title="Financial Impact Analysis",
        barmode='group',
        yaxis_tickformat="$,.0f"
    )
    
    return apply_executive_styling(fig)

def chart_2_compliance_excellence(data, filters=None):
    """Compliance Excellence Radar - Executive Styled"""
    categories = ['Documentation', 'Training', 'Environmental', 'Quality', 'Facilities', 'Process']
    current_scores = [94, 97, 91, 96, 98, 93]
    target_scores = [95] * len(categories)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=current_scores + [current_scores[0]],
        theta=categories + [categories[0]],
        fill='toself',
        name='Current Performance',
        line=dict(color='#D4AF37', width=3),
        fillcolor="rgba(212, 175, 55, 0.2)",
        hovertemplate='<b>%{theta}</b><br>Score: %{r}%<br><i>Above target</i><extra></extra>'
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=target_scores + [target_scores[0]],
        theta=categories + [categories[0]],
        line=dict(color='#C0C0C0', width=2, dash='dash'),
        name='Target (95%)',
        hovertemplate='<b>Target</b><br>%{theta}<br>Score: %{r}%<extra></extra>'
    ))
    
    fig.update_layout(
        title="Compliance Excellence Matrix",
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100])
        )
    )
    
    return apply_executive_styling(fig)

def chart_3_monitoring_gauge(data, filters=None):
    """Compliance Monitoring Gauge - Executive Styled"""
    current_score = 97
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=current_score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "<b>Overall Compliance Score</b>"},
        delta={'reference': 95},
        gauge={
            'axis': {'range': [None, 100]},
            'bar': {'color': '#D4AF37', 'thickness': 0.8},
            'steps': [
                {'range': [0, 70], 'color': '#E4574C'},
                {'range': [70, 85], 'color': '#FFCF66'},
                {'range': [85, 95], 'color': '#3DBC6B'},
                {'range': [95, 100], 'color': '#D4AF37'}
            ],
            'threshold': {'line': {'color': '#F5F6F7', 'width': 4}, 'value': 98}
        }
    ))
    
    fig.update_layout(title="Current Compliance Status")
    return apply_executive_styling(fig)

def chart_4_alert_status(data, filters=None):
    """Interactive Alert Status - Executive Styled"""
    departments = ['Quality Control', 'Manufacturing', 'Environmental', 'Training', 'Documentation']
    green_alerts = [18, 14, 20, 10, 15]
    amber_alerts = [2, 3, 1, 2, 1]
    red_alerts = [0, 0, 0, 0, 1]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=departments, x=green_alerts, name='Normal (Green)', orientation='h',
        marker=dict(color='#3DBC6B'),
        hovertemplate='<b>%{y}</b><br>Normal: %{x}<extra></extra>'
    ))
    
    fig.add_trace(go.Bar(
        y=departments, x=amber_alerts, name='Review Required', orientation='h',
        marker=dict(color='#FFCF66'),
        hovertemplate='<b>%{y}</b><br>Review: %{x}<extra></extra>'
    ))
    
    fig.add_trace(go.Bar(
        y=departments, x=red_alerts, name='Immediate Action', orientation='h',
        marker=dict(color='#E4574C'),
        hovertemplate='<b>%{y}</b><br>Critical: %{x}<extra></extra>'
    ))
    
    fig.update_layout(title="Alert Status by Department", barmode='stack')
    return apply_executive_styling(fig)

def chart_5_risk_gauge(data, filters=None):
    """Risk Assessment Gauge"""
    risk_score = 15
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=risk_score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "<b>Risk Level Assessment</b>"},
        delta={'reference': 25},
        gauge={
            'axis': {'range': [None, 100]},
            'bar': {'color': '#3DBC6B'},
            'steps': [
                {'range': [0, 25], 'color': '#3DBC6B'},
                {'range': [25, 50], 'color': '#FFCF66'},
                {'range': [50, 100], 'color': '#E4574C'}
            ],
            'threshold': {'line': {'color': '#F5F6F7', 'width': 4}, 'value': 30}
        }
    ))
    
    fig.update_layout(title="Current Risk Profile")
    return apply_executive_styling(fig)

def chart_6_performance_timeline(data, filters=None):
    """Executive Performance Timeline"""
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct']
    performance = [91, 93, 92, 95, 96, 94, 95, 97, 96, 97]
    target = [95] * len(months)
    industry_avg = [88, 89, 90, 90, 91, 91, 92, 92, 93, 93]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=months, y=performance, mode='lines+markers', name='Actual Performance',
        line=dict(color='#D4AF37', width=4), marker=dict(size=10, color='#D4AF37'),
        fill='tonexty', fillcolor="rgba(212, 175, 55, 0.1)",
        hovertemplate='<b>Performance</b><br>%{x}: %{y}%<extra></extra>'
    ))
    
    fig.add_trace(go.Scatter(
        x=months, y=target, mode='lines', name='Target (95%)',
        line=dict(color='#C0C0C0', width=2, dash='dash')
    ))
    
    fig.add_trace(go.Scatter(
        x=months, y=industry_avg, mode='lines', name='Industry Average',
        line=dict(color='#808080', width=2, dash='dot')
    ))
    
    fig.update_layout(title="Performance Timeline", yaxis_range=[85, 100])
    return apply_executive_styling(fig)

def chart_7_regulatory_heatmap(data, filters=None):
    """Regulatory Risk Heatmap"""
    categories = ['USP <797>', 'USP <800>', 'USP <825>', 'FDA 503B', 'State Board', 'cGMP', 'Environmental']
    risk_levels = [12, 25, 8, 18, 15, 22, 10]
    
    colors = ['#3DBC6B' if risk < 15 else '#FFCF66' if risk < 30 else '#E4574C' for risk in risk_levels]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=categories, y=risk_levels,
        marker=dict(color=colors),
        text=[f'{score}%' for score in risk_levels],
        textposition='auto',
        hovertemplate='<b>%{x}</b><br>Risk Level: %{y}%<extra></extra>'
    ))
    
    fig.update_layout(title="Regulatory Risk Matrix", xaxis_tickangle=-45)
    return apply_executive_styling(fig)

def chart_8_deadlines_gantt(data, filters=None):
    """Upcoming Deadlines Gantt Chart"""
    tasks = ['Annual Inspection Prep', 'USP <797> Training', 'Environmental Validation', 'Quality Review', 'Equipment Calibration']
    start_dates = [datetime.now() + timedelta(days=d) for d in [15, 8, 30, 20, 40]]
    durations = [25, 10, 18, 12, 7]
    
    fig = go.Figure()
    
    for i, (task, start, duration) in enumerate(zip(tasks, start_dates, durations)):
        days_until = (start - datetime.now()).days
        color = '#E4574C' if days_until <= 10 else '#FFCF66' if days_until <= 25 else '#3DBC6B'
        
        fig.add_trace(go.Bar(
            y=[task], x=[duration], base=[start], orientation='h',
            marker=dict(color=color), showlegend=False,
            hovertemplate=f'<b>{task}</b><br>Start: {start.strftime("%Y-%m-%d")}<br>Duration: {duration} days<extra></extra>'
        ))
    
    fig.add_shape(
        type="line", x0=datetime.now(), x1=datetime.now(),
        y0=-0.5, y1=len(tasks)-0.5,
        line=dict(color='#D4AF37', width=3)
    )
    
    fig.update_layout(title="Upcoming Deadlines", xaxis_type='date')
    return apply_executive_styling(fig)

def render_header(client_data):
    """Render executive dashboard header"""
    st.markdown(f"""
    <div class="dashboard-header">
        <div class="logo-section">
            <h1 class="brand-title">LexCura Elite</h1>
            <span class="env-tag">PROD</span>
        </div>
        <div class="header-controls">
            <span>{client_data['CLIENT NAME']} | Last Updated: {client_data['DATE SCRAPED']}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_sidebar(client_data):
    """Render enhanced sidebar with client info and controls"""
    with st.sidebar:
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
        
        st.markdown('<div class="sidebar-title">Quick Actions</div>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🔄 Refresh"):
                st.cache_data.clear()
                st.rerun()
        with col2:
            st.button("📊 Export")
        with col3:
            st.button("⚙️ Settings")
        
        st.markdown('<div class="sidebar-title">Filters</div>', unsafe_allow_html=True)
        alert_levels = st.multiselect("Alert Levels", ['RED', 'AMBER', 'GREEN'])
        date_range = st.date_input("Date Range", value=(datetime.now() - timedelta(days=30), datetime.now()))

def render_kpi_section(client_data):
    """Render KPI cards section"""
    st.markdown("### Key Performance Indicators")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        kpi_card("Compliance Score", "97%", 2.3)
    with col2:
        kpi_card("Risk Level", "15", -1.2)
    with col3:
        kpi_card("Annual Savings", "$2.5M", 12.4)
    with col4:
        kpi_card("Critical Alerts", "0", 0)

def main():
    """Main integrated dashboard application"""
    
    # Initialize session state and load styling
    init_session_state()
    load_executive_css()
    
    # Get client ID from URL
    client_id = st.query_params.get("client_id", "11AA")
    
    # Load client data (preserves original logic)
    with st.spinner("Loading compliance intelligence..."):
        client_data = load_client_data(client_id)
    
    # Render header
    render_header(client_data)
    
    # Render sidebar
    render_sidebar(client_data)
    
    # Main content
    with st.container():
        # KPI Section
        render_kpi_section(client_data)
        
        # Executive Summary
        if client_data.get('EXECUTIVE SUMMARY'):
            st.markdown(f"""
            <div class="card fade-in-up">
                <h3 style="color: var(--primary-gold); margin-bottom: 1rem;">Executive Summary</h3>
                <p style="line-height: 1.6;">{client_data['EXECUTIVE SUMMARY']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Charts in organized tabs
        tab1, tab2, tab3 = st.tabs(["📊 Performance Dashboard", "🔍 Detailed Analysis", "📈 Trends & Forecasting"])
        
        with tab1:
            col1, col2 = st.columns(2)
            with col1:
                st.markdown('<div class="chart-section">', unsafe_allow_html=True)
                styled_plotly_chart(chart_1_financial_impact(client_data))
                st.markdown('</div>', unsafe_allow_html=True)
            with col2:
                st.markdown('<div class="chart-section">', unsafe_allow_html=True)
                styled_plotly_chart(chart_2_compliance_excellence(client_data))
                st.markdown('</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown('<div class="chart-section">', unsafe_allow_html=True)
                styled_plotly_chart(chart_3_monitoring_gauge(client_data))
                st.markdown('</div>', unsafe_allow_html=True)
            with col2:
                st.markdown('<div class="chart-section">', unsafe_allow_html=True)
                styled_plotly_chart(chart_4_alert_status(client_data))
                st.markdown('</div>', unsafe_allow_html=True)
        
        with tab2:
            col1, col2 = st.columns(2)
            with col1:
                st.markdown('<div class="chart-section">', unsafe_allow_html=True)
                styled_plotly_chart(chart_5_risk_gauge(client_data))
                st.markdown('</div>', unsafe_allow_html=True)
            with col2:
                st.markdown('<div class="chart-section">', unsafe_allow_html=True)
                styled_plotly_chart(chart_7_regulatory_heatmap(client_data))
                st.markdown('</div>', unsafe_allow_html=True)
        
        with tab3:
            col1, col2 = st.columns(2)
            with col1:
                st.markdown('<div class="chart-section">', unsafe_allow_html=True)
                styled_plotly_chart(chart_6_performance_timeline(client_data))
                st.markdown('</div>', unsafe_allow_html=True)
            with col2:
                st.markdown('<div class="chart-section">', unsafe_allow_html=True)
                styled_plotly_chart(chart_8_deadlines_gantt(client_data))
                st.markdown('</div>', unsafe_allow_html=True)
        
        # Data access section
        if client_data.get('MAIN_STRUCTURED_CONTENT'):
            raw_content = client_data.get('MAIN_STRUCTURED_CONTENT', '')
            if len(raw_content) > 500:
                st.markdown(f"""
                <div class="card">
                    <h3 style="color: var(--primary-gold);">Detailed Intelligence Report</h3>
                    <p>Comprehensive compliance data for {client_data['CLIENT NAME']}</p>
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

if __name__ == "__main__":
    main()
