# LexCura Minimal Elegant Compliance Dashboard
# Clean, animated, professional design for 503B compliance monitoring

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import gspread
from google.oauth2.service_account import Credentials
import json
import io
from datetime import datetime, timedelta
import numpy as np
import time

# Page configuration
st.set_page_config(
    page_title="LexCura",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Minimal Elegant Design with Subtle Animations
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        box-sizing: border-box;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%);
        color: #e8e8e8;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Elegant header with subtle animation */
    .main-header {
        font-size: 2.2rem;
        font-weight: 300;
        text-align: center;
        font-family: 'Inter', sans-serif;
        color: #ffffff;
        margin: 2rem 0;
        letter-spacing: -0.02em;
        opacity: 0;
        animation: fadeInUp 0.8s ease-out forwards;
    }
    
    .main-header .accent {
        font-weight: 600;
        color: #a67c52;
        display: inline-block;
        animation: shimmer 3s ease-in-out infinite;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes shimmer {
        0%, 100% { color: #a67c52; }
        50% { color: #c19a6b; }
    }
    
    /* Clean client info card */
    .client-info-card {
        background: rgba(26, 26, 26, 0.8);
        border: 1px solid rgba(166, 124, 82, 0.2);
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        backdrop-filter: blur(20px);
        opacity: 0;
        animation: slideIn 0.6s ease-out 0.2s forwards;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    .metric-container {
        background: rgba(45, 45, 45, 0.4);
        border-radius: 6px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 2px solid #a67c52;
        transition: all 0.3s ease;
        transform: translateY(0);
    }
    
    .metric-container:hover {
        background: rgba(45, 45, 45, 0.6);
        transform: translateY(-1px);
        border-left: 2px solid #c19a6b;
    }
    
    .metric-label {
        font-size: 0.85rem;
        font-weight: 500;
        color: #a67c52;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.25rem;
    }
    
    .metric-value {
        font-size: 1.1rem;
        font-weight: 600;
        color: #ffffff;
    }
    
    /* Alert status colors */
    .alert-red { border-left-color: #dc3545; }
    .alert-amber { border-left-color: #ffc107; }
    .alert-green { border-left-color: #28a745; }
    
    /* Clean button styling */
    .stButton > button {
        background: linear-gradient(135deg, #a67c52 0%, #8b6441 100%);
        color: #ffffff;
        border: none;
        border-radius: 6px;
        font-weight: 500;
        font-family: 'Inter', sans-serif;
        padding: 0.5rem 1rem;
        font-size: 0.9rem;
        transition: all 0.3s ease;
        box-shadow: none;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #c19a6b 0%, #a67c52 100%);
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(166, 124, 82, 0.3);
    }
    
    /* Minimal chart containers */
    .chart-container {
        background: rgba(26, 26, 26, 0.6);
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
        opacity: 0;
        animation: fadeIn 0.8s ease-out forwards;
    }
    
    .chart-container:hover {
        border: 1px solid rgba(166, 124, 82, 0.3);
        background: rgba(26, 26, 26, 0.8);
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    /* Clean section titles */
    .section-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 1rem;
        text-align: center;
        letter-spacing: -0.01em;
    }
    
    /* Executive summary styling */
    .executive-summary {
        background: rgba(26, 26, 26, 0.8);
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        border-left: 3px solid #a67c52;
        animation: slideIn 0.6s ease-out 0.4s both;
    }
    
    .executive-summary h3 {
        color: #a67c52;
        font-weight: 500;
        margin-bottom: 0.75rem;
        font-size: 1.1rem;
    }
    
    .executive-summary p {
        line-height: 1.6;
        color: #d0d0d0;
        font-weight: 400;
    }
    
    /* Download section */
    .download-section {
        background: rgba(45, 45, 45, 0.6);
        border-radius: 8px;
        padding: 1.5rem;
        margin-top: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.08);
    }
    
    /* Loading animation */
    .loading-spinner {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 2px solid #333;
        border-radius: 50%;
        border-top-color: #a67c52;
        animation: spin 1s ease-in-out infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    /* Hide Streamlit elements */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header { visibility: hidden; }
    .stDeployButton { visibility: hidden; }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 6px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1a1a1a;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #a67c52;
        border-radius: 3px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #c19a6b;
    }
    
    /* Staggered animation for chart grid */
    .chart-container:nth-child(1) { animation-delay: 0.1s; }
    .chart-container:nth-child(2) { animation-delay: 0.2s; }
    .chart-container:nth-child(3) { animation-delay: 0.3s; }
    .chart-container:nth-child(4) { animation-delay: 0.4s; }
    .chart-container:nth-child(5) { animation-delay: 0.5s; }
    .chart-container:nth-child(6) { animation-delay: 0.6s; }
    .chart-container:nth-child(7) { animation-delay: 0.7s; }
    .chart-container:nth-child(8) { animation-delay: 0.8s; }
</style>
""", unsafe_allow_html=True)

# Minimal Color Palette
COLORS = {
    'primary': '#a67c52',      # Bronze metallic
    'secondary': '#c19a6b',    # Light bronze  
    'accent': '#8b6441',       # Dark bronze
    'white': '#ffffff',        # Pure white
    'light_grey': '#d0d0d0',   # Light grey
    'medium_grey': '#808080',  # Medium grey
    'dark_grey': '#4a4a4a',    # Dark grey
    'charcoal': '#2d2d2d',     # Charcoal
    'black': '#1a1a1a',        # Rich black
    'background': '#0a0a0a',   # Deep background
    'success': '#28a745',      # Green
    'warning': '#ffc107',      # Amber
    'danger': '#dc3545'        # Red
}

# Clean Typography
FONTS = {
    'family': 'Inter, system-ui, -apple-system, sans-serif',
    'title_size': 18,
    'axis_size': 12,
    'legend_size': 11,
    'data_size': 10
}

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
        st.error(f"Connection failed: {str(e)}")
        return None

@st.cache_data(ttl=60)
def load_client_data(client_id=None):
    """Load client data from Google Sheets"""
    try:
        gc = connect_to_sheets()
        if not gc:
            return get_demo_data()
            
        sheet_id = st.secrets.get("MASTER_SHEET_ID", "1oI-XqRbp8r3V8yMjnC5pNvDMljJDv4f6d01vRmrVH1g")
        
        # Connect directly to the MASTER SHEET worksheet
        spreadsheet = gc.open_by_key(sheet_id)
        
        try:
            sheet = spreadsheet.worksheet("MASTER SHEET")
            st.success("Connected to worksheet: MASTER SHEET")
        except Exception as e:
            available_sheets = [ws.title for ws in spreadsheet.worksheets()]
            st.error(f"Cannot access MASTER SHEET. Available sheets: {available_sheets}")
            st.error(f"Error details: {str(e)}")
            return get_demo_data()
        
        # Get data
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
            'MAIN STRUCTURED CONTENT': data.get('MAIN STRUCTURED CONTENT', ''),
            'EXECUTIVE SUMMARY': data.get('EXECUTIVE SUMMARY', ''),
            'ALERT LEVEL': data.get('ALERT LEVEL', 'GREEN'),
            'STATUS': data.get('STATUS', 'Active'),
            'DATE SCRAPED': data.get('DATE SCRAPED', datetime.now().strftime('%Y-%m-%d'))
        }
        
    except Exception as e:
        st.warning(f"Data loading failed: {str(e)}")
        return get_demo_data()

def get_demo_data():
    """Clean demo data"""
    return {
        'UNIQUE CLIENT ID': '11AA',
        'CLIENT NAME': 'Elite Pharmaceutical Corp',
        'TIER': 'Professional',
        'REGION': 'Northeast',
        'MAIN STRUCTURED CONTENT': 'Comprehensive compliance monitoring and regulatory intelligence for pharmaceutical manufacturing operations.',
        'EXECUTIVE SUMMARY': 'Current compliance status shows strong performance across all regulatory domains with consistent monitoring and proactive risk management.',
        'ALERT LEVEL': 'GREEN',
        'STATUS': 'Active',
        'DATE SCRAPED': datetime.now().strftime('%Y-%m-%d')
    }

def create_chart_layout(title):
    """Minimal chart layout"""
    return {
        'title': {
            'text': title,
            'font': {'family': FONTS['family'], 'size': FONTS['title_size'], 'color': COLORS['white']},
            'x': 0.5, 'xanchor': 'center'
        },
        'paper_bgcolor': COLORS['background'],
        'plot_bgcolor': COLORS['black'],
        'font': {'color': COLORS['light_grey'], 'family': FONTS['family'], 'size': FONTS['legend_size']},
        'margin': dict(l=50, r=50, t=60, b=50),
        'height': 350,
        'legend': {
            'font': {'color': COLORS['light_grey'], 'family': FONTS['family'], 'size': FONTS['legend_size']},
            'bgcolor': 'rgba(0,0,0,0)', 'borderwidth': 0
        },
        'hovermode': 'closest'
    }

def chart_1_financial_impact():
    """Clean Financial Impact Chart"""
    categories = ['Q1', 'Q2', 'Q3', 'Q4']
    savings = [185000, 220000, 195000, 240000]
    costs = [45000, 38000, 52000, 41000]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=categories, y=savings, name='Savings',
        marker_color=COLORS['primary'], marker_line=dict(width=0),
        hovertemplate='<b>Savings</b><br>%{x}: $%{y:,.0f}<extra></extra>'
    ))
    
    fig.add_trace(go.Bar(
        x=categories, y=costs, name='Costs',
        marker_color=COLORS['medium_grey'], marker_line=dict(width=0),
        hovertemplate='<b>Costs</b><br>%{x}: $%{y:,.0f}<extra></extra>'
    ))
    
    layout = create_chart_layout('Financial Impact')
    layout['barmode'] = 'group'
    layout['xaxis'] = dict(color=COLORS['light_grey'], gridcolor=COLORS['dark_grey'], tickfont=dict(size=FONTS['axis_size']))
    layout['yaxis'] = dict(color=COLORS['light_grey'], gridcolor=COLORS['dark_grey'], tickfont=dict(size=FONTS['axis_size']))
    
    fig.update_layout(layout)
    return fig

def chart_2_compliance_radar():
    """Clean Compliance Radar"""
    categories = ['Documentation', 'Training', 'Environmental', 'Quality', 'Facilities', 'Process']
    scores = [88, 94, 85, 91, 96, 87]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=scores + [scores[0]], theta=categories + [categories[0]],
        fill='toself', name='Current',
        line=dict(color=COLORS['primary'], width=2),
        fillcolor=f"rgba(166, 124, 82, 0.2)",
        hovertemplate='<b>%{theta}</b><br>Score: %{r}%<extra></extra>'
    ))
    
    layout = create_chart_layout('Compliance Performance')
    layout['polar'] = dict(
        radialaxis=dict(visible=True, range=[0, 100], gridcolor=COLORS['dark_grey'],
                       tickfont=dict(size=FONTS['data_size'], color=COLORS['medium_grey'])),
        angularaxis=dict(tickfont=dict(size=FONTS['axis_size'], color=COLORS['light_grey']))
    )
    
    fig.update_layout(layout)
    return fig

def chart_3_monitoring_gauge():
    """Clean Monitoring Gauge"""
    current_score = 94
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=current_score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Compliance Score", 'font': {'color': COLORS['white'], 'size': FONTS['title_size']}},
        gauge={
            'axis': {'range': [None, 100], 'tickcolor': COLORS['medium_grey']},
            'bar': {'color': COLORS['primary']},
            'steps': [
                {'range': [0, 60], 'color': COLORS['danger']},
                {'range': [60, 80], 'color': COLORS['warning']},
                {'range': [80, 100], 'color': COLORS['success']}
            ],
            'threshold': {'line': {'color': COLORS['white'], 'width': 4}, 'thickness': 0.75, 'value': 90}
        },
        number={'font': {'color': COLORS['white'], 'size': 32}}
    ))
    
    layout = create_chart_layout('Current Status')
    fig.update_layout(layout)
    return fig

def chart_4_alert_status():
    """Clean Alert Status"""
    departments = ['Quality', 'Manufacturing', 'Environmental', 'Training', 'Documentation']
    green = [12, 8, 15, 6, 10]
    amber = [3, 5, 2, 4, 1]
    red = [0, 1, 0, 0, 2]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(y=departments, x=green, name='Normal', orientation='h', 
                        marker_color=COLORS['success'], hovertemplate='<b>%{y}</b><br>Normal: %{x}<extra></extra>'))
    fig.add_trace(go.Bar(y=departments, x=amber, name='Attention', orientation='h', 
                        marker_color=COLORS['warning'], hovertemplate='<b>%{y}</b><br>Attention: %{x}<extra></extra>'))
    fig.add_trace(go.Bar(y=departments, x=red, name='Critical', orientation='h', 
                        marker_color=COLORS['danger'], hovertemplate='<b>%{y}</b><br>Critical: %{x}<extra></extra>'))
    
    layout = create_chart_layout('Alert Status')
    layout['barmode'] = 'stack'
    layout['xaxis'] = dict(color=COLORS['light_grey'], gridcolor=COLORS['dark_grey'], tickfont=dict(size=FONTS['axis_size']))
    layout['yaxis'] = dict(color=COLORS['light_grey'], tickfont=dict(size=FONTS['axis_size']))
    
    fig.update_layout(layout)
    return fig

def chart_5_risk_gauge():
    """Clean Risk Gauge"""
    risk_score = 23
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=risk_score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Risk Level", 'font': {'color': COLORS['white'], 'size': FONTS['title_size']}},
        gauge={
            'axis': {'range': [None, 100], 'tickcolor': COLORS['medium_grey']},
            'bar': {'color': COLORS['success']},
            'steps': [
                {'range': [0, 30], 'color': COLORS['success']},
                {'range': [30, 60], 'color': COLORS['warning']},
                {'range': [60, 100], 'color': COLORS['danger']}
            ],
            'threshold': {'line': {'color': COLORS['white'], 'width': 4}, 'thickness': 0.75, 'value': 40}
        },
        number={'font': {'color': COLORS['white'], 'size': 32}}
    ))
    
    layout = create_chart_layout('Risk Assessment')
    fig.update_layout(layout)
    return fig

def chart_6_performance_trend():
    """Clean Performance Trend"""
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
    performance = [87, 89, 88, 91, 93, 94]
    target = [90] * len(months)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(x=months, y=performance, mode='lines+markers', name='Actual',
                            line=dict(color=COLORS['primary'], width=3), marker=dict(size=6, color=COLORS['primary']),
                            hovertemplate='<b>Actual</b><br>%{x}: %{y}%<extra></extra>'))
    
    fig.add_trace(go.Scatter(x=months, y=target, mode='lines', name='Target',
                            line=dict(color=COLORS['medium_grey'], width=2, dash='dash'),
                            hovertemplate='<b>Target</b><br>%{x}: %{y}%<extra></extra>'))
    
    layout = create_chart_layout('Performance Trend')
    layout['xaxis'] = dict(color=COLORS['light_grey'], gridcolor=COLORS['dark_grey'], tickfont=dict(size=FONTS['axis_size']))
    layout['yaxis'] = dict(color=COLORS['light_grey'], gridcolor=COLORS['dark_grey'], tickfont=dict(size=FONTS['axis_size']), range=[80, 100])
    
    fig.update_layout(layout)
    return fig

def chart_7_regulatory_risk():
    """Clean Regulatory Risk"""
    categories = ['USP 797', 'USP 800', 'USP 825', 'FDA 503B', 'State Board', 'cGMP']
    risks = [25, 45, 15, 35, 30, 40]
    
    colors = [COLORS['success'] if r < 30 else COLORS['warning'] if r < 60 else COLORS['danger'] for r in risks]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(x=categories, y=risks, marker_color=colors, marker_line=dict(width=0),
                        hovertemplate='<b>%{x}</b><br>Risk: %{y}%<extra></extra>'))
    
    layout = create_chart_layout('Regulatory Risk')
    layout['xaxis'] = dict(color=COLORS['light_grey'], gridcolor=COLORS['dark_grey'], tickfont=dict(size=FONTS['axis_size']), tickangle=-30)
    layout['yaxis'] = dict(color=COLORS['light_grey'], gridcolor=COLORS['dark_grey'], tickfont=dict(size=FONTS['axis_size']))
    
    fig.update_layout(layout)
    return fig

def chart_8_deadlines():
    """Clean Deadlines Timeline"""
    tasks = ['Annual Review', 'Training Update', 'Environmental Check', 'Quality Audit']
    start_dates = [datetime.now() + timedelta(days=d) for d in [10, 5, 25, 15]]
    durations = [20, 7, 12, 8]
    
    colors = [COLORS['danger'] if (d - datetime.now()).days <= 7 else 
              COLORS['warning'] if (d - datetime.now()).days <= 20 else 
              COLORS['success'] for d in start_dates]
    
    fig = go.Figure()
    
    for task, start, duration, color in zip(tasks, start_dates, durations, colors):
        fig.add_trace(go.Bar(y=[task], x=[duration], base=[start], orientation='h',
                           marker_color=color, showlegend=False,
                           hovertemplate=f'<b>{task}</b><br>Start: {start.strftime("%Y-%m-%d")}<br>Duration: {duration} days<extra></extra>'))
    
    # Today line
    fig.add_shape(type="line", x0=datetime.now(), x1=datetime.now(), y0=-0.5, y1=len(tasks)-0.5,
                 line=dict(color=COLORS['primary'], width=2))
    
    layout = create_chart_layout('Upcoming Deadlines')
    layout['xaxis'] = dict(color=COLORS['light_grey'], tickfont=dict(size=FONTS['axis_size']), type='date')
    layout['yaxis'] = dict(color=COLORS['light_grey'], tickfont=dict(size=FONTS['axis_size']))
    
    fig.update_layout(layout)
    return fig

def main():
    """Main application"""
    
    # Animated header
    st.markdown('<h1 class="main-header"><span class="accent">LexCura</span> Compliance</h1>', unsafe_allow_html=True)
    
    # Get client ID
    client_id = st.query_params.get("client_id", "11AA")
    
    # Load data with loading animation
    with st.spinner('Loading compliance data...'):
        client_data = load_client_data(client_id)
    
    # Client info card
    st.markdown(f"""
    <div class="client-info-card">
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">
            <div class="metric-container">
                <div class="metric-label">Client ID</div>
                <div class="metric-value">{client_data['UNIQUE CLIENT ID']}</div>
            </div>
            <div class="metric-container">
                <div class="metric-label">Service Tier</div>
                <div class="metric-value">{client_data['TIER']} • {client_data['REGION']}</div>
            </div>
            <div class="metric-container alert-{client_data['ALERT LEVEL'].lower()}">
                <div class="metric-label">Status</div>
                <div class="metric-value">{client_data['ALERT LEVEL']} • {client_data['STATUS']}</div>
            </div>
            <div class="metric-container">
                <div class="metric-label">Last Update</div>
                <div class="metric-value">{client_data['DATE SCRAPED']}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Refresh button
    col1, col2, col3 = st.columns([1, 1, 4])
    with col1:
        if st.button("Refresh Data"):
            st.cache_data.clear()
            st.rerun()
    
    # Executive summary
    if client_data.get('EXECUTIVE SUMMARY'):
        st.markdown(f"""
        <div class="executive-summary">
            <h3>Executive Summary</h3>
            <p>{client_data['EXECUTIVE SUMMARY']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Charts section
    st.markdown('<h2 class="section-title">Analytics Dashboard</h2>', unsafe_allow_html=True)
    
    # Chart grid with staggered animations
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.plotly_chart(chart_1_financial_impact(), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.plotly_chart(chart_2_compliance_radar(), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.plotly_chart(chart_3_monitoring_gauge(), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.plotly_chart(chart_4_alert_status(), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.plotly_chart(chart_5_risk_gauge(), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.plotly_chart(chart_6_performance_trend(), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.plotly_chart(chart_7_regulatory_risk(), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.plotly_chart(chart_8_deadlines(), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Download section
    raw_content = client_data.get('MAIN STRUCTURED CONTENT', '')
    if raw_content and len(raw_content) > 500:
        st.markdown(f"""
        <div class="download-section">
            <h3 style="color: {COLORS['primary']}; font-weight: 500; margin-bottom: 1rem;">Data Access</h3>
            <p style="color: {COLORS['light_grey']};">Detailed compliance data for {client_data['CLIENT NAME']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if len(raw_content) > 1000:
            st.text_area("Preview", raw_content[:1000] + "...", height=150, disabled=True)
            st.download_button("Download Full Report", raw_content, 
                             file_name=f"compliance_data_{client_id}_{datetime.now().strftime('%Y%m%d')}.txt")
        else:
            st.text_area("Full Content", raw_content, height=200, disabled=True)
    
    # Clean footer
    st.markdown("---")
    st.markdown(f"""
    <div style="text-align: center; color: {COLORS['medium_grey']}; font-size: 0.9rem; padding: 1rem;">
        <strong>LexCura</strong> Compliance Dashboard • Generated: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')} • Client: {client_id}
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
