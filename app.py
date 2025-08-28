"""
Fortune 500 Executive Dashboard - LexCura Elite
Premium legal compliance analytics platform
Replicating Pinterest design reference with executive color palette

Version: 3.0.0 Executive
Built for Fortune 500 leadership and C-suite decision making
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.io as pio
import json
import hashlib
import secrets
import time
from datetime import datetime, timedelta, date
from typing import Dict, List, Optional, Tuple, Any, Union
import io
import base64
from pathlib import Path
import uuid
import re
from dataclasses import dataclass
from enum import Enum
import logging
import calendar

# ============================================================================
# EXECUTIVE CONFIGURATION & CONSTANTS
# ============================================================================

class ExecutivePalette:
    """Fortune 500 Executive Color Palette - Exact Match Required"""
    CHARCOAL_BG = "#0F1113"           # Background
    DARK_CARD = "#1B1D1F"             # Card backgrounds  
    LIGHT_CARD = "#252728"            # Light cards
    METALLIC_GOLD = "#D4AF37"         # Primary accent (replaces blue)
    GOLD_HIGHLIGHT = "#FFCF66"        # Bright accent (replaces bright blue)
    NEUTRAL_TEXT = "#B8B9BB"          # Body text
    HIGH_CONTRAST = "#F5F6F7"         # Headers/white text
    ERROR_SUBTLE = "#E4574C"          # Error states
    SUCCESS_SUBTLE = "#3DBC6B"        # Success states
    
    # Additional semantic colors
    WARNING = "#F59E0B"
    INFO = "#3B82F6" 
    
    # Gradient definitions
    GOLD_GRADIENT = f"linear-gradient(135deg, {METALLIC_GOLD} 0%, {GOLD_HIGHLIGHT} 100%)"
    CARD_GRADIENT = f"linear-gradient(145deg, {DARK_CARD} 0%, {LIGHT_CARD} 100%)"

class ExecutiveConfig:
    """Executive Application Configuration"""
    APP_NAME = "LexCura Elite"
    APP_SUBTITLE = "Executive Legal Intelligence Platform"
    VERSION = "3.0.0 Executive"
    COMPANY = "LexCura Executive Services"
    SUPPORT_EMAIL = "executive@lexcura.com"
    LOGO_PATH = "assets/lexcuralogo.png"
    SESSION_TIMEOUT = 3600
    MAX_LOGIN_ATTEMPTS = 3
    CACHE_TTL = 300

class UserRole(Enum):
    """User Access Levels"""
    EXECUTIVE = "executive"
    DIRECTOR = "director" 
    MANAGER = "manager"
    ANALYST = "analyst"
    VIEWER = "viewer"

@dataclass
class User:
    """User Profile Structure"""
    username: str
    email: str
    role: UserRole
    full_name: str
    avatar_url: Optional[str] = None
    last_login: Optional[datetime] = None
    login_count: int = 0

# ============================================================================
# PLOTLY THEME SYSTEM
# ============================================================================

def register_executive_plotly_theme():
    """Register custom executive Plotly theme matching design"""
    executive_theme = {
        "layout": {
            "paper_bgcolor": ExecutivePalette.CHARCOAL_BG,
            "plot_bgcolor": "rgba(0,0,0,0)",
            "colorway": [
                ExecutivePalette.METALLIC_GOLD,
                ExecutivePalette.GOLD_HIGHLIGHT,
                ExecutivePalette.SUCCESS_SUBTLE,
                ExecutivePalette.HIGH_CONTRAST,
                ExecutivePalette.ERROR_SUBTLE,
                ExecutivePalette.WARNING,
                ExecutivePalette.INFO
            ],
            "font": {
                "family": "Inter, 'Helvetica Neue', -apple-system, system-ui, sans-serif",
                "color": ExecutivePalette.HIGH_CONTRAST,
                "size": 12
            },
            "title": {
                "font": {
                    "family": "Inter, system-ui, sans-serif",
                    "size": 18,
                    "color": ExecutivePalette.METALLIC_GOLD
                },
                "x": 0.02,
                "xanchor": "left",
                "pad": {"t": 20, "b": 20}
            },
            "xaxis": {
                "gridcolor": "rgba(212, 175, 55, 0.1)",
                "linecolor": "rgba(212, 175, 55, 0.2)",
                "zerolinecolor": "rgba(212, 175, 55, 0.2)",
                "tickfont": {"color": ExecutivePalette.NEUTRAL_TEXT, "size": 10},
                "titlefont": {"color": ExecutivePalette.METALLIC_GOLD, "size": 12}
            },
            "yaxis": {
                "gridcolor": "rgba(212, 175, 55, 0.1)",
                "linecolor": "rgba(212, 175, 55, 0.2)",
                "zerolinecolor": "rgba(212, 175, 55, 0.2)",
                "tickfont": {"color": ExecutivePalette.NEUTRAL_TEXT, "size": 10},
                "titlefont": {"color": ExecutivePalette.METALLIC_GOLD, "size": 12}
            },
            "legend": {
                "bgcolor": "rgba(27, 29, 31, 0.9)",
                "bordercolor": ExecutivePalette.METALLIC_GOLD,
                "borderwidth": 1,
                "font": {"color": ExecutivePalette.HIGH_CONTRAST, "size": 10}
            },
            "margin": {"l": 40, "r": 20, "t": 60, "b": 40}
        }
    }
    
    pio.templates["executive"] = go.layout.Template(layout=executive_theme["layout"])
    pio.templates.default = "executive"

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

def configure_executive_page():
    """Configure Streamlit for executive experience"""
    st.set_page_config(
        page_title=f"{ExecutiveConfig.APP_NAME} | Executive Dashboard",
        page_icon="⚖️",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': f'mailto:{ExecutiveConfig.SUPPORT_EMAIL}',
            'Report a bug': f'mailto:{ExecutiveConfig.SUPPORT_EMAIL}',
            'About': f"{ExecutiveConfig.APP_NAME} {ExecutiveConfig.VERSION}"
        }
    )

def initialize_session_state():
    """Initialize comprehensive session state"""
    defaults = {
        'authenticated': False,
        'user': None,
        'login_attempts': 0,
        'session_start': None,
        'current_page': 'dashboard',
        'data_loaded': False,
        'last_refresh': None,
        'selected_client': None,
        'date_range': (datetime.now() - timedelta(days=30), datetime.now()),
        'theme': 'executive_dark',
        'notifications': [],
        'search_query': '',
        'sidebar_collapsed': False
    }
    
    for key, default_value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value

# ============================================================================
# EXECUTIVE CSS SYSTEM - PINTEREST DESIGN REPLICA
# ============================================================================

def load_executive_css():
    """Load comprehensive CSS matching Pinterest design with executive palette"""
    
    css_content = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    :root {{
        --bg-charcoal: {ExecutivePalette.CHARCOAL_BG};
        --bg-dark-card: {ExecutivePalette.DARK_CARD};
        --bg-light-card: {ExecutivePalette.LIGHT_CARD};
        --accent-gold: {ExecutivePalette.METALLIC_GOLD};
        --gold-highlight: {ExecutivePalette.GOLD_HIGHLIGHT};
        --text-neutral: {ExecutivePalette.NEUTRAL_TEXT};
        --text-contrast: {ExecutivePalette.HIGH_CONTRAST};
        --error-subtle: {ExecutivePalette.ERROR_SUBTLE};
        --success-subtle: {ExecutivePalette.SUCCESS_SUBTLE};
        --warning: {ExecutivePalette.WARNING};
        --info: {ExecutivePalette.INFO};
    }}
    
    /* Global Reset */
    .stApp {{
        background: var(--bg-charcoal);
        color: var(--text-neutral);
        font-family: 'Inter', 'Helvetica Neue', -apple-system, system-ui, sans-serif;
    }}
    
    /* Hide Streamlit Elements */
    #MainMenu {{ visibility: hidden; }}
    footer {{ visibility: hidden; }}
    header {{ visibility: hidden; }}
    .stDeployButton {{ visibility: hidden; }}
    
    /* ===== MAIN LAYOUT CONTAINER (Pinterest Style) ===== */
    .main-container {{
        display: flex;
        min-height: 100vh;
        background: var(--bg-charcoal);
    }}
    
    /* ===== SIDEBAR DESIGN (Exact Pinterest Match) ===== */
    .executive-sidebar {{
        width: 280px;
        background: var(--bg-dark-card);
        padding: 2rem 0;
        position: fixed;
        height: 100vh;
        left: 0;
        top: 0;
        z-index: 1000;
        border-right: 1px solid rgba(212, 175, 55, 0.1);
    }}
    
    .sidebar-logo {{
        padding: 0 2rem 3rem 2rem;
        text-align: center;
    }}
    
    .sidebar-logo h1 {{
        color: var(--text-contrast);
        font-size: 1.5rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: 2px;
    }}
    
    .sidebar-nav {{
        padding: 0 1rem;
    }}
    
    .nav-item {{
        display: flex;
        align-items: center;
        gap: 1rem;
        padding: 1rem 1.5rem;
        margin: 0.25rem 0;
        border-radius: 12px;
        color: var(--text-neutral);
        text-decoration: none;
        transition: all 0.3s ease;
        cursor: pointer;
        font-size: 0.9rem;
        font-weight: 500;
    }}
    
    .nav-item:hover {{
        background: rgba(212, 175, 55, 0.1);
        color: var(--gold-highlight);
        transform: translateX(4px);
    }}
    
    .nav-item.active {{
        background: linear-gradient(135deg, var(--accent-gold) 0%, var(--gold-highlight) 100%);
        color: var(--bg-charcoal);
        font-weight: 700;
    }}
    
    .nav-icon {{
        font-size: 1.2rem;
        width: 20px;
        text-align: center;
    }}
    
    .sidebar-logout {{
        position: absolute;
        bottom: 2rem;
        left: 1rem;
        right: 1rem;
    }}
    
    .logout-btn {{
        width: 100%;
        display: flex;
        align-items: center;
        gap: 1rem;
        padding: 1rem 1.5rem;
        background: transparent;
        border: 2px solid var(--accent-gold);
        border-radius: 12px;
        color: var(--accent-gold);
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-size: 0.8rem;
    }}
    
    .logout-btn:hover {{
        background: var(--accent-gold);
        color: var(--bg-charcoal);
    }}
    
    /* ===== MAIN CONTENT AREA ===== */
    .main-content {{
        margin-left: 280px;
        padding: 2rem 3rem;
        width: calc(100% - 280px);
        min-height: 100vh;
    }}
    
    /* ===== HEADER BAR (Pinterest Style) ===== */
    .content-header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 3rem;
        padding: 1.5rem 2rem;
        background: var(--bg-light-card);
        border-radius: 20px;
        border: 1px solid rgba(212, 175, 55, 0.1);
    }}
    
    .search-container {{
        position: relative;
        flex: 1;
        max-width: 400px;
        margin-right: 2rem;
    }}
    
    .search-input {{
        width: 100%;
        padding: 1rem 1rem 1rem 3rem;
        background: var(--accent-gold);
        border: none;
        border-radius: 25px;
        color: var(--bg-charcoal);
        font-size: 0.9rem;
        font-weight: 500;
    }}
    
    .search-input::placeholder {{
        color: rgba(15, 17, 19, 0.7);
    }}
    
    .search-icon {{
        position: absolute;
        left: 1rem;
        top: 50%;
        transform: translateY(-50%);
        color: var(--bg-charcoal);
        font-size: 1.1rem;
    }}
    
    .header-actions {{
        display: flex;
        align-items: center;
        gap: 1.5rem;
    }}
    
    .header-icon {{
        color: var(--text-neutral);
        font-size: 1.2rem;
        cursor: pointer;
        transition: color 0.3s ease;
    }}
    
    .header-icon:hover {{
        color: var(--accent-gold);
    }}
    
    .user-profile {{
        display: flex;
        align-items: center;
        gap: 1rem;
        padding: 0.75rem 1.5rem;
        background: var(--accent-gold);
        border-radius: 25px;
        cursor: pointer;
        transition: all 0.3s ease;
    }}
    
    .user-profile:hover {{
        background: var(--gold-highlight);
    }}
    
    .user-avatar {{
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background: var(--bg-charcoal);
        display: flex;
        align-items: center;
        justify-content: center;
        color: var(--accent-gold);
        font-weight: 700;
        font-size: 0.9rem;
    }}
    
    .user-name {{
        color: var(--bg-charcoal);
        font-weight: 700;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}
    
    /* ===== KPI CARDS (Pinterest Style) ===== */
    .kpi-container {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 2rem;
        margin-bottom: 3rem;
    }}
    
    .kpi-card {{
        background: var(--bg-light-card);
        padding: 2rem;
        border-radius: 20px;
        border: 1px solid rgba(212, 175, 55, 0.1);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }}
    
    .kpi-card::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: var(--accent-gold);
    }}
    
    .kpi-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
        border-color: rgba(212, 175, 55, 0.3);
    }}
    
    .kpi-card.featured {{
        background: linear-gradient(135deg, var(--accent-gold) 0%, var(--gold-highlight) 100%);
        color: var(--bg-charcoal);
    }}
    
    .kpi-card.featured .kpi-value,
    .kpi-card.featured .kpi-label {{
        color: var(--bg-charcoal);
    }}
    
    .kpi-header {{
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 1rem;
    }}
    
    .kpi-icon {{
        width: 50px;
        height: 50px;
        background: rgba(212, 175, 55, 0.1);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: var(--accent-gold);
        font-size: 1.5rem;
    }}
    
    .kpi-card.featured .kpi-icon {{
        background: rgba(15, 17, 19, 0.1);
        color: var(--bg-charcoal);
    }}
    
    .kpi-menu {{
        color: var(--text-neutral);
        cursor: pointer;
        font-size: 1.2rem;
    }}
    
    .kpi-value {{
        font-size: 2.5rem;
        font-weight: 800;
        color: var(--text-contrast);
        margin: 0.5rem 0;
        line-height: 1;
    }}
    
    .kpi-label {{
        color: var(--text-neutral);
        font-size: 0.9rem;
        margin-bottom: 1rem;
        text-transform: capitalize;
    }}
    
    .kpi-change {{
        font-size: 0.8rem;
        font-weight: 600;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        display: inline-block;
    }}
    
    .kpi-change.positive {{
        background: rgba(61, 188, 107, 0.2);
        color: var(--success-subtle);
    }}
    
    .kpi-change.negative {{
        background: rgba(228, 87, 76, 0.2);
        color: var(--error-subtle);
    }}
    
    /* ===== MAIN CHART AREA (Pinterest Style) ===== */
    .chart-main {{
        background: var(--bg-light-card);
        border-radius: 20px;
        padding: 2rem;
        margin-bottom: 3rem;
        border: 1px solid rgba(212, 175, 55, 0.1);
    }}
    
    .chart-header {{
        margin-bottom: 2rem;
    }}
    
    .chart-title {{
        color: var(--text-contrast);
        font-size: 1.2rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }}
    
    .chart-subtitle {{
        color: var(--text-neutral);
        font-size: 0.9rem;
    }}
    
    /* ===== RIGHT SIDEBAR CONTENT ===== */
    .content-grid {{
        display: grid;
        grid-template-columns: 1fr 350px;
        gap: 3rem;
        margin-bottom: 2rem;
    }}
    
    .right-sidebar {{
        display: flex;
        flex-direction: column;
        gap: 2rem;
    }}
    
    .widget-card {{
        background: var(--bg-light-card);
        border-radius: 20px;
        padding: 2rem;
        border: 1px solid rgba(212, 175, 55, 0.1);
    }}
    
    .widget-title {{
        color: var(--text-contrast);
        font-size: 1.1rem;
        font-weight: 700;
        margin-bottom: 1.5rem;
    }}
    
    /* ===== DONUT CHART WIDGET ===== */
    .donut-container {{
        text-align: center;
        position: relative;
    }}
    
    .donut-center {{
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        z-index: 10;
    }}
    
    .donut-value {{
        font-size: 2rem;
        font-weight: 800;
        color: var(--text-contrast);
        line-height: 1;
    }}
    
    .donut-label {{
        font-size: 0.8rem;
        color: var(--text-neutral);
        text-transform: uppercase;
        letter-spacing: 1px;
    }}
    
    .donut-legend {{
        display: flex;
        justify-content: center;
        gap: 1.5rem;
        margin-top: 1.5rem;
    }}
    
    .legend-item {{
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 0.8rem;
    }}
    
    .legend-dot {{
        width: 10px;
        height: 10px;
        border-radius: 50%;
    }}
    
    /* ===== TRAFFIC SOURCE WIDGET ===== */
    .traffic-list {{
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }}
    
    .traffic-item {{
        display: flex;
        justify-content: space-between;
        align-items: center;
    }}
    
    .traffic-source {{
        color: var(--text-contrast);
        font-size: 0.9rem;
        font-weight: 500;
    }}
    
    .traffic-bar {{
        flex: 1;
        height: 6px;
        background: rgba(212, 175, 55, 0.1);
        border-radius: 3px;
        margin: 0 1rem;
        position: relative;
        overflow: hidden;
    }}
    
    .traffic-fill {{
        height: 100%;
        background: var(--accent-gold);
        border-radius: 3px;
        transition: width 1s ease;
    }}
    
    .traffic-percent {{
        color: var(--text-neutral);
        font-size: 0.8rem;
        font-weight: 600;
        min-width: 35px;
        text-align: right;
    }}
    
    /* ===== CALENDAR WIDGET ===== */
    .calendar-container {{
        background: var(--bg-light-card);
        border-radius: 20px;
        padding: 2rem;
        border: 1px solid rgba(212, 175, 55, 0.1);
    }}
    
    .calendar-header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1.5rem;
    }}
    
    .calendar-month {{
        color: var(--text-contrast);
        font-size: 1.1rem;
        font-weight: 700;
    }}
    
    .calendar-nav {{
        display: flex;
        gap: 1rem;
    }}
    
    .calendar-nav-btn {{
        background: none;
        border: none;
        color: var(--text-neutral);
        font-size: 1.2rem;
        cursor: pointer;
        padding: 0.5rem;
        border-radius: 50%;
        transition: all 0.3s ease;
    }}
    
    .calendar-nav-btn:hover {{
        background: rgba(212, 175, 55, 0.1);
        color: var(--accent-gold);
    }}
    
    .calendar-grid {{
        display: grid;
        grid-template-columns: repeat(7, 1fr);
        gap: 0.5rem;
    }}
    
    .calendar-day {{
        aspect-ratio: 1;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.9rem;
        color: var(--text-neutral);
        cursor: pointer;
        border-radius: 8px;
        transition: all 0.3s ease;
        font-weight: 500;
    }}
    
    .calendar-day:hover {{
        background: rgba(212, 175, 55, 0.1);
        color: var(--accent-gold);
    }}
    
    .calendar-day.today {{
        background: var(--accent-gold);
        color: var(--bg-charcoal);
        font-weight: 700;
    }}
    
    .calendar-day.other-month {{
        opacity: 0.3;
    }}
    
    /* ===== RESPONSIVE DESIGN ===== */
    @media (max-width: 1400px) {{
        .content-grid {{
            grid-template-columns: 1fr 300px;
        }}
        
        .right-sidebar {{
            gap: 1.5rem;
        }}
    }}
    
    @media (max-width: 1200px) {{
        .executive-sidebar {{
            transform: translateX(-100%);
            transition: transform 0.3s ease;
        }}
        
        .executive-sidebar.open {{
            transform: translateX(0);
        }}
        
        .main-content {{
            margin-left: 0;
            width: 100%;
            padding: 1.5rem;
        }}
        
        .content-grid {{
            grid-template-columns: 1fr;
        }}
        
        .kpi-container {{
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.5rem;
        }}
    }}
    
    @media (max-width: 768px) {{
        .main-content {{
            padding: 1rem;
        }}
        
        .content-header {{
            flex-direction: column;
            gap: 1rem;
        }}
        
        .search-container {{
            max-width: 100%;
            margin-right: 0;
        }}
        
        .kpi-container {{
            grid-template-columns: 1fr;
        }}
        
        .user-profile {{
            padding: 0.5rem 1rem;
        }}
        
        .user-name {{
            display: none;
        }}
    }}
    
    /* ===== ANIMATIONS ===== */
    @keyframes slideIn {{
        from {{
            opacity: 0;
            transform: translateY(20px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}
    
    @keyframes fadeIn {{
        from {{
            opacity: 0;
        }}
        to {{
            opacity: 1;
        }}
    }}
    
    .animate-slide-in {{
        animation: slideIn 0.6s ease-out;
    }}
    
    .animate-fade-in {{
        animation: fadeIn 0.4s ease-out;
    }}
    
    /* ===== UTILITY CLASSES ===== */
    .text-gold {{ color: var(--accent-gold); }}
    .text-contrast {{ color: var(--text-contrast); }}
    .text-neutral {{ color: var(--text-neutral); }}
    .text-success {{ color: var(--success-subtle); }}
    .text-error {{ color: var(--error-subtle); }}
    
    .bg-dark {{ background: var(--bg-dark-card); }}
    .bg-light {{ background: var(--bg-light-card); }}
    
    .rounded {{ border-radius: 12px; }}
    .rounded-lg {{ border-radius: 20px; }}
    .rounded-full {{ border-radius: 50px; }}
    
    .shadow {{ box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2); }}
    .shadow-lg {{ box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3); }}
    
    .transition {{ transition: all 0.3s ease; }}
    .cursor-pointer {{ cursor: pointer; }}
    
    .flex {{ display: flex; }}
    .items-center {{ align-items: center; }}
    .justify-between {{ justify-content: space-between; }}
    .justify-center {{ justify-content: center; }}
    .gap-4 {{ gap: 1rem; }}
    .gap-8 {{ gap: 2rem; }}
    
    .hidden {{ display: none; }}
    .block {{ display: block; }}
    
    .w-full {{ width: 100%; }}
    .h-full {{ height: 100%; }}
    </style>
    """
    
    st.markdown(css_content, unsafe_allow_html=True)

# ============================================================================
# AUTHENTICATION SYSTEM
# ============================================================================

class AuthenticationManager:
    """Executive authentication system"""
    
    def __init__(self):
        self.users_db = self._initialize_users()
    
    def _initialize_users(self) -> Dict[str, Dict]:
        """Initialize user database"""
        return {
            "executive": {
                "password_hash": self._hash_password("Executive2024!"),
                "user_data": User(
                    username="executive",
                    email="executive@lexcura.com",
                    role=UserRole.EXECUTIVE,
                    full_name="Robert William"  # Matching Pinterest design
                )
            },
            "director": {
                "password_hash": self._hash_password("Director2024!"),
                "user_data": User(
                    username="director",
                    email="director@lexcura.com", 
                    role=UserRole.DIRECTOR,
                    full_name="Sarah Director"
                )
            },
            "demo": {
                "password_hash": self._hash_password("Demo2024!"),
                "user_data": User(
                    username="demo",
                    email="demo@lexcura.com",
                    role=UserRole.VIEWER,
                    full_name="Demo User"
                )
            }
        }
    
    def _hash_password(self, password: str) -> str:
        """Secure password hashing"""
        salt = "lexcura_executive_2024"
        return hashlib.sha256((password + salt).encode()).hexdigest()
    
    def _verify_password(self, password: str, password_hash: str) -> bool:
        """Verify password"""
        return self._hash_password(password) == password_hash
    
    def authenticate_user(self, username: str, password: str) -> Tuple[bool, Optional[User], str]:
        """Authenticate user"""
        try:
            if username not in self.users_db:
                return False, None, "Invalid credentials"
            
            user_record = self.users_db[username]
            if not self._verify_password(password, user_record["password_hash"]):
                st.session_state.login_attempts += 1
                attempts_left = ExecutiveConfig.MAX_LOGIN_ATTEMPTS - st.session_state.login_attempts
                if attempts_left <= 0:
                    return False, None, "Account locked"
                return False, None, f"Invalid credentials ({attempts_left} attempts left)"
            
            user = user_record["user_data"]
            user.last_login = datetime.now()
            user.login_count += 1
            
            st.session_state.login_attempts = 0
            return True, user, "Success"
            
        except Exception as e:
            return False, None, "System error"
    
    def logout_user(self):
        """Logout user"""
        for key in ['authenticated', 'user', 'session_start']:
            if key in st.session_state:
                del st.session_state[key]
        st.session_state.authenticated = False
        st.rerun()

# ============================================================================
# DATA MANAGEMENT
# ============================================================================

@st.cache_data(ttl=ExecutiveConfig.CACHE_TTL, show_spinner=False)
def load_executive_data() -> Dict[str, Any]:
    """Load comprehensive dashboard data"""
    
    # Generate sample time series data for charts
    dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
    np.random.seed(42)
    
    # Main area chart data (Pinterest style)
    area_data = []
    base_value = 15000
    for i, date in enumerate(dates):
        # Simulate realistic business data with trends and seasonality
        trend = i * 20
        seasonal = 5000 * np.sin(2 * np.pi * i / 365.25) 
        noise = np.random.normal(0, 1000)
        value = base_value + trend + seasonal + noise
        area_data.append({'date': date, 'value': max(0, value)})
    
    area_df = pd.DataFrame(area_data)
    
    # Generate monthly data for simplified view
    monthly_data = area_df.groupby(area_df['date'].dt.to_period('M')).agg({
        'value': 'mean'
    }).round(0)
    
    return {
        # KPI Data (matching Pinterest cards)
        'kpi_data': {
            'revenue': {'value': 36159, 'change': '+2.5%', 'trend': 'positive'},
            'users': {'value': 3359, 'change': '+12.3%', 'trend': 'positive'}, 
            'orders': {'value': 36159, 'change': '-1.2%', 'trend': 'negative'},
            'conversion': {'value': 2.45, 'change': '+0.3%', 'trend': 'positive'}
        },
        
        # Chart data
        'area_chart_data': area_df,
        'monthly_data': monthly_data,
        
        # Donut chart data (Top Product Sale)
        'product_sales': {
            'total': 95000,
            'segments': [
                {'name': 'Vector', 'value': 35, 'color': ExecutivePalette.METALLIC_GOLD},
                {'name': 'Template', 'value': 40, 'color': ExecutivePalette.NEUTRAL_TEXT},
                {'name': 'Presentation', 'value': 25, 'color': ExecutivePalette.LIGHT_CARD}
            ]
        },
        
        # Traffic source data
        'traffic_sources': [
            {'source': 'example.com', 'percentage': 65},
            {'source': 'example2.com', 'percentage': 45}, 
            {'source': 'example3.com', 'percentage': 30}
        ],
        
        # Calendar data
        'calendar': {
            'current_month': datetime.now().strftime('%B %Y'),
            'today': datetime.now().day
        },
        
        # Meta data
        'last_updated': datetime.now(),
        'user_count': 1247,
        'active_sessions': 89
    }

# ============================================================================
# CHART CREATION FUNCTIONS
# ============================================================================

def create_area_chart(data_df: pd.DataFrame) -> go.Figure:
    """Create main area chart matching Pinterest design"""
    
    # Sample data for the last 12 months
    recent_data = data_df.tail(365)
    
    fig = go.Figure()
    
    # Create smooth area chart
    fig.add_trace(go.Scatter(
        x=recent_data['date'],
        y=recent_data['value'],
        mode='lines',
        fill='tonexty',
        fillcolor='rgba(212, 175, 55, 0.3)',
        line=dict(
            color=ExecutivePalette.METALLIC_GOLD,
            width=3,
            shape='spline',
            smoothing=0.3
        ),
        name='Performance',
        hovertemplate='<b>%{y:,.0f}</b><br>%{x}<extra></extra>'
    ))
    
    # Add baseline
    fig.add_hline(
        y=recent_data['value'].min(),
        line_dash="dot",
        line_color=ExecutivePalette.NEUTRAL_TEXT,
        opacity=0.5
    )
    
    fig.update_layout(
        title='',
        showlegend=False,
        height=300,
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(212, 175, 55, 0.1)',
            showticklabels=True,
            tickformat='%b',
            tickangle=0
        ),
        yaxis=dict(
            showgrid=True, 
            gridcolor='rgba(212, 175, 55, 0.1)',
            showticklabels=True,
            tickformat=',.0f'
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        hovermode='x unified'
    )
    
    return fig

def create_donut_chart(product_data: Dict) -> go.Figure:
    """Create donut chart for product sales"""
    
    segments = product_data['segments']
    
    fig = go.Figure(data=[
        go.Pie(
            labels=[seg['name'] for seg in segments],
            values=[seg['value'] for seg in segments],
            hole=0.6,
            marker=dict(
                colors=[seg['color'] for seg in segments],
                line=dict(color=ExecutivePalette.CHARCOAL_BG, width=3)
            ),
            textinfo='none',
            hovertemplate='<b>%{label}</b><br>%{percent}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        showlegend=False,
        height=200,
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

def create_sparkline(values: List[float], color: str = None) -> go.Figure:
    """Create small sparkline charts for KPI cards"""
    
    if color is None:
        color = ExecutivePalette.METALLIC_GOLD
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        y=values,
        mode='lines',
        line=dict(color=color, width=2),
        fill='tonexty',
        fillcolor=f'rgba({",".join(str(int(color[i:i+2], 16)) for i in (1, 3, 5))}, 0.3)',
        showlegend=False,
        hoverinfo='skip'
    ))
    
    fig.update_layout(
        height=60,
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

# ============================================================================
# UI COMPONENTS
# ============================================================================

def render_login_page():
    """Render executive login matching design aesthetic"""
    
    st.markdown("""
    <div style="display: flex; justify-content: center; align-items: center; min-height: 100vh; background: var(--bg-charcoal);">
        <div style="background: var(--bg-light-card); padding: 3rem; border-radius: 20px; border: 1px solid rgba(212, 175, 55, 0.1); width: 400px; text-align: center;">
            <h1 style="color: var(--text-contrast); margin-bottom: 0.5rem; font-size: 2rem; font-weight: 800;">LOGO</h1>
            <p style="color: var(--text-neutral); margin-bottom: 2rem;">Executive Legal Intelligence</p>
    """, unsafe_allow_html=True)
    
    with st.form("login_form"):
        st.text_input("Username", placeholder="Enter username")
        st.text_input("Password", type="password", placeholder="Enter password")
        
        col1, col2 = st.columns(2)
        with col1:
            st.checkbox("Remember me")
        
        submitted = st.form_submit_button("LOGIN", use_container_width=True)
        
        if submitted:
            # For demo, always authenticate as Robert William
            st.session_state.authenticated = True
            st.session_state.user = User(
                username="executive",
                email="executive@lexcura.com", 
                role=UserRole.EXECUTIVE,
                full_name="ROBERT WILLIAM"
            )
            st.session_state.session_start = datetime.now()
            st.rerun()
    
    # Demo credentials
    with st.expander("Demo Credentials"):
        st.write("Username: `demo` | Password: `demo`")
        st.write("Username: `executive` | Password: `Executive2024!`")
    
    st.markdown("</div></div>", unsafe_allow_html=True)

def render_sidebar():
    """Render left sidebar navigation matching Pinterest design"""
    
    sidebar_html = f"""
    <div class="executive-sidebar">
        <div class="sidebar-logo">
            <h1>LOGO</h1>
        </div>
        
        <nav class="sidebar-nav">
            <div class="nav-item active" onclick="setActivePage('dashboard')">
                <span class="nav-icon">📊</span>
                <span>Dashboard</span>
            </div>
            <div class="nav-item" onclick="setActivePage('profile')">
                <span class="nav-icon">👤</span>
                <span>Profile</span>
            </div>
            <div class="nav-item" onclick="setActivePage('folders')">
                <span class="nav-icon">📁</span>
                <span>Folders</span>
            </div>
            <div class="nav-item" onclick="setActivePage('notification')">
                <span class="nav-icon">🔔</span>
                <span>Notification</span>
            </div>
            <div class="nav-item" onclick="setActivePage('messages')">
                <span class="nav-icon">💬</span>
                <span>Messages</span>
            </div>
            <div class="nav-item" onclick="setActivePage('help')">
                <span class="nav-icon">❓</span>
                <span>Help Center</span>
            </div>
            <div class="nav-item" onclick="setActivePage('settings')">
                <span class="nav-icon">⚙️</span>
                <span>Setting</span>
            </div>
        </nav>
        
        <div class="sidebar-logout">
            <button class="logout-btn" onclick="logout()">
                <span class="nav-icon">🚪</span>
                <span>LOGOUT</span>
            </button>
        </div>
    </div>
    
    <script>
    function setActivePage(page) {{
        // Remove active class from all nav items
        document.querySelectorAll('.nav-item').forEach(item => item.classList.remove('active'));
        // Add active class to clicked item
        event.target.closest('.nav-item').classList.add('active');
    }}
    
    function logout() {{
        if(confirm('Are you sure you want to logout?')) {{
            // This would trigger a Streamlit rerun in the actual app
            window.parent.postMessage({{'type': 'logout'}}, '*');
        }}
    }}
    </script>
    """
    
    st.markdown(sidebar_html, unsafe_allow_html=True)

def render_header(user: User):
    """Render top header bar matching Pinterest design"""
    
    header_html = f"""
    <div class="content-header">
        <div class="search-container">
            <span class="search-icon">🔍</span>
            <input type="text" class="search-input" placeholder="Search" />
        </div>
        
        <div class="header-actions">
            <span class="header-icon">📧</span>
            <span class="header-icon">🔔</span>
            <span class="header-icon">⚙️</span>
            
            <div class="user-profile">
                <div class="user-name">{user.full_name}</div>
                <div class="user-avatar">{user.full_name[0]}</div>
            </div>
        </div>
    </div>
    """
    
    st.markdown(header_html, unsafe_allow_html=True)

def render_kpi_cards(kpi_data: Dict):
    """Render KPI cards matching Pinterest design"""
    
    # Generate sparkline data
    sparkline_values = [20, 25, 22, 30, 28, 35, 32, 38, 36, 42]
    
    kpi_html = f"""
    <div class="kpi-container">
        <div class="kpi-card">
            <div class="kpi-header">
                <div class="kpi-icon">💰</div>
                <span class="kpi-menu">⋮</span>
            </div>
            <div class="kpi-value">36,159</div>
            <div class="kpi-label">8 mins read</div>
            <div class="kpi-change positive">+2.5% from last month</div>
        </div>
        
        <div class="kpi-card">
            <div class="kpi-header">
                <div class="kpi-icon">👥</div>
                <span class="kpi-menu">⋮</span>
            </div>
            <div class="kpi-value">3,359</div>
            <div class="kpi-label">6 mins read</div>
            <div class="kpi-change positive">+12.3% from last month</div>
        </div>
        
        <div class="kpi-card featured">
            <div class="kpi-header">
                <div class="kpi-icon">📈</div>
                <span class="kpi-menu">⋮</span>
            </div>
            <div class="kpi-value">36,159</div>
            <div class="kpi-label">4 mins read</div>
            <div class="kpi-change positive">+8.1% from last month</div>
        </div>
    </div>
    """
    
    st.markdown(kpi_html, unsafe_allow_html=True)

def render_calendar_widget():
    """Render calendar widget matching Pinterest design"""
    
    current_date = datetime.now()
    current_month = current_date.month
    current_year = current_date.year
    today = current_date.day
    
    # Get calendar data
    cal = calendar.monthcalendar(current_year, current_month)
    month_name = calendar.month_name[current_month]
    
    # Generate calendar HTML
    calendar_html = f"""
    <div class="calendar-container">
        <div class="calendar-header">
            <div class="calendar-month">{month_name} {current_year}</div>
            <div class="calendar-nav">
                <button class="calendar-nav-btn">❮</button>
                <button class="calendar-nav-btn">❯</button>
            </div>
        </div>
        
        <div class="calendar-grid">
    """
    
    # Add day headers
    days = ['S', 'M', 'T', 'W', 'T', 'F', 'S']
    for day in days:
        calendar_html += f'<div class="calendar-day" style="font-weight: 700; color: var(--text-neutral);">{day}</div>'
    
    # Add calendar days
    for week in cal:
        for day in week:
            if day == 0:
                calendar_html += '<div class="calendar-day other-month"></div>'
            else:
                classes = "calendar-day"
                if day == today:
                    classes += " today"
                calendar_html += f'<div class="{classes}">{day}</div>'
    
    calendar_html += """
        </div>
    </div>
    """
    
    st.markdown(calendar_html, unsafe_allow_html=True)

def render_donut_widget(product_data: Dict):
    """Render donut chart widget"""
    
    donut_html = f"""
    <div class="widget-card">
        <div class="widget-title">Top Product Sale</div>
        <div class="donut-container">
            <div class="donut-center">
                <div class="donut-value">95K</div>
                <div class="donut-label">TOTAL</div>
            </div>
        </div>
        <div class="donut-legend">
            <div class="legend-item">
                <div class="legend-dot" style="background: {ExecutivePalette.METALLIC_GOLD};"></div>
                <span>Vector</span>
            </div>
            <div class="legend-item">
                <div class="legend-dot" style="background: {ExecutivePalette.NEUTRAL_TEXT};"></div>
                <span>Template</span>
            </div>
            <div class="legend-item">
                <div class="legend-dot" style="background: {ExecutivePalette.LIGHT_CARD};"></div>
                <span>Presentation</span>
            </div>
        </div>
    </div>
    """
    
    st.markdown(donut_html, unsafe_allow_html=True)
    
    # Add actual donut chart
    fig = create_donut_chart(product_data)
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

def render_traffic_widget(traffic_data: List[Dict]):
    """Render traffic source widget"""
    
    traffic_html = f"""
    <div class="widget-card">
        <div class="widget-title">Traffic Source</div>
        <div class="traffic-list">
    """
    
    for item in traffic_data:
        traffic_html += f"""
        <div class="traffic-item">
            <span class="traffic-source">{item['source']}</span>
            <div class="traffic-bar">
                <div class="traffic-fill" style="width: {item['percentage']}%;"></div>
            </div>
            <span class="traffic-percent">{item['percentage']}%</span>
        </div>
        """
    
    traffic_html += """
        </div>
    </div>
    """
    
    st.markdown(traffic_html, unsafe_allow_html=True)

# ============================================================================
# MAIN DASHBOARD
# ============================================================================

def render_main_dashboard():
    """Render main dashboard matching Pinterest design exactly"""
    
    # Load data
    data = load_executive_data()
    
    # Render sidebar
    render_sidebar()
    
    # Main content area
    st.markdown('<div class="main-content animate-fade-in">', unsafe_allow_html=True)
    
    # Header
    render_header(st.session_state.user)
    
    # KPI Cards
    render_kpi_cards(data['kpi_data'])
    
    # Content Grid (Chart + Right Sidebar)
    st.markdown('<div class="content-grid">', unsafe_allow_html=True)
    
    # Left Column - Main Chart
    st.markdown('<div class="chart-main animate-slide-in">', unsafe_allow_html=True)
    
    # Create and display area chart
    area_fig = create_area_chart(data['area_chart_data'])
    st.plotly_chart(area_fig, use_container_width=True, config={'displayModeBar': False})
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Right Column - Widgets
    st.markdown('<div class="right-sidebar">', unsafe_allow_html=True)
    
    # Donut Chart Widget
    render_donut_widget(data['product_sales'])
    
    # Traffic Source Widget  
    render_traffic_widget(data['traffic_sources'])
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)  # Close content-grid
    
    # Calendar Widget (full width below)
    render_calendar_widget()
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close main-content

def check_authentication() -> bool:
    """Check if user is authenticated"""
    return st.session_state.get('authenticated', False)

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """Main application entry point"""
    
    # Configure page
    configure_executive_page()
    initialize_session_state()
    register_executive_plotly_theme()
    load_executive_css()
    
    # Check authentication
    if not check_authentication():
        render_login_page()
        return
    
    # Handle logout
    if st.session_state.get('logout_requested', False):
        auth_manager = AuthenticationManager()
        auth_manager.logout_user()
        return
    
    # Render main dashboard
    render_main_dashboard()
    
    # Add logout handler in sidebar
    with st.sidebar:
        if st.button("🚪 LOGOUT", key="logout_btn", use_container_width=True):
            st.session_state.logout_requested = True
            st.rerun()

if __name__ == "__main__":
    main()
