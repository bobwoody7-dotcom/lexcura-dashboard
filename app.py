# LexCura Interactive Compliance Dashboard
# Premium Production-ready Streamlit app for 503B compliance monitoring
# Luxury Edition with Premium Design

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

# Page configuration
st.set_page_config(
    page_title="LexCura Elite Compliance",
    page_icon="⚜️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Premium Dark Luxury Theme CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@400;500;600;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 50%, #0f0f0f 100%);
        color: #f8f9fa;
    }
    
    .main-header {
        background: linear-gradient(135deg, #d4af37 0%, #f4e8c1 50%, #c9a961 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.8rem;
        font-weight: 700;
        text-align: center;
        font-family: 'Playfair Display', serif;
        margin: 2rem 0;
        text-shadow: 0 0 30px rgba(212, 175, 55, 0.3);
        position: relative;
    }
    
    .main-header::after {
        content: '';
        position: absolute;
        bottom: -10px;
        left: 50%;
        transform: translateX(-50%);
        width: 150px;
        height: 2px;
        background: linear-gradient(90deg, transparent, #d4af37, transparent);
    }
    
    .logo-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 1rem;
    }
    
    .logo-container img {
        max-height: 80px;
        filter: drop-shadow(0 0 20px rgba(212, 175, 55, 0.4));
    }
    
    .client-info-card {
        background: linear-gradient(135deg, rgba(26, 26, 26, 0.95) 0%, rgba(40, 40, 40, 0.95) 100%);
        border: 1px solid rgba(212, 175, 55, 0.3);
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem 0;
        box-shadow: 
            0 20px 40px rgba(0, 0, 0, 0.5),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        position: relative;
        overflow: hidden;
    }
    
    .client-info-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, #d4af37, transparent);
    }
    
    .metric-container {
        background: linear-gradient(135deg, rgba(45, 45, 45, 0.8) 0%, rgba(25, 25, 25, 0.8) 100%);
        border-radius: 12px;
        padding: 1.5rem;
        border-left: 3px solid #d4af37;
        margin: 0.5rem 0;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, rgba(212, 175, 55, 0.05) 0%, transparent 100%);
        pointer-events: none;
    }
    
    .metric-container:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 35px rgba(0, 0, 0, 0.4);
        border-left-color: #f4e8c1;
    }
    
    .alert-red {
        border-left-color: #dc3545 !important;
        background: linear-gradient(135deg, rgba(220, 53, 69, 0.1) 0%, rgba(25, 25, 25, 0.8) 100%);
    }
    
    .alert-amber {
        border-left-color: #ffc107 !important;
        background: linear-gradient(135deg, rgba(255, 193, 7, 0.1) 0%, rgba(25, 25, 25, 0.8) 100%);
    }
    
    .alert-green {
        border-left-color: #28a745 !important;
        background: linear-gradient(135deg, rgba(40, 167, 69, 0.1) 0%, rgba(25, 25, 25, 0.8) 100%);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #d4af37 0%, #f4e8c1 50%, #c9a961 100%);
        color: #000000;
        border: none;
        border-radius: 12px;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
        padding: 0.75rem 1.5rem;
        box-shadow: 
            0 8px 20px rgba(212, 175, 55, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.2);
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 
            0 12px 30px rgba(212, 175, 55, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.3);
        background: linear-gradient(135deg, #f4e8c1 0%, #d4af37 50%, #c9a961 100%);
    }
    
    .chart-container {
        background: linear-gradient(135deg, rgba(26, 26, 26, 0.95) 0%, rgba(40, 40, 40, 0.95) 100%);
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        border: 1px solid rgba(212, 175, 55, 0.2);
        box-shadow: 
            0 15px 35px rgba(0, 0, 0, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px);
        position: relative;
        overflow: hidden;
    }
    
    .chart-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(212, 175, 55, 0.5), transparent);
    }
    
    .download-section {
        background: linear-gradient(135deg, rgba(40, 40, 40, 0.9) 0%, rgba(26, 26, 26, 0.9) 100%);
        border-radius: 15px;
        padding: 2rem;
        margin-top: 3rem;
        border: 1px solid rgba(248, 249, 250, 0.1);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    }
    
    .executive-summary {
        background: linear-gradient(135deg, rgba(26, 26, 26, 0.95) 0%, rgba(40, 40, 40, 0.95) 100%);
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem 0;
        border: 1px solid rgba(212, 175, 55, 0.3);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.4);
        position: relative;
    }
    
    .executive-summary::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, #d4af37, transparent);
    }
    
    .section-title {
        color: #d4af37;
        font-family: 'Playfair Display', serif;
        font-weight: 600;
        font-size: 1.5rem;
        margin-bottom: 1rem;
        text-align: center;
        position: relative;
    }
    
    .section-title::after {
        content: '';
        position: absolute;
        bottom: -5px;
        left: 50%;
        transform: translateX(-50%);
        width: 50px;
        height: 1px;
        background: #d4af37;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(26, 26, 26, 0.5);
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #d4af37, #c9a961);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #f4e8c1, #d4af37);
    }
</style>
""", unsafe_allow_html=True)

# Premium Color Palette
CHART_COLORS = {
    'primary_gold': '#D4AF37',      # Elegant gold
    'secondary_gold': '#F4E8C1',    # Light champagne gold
    'tertiary_gold': '#C9A961',     # Muted bronze gold
    'white': '#F8F9FA',             # Clean white
    'light_grey': '#E9ECEF',        # Light grey
    'medium_grey': '#6C757D',       # Medium grey
    'dark_grey': '#343A40',         # Dark grey
    'charcoal': '#2D2D2D',          # Charcoal
    'black': '#1A1A1A',             # Rich black
    'background': '#0A0A0A',        # Deep background
    'success': '#28A745',           # Success green
    'warning': '#FFC107',           # Warning amber
    'danger': '#DC3545',            # Danger red
    'accent_blue': '#17A2B8'        # Accent blue
}

# Premium Typography
CHART_FONT = {
    'family': 'Inter, Helvetica Neue, Arial, sans-serif',
    'title_family': 'Playfair Display, serif',
    'title_size': 28,
    'subtitle_size': 22,
    'axis_x_size': 14,
    'axis_y_size': 14,
    'axis_title_size': 16,
    'data_label_size': 12,
    'legend_size': 13
}

@st.cache_data(ttl=300)
def connect_to_sheets():
    """Connect to Google Sheets using service account credentials"""
    try:
        # Get credentials from Streamlit secrets
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
        st.error(f"Failed to connect to Google Sheets: {str(e)}")
        st.info("Make sure to add your Google service account JSON to Streamlit secrets as 'gcp_service_account'")
        return None

@st.cache_data(ttl=60)
def load_client_data(client_id=None):
    """Load client data from Compliance_Master_Sheet -> Master Sheet tab ROW 2"""
    try:
        gc = connect_to_sheets()
        if not gc:
            return get_dummy_data()
            
        # Open the Compliance_Master_Sheet and access Master Sheet tab
        sheet_id = st.secrets.get("MASTER_SHEET_ID", "your-sheet-id-here")
        spreadsheet = gc.open_by_key(sheet_id)
        sheet = spreadsheet.worksheet("Master Sheet")  # Updated worksheet name
        
        # Get headers from row 1 and data from row 2
        headers = sheet.row_values(1)
        row_data = sheet.row_values(2)
        
        # Pad row_data to match headers length
        while len(row_data) < len(headers):
            row_data.append("")
            
        # Create data dictionary
        data = dict(zip(headers, row_data))
        
        # Column mapping for Master Sheet
        columns = {
            'UNIQUE CLIENT ID': data.get('UNIQUE CLIENT ID', '11AA'),  # Updated client ID
            'CLIENT NAME': data.get('CLIENT NAME', 'Premier Client'),
            'TIER': data.get('TIER', 'Elite'),
            'REGION': data.get('REGION', 'Premium Zone'),
            'MAIN STRUCTURED CONTENT': data.get('MAIN STRUCTURED CONTENT', ''),
            'EXECUTIVE SUMMARY': data.get('EXECUTIVE SUMMARY', ''),
            'ALERT LEVEL': data.get('ALERT LEVEL', 'GREEN'),
            'STATUS': data.get('STATUS', 'Active'),
            'DATE SCRAPED': data.get('DATE SCRAPED', datetime.now().strftime('%Y-%m-%d'))
        }
        
        return columns
        
    except Exception as e:
        st.warning(f"Could not load live data: {str(e)}")
        st.info("Using premium demo data for dashboard preview")
        return get_dummy_data()

def get_dummy_data():
    """Return premium dummy data for immediate deployment and testing"""
    return {
        'UNIQUE CLIENT ID': '11AA',  # Updated client ID
        'CLIENT NAME': 'Elite Pharmaceutical Solutions',
        'TIER': 'Platinum',
        'REGION': 'Northeast Excellence Hub',
        'MAIN STRUCTURED CONTENT': 'Premium compliance content for elite pharmaceutical operations. Comprehensive regulatory analysis, advanced monitoring protocols, and executive-level compliance insights.',
        'EXECUTIVE SUMMARY': 'Q3 Elite Performance Review: Exceptional compliance achievement with 97.8% excellence rating. Premium service delivery includes advanced environmental monitoring, executive training protocols, and predictive compliance analytics.',
        'ALERT LEVEL': 'GREEN',
        'STATUS': 'Platinum Active',
        'DATE SCRAPED': datetime.now().strftime('%Y-%m-%d')
    }

def create_premium_chart_layout(title):
    """Create premium chart layout with luxury styling"""
    return {
        'title': {
            'text': f'<b>{title}</b>',
            'font': {
                'family': CHART_FONT['title_family'],
                'size': CHART_FONT['title_size'],
                'color': CHART_COLORS['primary_gold']
            },
            'x': 0.5,
            'xanchor': 'center'
        },
        'paper_bgcolor': CHART_COLORS['background'],
        'plot_bgcolor': CHART_COLORS['black'],
        'font': {
            'color': CHART_COLORS['white'], 
            'family': CHART_FONT['family'],
            'size': CHART_FONT['legend_size']
        },
        'margin': dict(l=70, r=70, t=100, b=70),
        'height': 450,
        'showlegend': True,
        'legend': {
            'font': {
                'color': CHART_COLORS['white'], 
                'family': CHART_FONT['family'],
                'size': CHART_FONT['legend_size']
            },
            'bgcolor': 'rgba(26, 26, 26, 0.8)',
            'bordercolor': CHART_COLORS['primary_gold'],
            'borderwidth': 1
        }
    }

def chart_1_financial_impact():
    """Premium Financial Impact Analysis"""
    categories = ['Q1 2024', 'Q2 2024', 'Q3 2024', 'Q4 2024 (Proj)']
    cost_savings = [285000, 320000, 295000, 340000]
    compliance_costs = [65000, 58000, 72000, 61000]
    
    fig = go.Figure()
    
    # Premium cost savings bars
    fig.add_trace(go.Bar(
        x=categories,
        y=cost_savings,
        name='Elite Cost Optimization',
        marker=dict(
            color=CHART_COLORS['primary_gold'],
            line=dict(color=CHART_COLORS['secondary_gold'], width=2)
        ),
        hovertemplate='<b>%{fullData.name}</b><br>%{x}<br><b>$%{y:,.0f}</b><extra></extra>',
        text=['$' + f'{val:,.0f}' for val in cost_savings],
        textposition='auto',
        textfont=dict(
            size=CHART_FONT['data_label_size'], 
            color=CHART_COLORS['black'], 
            family=CHART_FONT['family'],
            weight='bold'
        )
    ))
    
    # Premium compliance investment bars
    fig.add_trace(go.Bar(
        x=categories,
        y=compliance_costs,
        name='Premium Service Investment',
        marker=dict(
            color=CHART_COLORS['medium_grey'],
            line=dict(color=CHART_COLORS['light_grey'], width=2)
        ),
        hovertemplate='<b>%{fullData.name}</b><br>%{x}<br><b>$%{y:,.0f}</b><extra></extra>',
        text=['$' + f'{val:,.0f}' for val in compliance_costs],
        textposition='auto',
        textfont=dict(
            size=CHART_FONT['data_label_size'], 
            color=CHART_COLORS['white'], 
            family=CHART_FONT['family'],
            weight='bold'
        )
    ))
    
    layout = create_premium_chart_layout('Elite Financial Performance Analytics')
    layout['xaxis'] = dict(
        color=CHART_COLORS['white'],
        tickfont=dict(size=CHART_FONT['axis_x_size'], family=CHART_FONT['family']),
        title=dict(
            text='<b>Quarter</b>', 
            font=dict(size=CHART_FONT['axis_title_size'], family=CHART_FONT['family'], color=CHART_COLORS['primary_gold'])
        ),
        gridcolor=CHART_COLORS['dark_grey']
    )
    layout['yaxis'] = dict(
        color=CHART_COLORS['white'],
        tickfont=dict(size=CHART_FONT['axis_y_size'], family=CHART_FONT['family']),
        title=dict(
            text='<b>Investment Value (USD)</b>', 
            font=dict(size=CHART_FONT['axis_title_size'], family=CHART_FONT['family'], color=CHART_COLORS['primary_gold'])
        ),
        tickformat='$,.0f',
        gridcolor=CHART_COLORS['dark_grey']
    )
    layout['barmode'] = 'group'
    
    fig.update_layout(layout)
    return fig

def chart_2_compliance_excellence():
    """Premium Compliance Excellence Radar"""
    categories = ['Documentation<br>Excellence', 'Executive<br>Training', 'Environmental<br>Mastery', 
                 'Quality<br>Leadership', 'Facility<br>Excellence', 'Process<br>Innovation']
    scores = [94, 97, 91, 96, 98, 93]
    
    fig = go.Figure()
    
    # Current performance with premium styling
    fig.add_trace(go.Scatterpolar(
        r=scores + [scores[0]],
        theta=categories + [categories[0]],
        fill='toself',
        name='Elite Performance',
        line=dict(color=CHART_COLORS['primary_gold'], width=4),
        fillcolor=f"rgba(212, 175, 55, 0.2)",
        marker=dict(size=8, color=CHART_COLORS['secondary_gold']),
        hovertemplate='<b>%{theta}</b><br><b>Score: %{r}%</b><extra></extra>'
    ))
    
    # Premium target line
    target_scores = [95] * len(categories)
    fig.add_trace(go.Scatterpolar(
        r=target_scores + [target_scores[0]],
        theta=categories + [categories[0]],
        line=dict(color=CHART_COLORS['white'], width=2, dash='dash'),
        name='Excellence Target (95%)',
        hovertemplate='<b>Excellence Target</b><br>%{theta}<br><b>Score: %{r}%</b><extra></extra>'
    ))
    
    layout = create_premium_chart_layout('Elite Compliance Excellence Matrix')
    layout['polar'] = dict(
        radialaxis=dict(
            visible=True,
            range=[0, 100],
            tickfont=dict(size=12, color=CHART_COLORS['white'], family=CHART_FONT['family']),
            gridcolor=CHART_COLORS['dark_grey'],
            linecolor=CHART_COLORS['medium_grey']
        ),
        angularaxis=dict(
            tickfont=dict(size=CHART_FONT['axis_x_size'], color=CHART_COLORS['white'], family=CHART_FONT['family']),
            gridcolor=CHART_COLORS['dark_grey'],
            linecolor=CHART_COLORS['medium_grey']
        ),
        bgcolor=CHART_COLORS['black']
    )
    
    fig.update_layout(layout)
    return fig

def chart_3_monitoring_dashboard():
    """Premium Compliance Monitoring Executive Dashboard"""
    current_score = 97
    
    fig = make_subplots(
        rows=1, cols=2,
        specs=[[{"type": "indicator"}, {"type": "scatter"}]],
        subplot_titles=("<b>Executive Score</b>", "<b>Performance Trajectory</b>"),
        column_widths=[0.4, 0.6]
    )
    
    # Premium gauge chart
    fig.add_trace(go.Indicator(
        mode="gauge+number+delta",
        value=current_score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={
            'text': "<b>Elite Compliance</b>", 
            'font': {'color': CHART_COLORS['primary_gold'], 'family': CHART_FONT['title_family'], 'size': 18}
        },
        delta={
            'reference': 95, 
            'font': {'color': CHART_COLORS['white'], 'family': CHART_FONT['family'], 'size': 16}
        },
        gauge={
            'axis': {
                'range': [None, 100], 
                'tickcolor': CHART_COLORS['white'],
                'tickfont': {'family': CHART_FONT['family'], 'size': 12}
            },
            'bar': {'color': CHART_COLORS['primary_gold'], 'thickness': 0.8},
            'steps': [
                {'range': [0, 70], 'color': CHART_COLORS['danger']},
                {'range': [70, 85], 'color': CHART_COLORS['warning']},
                {'range': [85, 95], 'color': CHART_COLORS['success']},
                {'range': [95, 100], 'color': CHART_COLORS['primary_gold']}
            ],
            'threshold': {
                'line': {'color': CHART_COLORS['white'], 'width': 5},
                'thickness': 0.9,
                'value': 98
            },
            'bordercolor': CHART_COLORS['primary_gold'],
            'borderwidth': 3
        },
        number={'font': {'color': CHART_COLORS['white'], 'family': CHART_FONT['family'], 'size': 36}}
    ), row=1, col=1)
    
    # Premium trend line
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct']
    trend_scores = [91, 93, 92, 95, 96, 94, 95, 97, 96, 97]
    
    fig.add_trace(go.Scatter(
        x=months,
        y=trend_scores,
        mode='lines+markers',
        name='Elite Performance',
        line=dict(color=CHART_COLORS['primary_gold'], width=4, shape='spline'),
        marker=dict(size=10, color=CHART_COLORS['secondary_gold'], line=dict(color=CHART_COLORS['primary_gold'], width=2)),
        fill='tonexty',
        fillcolor=f"rgba(212, 175, 55, 0.1)",
        hovertemplate='<b>%{x}</b><br><b>Score: %{y}%</b><extra></extra>'
    ), row=1, col=2)
    
    layout = create_premium_chart_layout('Premium Monitoring Executive Dashboard')
    layout['height'] = 500
    fig.update_layout(layout)
    fig.update_xaxes(
        color=CHART_COLORS['white'], 
        tickfont=dict(size=CHART_FONT['axis_x_size'], family=CHART_FONT['family']),
        gridcolor=CHART_COLORS['dark_grey'],
        row=1, col=2
    )
    fig.update_yaxes(
        color=CHART_COLORS['white'], 
        tickfont=dict(size=CHART_FONT['axis_y_size'], family=CHART_FONT['family']),
        gridcolor=CHART_COLORS['dark_grey'],
        range=[85, 100],
        row=1, col=2
    )
    
    return fig

def chart_4_alert_status():
    """Premium Alert Status Executive Overview"""
    fig = go.Figure()
    
    departments = ['Quality Excellence', 'Manufacturing Elite', 'Environmental Mastery', 'Executive Training', 'Documentation Premium']
    excellent = [18, 14, 20, 10, 15]
    attention = [2, 3, 1, 2, 1]
    critical = [0, 0, 0, 0, 1]
    
    fig.add_trace(go.Bar(
        y=departments,
        x=excellent,
        name='Excellent Status',
        orientation='h',
        marker=dict(color=CHART_COLORS['primary_gold'], line=dict(color=CHART_COLORS['secondary_gold'], width=1)),
        hovertemplate='<b>%{y}</b><br><b>Excellent: %{x}</b><extra></extra>'
    ))
    
    fig.add_trace(go.Bar(
        y=departments,
        x=attention,
        name='Premium Attention',
        orientation='h',
        marker=dict(color=CHART_COLORS['warning'], line=dict(color=CHART_COLORS['white'], width=1)),
        hovertemplate='<b>%{y}</b><br><b>Attention: %{x}</b><extra></extra>'
    ))
    
    fig.add_trace(go.Bar(
        y=departments,
        x=critical,
        name='Immediate Action',
        orientation='h',
        marker=dict(color=CHART_COLORS['danger'], line=dict(color=CHART_COLORS['white'], width=1)),
        hovertemplate='<b>%{y}</b><br><b>Critical: %{x}</b><extra></extra>'
    ))
    
    layout = create_premium_chart_layout('Elite Alert Status by Excellence Center')
    layout['barmode'] = 'stack'
    layout['xaxis'] = dict(
        color=CHART_COLORS['white'],
        tickfont=dict(size=CHART_FONT['axis_x_size'], family=CHART_FONT['family']),
        title=dict(
            text='<b>Alert Distribution</b>', 
            font=dict(size=CHART_FONT['axis_title_size'], family=CHART_FONT['family'], color=CHART_COLORS['primary_gold'])
        ),
        gridcolor=CHART_COLORS['dark_grey']
    )
    layout['yaxis'] = dict(
        color=CHART_COLORS['white'],
        tickfont=dict(size=CHART_FONT['axis_y_size']-1, family=CHART_FONT['family']),
        gridcolor=CHART_COLORS['dark_grey']
    )
    
    fig.update_layout(layout)
    return fig

def chart_5_risk_assessment():
    """Premium Risk Assessment Executive Gauge"""
    risk_score = 15  # Very low risk for premium service
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=risk_score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={
            'text': "<b>Executive Risk Profile</b>", 
            'font': {
                'color': CHART_COLORS['primary_gold'], 
                'family': CHART_FONT['title_family'], 
                'size': 20
            }
        },
        delta={
            'reference': 25, 
            'font': {'color': CHART_COLORS['white'], 'family': CHART_FONT['family'], 'size': 16}
        },
        gauge={
            'axis': {
                'range': [None, 100], 
                'tickcolor': CHART_COLORS['white'],
                'tickfont': {'family': CHART_FONT['family'], 'size': 12}
            },
            'bar': {'color': CHART_COLORS['success'], 'thickness': 0.8},
            'steps': [
                {'range': [0, 25], 'color': CHART_COLORS['primary_gold']},
                {'range': [25, 50], 'color': CHART_COLORS['warning']},
                {'range': [50, 75], 'color': CHART_COLORS['danger']},
                {'range': [75, 100], 'color': '#8B0000'}  # Dark red for extreme risk
            ],
            'threshold': {
                'line': {'color': CHART_COLORS['white'], 'width': 5},
                'thickness': 0.9,
                'value': 30
            },
            'bordercolor': CHART_COLORS['primary_gold'],
            'borderwidth': 3
        },
        number={'font': {'color': CHART_COLORS['white'], 'family': CHART_FONT['family'], 'size': 42}}
    ))
    
    layout = create_premium_chart_layout('Premium Risk Assessment Matrix')
    layout['height'] = 500
    fig.update_layout(layout)
    return fig

def chart_6_executive_performance():
    """Executive Performance Premium Summary"""
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct']
    performance = [91, 93, 92, 95, 96, 94, 95, 97, 96, 97]
    target = [95] * len(months)
    benchmark = [88, 89, 90, 90, 91, 91, 92, 92, 93, 93]
    
    fig = go.Figure()
    
    # Premium actual performance
    fig.add_trace(go.Scatter(
        x=months,
        y=performance,
        mode='lines+markers',
        name='Elite Performance',
        line=dict(color=CHART_COLORS['primary_gold'], width=5, shape='spline'),
        marker=dict(
            size=12, 
            color=CHART_COLORS['secondary_gold'], 
            line=dict(color=CHART_COLORS['primary_gold'], width=3)
        ),
        fill='tonexty',
        fillcolor=f"rgba(212, 175, 55, 0.15)",
        hovertemplate='<b>Elite Performance</b><br>%{x}: <b>%{y}%</b><extra></extra>'
    ))
    
    # Premium target line
    fig.add_trace(go.Scatter(
        x=months,
        y=target,
        mode='lines',
        name='Excellence Target (95%)',
        line=dict(color=CHART_COLORS['white'], width=3, dash='dash'),
        hovertemplate='<b>Target</b><br>%{x}: <b>%{y}%</b><extra></extra>'
    ))
    
    # Industry benchmark
    fig.add_trace(go.Scatter(
        x=months,
        y=benchmark,
        mode='lines',
        name='Industry Standard',
        line=dict(color=CHART_COLORS['medium_grey'], width=2, dash='dot'),
        hovertemplate='<b>Industry</b><br>%{x}: <b>%{y}%</b><extra></extra>'
    ))
    
    layout = create_premium_chart_layout('Executive Performance Excellence Summary')
    layout['xaxis'] = dict(
        color=CHART_COLORS['white'],
        tickfont=dict(size=CHART_FONT['axis_x_size'], family=CHART_FONT['family']),
        title=dict(
            text='<b>Month</b>', 
            font=dict(size=CHART_FONT['axis_title_size'], family=CHART_FONT['family'], color=CHART_COLORS['primary_gold'])
        ),
        gridcolor=CHART_COLORS['dark_grey']
    )
    layout['yaxis'] = dict(
        color=CHART_COLORS['white'],
        tickfont=dict(size=CHART_FONT['axis_y_size'], family=CHART_FONT['family']),
        title=dict(
            text='<b>Excellence Score (%)</b>', 
            font=dict(size=CHART_FONT['axis_title_size'], family=CHART_FONT['family'], color=CHART_COLORS['primary_gold'])
        ),
        range=[85, 100],
        gridcolor=CHART_COLORS['dark_grey']
    )
    
    fig.update_layout(layout)
    return fig

def chart_7_regulatory_risk():
    """Premium Regulatory Risk by Excellence Category"""
    categories = ['USP <797>\nElite', 'USP <800>\nPremium', 'USP <825>\nAdvanced', 'FDA 503B\nExcellence', 'State Board\nMastery', 'cGMP\nPlatinum', 'Environmental\nElite']
    risk_scores = [12, 25, 8, 18, 15, 22, 10]
    
    # Premium color mapping
    colors = []
    for score in risk_scores:
        if score < 15:
            colors.append(CHART_COLORS['primary_gold'])
        elif score < 30:
            colors.append(CHART_COLORS['warning'])
        else:
            colors.append(CHART_COLORS['danger'])
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=categories,
        y=risk_scores,
        marker=dict(
            color=colors, 
            line=dict(color=CHART_COLORS['white'], width=2),
            pattern_shape="/"
        ),
        text=[f'<b>{score}%</b>' for score in risk_scores],
        textposition='auto',
        textfont=dict(
            size=CHART_FONT['data_label_size']+2, 
            color=CHART_COLORS['white'], 
            family=CHART_FONT['family']
        ),
        hovertemplate='<b>%{x}</b><br><b>Risk Level: %{y}%</b><extra></extra>'
    ))
    
    layout = create_premium_chart_layout('Premium Regulatory Risk Excellence Matrix')
    layout['xaxis'] = dict(
        color=CHART_COLORS['white'],
        tickfont=dict(size=CHART_FONT['axis_x_size']-1, family=CHART_FONT['family']),
        title=dict(
            text='<b>Regulatory Excellence Categories</b>', 
            font=dict(size=CHART_FONT['axis_title_size'], family=CHART_FONT['family'], color=CHART_COLORS['primary_gold'])
        ),
        tickangle=-30,
        gridcolor=CHART_COLORS['dark_grey']
    )
    layout['yaxis'] = dict(
        color=CHART_COLORS['white'],
        tickfont=dict(size=CHART_FONT['axis_y_size'], family=CHART_FONT['family']),
        title=dict(
            text='<b>Risk Level (%)</b>', 
            font=dict(size=CHART_FONT['axis_title_size'], family=CHART_FONT['family'], color=CHART_COLORS['primary_gold'])
        ),
        range=[0, 100],
        gridcolor=CHART_COLORS['dark_grey']
    )
    
    fig.update_layout(layout)
    return fig

def chart_8_upcoming_deadlines():
    """Premium Upcoming Deadlines Executive Tracker"""
    tasks = ['Elite Annual Review', 'USP <797> Premium Update', 'Environmental Excellence', 'Quality Leadership Review', 'Equipment Elite Calibration']
    start_dates = [datetime.now() + timedelta(days=15), 
                   datetime.now() + timedelta(days=8),
                   datetime.now() + timedelta(days=30),
                   datetime.now() + timedelta(days=20),
                   datetime.now() + timedelta(days=40)]
    durations = [25, 10, 18, 12, 7]  # Days
    
    fig = go.Figure()
    
    # Premium color coding
    colors = []
    for start_date in start_dates:
        days_until = (start_date - datetime.now()).days
        if days_until <= 10:
            colors.append(CHART_COLORS['danger'])
        elif days_until <= 25:
            colors.append(CHART_COLORS['warning'])
        else:
            colors.append(CHART_COLORS['primary_gold'])
    
    # Create premium timeline bars
    for i, (task, start, duration, color) in enumerate(zip(tasks, start_dates, durations, colors)):
        fig.add_trace(go.Bar(
            y=[task],
            x=[duration],
            base=[start],
            orientation='h',
            name=task,
            marker=dict(
                color=color,
                line=dict(color=CHART_COLORS['white'], width=2),
                opacity=0.8
            ),
            showlegend=False,
            hovertemplate=f'<b>{task}</b><br>Start: <b>{start.strftime("%Y-%m-%d")}</b><br>Duration: <b>{duration} days</b><extra></extra>'
        ))
    
    # Premium "today" indicator
    today = datetime.now()
    fig.add_shape(
        type="line",
        x0=today,
        x1=today,
        y0=-0.5,
        y1=len(tasks)-0.5,
        line=dict(color=CHART_COLORS['primary_gold'], width=4, dash="solid")
    )
    
    layout = create_premium_chart_layout('Executive Deadline Excellence Tracker')
    layout['xaxis'] = dict(
        color=CHART_COLORS['white'],
        tickfont=dict(size=CHART_FONT['axis_x_size'], family=CHART_FONT['family']),
        title=dict(
            text='<b>Premium Timeline</b>', 
            font=dict(size=CHART_FONT['axis_title_size'], family=CHART_FONT['family'], color=CHART_COLORS['primary_gold'])
        ),
        type='date',
        gridcolor=CHART_COLORS['dark_grey']
    )
    layout['yaxis'] = dict(
        color=CHART_COLORS['white'],
        tickfont=dict(size=CHART_FONT['axis_y_size'], family=CHART_FONT['family']),
        gridcolor=CHART_COLORS['dark_grey']
    )
    
    fig.update_layout(layout)
    return fig

def create_download_link(content, filename):
    """Create premium download link for executive content"""
    if len(content) > 45000:
        buffer = io.StringIO()
        buffer.write(content)
        buffer.seek(0)
        
        return st.download_button(
            label="📥 Download Executive Report",
            data=buffer.getvalue(),
            file_name=f"LexCura_Executive_{filename}_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain",
            help="Premium executive content - Click to download the comprehensive compliance report.",
            key=f"download_{filename}"
        )
    return None

def main():
    """Premium Dashboard Application"""
    
    # Premium Logo Section
    st.markdown("""
    <div class="logo-container">
        <img src="https://drive.google.com/uc?export=view&id=1KUnvmqcbtvyyqqx4R8z5dmLlcNFlSwcC" 
             alt="LexCura Logo" style="max-height: 80px;">
    </div>
    """, unsafe_allow_html=True)
    
    # Premium Header
    st.markdown('<h1 class="main-header">LexCura Elite Compliance Excellence</h1>', unsafe_allow_html=True)
    
    # Get client ID from URL parameters
    client_id = st.query_params.get("client_id", "11AA")  # Updated default client ID
    
    # Load premium client data
    client_data = load_client_data(client_id)
    
    # Premium Client Information Card
    st.markdown(f"""
    <div class="client-info-card">
        <h2 style="color: {CHART_COLORS['primary_gold']}; margin-bottom: 1.5rem; font-family: {CHART_FONT['title_family']}; font-size: 1.8rem;">
            ⚜️ {client_data['CLIENT NAME']} - Executive Compliance Overview
        </h2>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1.5rem;">
            <div class="metric-container">
                <strong style="color: {CHART_COLORS['primary_gold']}; font-size: 1.1rem;">Elite Client ID</strong><br>
                <span style="font-size: 1.3rem; font-weight: 600;">{client_data['UNIQUE CLIENT ID']}</span>
            </div>
            <div class="metric-container">
                <strong style="color: {CHART_COLORS['primary_gold']}; font-size: 1.1rem;">Premium Service Tier</strong><br>
                <span style="font-size: 1.3rem; font-weight: 600;">{client_data['TIER']} • {client_data['REGION']}</span>
            </div>
            <div class="metric-container alert-{client_data['ALERT LEVEL'].lower()}">
                <strong style="color: {CHART_COLORS['primary_gold']}; font-size: 1.1rem;">Excellence Status</strong><br>
                <span style="font-size: 1.3rem; font-weight: 600;">{client_data['ALERT LEVEL']} • {client_data['STATUS']}</span>
            </div>
            <div class="metric-container">
                <strong style="color: {CHART_COLORS['primary_gold']}; font-size: 1.1rem;">Last Executive Update</strong><br>
                <span style="font-size: 1.3rem; font-weight: 600;">{client_data['DATE SCRAPED']}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Premium control buttons
    col1, col2, col3 = st.columns([1, 1, 4])
    with col1:
        if st.button("🔄 Elite Refresh", help="Refresh premium data analytics"):
            st.cache_data.clear()
            st.rerun()
    
    # Executive Summary Section
    if client_data.get('EXECUTIVE SUMMARY'):
        st.markdown(f"""
        <div class="executive-summary">
            <h3 class="section-title">📊 Executive Intelligence Summary</h3>
            <p style="line-height: 1.8; color: {CHART_COLORS['white']}; font-size: 1.1rem; font-weight: 400;">
                {client_data['EXECUTIVE SUMMARY']}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Premium Analytics Section
    st.markdown(f"""
    <div style="text-align: center; margin: 3rem 0;">
        <h2 style="color: {CHART_COLORS['secondary_gold']}; font-family: {CHART_FONT['title_family']}; font-size: 2.2rem; font-weight: 600;">
            📈 Executive Analytics Intelligence Dashboard
        </h2>
        <div style="width: 100px; height: 2px; background: linear-gradient(90deg, transparent, {CHART_COLORS['primary_gold']}, transparent); margin: 1rem auto;"></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Premium Charts Layout
    
    # Row 1: Financial Excellence and Compliance Matrix
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.plotly_chart(chart_1_financial_impact(), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.plotly_chart(chart_2_compliance_excellence(), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Row 2: Executive Monitoring and Premium Alerts
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.plotly_chart(chart_3_monitoring_dashboard(), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.plotly_chart(chart_4_alert_status(), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Row 3: Risk Assessment and Performance Excellence
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.plotly_chart(chart_5_risk_assessment(), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.plotly_chart(chart_6_executive_performance(), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Row 4: Regulatory Excellence and Executive Timeline
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.plotly_chart(chart_7_regulatory_risk(), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.plotly_chart(chart_8_upcoming_deadlines(), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Premium Executive Content Access
    raw_content = client_data.get('MAIN STRUCTURED CONTENT', '')
    if raw_content and len(raw_content) > 500:
        st.markdown(f"""
        <div class="download-section">
            <h3 style="color: {CHART_COLORS['primary_gold']}; font-family: {CHART_FONT['title_family']}; font-size: 1.6rem;">
                📄 Executive Intelligence Data Access
            </h3>
            <p style="font-size: 1.1rem; color: {CHART_COLORS['light_grey']};">
                Comprehensive regulatory intelligence and executive compliance analytics for {client_data['CLIENT NAME']}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Premium content preview
        if len(raw_content) > 1000:
            st.text_area(
                "Executive Content Preview", 
                raw_content[:1000] + "\n\n... (Executive content continues - download for full intelligence report)", 
                height=180,
                disabled=True
            )
            create_download_link(raw_content, f"executive_intelligence_{client_id}")
        else:
            st.text_area("Full Executive Intelligence", raw_content, height=220, disabled=True)
    
    # Premium Footer
    st.markdown("---")
    st.markdown(f"""
    <div style="text-align: center; color: {CHART_COLORS['medium_grey']}; font-family: {CHART_FONT['family']}; margin-top: 2rem;">
        <p style="font-size: 1.2rem; font-weight: 600; color: {CHART_COLORS['primary_gold']};">
            <strong>LexCura Elite</strong> - Premium Automated Compliance Excellence for 503B Elite Manufacturing
        </p>
        <p style="font-size: 1rem; margin-top: 1rem;">
            Executive Dashboard Generated: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')} | Elite Client: {client_id}
        </p>
        <p style="font-size: 0.9rem; color: {CHART_COLORS['dark_grey']}; margin-top: 0.5rem;">
            £6,000/month Premium Service | Confidential Executive Intelligence
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
