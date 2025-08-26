# LexCura Interactive Compliance Dashboard
# Production-ready Streamlit app for 503B compliance monitoring
# Fixed version with updated Streamlit functions

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
    page_title="LexCura Compliance Dashboard",
    page_icon="⚕️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for premium dark theme
st.markdown("""
<style>
    .stApp {
        background-color: #111827;
        color: #FFFFFF;
    }
    
    .main-header {
        background: linear-gradient(45deg, #D4AF37, #C0C0C0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        font-family: 'Montserrat', 'Helvetica Neue', Arial, sans-serif;
        margin-bottom: 1rem;
    }
    
    .client-info-card {
        background: linear-gradient(135deg, rgba(212, 175, 55, 0.1), rgba(192, 192, 192, 0.1));
        border: 1px solid #D4AF37;
        border-radius: 15px;
        padding: 1.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(212, 175, 55, 0.1);
        backdrop-filter: blur(10px);
    }
    
    .metric-container {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        padding: 1rem;
        border-left: 4px solid #D4AF37;
        margin: 0.5rem 0;
    }
    
    .alert-red {
        border-left-color: #DC2626 !important;
        background: rgba(220, 38, 38, 0.1);
    }
    
    .alert-amber {
        border-left-color: #F59E0B !important;
        background: rgba(245, 158, 11, 0.1);
    }
    
    .alert-green {
        border-left-color: #10B981 !important;
        background: rgba(16, 185, 129, 0.1);
    }
    
    .stButton > button {
        background: linear-gradient(45deg, #D4AF37, #C0C0C0);
        color: #111827;
        border: none;
        border-radius: 8px;
        font-weight: bold;
        font-family: 'Montserrat', 'Helvetica Neue', Arial, sans-serif;
        box-shadow: 0 4px 16px rgba(212, 175, 55, 0.3);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(212, 175, 55, 0.4);
    }
    
    .chart-container {
        background: rgba(255, 255, 255, 0.02);
        border-radius: 15px;
        padding: 1rem;
        margin: 1rem 0;
        border: 1px solid rgba(212, 175, 55, 0.2);
    }
    
    .download-section {
        background: linear-gradient(135deg, rgba(173, 216, 230, 0.1), rgba(128, 128, 128, 0.1));
        border-radius: 10px;
        padding: 1rem;
        margin-top: 2rem;
        border: 1px solid #ADD8E6;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Chart styling configuration
CHART_COLORS = {
    'gold': '#D4AF37',
    'silver': '#C0C0C0', 
    'grey': '#808080',
    'light_blue': '#ADD8E6',
    'white': '#FFFFFF',
    'background': '#111827',
    'red': '#DC2626',
    'amber': '#F59E0B',
    'green': '#10B981'
}

CHART_FONT = {
    'family': 'Montserrat, Helvetica Neue, Arial, sans-serif',
    'title_size': 25,
    'axis_x_size': 21,
    'axis_y_size': 18,
    'axis_title_size': 18,
    'data_label_size': 15
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
    """Load client data from MASTER sheet ROW 2"""
    try:
        gc = connect_to_sheets()
        if not gc:
            return get_dummy_data()
            
        # Open the MASTER sheet (replace with your actual sheet ID)
        sheet_id = st.secrets.get("MASTER_SHEET_ID", "your-sheet-id-here")
        sheet = gc.open_by_key(sheet_id).worksheet("MASTER")
        
        # Get headers from row 1 and data from row 2
        headers = sheet.row_values(1)
        row_data = sheet.row_values(2)
        
        # Pad row_data to match headers length
        while len(row_data) < len(headers):
            row_data.append("")
            
        # Create data dictionary
        data = dict(zip(headers, row_data))
        
        # Column mapping for MASTER sheet (A-V)
        columns = {
            'UNIQUE CLIENT ID': data.get('UNIQUE CLIENT ID', 'CB999'),
            'CLIENT NAME': data.get('CLIENT NAME', 'Demo Client'),
            'TIER': data.get('TIER', 'Premium'),
            'REGION': data.get('REGION', 'Northeast'),
            'MAIN STRUCTURED CONTENT': data.get('MAIN STRUCTURED CONTENT', ''),
            'EXECUTIVE SUMMARY': data.get('EXECUTIVE SUMMARY', ''),
            'ALERT LEVEL': data.get('ALERT LEVEL', 'GREEN'),
            'STATUS': data.get('STATUS', 'Active'),
            'DATE SCRAPED': data.get('DATE SCRAPED', datetime.now().strftime('%Y-%m-%d'))
        }
        
        return columns
        
    except Exception as e:
        st.warning(f"Could not load live data: {str(e)}")
        st.info("Using demo data for dashboard preview")
        return get_dummy_data()

def get_dummy_data():
    """Return dummy data for immediate deployment and testing"""
    return {
        'UNIQUE CLIENT ID': 'CB999',
        'CLIENT NAME': 'Premier Sterile Solutions',
        'TIER': 'Premium',
        'REGION': 'Northeast',
        'MAIN STRUCTURED CONTENT': 'Sample compliance content for demo purposes. This would contain regulatory updates, inspection findings, and compliance analysis.',
        'EXECUTIVE SUMMARY': 'Q3 compliance review shows strong performance with 94% compliance score. Key areas of focus include environmental monitoring and personnel training updates.',
        'ALERT LEVEL': 'GREEN',
        'STATUS': 'Active',
        'DATE SCRAPED': datetime.now().strftime('%Y-%m-%d')
    }

def create_chart_layout(title):
    """Create standardized chart layout with premium styling"""
    return {
        'title': {
            'text': title,
            'font': {
                'family': CHART_FONT['family'],
                'size': CHART_FONT['title_size'],
                'color': CHART_COLORS['white']
            },
            'x': 0.5,
            'xanchor': 'center'
        },
        'paper_bgcolor': CHART_COLORS['background'],
        'plot_bgcolor': CHART_COLORS['background'],
        'font': {'color': CHART_COLORS['white'], 'family': CHART_FONT['family']},
        'margin': dict(l=60, r=60, t=80, b=60),
        'height': 400
    }

def chart_1_financial_impact():
    """Financial Impact Chart (Bar/Column)"""
    # Dummy data - replace with real data from ROW 2
    categories = ['Q1 2024', 'Q2 2024', 'Q3 2024', 'Q4 2024 (Proj)']
    cost_savings = [185000, 220000, 195000, 240000]
    compliance_costs = [45000, 38000, 52000, 41000]
    
    fig = go.Figure()
    
    # Cost savings bars
    fig.add_trace(go.Bar(
        x=categories,
        y=cost_savings,
        name='Cost Savings',
        marker_color=CHART_COLORS['gold'],
        hovertemplate='<b>%{fullData.name}</b><br>%{x}<br>$%{y:,.0f}<extra></extra>',
        text=['$' + f'{val:,.0f}' for val in cost_savings],
        textposition='auto',
        textfont=dict(size=CHART_FONT['data_label_size'], color=CHART_COLORS['background'], family=CHART_FONT['family'])
    ))
    
    # Compliance costs bars
    fig.add_trace(go.Bar(
        x=categories,
        y=compliance_costs,
        name='Compliance Costs',
        marker_color=CHART_COLORS['light_blue'],
        hovertemplate='<b>%{fullData.name}</b><br>%{x}<br>$%{y:,.0f}<extra></extra>',
        text=['$' + f'{val:,.0f}' for val in compliance_costs],
        textposition='auto',
        textfont=dict(size=CHART_FONT['data_label_size'], color=CHART_COLORS['background'], family=CHART_FONT['family'])
    ))
    
    layout = create_chart_layout('Financial Impact Analysis')
    layout['xaxis'] = dict(
        color=CHART_COLORS['white'],
        tickfont=dict(size=CHART_FONT['axis_x_size'], family=CHART_FONT['family']),
        title=dict(text='Quarter', font=dict(size=CHART_FONT['axis_title_size'], family=CHART_FONT['family']))
    )
    layout['yaxis'] = dict(
        color=CHART_COLORS['white'],
        tickfont=dict(size=CHART_FONT['axis_y_size'], family=CHART_FONT['family']),
        title=dict(text='Amount (USD)', font=dict(size=CHART_FONT['axis_title_size'], family=CHART_FONT['family'])),
        tickformat='$,.0f'
    )
    layout['barmode'] = 'group'
    layout['legend'] = dict(font=dict(color=CHART_COLORS['white'], family=CHART_FONT['family']))
    
    fig.update_layout(layout)
    return fig

def chart_2_compliance_excellence():
    """Compliance Excellence Radar Chart"""
    categories = ['Documentation', 'Training', 'Environmental<br>Monitoring', 
                 'Quality Control', 'Facility<br>Standards', 'Process<br>Validation']
    scores = [88, 94, 85, 91, 96, 87]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=scores + [scores[0]],  # Close the polygon
        theta=categories + [categories[0]],
        fill='toself',
        name='Current Performance',
        line=dict(color=CHART_COLORS['gold'], width=3),
        fillcolor=f"rgba{tuple(list(bytes.fromhex(CHART_COLORS['gold'][1:])) + [0.3])}",
        hovertemplate='<b>%{theta}</b><br>Score: %{r}%<extra></extra>'
    ))
    
    # Add target line
    target_scores = [90] * len(categories)
    fig.add_trace(go.Scatterpolar(
        r=target_scores + [target_scores[0]],
        theta=categories + [categories[0]],
        line=dict(color=CHART_COLORS['silver'], width=2, dash='dash'),
        name='Target (90%)',
        hovertemplate='<b>Target</b><br>%{theta}<br>Score: %{r}%<extra></extra>'
    ))
    
    layout = create_chart_layout('Compliance Excellence Radar')
    layout['polar'] = dict(
        radialaxis=dict(
            visible=True,
            range=[0, 100],
            tickfont=dict(size=14, color=CHART_COLORS['white'], family=CHART_FONT['family']),
            gridcolor=CHART_COLORS['grey']
        ),
        angularaxis=dict(
            tickfont=dict(size=CHART_FONT['axis_x_size'], color=CHART_COLORS['white'], family=CHART_FONT['family'])
        )
    )
    layout['legend'] = dict(font=dict(color=CHART_COLORS['white'], family=CHART_FONT['family']))
    
    fig.update_layout(layout)
    return fig

def chart_3_monitoring_dashboard():
    """Compliance Monitoring Dashboard (Gauge/Line combination)"""
    current_score = 94
    
    fig = make_subplots(
        rows=1, cols=2,
        specs=[[{"type": "indicator"}, {"type": "scatter"}]],
        subplot_titles=("Current Compliance Score", "Trend Over Time"),
        column_widths=[0.4, 0.6]
    )
    
    # Gauge chart
    fig.add_trace(go.Indicator(
        mode="gauge+number+delta",
        value=current_score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Compliance Score", 'font': {'color': CHART_COLORS['white'], 'family': CHART_FONT['family']}},
        delta={'reference': 90, 'font': {'color': CHART_COLORS['white'], 'family': CHART_FONT['family']}},
        gauge={
            'axis': {'range': [None, 100], 'tickcolor': CHART_COLORS['white']},
            'bar': {'color': CHART_COLORS['gold']},
            'steps': [
                {'range': [0, 60], 'color': CHART_COLORS['red']},
                {'range': [60, 80], 'color': CHART_COLORS['amber']},
                {'range': [80, 100], 'color': CHART_COLORS['green']}
            ],
            'threshold': {
                'line': {'color': CHART_COLORS['white'], 'width': 4},
                'thickness': 0.75,
                'value': 95
            }
        },
        number={'font': {'color': CHART_COLORS['white'], 'family': CHART_FONT['family']}}
    ), row=1, col=1)
    
    # Trend line
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct']
    trend_scores = [87, 89, 88, 91, 93, 90, 92, 94, 93, 94]
    
    fig.add_trace(go.Scatter(
        x=months,
        y=trend_scores,
        mode='lines+markers',
        name='Monthly Score',
        line=dict(color=CHART_COLORS['light_blue'], width=3),
        marker=dict(size=8, color=CHART_COLORS['gold']),
        hovertemplate='<b>%{x}</b><br>Score: %{y}%<extra></extra>'
    ), row=1, col=2)
    
    layout = create_chart_layout('Compliance Monitoring Dashboard')
    fig.update_layout(layout)
    fig.update_xaxes(color=CHART_COLORS['white'], tickfont=dict(size=CHART_FONT['axis_x_size'], family=CHART_FONT['family']), row=1, col=2)
    fig.update_yaxes(color=CHART_COLORS['white'], tickfont=dict(size=CHART_FONT['axis_y_size'], family=CHART_FONT['family']), row=1, col=2)
    
    return fig

def chart_4_alert_status():
    """Alert Status Indicator (Stacked Bar/Heatmap)"""
    fig = go.Figure()
    
    # Alert data
    departments = ['Quality Control', 'Manufacturing', 'Environmental', 'Training', 'Documentation']
    green_alerts = [12, 8, 15, 6, 10]
    amber_alerts = [3, 5, 2, 4, 1]
    red_alerts = [0, 1, 0, 0, 2]
    
    fig.add_trace(go.Bar(
        y=departments,
        x=green_alerts,
        name='Normal (Green)',
        orientation='h',
        marker_color=CHART_COLORS['green'],
        hovertemplate='<b>%{y}</b><br>Normal: %{x}<extra></extra>'
    ))
    
    fig.add_trace(go.Bar(
        y=departments,
        x=amber_alerts,
        name='Attention (Amber)',
        orientation='h',
        marker_color=CHART_COLORS['amber'],
        hovertemplate='<b>%{y}</b><br>Attention: %{x}<extra></extra>'
    ))
    
    fig.add_trace(go.Bar(
        y=departments,
        x=red_alerts,
        name='Critical (Red)',
        orientation='h',
        marker_color=CHART_COLORS['red'],
        hovertemplate='<b>%{y}</b><br>Critical: %{x}<extra></extra>'
    ))
    
    layout = create_chart_layout('Alert Status by Department')
    layout['barmode'] = 'stack'
    layout['xaxis'] = dict(
        color=CHART_COLORS['white'],
        tickfont=dict(size=CHART_FONT['axis_x_size'], family=CHART_FONT['family']),
        title=dict(text='Number of Alerts', font=dict(size=CHART_FONT['axis_title_size'], family=CHART_FONT['family']))
    )
    layout['yaxis'] = dict(
        color=CHART_COLORS['white'],
        tickfont=dict(size=CHART_FONT['axis_y_size'], family=CHART_FONT['family'])
    )
    layout['legend'] = dict(font=dict(color=CHART_COLORS['white'], family=CHART_FONT['family']))
    
    fig.update_layout(layout)
    return fig

def chart_5_risk_assessment():
    """Risk Assessment Gauge (Dial)"""
    risk_score = 23  # Low risk
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=risk_score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Overall Risk Level", 'font': {'color': CHART_COLORS['white'], 'family': CHART_FONT['family'], 'size': CHART_FONT['title_size']}},
        delta={'reference': 30, 'font': {'color': CHART_COLORS['white'], 'family': CHART_FONT['family']}},
        gauge={
            'axis': {'range': [None, 100], 'tickcolor': CHART_COLORS['white'], 'tickfont': {'family': CHART_FONT['family']}},
            'bar': {'color': CHART_COLORS['gold']},
            'steps': [
                {'range': [0, 30], 'color': CHART_COLORS['green']},
                {'range': [30, 60], 'color': CHART_COLORS['amber']},
                {'range': [60, 100], 'color': CHART_COLORS['red']}
            ],
            'threshold': {
                'line': {'color': CHART_COLORS['white'], 'width': 4},
                'thickness': 0.75,
                'value': 40
            }
        },
        number={'font': {'color': CHART_COLORS['white'], 'family': CHART_FONT['family'], 'size': 36}}
    ))
    
    layout = create_chart_layout('Risk Assessment Gauge')
    layout['height'] = 450
    fig.update_layout(layout)
    return fig

def chart_6_executive_performance():
    """Executive Performance Summary (Line/Area)"""
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct']
    performance = [87, 89, 88, 91, 93, 90, 92, 94, 93, 94]
    target = [90] * len(months)
    benchmark = [85, 86, 87, 88, 89, 89, 90, 90, 91, 91]
    
    fig = go.Figure()
    
    # Actual performance
    fig.add_trace(go.Scatter(
        x=months,
        y=performance,
        mode='lines+markers',
        name='Actual Performance',
        line=dict(color=CHART_COLORS['gold'], width=4),
        marker=dict(size=10, color=CHART_COLORS['gold']),
        fill='tonexty',
        fillcolor=f"rgba{tuple(list(bytes.fromhex(CHART_COLORS['gold'][1:])) + [0.3])}",
        hovertemplate='<b>Actual</b><br>%{x}: %{y}%<extra></extra>'
    ))
    
    # Target line
    fig.add_trace(go.Scatter(
        x=months,
        y=target,
        mode='lines',
        name='Target (90%)',
        line=dict(color=CHART_COLORS['silver'], width=2, dash='dash'),
        hovertemplate='<b>Target</b><br>%{x}: %{y}%<extra></extra>'
    ))
    
    # Industry benchmark
    fig.add_trace(go.Scatter(
        x=months,
        y=benchmark,
        mode='lines',
        name='Industry Benchmark',
        line=dict(color=CHART_COLORS['light_blue'], width=2, dash='dot'),
        hovertemplate='<b>Benchmark</b><br>%{x}: %{y}%<extra></extra>'
    ))
    
    layout = create_chart_layout('Executive Performance Summary')
    layout['xaxis'] = dict(
        color=CHART_COLORS['white'],
        tickfont=dict(size=CHART_FONT['axis_x_size'], family=CHART_FONT['family']),
        title=dict(text='Month', font=dict(size=CHART_FONT['axis_title_size'], family=CHART_FONT['family']))
    )
    layout['yaxis'] = dict(
        color=CHART_COLORS['white'],
        tickfont=dict(size=CHART_FONT['axis_y_size'], family=CHART_FONT['family']),
        title=dict(text='Performance Score (%)', font=dict(size=CHART_FONT['axis_title_size'], family=CHART_FONT['family'])),
        range=[80, 100]
    )
    layout['legend'] = dict(font=dict(color=CHART_COLORS['white'], family=CHART_FONT['family']))
    
    fig.update_layout(layout)
    return fig

def chart_7_regulatory_risk():
    """Regulatory Risk by Category (Heatmap/Bar)"""
    categories = ['USP <797>', 'USP <800>', 'USP <825>', 'FDA 503B', 'State Board', 'cGMP', 'Environmental']
    risk_scores = [25, 45, 15, 35, 30, 40, 20]
    
    # Color mapping for risk levels
    colors = []
    for score in risk_scores:
        if score < 30:
            colors.append(CHART_COLORS['green'])
        elif score < 60:
            colors.append(CHART_COLORS['amber'])
        else:
            colors.append(CHART_COLORS['red'])
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=categories,
        y=risk_scores,
        marker=dict(color=colors, line=dict(color=CHART_COLORS['white'], width=1)),
        text=[f'{score}%' for score in risk_scores],
        textposition='auto',
        textfont=dict(size=CHART_FONT['data_label_size'], color=CHART_COLORS['white'], family=CHART_FONT['family']),
        hovertemplate='<b>%{x}</b><br>Risk Level: %{y}%<extra></extra>'
    ))
    
    layout = create_chart_layout('Regulatory Risk by Category')
    layout['xaxis'] = dict(
        color=CHART_COLORS['white'],
        tickfont=dict(size=CHART_FONT['axis_x_size']-2, family=CHART_FONT['family']),  # Slightly smaller for category names
        title=dict(text='Regulatory Category', font=dict(size=CHART_FONT['axis_title_size'], family=CHART_FONT['family'])),
        tickangle=-45
    )
    layout['yaxis'] = dict(
        color=CHART_COLORS['white'],
        tickfont=dict(size=CHART_FONT['axis_y_size'], family=CHART_FONT['family']),
        title=dict(text='Risk Level (%)', font=dict(size=CHART_FONT['axis_title_size'], family=CHART_FONT['family'])),
        range=[0, 100]
    )
    
    fig.update_layout(layout)
    return fig

def chart_8_upcoming_deadlines():
    """Upcoming Deadlines Tracker (Timeline/Gantt-style)"""
    tasks = ['Annual Inspection Prep', 'USP <797> Training Update', 'Environmental Validation', 'Quality Review', 'Equipment Calibration']
    start_dates = [datetime.now() + timedelta(days=10), 
                   datetime.now() + timedelta(days=5),
                   datetime.now() + timedelta(days=25),
                   datetime.now() + timedelta(days=15),
                   datetime.now() + timedelta(days=35)]
    durations = [30, 7, 14, 10, 5]  # Days
    
    fig = go.Figure()
    
    # Color coding based on urgency (days until start)
    colors = []
    for start_date in start_dates:
        days_until = (start_date - datetime.now()).days
        if days_until <= 7:
            colors.append(CHART_COLORS['red'])
        elif days_until <= 20:
            colors.append(CHART_COLORS['amber'])
        else:
            colors.append(CHART_COLORS['green'])
    
    # Create horizontal bars for timeline
    for i, (task, start, duration, color) in enumerate(zip(tasks, start_dates, durations, colors)):
        fig.add_trace(go.Bar(
            y=[task],
            x=[duration],
            base=[start],
            orientation='h',
            name=task,
            marker_color=color,
            showlegend=False,
            hovertemplate=f'<b>{task}</b><br>Start: {start.strftime("%Y-%m-%d")}<br>Duration: {duration} days<extra></extra>'
        ))
    
    # Add "today" line
    today = datetime.now()
    fig.add_shape(
        type="line",
        x0=today,
        x1=today,
        y0=-0.5,
        y1=len(tasks)-0.5,
        line=dict(color=CHART_COLORS['white'], width=3, dash="dash")
    )
    
    layout = create_chart_layout('Upcoming Deadlines Tracker')
    layout['xaxis'] = dict(
        color=CHART_COLORS['white'],
        tickfont=dict(size=CHART_FONT['axis_x_size'], family=CHART_FONT['family']),
        title=dict(text='Timeline', font=dict(size=CHART_FONT['axis_title_size'], family=CHART_FONT['family'])),
        type='date'
    )
    layout['yaxis'] = dict(
        color=CHART_COLORS['white'],
        tickfont=dict(size=CHART_FONT['axis_y_size'], family=CHART_FONT['family'])
    )
    
    fig.update_layout(layout)
    return fig

def create_download_link(content, filename):
    """Create download link for large content"""
    if len(content) > 45000:
        # In a real implementation, this would save to Google Drive
        # For now, we'll create a text download
        buffer = io.StringIO()
        buffer.write(content)
        buffer.seek(0)
        
        return st.download_button(
            label="📥 Download Full Content",
            data=buffer.getvalue(),
            file_name=f"{filename}_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain",
            help="Content is too large to display. Click to download the full report."
        )
    return None

def main():
    """Main dashboard application"""
    
    # Header
    st.markdown('<h1 class="main-header">LexCura Compliance Dashboard</h1>', unsafe_allow_html=True)
    
    # Get client ID from URL parameters (FIXED)
    client_id = st.query_params.get("client_id", "CB999")
    
    # Load client data
    client_data = load_client_data(client_id)
    
    # Client information card
    st.markdown(f"""
    <div class="client-info-card">
        <h2 style="color: {CHART_COLORS['gold']}; margin-bottom: 1rem; font-family: {CHART_FONT['family']};">
            📊 {client_data['CLIENT NAME']} - Compliance Overview
        </h2>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">
            <div class="metric-container">
                <strong style="color: {CHART_COLORS['gold']};">Client ID</strong><br>
                {client_data['UNIQUE CLIENT ID']}
            </div>
            <div class="metric-container">
                <strong style="color: {CHART_COLORS['gold']};">Service Tier</strong><br>
                {client_data['TIER']} • {client_data['REGION']}
            </div>
            <div class="metric-container alert-{client_data['ALERT LEVEL'].lower()}">
                <strong style="color: {CHART_COLORS['gold']};">Alert Status</strong><br>
                {client_data['ALERT LEVEL']} • {client_data['STATUS']}
            </div>
            <div class="metric-container">
                <strong style="color: {CHART_COLORS['gold']};">Last Updated</strong><br>
                {client_data['DATE SCRAPED']}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Force refresh button (FIXED)
    col1, col2, col3 = st.columns([1, 1, 4])
    with col1:
        if st.button("🔄 Force Refresh", help="Clear cache and reload data"):
            st.cache_data.clear()
            st.rerun()
    
    # Executive Summary
    if client_data.get('EXECUTIVE SUMMARY'):
        st.markdown(f"""
        <div class="chart-container">
            <h3 style="color: {CHART_COLORS['gold']}; font-family: {CHART_FONT['family']};">📋 Executive Summary</h3>
            <p style="line-height: 1.6; color: {CHART_COLORS['white']};">{client_data['EXECUTIVE SUMMARY']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Charts section
    st.markdown(f"<h2 style='color: {CHART_COLORS['silver']}; font-family: {CHART_FONT['family']}; text-align: center; margin: 2rem 0;'>📈 Interactive Analytics Dashboard</h2>", unsafe_allow_html=True)
    
    # Row 1: Financial and Compliance Overview
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.plotly_chart(chart_1_financial_impact(), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.plotly_chart(chart_2_compliance_excellence(), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Row 2: Monitoring and Alerts
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.plotly_chart(chart_3_monitoring_dashboard(), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.plotly_chart(chart_4_alert_status(), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Row 3: Risk Assessment
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.plotly_chart(chart_5_risk_assessment(), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.plotly_chart(chart_6_executive_performance(), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Row 4: Regulatory and Timeline
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.plotly_chart(chart_7_regulatory_risk(), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.plotly_chart(chart_8_upcoming_deadlines(), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Raw content download section
    raw_content = client_data.get('MAIN STRUCTURED CONTENT', '')
    if raw_content and len(raw_content) > 500:  # Only show if there's substantial content
        st.markdown(f"""
        <div class="download-section">
            <h3 style="color: {CHART_COLORS['light_blue']}; font-family: {CHART_FONT['family']};">📄 Raw Data Access</h3>
            <p>Detailed compliance data and regulatory content for {client_data['CLIENT NAME']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Show truncated content
        if len(raw_content) > 1000:
            st.text_area(
                "Content Preview (truncated)", 
                raw_content[:1000] + "\n\n... (content truncated)", 
                height=150,
                disabled=True
            )
            create_download_link(raw_content, f"compliance_data_{client_id}")
        else:
            st.text_area("Full Content", raw_content, height=200, disabled=True)
    
    # Footer
    st.markdown("---")
    st.markdown(f"""
    <div style="text-align: center; color: {CHART_COLORS['grey']}; font-family: {CHART_FONT['family']};">
        <p><strong>LexCura</strong> - Elite Automated Compliance for 503B Sterile Manufacturing</p>
        <p>Dashboard generated: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')} | Client: {client_id}</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
