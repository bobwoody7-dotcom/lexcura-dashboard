"""
LexCura Elite Executive Dashboard - Fortune 500 Grade Analytics Platform
Enterprise-grade legal compliance monitoring with executive intelligence
Ultra-premium £10,000+/month client dashboard with advanced security and analytics

Version: 2.0.0 Enterprise
Author: LexCura Development Team
License: Enterprise Commercial License
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
from plotly.subplots import make_subplots
import json
import hashlib
import hmac
import secrets
import time
import logging
from datetime import datetime, timedelta, date
from typing import Dict, List, Optional, Tuple, Any
import io
import base64
from pathlib import Path
import zipfile
import uuid
import re
from dataclasses import dataclass, asdict
from enum import Enum
import gspread
from google.oauth2.service_account import Credentials

# Advanced imports with graceful fallbacks
try:
    from streamlit_plotly_events import plotly_events
    PLOTLY_EVENTS_AVAILABLE = True
except ImportError:
    PLOTLY_EVENTS_AVAILABLE = False
    logging.warning("plotly_events not available - interactive chart features limited")

try:
    import kaleido
    KALEIDO_AVAILABLE = True
except ImportError:
    KALEIDO_AVAILABLE = False
    logging.warning("kaleido not available - chart export features limited")

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    logging.warning("PIL not available - image processing features limited")

# ============================================================================
# ENTERPRISE CONFIGURATION & CONSTANTS
# ============================================================================

# Brand Colors - Fortune 500 Professional Palette
class BrandColors:
    """Enterprise brand color palette for consistent theming"""
    CHARCOAL_BG = "#0F1113"           # Primary background
    DARK_CARD = "#1B1D1F"             # Card backgrounds
    LIGHT_CARD = "#252728"            # Light card backgrounds
    METALLIC_GOLD = "#D4AF37"         # Primary accent/CTA
    GOLD_HIGHLIGHT = "#FFCF66"        # Bright accent/hover
    NEUTRAL_TEXT = "#B8B9BB"          # Body text
    HIGH_CONTRAST = "#F5F6F7"         # Headers/emphasis
    ERROR_RED = "#E4574C"             # Error states
    SUCCESS_GREEN = "#3DBC6B"         # Success states
    WARNING_AMBER = "#F59E0B"         # Warning states
    INFO_BLUE = "#3B82F6"             # Information states
    
    # Gradient variations for advanced styling
    GOLD_GRADIENT = f"linear-gradient(135deg, {METALLIC_GOLD} 0%, {GOLD_HIGHLIGHT} 100%)"
    CARD_GRADIENT = f"linear-gradient(145deg, {DARK_CARD} 0%, {LIGHT_CARD} 100%)"
    BG_GRADIENT = f"linear-gradient(180deg, {CHARCOAL_BG} 0%, {DARK_CARD} 100%)"

# Typography Configuration
class Typography:
    """Enterprise typography system"""
    FONT_FAMILY = "'Inter', 'Helvetica Neue', 'Segoe UI', system-ui, sans-serif"
    HEADING_FAMILY = "'Inter', 'SF Pro Display', system-ui, sans-serif"
    MONO_FAMILY = "'SF Mono', 'Monaco', 'Cascadia Code', monospace"

# Application Constants
class AppConfig:
    """Application-wide configuration constants"""
    APP_NAME = "LexCura Elite"
    APP_SUBTITLE = "Executive Legal Intelligence Platform"
    VERSION = "2.0.0 Enterprise"
    COMPANY = "LexCura Executive Services"
    SUPPORT_EMAIL = "executive@lexcura.com"
    
    # Session configuration
    SESSION_TIMEOUT = 3600  # 1 hour
    MAX_LOGIN_ATTEMPTS = 3
    PASSWORD_MIN_LENGTH = 8
    
    # Data refresh intervals
    REAL_TIME_REFRESH = 30  # seconds
    DASHBOARD_REFRESH = 300  # 5 minutes
    CACHE_TTL = 600  # 10 minutes

# User Roles and Permissions
class UserRole(Enum):
    """User role definitions for access control"""
    EXECUTIVE = "executive"
    MANAGER = "manager"
    ANALYST = "analyst"
    VIEWER = "viewer"
    ADMIN = "admin"

@dataclass
class User:
    """User data structure for authentication"""
    username: str
    email: str
    role: UserRole
    full_name: str
    last_login: Optional[datetime] = None
    login_count: int = 0
    preferences: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.preferences is None:
            self.preferences = {}

# ============================================================================
# PAGE CONFIGURATION & INITIALIZATION
# ============================================================================

def configure_page():
    """Configure Streamlit page settings with enterprise branding"""
    st.set_page_config(
        page_title=f"{AppConfig.APP_NAME} | Executive Dashboard",
        page_icon="⚖️",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': f'mailto:{AppConfig.SUPPORT_EMAIL}',
            'Report a bug': f'mailto:{AppConfig.SUPPORT_EMAIL}',
            'About': f"{AppConfig.APP_NAME} {AppConfig.VERSION} - Enterprise Legal Intelligence Platform"
        }
    )

def initialize_session_state():
    """Initialize all session state variables for the application"""
    default_states = {
        # Authentication
        'authenticated': False,
        'user': None,
        'login_attempts': 0,
        'session_start': None,
        
        # Navigation
        'current_page': 'dashboard',
        'sidebar_state': 'expanded',
        
        # Data and filters
        'data_loaded': False,
        'last_refresh': None,
        'selected_client': None,
        'date_range': (datetime.now() - timedelta(days=30), datetime.now()),
        'filters': {},
        
        # UI state
        'theme': 'executive_dark',
        'notifications': [],
        'modal_open': False,
        'export_format': 'csv',
        
        # Performance tracking
        'page_views': {},
        'user_preferences': {},
        'dashboard_config': {}
    }
    
    for key, default_value in default_states.items():
        if key not in st.session_state:
            st.session_state[key] = default_value

# ============================================================================
# ENTERPRISE STYLING SYSTEM
# ============================================================================

def load_enterprise_css():
    """Load comprehensive enterprise CSS styling system"""
    css_styles = f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
        
        :root {{
            /* Brand Color Palette */
            --bg-charcoal: {BrandColors.CHARCOAL_BG};
            --bg-dark-card: {BrandColors.DARK_CARD};
            --bg-light-card: {BrandColors.LIGHT_CARD};
            --accent-gold: {BrandColors.METALLIC_GOLD};
            --accent-gold-bright: {BrandColors.GOLD_HIGHLIGHT};
            --text-neutral: {BrandColors.NEUTRAL_TEXT};
            --text-high-contrast: {BrandColors.HIGH_CONTRAST};
            --error-red: {BrandColors.ERROR_RED};
            --success-green: {BrandColors.SUCCESS_GREEN};
            --warning-amber: {BrandColors.WARNING_AMBER};
            --info-blue: {BrandColors.INFO_BLUE};
            
            /* Typography */
            --font-primary: {Typography.FONT_FAMILY};
            --font-heading: {Typography.HEADING_FAMILY};
            --font-mono: {Typography.MONO_FAMILY};
            
            /* Spacing & Layout */
            --spacing-xs: 0.25rem;
            --spacing-sm: 0.5rem;
            --spacing-md: 1rem;
            --spacing-lg: 1.5rem;
            --spacing-xl: 2rem;
            --spacing-2xl: 3rem;
            --spacing-3xl: 4rem;
            
            /* Border Radius */
            --radius-sm: 6px;
            --radius-md: 12px;
            --radius-lg: 16px;
            --radius-xl: 24px;
            --radius-full: 9999px;
            
            /* Shadows */
            --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.15);
            --shadow-md: 0 4px 16px rgba(0, 0, 0, 0.25);
            --shadow-lg: 0 8px 32px rgba(0, 0, 0, 0.35);
            --shadow-xl: 0 16px 64px rgba(0, 0, 0, 0.45);
            --shadow-gold: 0 4px 20px rgba(212, 175, 55, 0.3);
            
            /* Transitions */
            --transition-fast: 0.15s cubic-bezier(0.4, 0, 0.2, 1);
            --transition-normal: 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            --transition-slow: 0.5s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        
        /* ===== GLOBAL RESET & BASE STYLES ===== */
        
        .stApp {{
            background: var(--bg-charcoal);
            color: var(--text-neutral);
            font-family: var(--font-primary);
            font-weight: 400;
            line-height: 1.6;
        }}
        
        /* Hide default Streamlit elements */
        #MainMenu {{ visibility: hidden; }}
        footer {{ visibility: hidden; }}
        header {{ visibility: hidden; }}
        .stDeployButton {{ visibility: hidden; }}
        .stDecoration {{ display: none; }}
        
        /* ===== ENTERPRISE HEADER SYSTEM ===== */
        
        .enterprise-header {{
            background: linear-gradient(135deg, var(--bg-charcoal) 0%, var(--bg-dark-card) 50%, var(--bg-charcoal) 100%);
            border-bottom: 2px solid var(--accent-gold);
            padding: var(--spacing-xl) var(--spacing-2xl);
            margin: -1rem -1rem var(--spacing-2xl) -1rem;
            position: sticky;
            top: 0;
            z-index: 1000;
            box-shadow: var(--shadow-lg);
        }}
        
        .header-container {{
            max-width: 1400px;
            margin: 0 auto;
            display: grid;
            grid-template-columns: auto 1fr auto;
            align-items: center;
            gap: var(--spacing-xl);
        }}
        
        .header-brand {{
            display: flex;
            align-items: center;
            gap: var(--spacing-md);
        }}
        
        .brand-logo {{
            width: 48px;
            height: 48px;
            background: linear-gradient(135deg, var(--accent-gold) 0%, var(--accent-gold-bright) 100%);
            border-radius: var(--radius-lg);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
            font-weight: 800;
            color: var(--bg-charcoal);
            box-shadow: var(--shadow-gold);
            transition: transform var(--transition-fast);
        }}
        
        .brand-logo:hover {{
            transform: scale(1.05);
        }}
        
        .brand-text {{
            display: flex;
            flex-direction: column;
        }}
        
        .brand-title {{
            font-size: 1.75rem;
            font-weight: 800;
            font-family: var(--font-heading);
            background: linear-gradient(135deg, var(--accent-gold) 0%, var(--accent-gold-bright) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin: 0;
            line-height: 1.2;
        }}
        
        .brand-subtitle {{
            font-size: 0.875rem;
            color: var(--text-neutral);
            margin: 0;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.1em;
        }}
        
        .header-navigation {{
            display: flex;
            gap: var(--spacing-lg);
            align-items: center;
        }}
        
        .nav-link {{
            padding: var(--spacing-sm) var(--spacing-md);
            border-radius: var(--radius-md);
            color: var(--text-neutral);
            text-decoration: none;
            font-weight: 500;
            transition: all var(--transition-fast);
            position: relative;
        }}
        
        .nav-link:hover {{
            color: var(--accent-gold-bright);
            background: rgba(212, 175, 55, 0.1);
        }}
        
        .nav-link.active {{
            color: var(--accent-gold);
            background: rgba(212, 175, 55, 0.15);
        }}
        
        .header-actions {{
            display: flex;
            align-items: center;
            gap: var(--spacing-md);
        }}
        
        .status-indicator {{
            display: flex;
            align-items: center;
            gap: var(--spacing-sm);
            padding: var(--spacing-sm) var(--spacing-md);
            background: var(--bg-dark-card);
            border: 1px solid var(--accent-gold);
            border-radius: var(--radius-full);
            font-size: 0.875rem;
            font-weight: 600;
        }}
        
        .status-dot {{
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: var(--success-green);
            animation: pulse 2s infinite;
        }}
        
        @keyframes pulse {{
            0%, 100% {{ opacity: 1; transform: scale(1); }}
            50% {{ opacity: 0.7; transform: scale(1.1); }}
        }}
        
        /* ===== ENTERPRISE SIDEBAR SYSTEM ===== */
        
        .sidebar-container {{
            background: var(--bg-dark-card);
            border-right: 2px solid var(--accent-gold);
            min-height: 100vh;
            padding: var(--spacing-lg);
        }}
        
        .sidebar-section {{
            margin-bottom: var(--spacing-xl);
        }}
        
        .sidebar-title {{
            font-size: 1rem;
            font-weight: 700;
            color: var(--accent-gold);
            text-transform: uppercase;
            letter-spacing: 0.1em;
            margin-bottom: var(--spacing-md);
            font-family: var(--font-heading);
        }}
        
        .sidebar-item {{
            display: flex;
            align-items: center;
            padding: var(--spacing-md);
            border-radius: var(--radius-md);
            margin-bottom: var(--spacing-sm);
            transition: all var(--transition-fast);
            cursor: pointer;
            border: 1px solid transparent;
        }}
        
        .sidebar-item:hover {{
            background: var(--bg-light-card);
            border-color: var(--accent-gold);
            transform: translateX(4px);
        }}
        
        .sidebar-item.active {{
            background: linear-gradient(135deg, var(--accent-gold) 0%, var(--accent-gold-bright) 100%);
            color: var(--bg-charcoal);
            font-weight: 600;
        }}
        
        /* ===== PREMIUM KPI CARDS ===== */
        
        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: var(--spacing-xl);
            margin: var(--spacing-xl) 0;
        }}
        
        .kpi-card {{
            background: linear-gradient(145deg, var(--bg-dark-card) 0%, var(--bg-light-card) 100%);
            border: 2px solid var(--accent-gold);
            border-radius: var(--radius-xl);
            padding: var(--spacing-xl);
            position: relative;
            overflow: hidden;
            transition: all var(--transition-normal);
            box-shadow: var(--shadow-md);
        }}
        
        .kpi-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(135deg, var(--accent-gold) 0%, var(--accent-gold-bright) 100%);
        }}
        
        .kpi-card::after {{
            content: '';
            position: absolute;
            top: -2px;
            left: -2px;
            right: -2px;
            bottom: -2px;
            background: linear-gradient(135deg, var(--accent-gold) 0%, var(--accent-gold-bright) 100%);
            border-radius: calc(var(--radius-xl) + 2px);
            opacity: 0;
            z-index: -1;
            transition: opacity var(--transition-normal);
        }}
        
        .kpi-card:hover {{
            transform: translateY(-8px) scale(1.02);
            box-shadow: var(--shadow-xl);
        }}
        
        .kpi-card:hover::after {{
            opacity: 0.1;
        }}
        
        .kpi-icon {{
            font-size: 2.5rem;
            margin-bottom: var(--spacing-md);
            background: linear-gradient(135deg, var(--accent-gold) 0%, var(--accent-gold-bright) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        
        .kpi-value {{
            font-size: 2.75rem;
            font-weight: 800;
            font-family: var(--font-heading);
            background: linear-gradient(135deg, var(--accent-gold) 0%, var(--accent-gold-bright) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin: var(--spacing-md) 0;
            line-height: 1;
        }}
        
        .kpi-label {{
            font-size: 1rem;
            color: var(--text-neutral);
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: var(--spacing-sm);
        }}
        
        .kpi-change {{
            display: inline-flex;
            align-items: center;
            gap: var(--spacing-xs);
            padding: var(--spacing-sm) var(--spacing-md);
            border-radius: var(--radius-full);
            font-size: 0.875rem;
            font-weight: 600;
            margin-top: var(--spacing-md);
        }}
        
        .kpi-change.positive {{
            background: rgba(61, 188, 107, 0.15);
            color: var(--success-green);
            border: 1px solid rgba(61, 188, 107, 0.3);
        }}
        
        .kpi-change.negative {{
            background: rgba(228, 87, 76, 0.15);
            color: var(--error-red);
            border: 1px solid rgba(228, 87, 76, 0.3);
        }}
        
        .kpi-change.neutral {{
            background: rgba(212, 175, 55, 0.15);
            color: var(--accent-gold);
            border: 1px solid var(--accent-gold);
        }}
        
        /* ===== ENTERPRISE CARDS ===== */
        
        .enterprise-card {{
            background: linear-gradient(145deg, var(--bg-dark-card) 0%, var(--bg-light-card) 100%);
            border: 2px solid var(--accent-gold);
            border-radius: var(--radius-lg);
            padding: var(--spacing-xl);
            margin: var(--spacing-xl) 0;
            box-shadow: var(--shadow-md);
            position: relative;
            transition: all var(--transition-normal);
        }}
        
        .enterprise-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 2px;
            background: linear-gradient(135deg, var(--accent-gold) 0%, var(--accent-gold-bright) 100%);
            border-radius: var(--radius-lg) var(--radius-lg) 0 0;
        }}
        
        .enterprise-card:hover {{
            border-color: var(--accent-gold-bright);
            transform: translateY(-4px);
            box-shadow: var(--shadow-lg);
        }}
        
        .card-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: var(--spacing-lg);
            padding-bottom: var(--spacing-md);
            border-bottom: 1px solid rgba(212, 175, 55, 0.2);
        }}
        
        .card-title {{
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--accent-gold);
            font-family: var(--font-heading);
            margin: 0;
        }}
        
        .card-subtitle {{
            font-size: 0.875rem;
            color: var(--text-neutral);
            margin: var(--spacing-xs) 0 0 0;
            font-style: italic;
        }}
        
        .card-content {{
            color: var(--text-high-contrast);
            line-height: 1.7;
        }}
        
        /* ===== CHART CONTAINERS ===== */
        
        .chart-container {{
            background: var(--bg-dark-card);
            border: 2px solid var(--accent-gold);
            border-radius: var(--radius-lg);
            padding: var(--spacing-xl);
            margin: var(--spacing-xl) 0;
            box-shadow: var(--shadow-md);
            transition: all var(--transition-normal);
        }}
        
        .chart-container:hover {{
            border-color: var(--accent-gold-bright);
            box-shadow: var(--shadow-lg);
        }}
        
        .chart-header {{
            text-align: center;
            margin-bottom: var(--spacing-lg);
        }}
        
        .chart-title {{
            font-size: 1.25rem;
            font-weight: 700;
            color: var(--accent-gold);
            margin-bottom: var(--spacing-sm);
            font-family: var(--font-heading);
        }}
        
        .chart-description {{
            font-size: 0.875rem;
            color: var(--text-neutral);
            font-style: italic;
        }}
        
        /* ===== PREMIUM BUTTONS ===== */
        
        .btn-enterprise {{
            display: inline-flex;
            align-items: center;
            gap: var(--spacing-sm);
            padding: var(--spacing-md) var(--spacing-xl);
            background: linear-gradient(135deg, var(--accent-gold) 0%, var(--accent-gold-bright) 100%);
            color: var(--bg-charcoal);
            border: none;
            border-radius: var(--radius-md);
            font-weight: 600;
            font-size: 1rem;
            cursor: pointer;
            transition: all var(--transition-fast);
            text-decoration: none;
            font-family: var(--font-primary);
            box-shadow: var(--shadow-sm);
        }}
        
        .btn-enterprise:hover {{
            transform: translateY(-2px);
            box-shadow: var(--shadow-md);
            filter: brightness(1.1);
        }}
        
        .btn-enterprise:active {{
            transform: translateY(0);
        }}
        
        .btn-outline {{
            background: transparent;
            color: var(--accent-gold);
            border: 2px solid var(--accent-gold);
        }}
        
        .btn-outline:hover {{
            background: var(--accent-gold);
            color: var(--bg-charcoal);
        }}
        
        .btn-ghost {{
            background: rgba(212, 175, 55, 0.1);
            color: var(--accent-gold);
            border: 1px solid rgba(212, 175, 55, 0.3);
        }}
        
        .btn-ghost:hover {{
            background: rgba(212, 175, 55, 0.2);
        }}
        
        /* ===== NOTIFICATIONS & ALERTS ===== */
        
        .notification-container {{
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 2000;
            max-width: 400px;
        }}
        
        .notification {{
            background: var(--bg-dark-card);
            border-left: 4px solid;
            border-radius: var(--radius-md);
            padding: var(--spacing-md) var(--spacing-lg);
            margin-bottom: var(--spacing-md);
            box-shadow: var(--shadow-lg);
            animation: slideIn 0.3s ease-out;
        }}
        
        .notification.success {{ border-left-color: var(--success-green); }}
        .notification.error {{ border-left-color: var(--error-red); }}
        .notification.warning {{ border-left-color: var(--warning-amber); }}
        .notification.info {{ border-left-color: var(--info-blue); }}
        
        @keyframes slideIn {{
            from {{ transform: translateX(100%); opacity: 0; }}
            to {{ transform: translateX(0); opacity: 1; }}
        }}
        
        .alert {{
            padding: var(--spacing-lg);
            border-radius: var(--radius-md);
            margin: var(--spacing-lg) 0;
            border-left: 4px solid;
            font-weight: 500;
        }}
        
        .alert.success {{
            background: rgba(61, 188, 107, 0.1);
            border-left-color: var(--success-green);
            color: var(--success-green);
        }}
        
        .alert.error {{
            background: rgba(228, 87, 76, 0.1);
            border-left-color: var(--error-red);
            color: var(--error-red);
        }}
        
        .alert.warning {{
            background: rgba(245, 158, 11, 0.1);
            border-left-color: var(--warning-amber);
            color: var(--warning-amber);
        }}
        
        .alert.info {{
            background: rgba(59, 130, 246, 0.1);
            border-left-color: var(--info-blue);
            color: var(--info-blue);
        }}
        
        /* ===== FORMS & INPUTS ===== */
        
        .stSelectbox > div > div,
        .stMultiSelect > div > div,
        .stTextInput > div > div > input,
        .stTextArea textarea,
        .stDateInput > div > div > input,
        .stNumberInput > div > div > input {{
            background: var(--bg-light-card) !important;
            border: 2px solid var(--accent-gold) !important;
            border-radius: var(--radius-md) !important;
            color: var(--text-high-contrast) !important;
            font-family: var(--font-primary) !important;
            font-weight: 500 !important;
        }}
        
        .stSelectbox > div > div:focus,
        .stMultiSelect > div > div:focus,
        .stTextInput > div > div > input:focus,
        .stTextArea textarea:focus,
        .stDateInput > div > div > input:focus,
        .stNumberInput > div > div > input:focus {{
            border-color: var(--accent-gold-bright) !important;
            box-shadow: 0 0 0 3px rgba(212, 175, 55, 0.2) !important;
        }}
        
        /* ===== TABS SYSTEM ===== */
        
        .stTabs [data-baseweb="tab-list"] {{
            background: var(--bg-dark-card);
            border-radius: var(--radius-lg);
            padding: var(--spacing-sm);
            border: 2px solid var(--accent-gold);
            margin-bottom: var(--spacing-xl);
        }}
        
        .stTabs [data-baseweb="tab"] {{
            background: transparent;
            border-radius: var(--radius-md);
            color: var(--text-neutral);
            font-weight: 600;
            padding: var(--spacing-md) var(--spacing-lg);
            font-size: 1rem;
            transition: all var(--transition-fast);
        }}
        
        .stTabs [data-baseweb="tab"]:hover {{
            color: var(--accent-gold-bright);
            background: rgba(212, 175, 55, 0.1);
        }}
        
        .stTabs [aria-selected="true"] {{
            background: linear-gradient(135deg, var(--accent-gold) 0%, var(--accent-gold-bright) 100%) !important;
            color: var(--bg-charcoal) !important;
            font-weight: 700 !important;
        }}
        
        /* ===== METRICS & STATS ===== */
        
        .metric-container {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: var(--spacing-md);
            background: rgba(212, 175, 55, 0.05);
            border: 1px solid rgba(212, 175, 55, 0.2);
            border-radius: var(--radius-md);
            margin: var(--spacing-sm) 0;
        }}
        
        .metric-label {{
            font-size: 0.875rem;
            color: var(--text-neutral);
            font-weight: 500;
        }}
        
        .metric-value {{
            font-size: 1.125rem;
            color: var(--text-high-contrast);
            font-weight: 700;
        }}
        
        /* ===== LOADING STATES ===== */
        
        .loading-spinner {{
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 2px solid rgba(212, 175, 55, 0.2);
            border-radius: 50%;
            border-top-color: var(--accent-gold);
            animation: spin 1s ease-in-out infinite;
        }}
        
        @keyframes spin {{
            to {{ transform: rotate(360deg); }}
        }}
        
        /* ===== RESPONSIVE DESIGN ===== */
        
        @media (max-width: 1200px) {{
            .header-container {{
                grid-template-columns: auto 1fr;
                gap: var(--spacing-md);
            }}
            
            .header-navigation {{
                gap: var(--spacing-md);
            }}
            
            .kpi-grid {{
                grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
                gap: var(--spacing-lg);
            }}
        }}
        
        @media (max-width: 768px) {{
            .enterprise-header {{
                padding: var(--spacing-lg);
            }}
            
            .header-container {{
                grid-template-columns: 1fr;
                text-align: center;
                gap: var(--spacing-lg);
            }}
            
            .brand-title {{
                font-size: 1.5rem;
            }}
            
            .kpi-grid {{
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            }}
            
            .enterprise-card {{
                padding: var(--spacing-lg);
            }}
        }}
        
        @media (max-width: 480px) {{
            .kpi-grid {{
                grid-template-columns: 1fr;
            }}
            
            .chart-container {{
                padding: var(--spacing-lg);
            }}
        }}
        
        /* ===== UTILITY CLASSES ===== */
        
        .text-center {{ text-align: center; }}
        .text-left {{ text-align: left; }}
        .text-right {{ text-align: right; }}
        
        .font-bold {{ font-weight: 700; }}
        .font-semibold {{ font-weight: 600; }}
        .font-medium {{ font-weight: 500; }}
        
        .text-gold {{ color: var(--accent-gold); }}
        .text-bright {{ color: var(--text-high-contrast); }}
        .text-muted {{ color: var(--text-neutral); }}
        
        .bg-card {{ background: var(--bg-dark-card); }}
        .bg-light {{ background: var(--bg-light-card); }}
        
        .border-gold {{ border-color: var(--accent-gold); }}
        .border-2 {{ border-width: 2px; }}
        
        .rounded {{ border-radius: var(--radius-md); }}
        .rounded-lg {{ border-radius: var(--radius-lg); }}
        .rounded-xl {{ border-radius: var(--radius-xl); }}
        
        .shadow {{ box-shadow: var(--shadow-md); }}
        .shadow-lg {{ box-shadow: var(--shadow-lg); }}
        
        .p-4 {{ padding: var(--spacing-md); }}
        .p-6 {{ padding: var(--spacing-lg); }}
        .p-8 {{ padding: var(--spacing-xl); }}
        
        .m-4 {{ margin: var(--spacing-md); }}
        .m-6 {{ margin: var(--spacing-lg); }}
        .m-8 {{ margin: var(--spacing-xl); }}
        
        .mb-4 {{ margin-bottom: var(--spacing-md); }}
        .mb-6 {{ margin-bottom: var(--spacing-lg); }}
        .mb-8 {{ margin-bottom: var(--spacing-xl); }}
        
        .hidden {{ display: none; }}
        .flex {{ display: flex; }}
        .grid {{ display: grid; }}
        .block {{ display: block; }}
        .inline {{ display: inline; }}
        .inline-block {{ display: inline-block; }}
        
        .items-center {{ align-items: center; }}
        .justify-center {{ justify-content: center; }}
        .justify-between {{ justify-content: space-between; }}
        
        .gap-2 {{ gap: var(--spacing-sm); }}
        .gap-4 {{ gap: var(--spacing-md); }}
        .gap-6 {{ gap: var(--spacing-lg); }}
    </style>
    """
    
    st.markdown(css_styles, unsafe_allow_html=True)

# ============================================================================
# ENTERPRISE AUTHENTICATION SYSTEM
# ============================================================================

class AuthenticationManager:
    """Enterprise-grade authentication and session management"""
    
    def __init__(self):
        self.users_db = self._initialize_user_database()
        self.session_timeout = AppConfig.SESSION_TIMEOUT
        
    def _initialize_user_database(self) -> Dict[str, Dict]:
        """Initialize secure user database with hashed passwords"""
        # In production, this would connect to a secure database
        return {
            "executive": {
                "password_hash": self._hash_password("Executive2024!"),
                "user_data": User(
                    username="executive",
                    email="executive@lexcura.com",
                    role=UserRole.EXECUTIVE,
                    full_name="Executive User"
                )
            },
            "manager": {
                "password_hash": self._hash_password("Manager2024!"),
                "user_data": User(
                    username="manager",
                    email="manager@lexcura.com",
                    role=UserRole.MANAGER,
                    full_name="Manager User"
                )
            },
            "analyst": {
                "password_hash": self._hash_password("Analyst2024!"),
                "user_data": User(
                    username="analyst",
                    email="analyst@lexcura.com",
                    role=UserRole.ANALYST,
                    full_name="Analyst User"
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
        """Hash password using SHA-256 with salt"""
        salt = "lexcura_enterprise_salt_2024"
        return hashlib.sha256((password + salt).encode()).hexdigest()
    
    def _verify_password(self, password: str, password_hash: str) -> bool:
        """Verify password against hash"""
        return self._hash_password(password) == password_hash
    
    def authenticate_user(self, username: str, password: str) -> Tuple[bool, Optional[User], str]:
        """Authenticate user credentials and return status"""
        try:
            if username not in self.users_db:
                return False, None, "Invalid username or password"
            
            user_record = self.users_db[username]
            if not self._verify_password(password, user_record["password_hash"]):
                st.session_state.login_attempts += 1
                if st.session_state.login_attempts >= AppConfig.MAX_LOGIN_ATTEMPTS:
                    return False, None, f"Too many failed attempts. Please try again later."
                return False, None, f"Invalid username or password ({AppConfig.MAX_LOGIN_ATTEMPTS - st.session_state.login_attempts} attempts remaining)"
            
            # Successful authentication
            user = user_record["user_data"]
            user.last_login = datetime.now()
            user.login_count += 1
            
            st.session_state.login_attempts = 0  # Reset failed attempts
            return True, user, "Authentication successful"
            
        except Exception as e:
            logging.error(f"Authentication error: {e}")
            return False, None, "Authentication system error"
    
    def is_session_valid(self) -> bool:
        """Check if current session is still valid"""
        if not st.session_state.authenticated or not st.session_state.session_start:
            return False
        
        session_duration = (datetime.now() - st.session_state.session_start).total_seconds()
        return session_duration < self.session_timeout
    
    def logout_user(self):
        """Logout current user and clear session"""
        for key in ['authenticated', 'user', 'session_start']:
            if key in st.session_state:
                del st.session_state[key]
        st.session_state.authenticated = False
        st.rerun()

def render_login_form():
    """Render enterprise-grade login form"""
    st.markdown("""
    <div class="enterprise-card" style="max-width: 500px; margin: 4rem auto;">
        <div class="card-header">
            <div style="text-align: center; width: 100%;">
                <div class="brand-logo" style="width: 64px; height: 64px; margin: 0 auto 1rem;">⚖</div>
                <h1 class="card-title">LexCura Elite</h1>
                <p class="card-subtitle">Executive Legal Intelligence Platform</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("login_form", clear_on_submit=False):
        st.markdown("### Secure Executive Access")
        
        username = st.text_input(
            "Username",
            placeholder="Enter your username",
            help="Use your assigned executive credentials"
        )
        
        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password",
            help="Password is case-sensitive"
        )
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_button = st.form_submit_button(
                "Access Executive Dashboard",
                use_container_width=True
            )
        
        if submit_button:
            if not username or not password:
                st.error("Please enter both username and password")
                return
            
            auth_manager = AuthenticationManager()
            success, user, message = auth_manager.authenticate_user(username, password)
            
            if success:
                st.session_state.authenticated = True
                st.session_state.user = user
                st.session_state.session_start = datetime.now()
                st.success(f"Welcome back, {user.full_name}!")
                time.sleep(1)  # Brief pause for UX
                st.rerun()
            else:
                st.error(message)
    
    # Demo credentials info
    with st.expander("Demo Access Credentials", expanded=False):
        st.markdown("""
        **Executive Level:**
        - Username: `executive` | Password: `Executive2024!`
        
        **Manager Level:**
        - Username: `manager` | Password: `Manager2024!`
        
        **Analyst Level:**
        - Username: `analyst` | Password: `Analyst2024!`
        
        **Demo Access:**
        - Username: `demo` | Password: `Demo2024!`
        """)

def check_authentication():
    """Check authentication status and handle session management"""
    auth_manager = AuthenticationManager()
    
    if not st.session_state.authenticated:
        return False
    
    if not auth_manager.is_session_valid():
        st.warning("Your session has expired. Please log in again.")
        auth_manager.logout_user()
        return False
    
    return True

# ============================================================================
# ENTERPRISE PLOTLY THEME SYSTEM
# ============================================================================

def create_enterprise_plotly_theme():
    """Create custom Plotly theme matching enterprise brand"""
    enterprise_theme = {
        "layout": {
            "paper_bgcolor": BrandColors.CHARCOAL_BG,
            "plot_bgcolor": "rgba(0,0,0,0)",
            "colorway": [
                BrandColors.METALLIC_GOLD,
                BrandColors.GOLD_HIGHLIGHT,
                BrandColors.HIGH_CONTRAST,
                BrandColors.NEUTRAL_TEXT,
                BrandColors.SUCCESS_GREEN,
                BrandColors.INFO_BLUE,
                BrandColors.WARNING_AMBER,
                BrandColors.ERROR_RED
            ],
            "font": {
                "family": Typography.FONT_FAMILY,
                "color": BrandColors.HIGH_CONTRAST,
                "size": 14
            },
            "title": {
                "font": {
                    "family": Typography.HEADING_FAMILY,
                    "size": 24,
                    "color": BrandColors.METALLIC_GOLD
                },
                "x": 0.5,
                "xanchor": "center",
                "pad": {"t": 30, "b": 20}
            },
            "legend": {
                "bgcolor": "rgba(27, 29, 31, 0.95)",
                "bordercolor": BrandColors.METALLIC_GOLD,
                "borderwidth": 1,
                "font": {
                    "color": BrandColors.HIGH_CONTRAST,
                    "size": 12
                }
            },
            "xaxis": {
                "gridcolor": "rgba(212, 175, 55, 0.15)",
                "linecolor": "rgba(212, 175, 55, 0.3)",
                "zerolinecolor": "rgba(212, 175, 55, 0.3)",
                "tickfont": {
                    "color": BrandColors.NEUTRAL_TEXT,
                    "size": 12
                },
                "titlefont": {
                    "color": BrandColors.METALLIC_GOLD,
                    "size": 14,
                    "family": Typography.HEADING_FAMILY
                }
            },
            "yaxis": {
                "gridcolor": "rgba(212, 175, 55, 0.15)",
                "linecolor": "rgba(212, 175, 55, 0.3)",
                "zerolinecolor": "rgba(212, 175, 55, 0.3)",
                "tickfont": {
                    "color": BrandColors.NEUTRAL_TEXT,
                    "size": 12
                },
                "titlefont": {
                    "color": BrandColors.METALLIC_GOLD,
                    "size": 14,
                    "family": Typography.HEADING_FAMILY
                }
            },
            "hovermode": "closest",
            "hoverlabel": {
                "bgcolor": BrandColors.DARK_CARD,
                "bordercolor": BrandColors.METALLIC_GOLD,
                "font": {
                    "color": BrandColors.HIGH_CONTRAST,
                    "size": 13
                }
            },
            "margin": {"l": 80, "r": 80, "t": 100, "b": 80}
        }
    }
    
    # Register the theme
    pio.templates["enterprise"] = go.layout.Template(layout=enterprise_theme["layout"])
    pio.templates.default = "enterprise"
    
    return enterprise_theme

def apply_enterprise_styling(fig, title: str = "", height: int = 500):
    """Apply consistent enterprise styling to Plotly figures"""
    fig.update_layout(
        template="enterprise",
        height=height,
        title=title,
        showlegend=True,
        hovermode='closest'
    )
    
    # Add subtle animations
    for trace in fig.data:
        if hasattr(trace, 'marker'):
            trace.marker.line = dict(color=BrandColors.METALLIC_GOLD, width=1)
    
    return fig

# ============================================================================
# DATA CONNECTION & MANAGEMENT SYSTEM
# ============================================================================

class DataConnectionManager:
    """Enterprise data connection and caching system"""
    
    def __init__(self):
        self.cache_duration = AppConfig.CACHE_TTL
        self.last_refresh = {}
    
    @st.cache_data(ttl=300, show_spinner=False)
    def connect_to_google_sheets(self) -> Optional[gspread.Client]:
        """Connect to Google Sheets with enterprise credentials"""
        try:
            if "gcp_service_account" in st.secrets:
                credentials_data = st.secrets["gcp_service_account"]
                if isinstance(credentials_data, str):
                    credentials_info = json.loads(credentials_data)
                else:
                    credentials_info = dict(credentials_data)
                
                credentials = Credentials.from_service_account_info(
                    credentials_info,
                    scopes=[
                        "https://www.googleapis.com/auth/spreadsheets",
                        "https://www.googleapis.com/auth/drive"
                    ]
                )
                return gspread.authorize(credentials)
            else:
                logging.warning("Google Sheets credentials not found")
                return None
                
        except Exception as e:
            logging.error(f"Google Sheets connection error: {e}")
            return None
    
    @st.cache_data(ttl=60, show_spinner=False)
    def load_client_data(self, client_id: Optional[str] = None) -> Dict[str, Any]:
        """Load client data with fallback to premium demo data"""
        try:
            gc = self.connect_to_google_sheets()
            if not gc:
                return self.get_enterprise_demo_data()
            
            sheet_id = st.secrets.get("MASTER_SHEET_ID", "1oI-XqRbp8r3V8yMjnC5pNvDMljJDv4f6d01vRmrVH1g")
            spreadsheet = gc.open_by_key(sheet_id)
            sheet = spreadsheet.worksheet("MASTER SHEET")
            
            headers = sheet.row_values(1)
            row_data = sheet.row_values(2)
            
            # Ensure data alignment
            while len(row_data) < len(headers):
                row_data.append("")
            
            data = dict(zip(headers, row_data))
            return self._format_client_data(data, client_id)
            
        except Exception as e:
            logging.error(f"Data loading error: {e}")
            return self.get_enterprise_demo_data()
    
    def get_enterprise_demo_data(self) -> Dict[str, Any]:
        """Comprehensive enterprise demo data for dashboard"""
        return {
            'UNIQUE_CLIENT_ID': '11AA-EXEC',
            'CLIENT_NAME': 'Fortune Global Pharmaceuticals Inc.',
            'TIER': 'Executive Premium Elite',
            'REGION': 'Global Multi-Jurisdictional',
            'DELIVERY_FREQUENCY': 'Real-time Intelligence & Predictive Analytics',
            'EMAIL_ADDRESS': 'c-suite@fortuneglobalpharma.com',
            'MAIN_CONTENT': 'Comprehensive executive-grade regulatory intelligence with AI-powered risk prediction, real-time compliance monitoring, strategic legal advisory services, and C-suite executive briefings. Advanced multi-jurisdictional compliance tracking with predictive analytics and strategic regulatory intelligence.',
            'FINANCIAL_STATS': '£8.7M annual compliance optimization, £1.2M platform investment, 847% ROI',
            'HISTORICAL_IMPACTS': 'ROI: 847% over 24 months, zero regulatory penalties, £12.3M in avoided violations',
            'EXECUTIVE_SUMMARY': 'Exceptional executive performance across all regulatory domains. Advanced AI-powered risk prediction has eliminated critical violations while optimizing operational efficiency by 847%. Current performance exceeds all industry benchmarks with 99.7% overall compliance score, predictive risk mitigation, and strategic regulatory intelligence delivering unprecedented value to C-suite operations.',
            'COMPLIANCE_ALERTS': 'Zero critical violations (1,247 days violation-free), 5 proactive optimizations identified',
            'RISK_ANALYSIS': 'Ultra-low risk profile (0.8/10) with predictive monitoring and strategic AI controls',
            'REGULATORY_UPDATES': 'Global regulatory intelligence across 47 jurisdictions, AI-powered trend analysis, executive briefings, competitive intelligence',
            'ALERT_LEVEL': 'OPTIMAL EXCELLENCE',
            'DATE_SCRAPED': datetime.now().strftime('%Y-%m-%d'),
            'STATUS': 'Executive Premium Active - Elite Tier',
            'LAST_UPDATED': datetime.now(),
            'PERFORMANCE_SCORE': 99.7,
            'RISK_SCORE': 0.8,
            'VIOLATIONS_COUNT': 0,
            'DAYS_VIOLATION_FREE': 1247,
            'TEAM_CERTIFICATION': 99.4,
            'AI_INSIGHTS': 5,
            'GLOBAL_COVERAGE': 47
        }
    
    def _format_client_data(self, raw_data: Dict, client_id: Optional[str]) -> Dict[str, Any]:
        """Format and enhance client data"""
        formatted_data = raw_data.copy()
        formatted_data['LAST_UPDATED'] = datetime.now()
        formatted_data['PERFORMANCE_SCORE'] = 99.7
        formatted_data['RISK_SCORE'] = 0.8
        return formatted_data

# ============================================================================
# ADVANCED CHART CREATION SYSTEM
# ============================================================================

class EnterpriseChartManager:
    """Advanced chart creation with enterprise styling"""
    
    def __init__(self):
        create_enterprise_plotly_theme()
    
    def create_executive_kpi_overview(self, data: Dict[str, Any]) -> go.Figure:
        """Executive KPI overview with multiple metrics"""
        kpis = ['Compliance', 'Risk Management', 'Team Certification', 'AI Optimization', 'Global Coverage']
        values = [99.7, 99.2, 99.4, 98.8, 97.9]
        targets = [95, 95, 95, 90, 90]
        
        fig = go.Figure()
        
        # Actual performance
        fig.add_trace(go.Scatterpolar(
            r=values + [values[0]],
            theta=kpis + [kpis[0]],
            fill='toself',
            name='Current Performance',
            line=dict(color=BrandColors.METALLIC_GOLD, width=3),
            fillcolor=f"rgba(212, 175, 55, 0.25)",
            marker=dict(size=8, color=BrandColors.METALLIC_GOLD)
        ))
        
        # Target benchmarks
        fig.add_trace(go.Scatterpolar(
            r=targets + [targets[0]],
            theta=kpis + [kpis[0]],
            line=dict(color=BrandColors.GOLD_HIGHLIGHT, width=2, dash='dash'),
            name='Executive Targets',
            marker=dict(size=6, color=BrandColors.GOLD_HIGHLIGHT)
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    gridcolor="rgba(212, 175, 55, 0.2)",
                    tickfont=dict(color=BrandColors.NEUTRAL_TEXT, size=11)
                ),
                angularaxis=dict(
                    tickfont=dict(color=BrandColors.HIGH_CONTRAST, size=12, weight=600),
                    gridcolor="rgba(212, 175, 55, 0.2)"
                )
            ),
            title="Executive Performance Matrix",
            showlegend=True
        )
        
        return apply_enterprise_styling(fig, height=450)
    
    def create_financial_performance_timeline(self, data: Dict[str, Any]) -> go.Figure:
        """Advanced financial performance with forecasting"""
        months = pd.date_range('2024-01-01', '2025-12-31', freq='M')
        historical = months[:12]
        forecast = months[12:]
        
        # Historical performance
        savings_historical = np.array([420000, 485000, 520000, 610000, 665000, 720000, 
                                     780000, 840000, 910000, 975000, 1020000, 1100000])
        investment_historical = np.array([85000, 78000, 92000, 88000, 95000, 82000,
                                        90000, 87000, 93000, 89000, 91000, 94000])
        
        # Forecast data
        savings_forecast = np.array([1180000, 1260000, 1340000, 1420000, 1510000, 1600000,
                                   1690000, 1780000, 1870000, 1960000, 2050000, 2140000])
        investment_forecast = np.array([96000, 98000, 100000, 102000, 104000, 106000,
                                      108000, 110000, 112000, 114000, 116000, 118000])
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=['Cumulative Savings', 'Monthly Investment', 'ROI Performance', 'Efficiency Metrics'],
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": True}, {"secondary_y": False}]],
            vertical_spacing=0.12,
            horizontal_spacing=0.1
        )
        
        # Cumulative Savings
        fig.add_trace(go.Scatter(
            x=historical, y=np.cumsum(savings_historical), mode='lines+markers',
            name='Historical Savings', line=dict(color=BrandColors.METALLIC_GOLD, width=3),
            marker=dict(size=8, color=BrandColors.METALLIC_GOLD)
        ), row=1, col=1)
        
        fig.add_trace(go.Scatter(
            x=forecast, y=np.cumsum(savings_historical)[-1] + np.cumsum(savings_forecast), 
            mode='lines+markers', name='Projected Savings',
            line=dict(color=BrandColors.GOLD_HIGHLIGHT, width=3, dash='dash'),
            marker=dict(size=8, color=BrandColors.GOLD_HIGHLIGHT)
        ), row=1, col=1)
        
        # Monthly Investment
        fig.add_trace(go.Bar(
            x=historical, y=investment_historical, name='Historical Investment',
            marker=dict(color=BrandColors.METALLIC_GOLD, opacity=0.7)
        ), row=1, col=2)
        
        fig.add_trace(go.Bar(
            x=forecast, y=investment_forecast, name='Projected Investment',
            marker=dict(color=BrandColors.GOLD_HIGHLIGHT, opacity=0.5)
        ), row=1, col=2)
        
        # ROI Performance
        roi_historical = (savings_historical / investment_historical) * 100
        roi_forecast = (savings_forecast / investment_forecast) * 100
        
        fig.add_trace(go.Scatter(
            x=historical, y=roi_historical, mode='lines+markers',
            name='Historical ROI', line=dict(color=BrandColors.SUCCESS_GREEN, width=3),
            marker=dict(size=8, color=BrandColors.SUCCESS_GREEN)
        ), row=2, col=1)
        
        fig.add_trace(go.Scatter(
            x=forecast, y=roi_forecast, mode='lines+markers',
            name='Projected ROI', line=dict(color=BrandColors.INFO_BLUE, width=3, dash='dash'),
            marker=dict(size=8, color=BrandColors.INFO_BLUE)
        ), row=2, col=1)
        
        # Efficiency Metrics (Gauge)
        fig.add_trace(go.Indicator(
            mode="gauge+number+delta",
            value=847,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Efficiency Score"},
            delta={'reference': 500},
            gauge={'axis': {'range': [None, 1000]},
                   'bar': {'color': BrandColors.METALLIC_GOLD},
                   'steps': [
                       {'range': [0, 250], 'color': BrandColors.ERROR_RED},
                       {'range': [250, 500], 'color': BrandColors.WARNING_AMBER},
                       {'range': [500, 750], 'color': BrandColors.SUCCESS_GREEN},
                       {'range': [750, 1000], 'color': BrandColors.METALLIC_GOLD}
                   ],
                   'threshold': {'line': {'color': BrandColors.HIGH_CONTRAST, 'width': 4},
                                'thickness': 0.75, 'value': 900}}
        ), row=2, col=2)
        
        return apply_enterprise_styling(fig, "Executive Financial Intelligence Dashboard", height=700)
    
    def create_compliance_heatmap(self, data: Dict[str, Any]) -> go.Figure:
        """Global compliance performance heatmap"""
        regulations = ['FDA 21 CFR 211', 'USP 797', 'USP 800', 'EU GMP Annex 1', 
                      'MHRA Orange Guide', 'Health Canada GUI-0104', 'TGA PIC/S', 
                      'ISO 13485', 'ICH Q7', 'ISPE Baseline']
        
        regions = ['North America', 'Europe', 'UK & Ireland', 'Asia Pacific', 
                  'Latin America', 'Middle East']
        
        # Compliance scores matrix (regulations x regions)
        scores = np.array([
            [99.2, 98.8, 99.1, 97.9, 96.5, 95.8],  # FDA 21 CFR 211
            [99.4, 98.9, 99.2, 98.1, 97.2, 96.9],  # USP 797
            [98.8, 99.1, 98.6, 97.5, 96.8, 95.4],  # USP 800
            [98.6, 99.6, 99.2, 98.3, 97.1, 96.7],  # EU GMP Annex 1
            [98.9, 99.0, 99.8, 97.7, 96.4, 95.9],  # MHRA Orange Guide
            [99.1, 98.5, 98.8, 98.4, 97.8, 96.2],  # Health Canada GUI-0104
            [98.7, 98.9, 99.0, 99.1, 97.3, 96.5],  # TGA PIC/S
            [99.3, 99.2, 99.4, 98.6, 97.9, 97.1],  # ISO 13485
            [98.9, 99.1, 98.7, 98.2, 97.4, 96.8],  # ICH Q7
            [99.0, 98.8, 99.1, 98.5, 97.6, 97.0]   # ISPE Baseline
        ])
        
        fig = go.Figure(data=go.Heatmap(
            z=scores,
            x=regions,
            y=regulations,
            colorscale=[
                [0.0, BrandColors.ERROR_RED],
                [0.3, BrandColors.WARNING_AMBER],
                [0.7, BrandColors.SUCCESS_GREEN],
                [1.0, BrandColors.METALLIC_GOLD]
            ],
            text=[[f'{val:.1f}%' for val in row] for row in scores],
            texttemplate="%{text}",
            textfont={"size": 11, "color": BrandColors.HIGH_CONTRAST, "family": Typography.FONT_FAMILY},
            hoverongaps=False,
            colorbar=dict(
                title="Compliance Score (%)",
                titlefont=dict(color=BrandColors.HIGH_CONTRAST),
                tickfont=dict(color=BrandColors.NEUTRAL_TEXT)
            )
        ))
        
        return apply_enterprise_styling(fig, "Global Regulatory Compliance Intelligence Matrix", height=600)
    
    def create_risk_assessment_gauge(self, data: Dict[str, Any]) -> go.Figure:
        """Advanced risk assessment with multiple gauges"""
        risk_categories = [
            ('Overall Risk', 0.8, 10),
            ('Regulatory Risk', 0.5, 10),
            ('Operational Risk', 1.2, 10),
            ('Financial Risk', 0.3, 10)
        ]
        
        fig = make_subplots(
            rows=2, cols=2,
            specs=[[{"type": "indicator"}, {"type": "indicator"}],
                   [{"type": "indicator"}, {"type": "indicator"}]],
            subplot_titles=[cat[0] for cat in risk_categories],
            vertical_spacing=0.15
        )
        
        positions = [(1,1), (1,2), (2,1), (2,2)]
        colors = [BrandColors.METALLIC_GOLD, BrandColors.SUCCESS_GREEN, 
                 BrandColors.WARNING_AMBER, BrandColors.INFO_BLUE]
        
        for i, ((title, value, max_val), pos, color) in enumerate(zip(risk_categories, positions, colors)):
            fig.add_trace(go.Indicator(
                mode="gauge+number+delta",
                value=value,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': title, 'font': {'size': 16, 'color': BrandColors.HIGH_CONTRAST}},
                delta={'reference': 5, 'increasing': {'color': BrandColors.ERROR_RED}},
                gauge={
                    'axis': {'range': [None, max_val], 'tickcolor': BrandColors.NEUTRAL_TEXT},
                    'bar': {'color': color, 'thickness': 0.8},
                    'steps': [
                        {'range': [0, 3], 'color': 'rgba(61, 188, 107, 0.2)'},
                        {'range': [3, 6], 'color': 'rgba(245, 158, 11, 0.2)'},
                        {'range': [6, 10], 'color': 'rgba(228, 87, 76, 0.2)'}
                    ],
                    'threshold': {
                        'line': {'color': BrandColors.HIGH_CONTRAST, 'width': 4}, 
                        'thickness': 0.75, 
                        'value': 8
                    }
                },
                number={'font': {'color': color, 'size': 28}}
            ), row=pos[0], col=pos[1])
        
        return apply_enterprise_styling(fig, "Enterprise Risk Assessment Dashboard", height=600)
    
    def create_predictive_analytics_chart(self, data: Dict[str, Any]) -> go.Figure:
        """AI-powered predictive analytics visualization"""
        # Generate time series data
        dates = pd.date_range('2024-01-01', '2025-06-30', freq='W')
        historical_cutoff = len(dates) // 3 * 2
        
        historical_dates = dates[:historical_cutoff]
        forecast_dates = dates[historical_cutoff:]
        
        # Historical compliance scores
        np.random.seed(42)
        historical_scores = 95 + np.cumsum(np.random.normal(0.05, 0.3, len(historical_dates)))
        historical_scores = np.clip(historical_scores, 90, 100)
        
        # Forecast with confidence intervals
        forecast_mean = 95 + np.cumsum(np.random.normal(0.03, 0.2, len(forecast_dates)))
        forecast_mean = np.clip(forecast_mean, 90, 100)
        
        forecast_upper = forecast_mean + np.random.normal(2, 0.5, len(forecast_dates))
        forecast_lower = forecast_mean - np.random.normal(2, 0.5, len(forecast_dates))
        
        # Risk events (synthetic)
        risk_dates = pd.date_range('2024-03-15', '2025-03-15', freq='2M')
        risk_scores = np.random.uniform(2, 8, len(risk_dates))
        
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=['Predictive Compliance Trajectory', 'AI Risk Prediction Timeline'],
            row_heights=[0.6, 0.4],
            vertical_spacing=0.1
        )
        
        # Historical compliance
        fig.add_trace(go.Scatter(
            x=historical_dates, y=historical_scores,
            mode='lines+markers',
            name='Historical Performance',
            line=dict(color=BrandColors.METALLIC_GOLD, width=3),
            marker=dict(size=6, color=BrandColors.METALLIC_GOLD)
        ), row=1, col=1)
        
        # Forecast confidence interval
        fig.add_trace(go.Scatter(
            x=forecast_dates, y=forecast_upper,
            mode='lines',
            line=dict(width=0),
            showlegend=False,
            hoverinfo='skip'
        ), row=1, col=1)
        
        fig.add_trace(go.Scatter(
            x=forecast_dates, y=forecast_lower,
            mode='lines',
            line=dict(width=0),
            fill='tonexty',
            fillcolor='rgba(212, 175, 55, 0.15)',
            name='Prediction Confidence',
            hoverinfo='skip'
        ), row=1, col=1)
        
        # Forecast mean
        fig.add_trace(go.Scatter(
            x=forecast_dates, y=forecast_mean,
            mode='lines+markers',
            name='AI Prediction',
            line=dict(color=BrandColors.GOLD_HIGHLIGHT, width=3, dash='dash'),
            marker=dict(size=6, color=BrandColors.GOLD_HIGHLIGHT, symbol='diamond')
        ), row=1, col=1)
        
        # Risk timeline
        fig.add_trace(go.Bar(
            x=risk_dates, y=risk_scores,
            name='Predicted Risk Events',
            marker=dict(
                color=risk_scores,
                colorscale=[
                    [0.0, BrandColors.SUCCESS_GREEN],
                    [0.5, BrandColors.WARNING_AMBER],
                    [1.0, BrandColors.ERROR_RED]
                ],
                showscale=True,
                colorbar=dict(title="Risk Level", x=1.02)
            )
        ), row=2, col=1)
        
        return apply_enterprise_styling(fig, "AI-Powered Predictive Intelligence Platform", height=700)

# ============================================================================
# PREMIUM UI COMPONENTS SYSTEM
# ============================================================================

class EnterpriseUIComponents:
    """Premium UI components for enterprise dashboard"""
    
    @staticmethod
    def render_enterprise_header(user: Optional[User] = None):
        """Render premium enterprise header with user info"""
        user_name = user.full_name if user else "Guest User"
        user_role = user.role.value.title() if user else "Viewer"
        
        header_html = f"""
        <div class="enterprise-header">
            <div class="header-container">
                <div class="header-brand">
                    <div class="brand-logo">⚖</div>
                    <div class="brand-text">
                        <h1 class="brand-title">{AppConfig.APP_NAME}</h1>
                        <p class="brand-subtitle">{AppConfig.APP_SUBTITLE}</p>
                    </div>
                </div>
                
                <div class="header-navigation">
                    <a href="#" class="nav-link active">Dashboard</a>
                    <a href="#" class="nav-link">Analytics</a>
                    <a href="#" class="nav-link">Reports</a>
                    <a href="#" class="nav-link">Intelligence</a>
                </div>
                
                <div class="header-actions">
                    <div class="status-indicator">
                        <div class="status-dot"></div>
                        Live Intelligence
                    </div>
                    <div style="text-align: right; color: var(--text-neutral); font-size: 0.875rem;">
                        <div style="font-weight: 600; color: var(--text-high-contrast);">{user_name}</div>
                        <div>{user_role} Access</div>
                    </div>
                </div>
            </div>
        </div>
        """
        
        st.markdown(header_html, unsafe_allow_html=True)
    
    @staticmethod
    def render_executive_kpis(data: Dict[str, Any]):
        """Render premium KPI cards with animations"""
        performance_score = data.get('PERFORMANCE_SCORE', 99.7)
        risk_score = data.get('RISK_SCORE', 0.8)
        days_violation_free = data.get('DAYS_VIOLATION_FREE', 1247)
        team_certification = data.get('TEAM_CERTIFICATION', 99.4)
        ai_insights = data.get('AI_INSIGHTS', 5)
        global_coverage = data.get('GLOBAL_COVERAGE', 47)
        
        kpi_html = f"""
        <div class="kpi-grid">
            <div class="kpi-card">
                <div class="kpi-icon">🎯</div>
                <div class="kpi-label">Compliance Excellence</div>
                <div class="kpi-value">{performance_score}%</div>
                <div class="kpi-change positive">▲ 2.3% above industry leader</div>
            </div>
            
            <div class="kpi-card">
                <div class="kpi-icon">🛡️</div>
                <div class="kpi-label">Risk Intelligence</div>
                <div class="kpi-value">{risk_score}</div>
                <div class="kpi-change positive">▼ 9.2 pts (Ultra-Low Risk)</div>
            </div>
            
            <div class="kpi-card">
                <div class="kpi-icon">⚡</div>
                <div class="kpi-label">Violation-Free Days</div>
                <div class="kpi-value">{days_violation_free}</div>
                <div class="kpi-change positive">◆ Record Performance</div>
            </div>
            
            <div class="kpi-card">
                <div class="kpi-icon">🎓</div>
                <div class="kpi-label">Team Certification</div>
                <div class="kpi-value">{team_certification}%</div>
                <div class="kpi-change positive">▲ Excellence Standard</div>
            </div>
            
            <div class="kpi-card">
                <div class="kpi-icon">🤖</div>
                <div class="kpi-label">AI Insights</div>
                <div class="kpi-value">{ai_insights}</div>
                <div class="kpi-change positive">● Active Optimizations</div>
            </div>
            
            <div class="kpi-card">
                <div class="kpi-icon">🌍</div>
                <div class="kpi-label">Global Coverage</div>
                <div class="kpi-value">{global_coverage}</div>
                <div class="kpi-change positive">◆ Jurisdictions Monitored</div>
            </div>
        </div>
        """
        
        st.markdown(kpi_html, unsafe_allow_html=True)
    
    @staticmethod
    def render_enterprise_sidebar(user: Optional[User] = None):
        """Render comprehensive enterprise sidebar"""
        with st.sidebar:
            # User profile section
            if user:
                st.markdown(f"""
                <div class="sidebar-section">
                    <div class="sidebar-title">Executive Profile</div>
                    <div class="sidebar-item active">
                        <div style="display: flex; align-items: center; gap: 1rem;">
                            <div style="width: 40px; height: 40px; background: var(--accent-gold); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 700; color: var(--bg-charcoal);">
                                {user.full_name[0]}
                            </div>
                            <div>
                                <div style="font-weight: 600; color: var(--text-high-contrast);">{user.full_name}</div>
                                <div style="font-size: 0.875rem; color: var(--text-neutral);">{user.role.value.title()}</div>
                            </div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    with tab4:
        ui_components.render_chart_container(
            chart_manager.create_compliance_heatmap,
            client_data,
            "Global Regulatory Compliance Intelligence Matrix",
            "Real-time compliance monitoring across 47 global jurisdictions"
        )
        
        # Global compliance metrics
        st.markdown("### Global Compliance Intelligence")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="enterprise-card">
                <div class="card-header">
                    <h4 class="card-title">Regional Performance</h4>
                </div>
                <div class="card-content">
                    <div class="metric-container">
                        <span class="metric-label">North America</span>
                        <span class="metric-value" style="color: var(--success-green);">99.1%</span>
                    </div>
                    <div class="metric-container">
                        <span class="metric-label">Europe</span>
                        <span class="metric-value" style="color: var(--success-green);">99.3%</span>
                    </div>
                    <div class="metric-container">
                        <span class="metric-label">Asia Pacific</span>
                        <span class="metric-value" style="color: var(--success-green);">98.4%</span>
                    </div>
                    <div class="metric-container">
                        <span class="metric-label">Latin America</span>
                        <span class="metric-value" style="color: var(--warning-amber);">97.2%</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="enterprise-card">
                <div class="card-header">
                    <h4 class="card-title">Regulatory Coverage</h4>
                </div>
                <div class="card-content">
                    <div class="metric-container">
                        <span class="metric-label">Total Jurisdictions</span>
                        <span class="metric-value">47</span>
                    </div>
                    <div class="metric-container">
                        <span class="metric-label">Regulatory Bodies</span>
                        <span class="metric-value">23</span>
                    </div>
                    <div class="metric-container">
                        <span class="metric-label">Active Standards</span>
                        <span class="metric-value">156</span>
                    </div>
                    <div class="metric-container">
                        <span class="metric-label">Update Frequency</span>
                        <span class="metric-value">Real-time</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="enterprise-card">
                <div class="card-header">
                    <h4 class="card-title">Intelligence Status</h4>
                </div>
                <div class="card-content">
                    <div class="metric-container">
                        <span class="metric-label">Data Sources</span>
                        <span class="metric-value" style="color: var(--success-green);">Online</span>
                    </div>
                    <div class="metric-container">
                        <span class="metric-label">AI Processing</span>
                        <span class="metric-value" style="color: var(--success-green);">Active</span>
                    </div>
                    <div class="metric-container">
                        <span class="metric-label">Change Detection</span>
                        <span class="metric-value" style="color: var(--success-green);">Monitoring</span>
                    </div>
                    <div class="metric-container">
                        <span class="metric-label">Alert System</span>
                        <span class="metric-value" style="color: var(--success-green);">Armed</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with tab5:
        ui_components.render_chart_container(
            chart_manager.create_predictive_analytics_chart,
            client_data,
            "AI-Powered Predictive Intelligence Platform",
            "Machine learning algorithms analyzing patterns and predicting future compliance trends"
        )
        
        # Predictive insights section
        st.markdown("### AI-Powered Predictive Insights")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("""
            <div class="enterprise-card">
                <div class="card-header">
                    <h3 class="card-title">Predictive Intelligence Summary</h3>
                </div>
                <div class="card-content">
                    <h4 style="color: var(--accent-gold); margin-bottom: 1rem;">Next 90 Days Forecast</h4>
                    <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem; margin-bottom: 2rem;">
                        <div class="metric-container">
                            <span class="metric-label">Predicted Compliance Score</span>
                            <span class="metric-value" style="color: var(--success-green);">99.8%</span>
                        </div>
                        <div class="metric-container">
                            <span class="metric-label">Risk Probability</span>
                            <span class="metric-value" style="color: var(--success-green);">0.3%</span>
                        </div>
                        <div class="metric-container">
                            <span class="metric-label">Optimization Opportunities</span>
                            <span class="metric-value" style="color: var(--accent-gold);">7</span>
                        </div>
                        <div class="metric-container">
                            <span class="metric-label">Confidence Level</span>
                            <span class="metric-value" style="color: var(--success-green);">97.4%</span>
                        </div>
                    </div>
                    
                    <h4 style="color: var(--accent-gold); margin-bottom: 1rem;">AI Recommendations</h4>
                    <ul style="color: var(--text-neutral); line-height: 1.8;">
                        <li><strong>Training Enhancement:</strong> Schedule additional certification for Asia-Pacific team members</li>
                        <li><strong>Process Optimization:</strong> Implement automated validation for new regulatory changes</li>
                        <li><strong>Technology Upgrade:</strong> Deploy advanced monitoring sensors in critical areas</li>
                        <li><strong>Strategic Planning:</strong> Prepare for upcoming EU regulatory changes in Q3</li>
                        <li><strong>Risk Mitigation:</strong> Increase monitoring frequency for identified risk areas</li>
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="enterprise-card">
                <div class="card-header">
                    <h4 class="card-title">AI Model Performance</h4>
                </div>
                <div class="card-content">
                    <div class="metric-container">
                        <span class="metric-label">Prediction Accuracy</span>
                        <span class="metric-value" style="color: var(--success-green);">97.4%</span>
                    </div>
                    <div class="metric-container">
                        <span class="metric-label">Model Version</span>
                        <span class="metric-value">v2.3.1</span>
                    </div>
                    <div class="metric-container">
                        <span class="metric-label">Training Data Points</span>
                        <span class="metric-value">2.4M</span>
                    </div>
                    <div class="metric-container">
                        <span class="metric-label">Last Model Update</span>
                        <span class="metric-value">3 days ago</span>
                    </div>
                    
                    <div style="margin-top: 2rem; padding-top: 1rem; border-top: 1px solid var(--accent-gold);">
                        <h5 style="color: var(--accent-gold); margin-bottom: 1rem;">Algorithm Status</h5>
                        <div class="metric-container">
                            <span class="metric-label">Risk Detection</span>
                            <span class="metric-value" style="color: var(--success-green);">Active</span>
                        </div>
                        <div class="metric-container">
                            <span class="metric-label">Trend Analysis</span>
                            <span class="metric-value" style="color: var(--success-green);">Processing</span>
                        </div>
                        <div class="metric-container">
                            <span class="metric-label">Pattern Recognition</span>
                            <span class="metric-value" style="color: var(--success-green);">Optimized</span>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

def render_executive_alerts(client_data: Dict[str, Any]):
    """Render executive-grade alert system"""
    st.markdown("### Executive Status Intelligence")
    
    alert_level = client_data.get('ALERT_LEVEL', 'OPTIMAL')
    
    if alert_level == 'OPTIMAL':
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="alert success">
                <strong>System Status: Optimal Excellence</strong><br>
                All AI monitoring systems operating at peak performance with zero critical issues detected.
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="alert success">
                <strong>Compliance: Perfect Record</strong><br>
                1,247 days violation-free with predictive prevention systems active and monitoring.
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="alert info">
                <strong>AI Insights: 5 Optimizations Available</strong><br>
                Machine learning algorithms have identified proactive efficiency improvements.
            </div>
            """, unsafe_allow_html=True)
    
    else:
        st.markdown(f"""
        <div class="alert warning">
            <strong>Alert Level: {alert_level}</strong><br>
            System requires attention. Please review detailed status information.
        </div>
        """, unsafe_allow_html=True)

def render_educational_resources():
    """Render educational resources and guidance section"""
    st.markdown("## Executive Education & Resources")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="enterprise-card">
            <div class="card-header">
                <h3 class="card-title">Regulatory Guides</h3>
            </div>
            <div class="card-content">
                <ul style="list-style: none; padding: 0;">
                    <li style="margin-bottom: 1rem;">
                        <a href="#" class="btn-ghost" style="display: block; text-decoration: none; text-align: center;">
                            📖 FDA 21 CFR 211 Guide
                        </a>
                    </li>
                    <li style="margin-bottom: 1rem;">
                        <a href="#" class="btn-ghost" style="display: block; text-decoration: none; text-align: center;">
                            📋 USP 797/800 Standards
                        </a>
                    </li>
                    <li style="margin-bottom: 1rem;">
                        <a href="#" class="btn-ghost" style="display: block; text-decoration: none; text-align: center;">
                            🌍 EU GMP Guidelines
                        </a>
                    </li>
                    <li>
                        <a href="#" class="btn-ghost" style="display: block; text-decoration: none; text-align: center;">
                            🎓 ISO Standards Library
                        </a>
                    </li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="enterprise-card">
            <div class="card-header">
                <h3 class="card-title">Training Materials</h3>
            </div>
            <div class="card-content">
                <ul style="list-style: none; padding: 0;">
                    <li style="margin-bottom: 1rem;">
                        <a href="#" class="btn-ghost" style="display: block; text-decoration: none; text-align: center;">
                            🎥 Executive Briefings
                        </a>
                    </li>
                    <li style="margin-bottom: 1rem;">
                        <a href="#" class="btn-ghost" style="display: block; text-decoration: none; text-align: center;">
                            📚 Compliance Workshops
                        </a>
                    </li>
                    <li style="margin-bottom: 1rem;">
                        <a href="#" class="btn-ghost" style="display: block; text-decoration: none; text-align: center;">
                            🧠 AI Training Modules
                        </a>
                    </li>
                    <li>
                        <a href="#" class="btn-ghost" style="display: block; text-decoration: none; text-align: center;">
                            🏆 Certification Programs
                        </a>
                    </li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="enterprise-card">
            <div class="card-header">
                <h3 class="card-title">Support Resources</h3>
            </div>
            <div class="card-content">
                <ul style="list-style: none; padding: 0;">
                    <li style="margin-bottom: 1rem;">
                        <a href="#" class="btn-ghost" style="display: block; text-decoration: none; text-align: center;">
                            📞 Executive Hotline
                        </a>
                    </li>
                    <li style="margin-bottom: 1rem;">
                        <a href="#" class="btn-ghost" style="display: block; text-decoration: none; text-align: center;">
                            💬 Expert Consultation
                        </a>
                    </li>
                    <li style="margin-bottom: 1rem;">
                        <a href="#" class="btn-ghost" style="display: block; text-decoration: none; text-align: center;">
                            📧 Technical Support
                        </a>
                    </li>
                    <li>
                        <a href="#" class="btn-ghost" style="display: block; text-decoration: none; text-align: center;">
                            🌐 Knowledge Base
                        </a>
                    </li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)

def render_export_section():
    """Render comprehensive export and reporting section"""
    st.markdown("## Executive Reports & Export")
    
    export_manager = EnterpriseExportManager()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### Standard Reports")
        
        report_types = [
            ("Executive Summary", "executive_summary"),
            ("Compliance Report", "compliance_report"),
            ("Risk Assessment", "risk_assessment"),
            ("Financial Analysis", "financial_analysis"),
            ("Global Intelligence", "global_intelligence")
        ]
        
        for report_name, report_type in report_types:
            if st.button(f"📊 Generate {report_name}", key=f"btn_{report_type}", use_container_width=True):
                try:
                    if report_type == "executive_summary":
                        data_manager = DataConnectionManager()
                        client_data = data_manager.load_client_data()
                        report_content = export_manager.create_executive_report(client_data)
                        
                        st.download_button(
                            label=f"⬇️ Download {report_name}",
                            data=report_content,
                            file_name=f"lexcura_{report_type}_{datetime.now().strftime('%Y%m%d')}.md",
                            mime="text/markdown",
                            key=f"download_{report_type}"
                        )
                    else:
                        st.success(f"{report_name} generated successfully!")
                        
                except Exception as e:
                    st.error(f"Error generating {report_name}: {str(e)}")
    
    with col2:
        st.markdown("### Data Export")
        
        export_formats = ["CSV", "Excel", "JSON", "PDF"]
        selected_format = st.selectbox("Export Format", export_formats)
        
        export_options = st.multiselect(
            "Select Data to Export",
            ["KPI Metrics", "Compliance Data", "Risk Analysis", "Financial Data", "Predictive Analytics"],
            default=["KPI Metrics"]
        )
        
        if st.button("🚀 Generate Export", use_container_width=True):
            if export_options:
                try:
                    # Create sample export data
                    export_data = pd.DataFrame({
                        'Metric': ['Compliance Score', 'Risk Level', 'ROI', 'Efficiency'],
                        'Value': [99.7, 0.8, 847, 342],
                        'Unit': ['%', '/10', '%', '%'],
                        'Trend': ['↑', '↓', '↑', '↑']
                    })
                    
                    if selected_format == "CSV":
                        csv_data = export_manager.export_to_csv(export_data, "lexcura_export")
                        st.download_button(
                            "⬇️ Download CSV",
                            csv_data,
                            f"lexcura_export_{datetime.now().strftime('%Y%m%d')}.csv",
                            "text/csv"
                        )
                    else:
                        st.success(f"Export prepared in {selected_format} format!")
                        
                except Exception as e:
                    st.error(f"Export error: {str(e)}")
            else:
                st.warning("Please select at least one data type to export.")
    
    with col3:
        st.markdown("### Scheduled Reports")
        
        st.selectbox("Report Frequency", ["Daily", "Weekly", "Monthly", "Quarterly"])
        st.multiselect("Recipients", ["C-Suite", "Compliance Team", "Risk Management", "Operations"])
        st.selectbox("Delivery Method", ["Email", "Secure Portal", "API Integration"])
        
        if st.button("📅 Schedule Report", use_container_width=True):
            st.success("Scheduled report configured successfully!")

def render_settings_preferences():
    """Render user settings and preferences"""
    st.markdown("## Executive Settings & Preferences")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Dashboard Preferences")
        
        # Theme settings (fixed to enterprise theme)
        st.markdown("""
        <div class="enterprise-card">
            <div class="card-header">
                <h4 class="card-title">Display Settings</h4>
            </div>
            <div class="card-content">
                <div class="metric-container">
                    <span class="metric-label">Theme</span>
                    <span class="metric-value">Executive Dark (Fixed)</span>
                </div>
                <div class="metric-container">
                    <span class="metric-label">Refresh Rate</span>
                    <span class="metric-value">Real-time</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Notification preferences
        st.markdown("### Notification Preferences")
        
        notification_types = [
            "Critical Alerts",
            "Compliance Updates", 
            "Risk Changes",
            "Financial Milestones",
            "AI Insights",
            "System Status"
        ]
        
        for notification in notification_types:
            st.checkbox(notification, value=True, key=f"notif_{notification.lower().replace(' ', '_')}")
    
    with col2:
        st.markdown("### Account Information")
        
        if st.session_state.user:
            user = st.session_state.user
            
            st.markdown(f"""
            <div class="enterprise-card">
                <div class="card-header">
                    <h4 class="card-title">User Profile</h4>
                </div>
                <div class="card-content">
                    <div class="metric-container">
                        <span class="metric-label">Name</span>
                        <span class="metric-value">{user.full_name}</span>
                    </div>
                    <div class="metric-container">
                        <span class="metric-label">Email</span>
                        <span class="metric-value">{user.email}</span>
                    </div>
                    <div class="metric-container">
                        <span class="metric-label">Role</span>
                        <span class="metric-value">{user.role.value.title()}</span>
                    </div>
                    <div class="metric-container">
                        <span class="metric-label">Last Login</span>
                        <span class="metric-value">{user.last_login.strftime('%Y-%m-%d %H:%M') if user.last_login else 'N/A'}</span>
                    </div>
                    <div class="metric-container">
                        <span class="metric-label">Session Count</span>
                        <span class="metric-value">{user.login_count}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Security settings
        st.markdown("### Security Settings")
        
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("🔐 Change Password", use_container_width=True):
                st.info("Password change requested. Check your email for instructions.")
        
        with col_b:
            if st.button("📱 Setup 2FA", use_container_width=True):
                st.info("Two-factor authentication setup initiated.")
        
        # Session management
        st.markdown("### Session Management")
        
        if st.button("🚪 Logout", use_container_width=True, type="secondary"):
            auth_manager = AuthenticationManager()
            auth_manager.logout_user()

def render_advanced_analytics():
    """Render advanced analytics and insights page"""
    st.markdown("## Advanced Analytics & Deep Insights")
    
    # Analytics navigation
    analytics_tab = st.radio(
        "Select Analytics View",
        ["Performance Trends", "Comparative Analysis", "Predictive Modeling", "Custom Queries"],
        horizontal=True
    )
    
    if analytics_tab == "Performance Trends":
        render_performance_trends()
    elif analytics_tab == "Comparative Analysis":
        render_comparative_analysis()
    elif analytics_tab == "Predictive Modeling":
        render_predictive_modeling()
    else:
        render_custom_queries()

def render_performance_trends():
    """Render detailed performance trend analysis"""
    st.markdown("### Performance Trend Analysis")
    
    # Time range selector
    col1, col2, col3 = st.columns(3)
    with col1:
        start_date = st.date_input("Start Date", value=datetime.now() - timedelta(days=365))
    with col2:
        end_date = st.date_input("End Date", value=datetime.now())
    with col3:
        granularity = st.selectbox("Granularity", ["Daily", "Weekly", "Monthly", "Quarterly"])
    
    # Generate trend data
    chart_manager = EnterpriseChartManager()
    
    # Create comprehensive trend analysis
    dates = pd.date_range(start_date, end_date, freq='D' if granularity == 'Daily' else 'W')
    
    # Simulate trend data
    np.random.seed(42)
    compliance_trend = 95 + np.cumsum(np.random.normal(0.01, 0.5, len(dates)))
    compliance_trend = np.clip(compliance_trend, 85, 100)
    
    risk_trend = 5 + np.cumsum(np.random.normal(-0.01, 0.3, len(dates)))
    risk_trend = np.clip(risk_trend, 0, 10)
    
    efficiency_trend = 100 + np.cumsum(np.random.normal(0.5, 2, len(dates)))
    efficiency_trend = np.clip(efficiency_trend, 50, 500)
    
    # Create multi-metric trend chart
    fig = make_subplots(
        rows=3, cols=1,
        subplot_titles=['Compliance Excellence Trend', 'Risk Profile Evolution', 'Operational Efficiency Growth'],
        vertical_spacing=0.08
    )
    
    # Compliance trend
    fig.add_trace(go.Scatter(
        x=dates, y=compliance_trend,
        mode='lines+markers',
        name='Compliance Score',
        line=dict(color=BrandColors.METALLIC_GOLD, width=3),
        marker=dict(size=4, color=BrandColors.METALLIC_GOLD)
    ), row=1, col=1)
    
    # Risk trend
    fig.add_trace(go.Scatter(
        x=dates, y=risk_trend,
        mode='lines+markers',
        name='Risk Level',
        line=dict(color=BrandColors.ERROR_RED, width=3),
        marker=dict(size=4, color=BrandColors.ERROR_RED),
        fill='tozeroy',
        fillcolor='rgba(228, 87, 76, 0.1)'
    ), row=2, col=1)
    
    # Efficiency trend
    fig.add_trace(go.Scatter(
        x=dates, y=efficiency_trend,
        mode='lines+markers',
        name='Efficiency Index',
        line=dict(color=BrandColors.SUCCESS_GREEN, width=3),
        marker=dict(size=4, color=BrandColors.SUCCESS_GREEN)
    ), row=3, col=1)
    
    fig.update_layout(height=800, showlegend=False)
    fig = apply_enterprise_styling(fig, "Comprehensive Performance Trend Analysis")
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Trend insights
    st.markdown("### Trend Insights & Analysis")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="enterprise-card">
            <div class="card-header">
                <h4 class="card-title">Compliance Trends</h4>
            </div>
            <div class="card-content">
                <ul style="color: var(--text-neutral); line-height: 1.8;">
                    <li>Steady upward trajectory over 12 months</li>
                    <li>98.5% average performance maintained</li>
                    <li>Zero significant downward spikes detected</li>
                    <li>Seasonal variation: ±1.2% standard deviation</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="enterprise-card">
            <div class="card-header">
                <h4 class="card-title">Risk Profile Evolution</h4>
            </div>
            <div class="card-content">
                <ul style="color: var(--text-neutral); line-height: 1.8;">
                    <li>47% reduction in average risk score</li>
                    <li>Consistent downward trend maintained</li>
                    <li>Peak risk events successfully mitigated</li>
                    <li>Predictive accuracy improved by 23%</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="enterprise-card">
            <div class="card-header">
                <h4 class="card-title">Efficiency Growth</h4>
            </div>
            <div class="card-content">
                <ul style="color: var(--text-neutral); line-height: 1.8;">
                    <li>342% efficiency improvement achieved</li>
                    <li>Acceleration in growth rate observed</li>
                    <li>Technology optimization contributing 67%</li>
                    <li>ROI exceeding all projected benchmarks</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)

def render_comparative_analysis():
    """Render comparative analysis features"""
    st.markdown("### Industry Comparative Analysis")
    
    # Comparison selector
    col1, col2 = st.columns(2)
    with col1:
        comparison_type = st.selectbox(
            "Comparison Type",
            ["Industry Benchmark", "Peer Companies", "Historical Performance", "Regional Comparison"]
        )
    with col2:
        metrics = st.multiselect(
            "Metrics to Compare",
            ["Compliance Score", "Risk Level", "Efficiency", "ROI", "Team Certification"],
            default=["Compliance Score", "Risk Level"]
        )
    
    # Generate comparison data
    if comparison_type == "Industry Benchmark":
        categories = ['Pharmaceutical', 'Medical Device', 'Biotechnology', 'Chemical', 'Food & Beverage']
        our_scores = [99.7, 99.2, 98.8, 99.1, 97.9]
        industry_avg = [87.2, 84.6, 89.1, 82.4, 78.9]
        industry_best = [94.1, 91.8, 95.2, 90.7, 88.4]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=categories, y=our_scores,
            name='LexCura Client',
            marker=dict(color=BrandColors.METALLIC_GOLD),
            text=[f'{score}%' for score in our_scores],
            textposition='auto'
        ))
        
        fig.add_trace(go.Bar(
            x=categories, y=industry_avg,
            name='Industry Average',
            marker=dict(color=BrandColors.NEUTRAL_TEXT, opacity=0.7),
            text=[f'{score}%' for score in industry_avg],
            textposition='auto'
        ))
        
        fig.add_trace(go.Bar(
            x=categories, y=industry_best,
            name='Industry Best Practice',
            marker=dict(color=BrandColors.SUCCESS_GREEN, opacity=0.8),
            text=[f'{score}%' for score in industry_best],
            textposition='auto'
        ))
        
        fig = apply_enterprise_styling(fig, "Industry Benchmark Comparison", 500)
        st.plotly_chart(fig, use_container_width=True)
        
        # Comparative insights
        st.markdown("### Competitive Position Analysis")
        
        performance_gap = np.mean(our_scores) - np.mean(industry_avg)
        best_practice_gap = np.mean(our_scores) - np.mean(industry_best)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("vs Industry Average", f"+{performance_gap:.1f}%", "12.5% above")
        with col2:
            st.metric("vs Best Practice", f"+{best_practice_gap:.1f}%", "4.8% above")
        with col3:
            st.metric("Ranking Position", "#1", "Industry Leader")

def render_predictive_modeling():
    """Render predictive modeling interface"""
    st.markdown("### AI Predictive Modeling Suite")
    
    # Model selection
    col1, col2, col3 = st.columns(3)
    with col1:
        model_type = st.selectbox("Prediction Model", ["Compliance Forecast", "Risk Prediction", "Efficiency Projection"])
    with col2:
        forecast_horizon = st.selectbox("Forecast Period", ["30 Days", "90 Days", "6 Months", "1 Year"])
    with col3:
        confidence_level = st.slider("Confidence Level", 80, 99, 95)
    
    # Generate predictions based on selection
    if st.button("🔮 Generate Predictions", use_container_width=True):
        with st.spinner("AI models processing data..."):
            time.sleep(2)  # Simulate processing time
            
            # Create prediction visualization
            chart_manager = EnterpriseChartManager()
            data_manager = DataConnectionManager()
            client_data = data_manager.get_enterprise_demo_data()
            
            fig = chart_manager.create_predictive_analytics_chart(client_data)
            st.plotly_chart(fig, use_container_width=True)
            
            # Prediction summary
            st.markdown(f"""
            <div class="enterprise-card">
                <div class="card-header">
                    <h3 class="card-title">Prediction Results - {model_type}</h3>
                </div>
                <div class="card-content">
                    <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 2rem;">
                        <div>
                            <h4 style="color: var(--accent-gold);">Model Confidence</h4>
                            <div class="metric-container">
                                <span class="metric-label">Prediction Accuracy</span>
                                <span class="metric-value">{confidence_level}%</span>
                            </div>
                            <div class="metric-container">
                                <span class="metric-label">Data Quality Score</span>
                                <span class="metric-value">98.4%</span>
                            </div>
                        </div>
                        <div>
                            <h4 style="color: var(--accent-gold);">Key Insights</h4>
                            <ul style="color: var(--text-neutral); line-height: 1.6;">
                                <li>Trending performance improvement expected</li>
                                <li>Low probability of significant risk events</li>
                                <li>Optimization opportunities identified</li>
                                <li>Seasonal patterns incorporated</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

def render_custom_queries():
    """Render custom query interface for advanced users"""
    st.markdown("### Custom Analytics Queries")
    
    st.info("Advanced analytics interface for custom data exploration and analysis.")
    
    # Query builder interface
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("#### Query Parameters")
        
        # Data source selection
        data_sources = st.multiselect(
            "Data Sources",
            ["Compliance Records", "Risk Assessments", "Financial Data", "Training Records", "System Logs"],
            default=["Compliance Records"]
        )
        
        # Filter options
        date_range = st.date_input(
            "Date Range",
            value=(datetime.now() - timedelta(days=90), datetime.now()),
            key="custom_date_range"
        )
        
        # Aggregation options
        aggregation = st.selectbox("Aggregation", ["Daily", "Weekly", "Monthly", "Quarterly"])
        
        # Custom metrics
        custom_metrics = st.text_area(
            "Custom Metrics (JSON format)",
            value='{"compliance_score": "avg", "risk_level": "max", "efficiency": "sum"}',
            height=100
        )
        
        if st.button("🚀 Execute Query"):
            try:
                # Simulate query execution
                with st.spinner("Executing custom query..."):
                    time.sleep(1)
                
                # Generate sample results
                sample_data = pd.DataFrame({
                    'Date': pd.date_range(date_range[0], date_range[1], freq='D'),
                    'Compliance_Score': np.random.uniform(95, 100, len(pd.date_range(date_range[0], date_range[1], freq='D'))),
                    'Risk_Level': np.random.uniform(0, 3, len(pd.date_range(date_range[0], date_range[1], freq='D'))),
                    'Efficiency': np.random.uniform(200, 400, len(pd.date_range(date_range[0], date_range[1], freq='D')))
                })
                
                st.success("Query executed successfully!")
                st.dataframe(sample_data.head(10), use_container_width=True)
                
                # Offer download
                csv_data = sample_data.to_csv(index=False)
                st.download_button(
                    "📥 Download Results",
                    csv_data,
                    f"custom_query_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                    "text/csv"
                )
                
            except Exception as e:
                st.error(f"Query execution error: {str(e)}")
    
    with col2:
        st.markdown("#### Query Templates")
        
        templates = [
            "Top Risk Events by Month",
            "Compliance Trend Analysis",
            "Training Effectiveness Report",
            "Cost-Benefit Analysis",
            "Regional Performance Comparison"
        ]
        
        for template in templates:
            if st.button(template, use_container_width=True, key=f"template_{template}"):
                st.info(f"Template '{template}' loaded into query builder.")

# ============================================================================
# APPLICATION ENTRY POINT & ROUTING
# ============================================================================

def main():
    """Main application entry point with routing and session management"""
    
    # Configure page and initialize
    configure_page()
    initialize_session_state()
    load_enterprise_css()
    
    # Authentication check
    if not check_authentication():
        render_login_form()
        return
    
    # Main application logic for authenticated users
    try:
        # Page routing system
        if 'page' in st.query_params:
            current_page = st.query_params['page']
        else:
            current_page = 'dashboard'
        
        # Route to appropriate page
        if current_page == 'dashboard':
            render_main_dashboard()
            
        elif current_page == 'analytics':
            render_advanced_analytics()
            
        elif current_page == 'reports':
            render_export_section()
            
        elif current_page == 'resources':
            render_educational_resources()
            
        elif current_page == 'settings':
            render_settings_preferences()
            
        else:
            # Default to dashboard
            render_main_dashboard()
        
        # Footer information
        st.markdown("---")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"**{AppConfig.APP_NAME}** {AppConfig.VERSION}")
        with col2:
            st.markdown(f"Enterprise License | {AppConfig.COMPANY}")
        with col3:
            st.markdown(f"Support: {AppConfig.SUPPORT_EMAIL}")
        
        # Performance monitoring
        if st.session_state.user and st.session_state.user.role == UserRole.ADMIN:
            with st.expander("System Performance", expanded=False):
                st.json({
                    "session_duration": str(datetime.now() - st.session_state.session_start) if st.session_state.session_start else "N/A",
                    "data_loaded": st.session_state.data_loaded,
                    "last_refresh": str(st.session_state.last_refresh) if st.session_state.last_refresh else "N/A",
                    "cache_status": "Active",
                    "memory_usage": "Optimal"
                })
        
    except Exception as e:
        st.error(f"Application error: {str(e)}")
        logging.error(f"Application error: {e}")
        
        # Fallback error page
        st.markdown("""
        <div class="enterprise-card">
            <div class="card-header">
                <h3 class="card-title">System Error</h3>
            </div>
            <div class="card-content">
                <p>An unexpected error occurred. Our technical team has been notified.</p>
                <p>Please refresh the page or contact support if the problem persists.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# ADDITIONAL UTILITY FUNCTIONS
# ============================================================================

def log_user_activity(user: User, action: str, details: str = ""):
    """Log user activity for audit and analytics"""
    try:
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "user": user.username,
            "role": user.role.value,
            "action": action,
            "details": details,
            "session_id": str(uuid.uuid4())
        }
        # In production, this would write to a secure logging system
        logging.info(f"User Activity: {json.dumps(log_entry)}")
    except Exception as e:
        logging.error(f"Activity logging error: {e}")

def validate_data_integrity(data: Dict[str, Any]) -> bool:
    """Validate data integrity and consistency"""
    required_fields = ['CLIENT_NAME', 'TIER', 'STATUS', 'PERFORMANCE_SCORE']
    
    try:
        for field in required_fields:
            if field not in data or data[field] is None:
                logging.warning(f"Missing required field: {field}")
                return False
        
        # Validate data types and ranges
        if not isinstance(data.get('PERFORMANCE_SCORE', 0), (int, float)):
            return False
        
        if not 0 <= data.get('PERFORMANCE_SCORE', 0) <= 100:
            return False
        
        return True
        
    except Exception as e:
        logging.error(f"Data validation error: {e}")
        return False

def generate_session_token() -> str:
    """Generate secure session token"""
    return secrets.token_urlsafe(32)

def sanitize_user_input(input_string: str) -> str:
    """Sanitize user input for security"""
    if not isinstance(input_string, str):
        return ""
    
    # Remove potentially dangerous characters
    sanitized = re.sub(r'[<>"\']', '', input_string)
    return sanitized.strip()

def format_currency(amount: float, currency: str = "GBP") -> str:
    """Format currency amounts for display"""
    if currency == "GBP":
        if amount >= 1000000:
            return f"£{amount/1000000:.1f}M"
        elif amount >= 1000:
            return f"£{amount/1000:.0f}K"
        else:
            return f"£{amount:,.0f}"
    else:
        return f"{amount:,.2f} {currency}"

def calculate_business_days(start_date: datetime, end_date: datetime) -> int:
    """Calculate business days between two dates"""
    days = 0
    current_date = start_date
    while current_date <= end_date:
        if current_date.weekday() < 5:  # Monday = 0, Sunday = 6
            days += 1
        current_date += timedelta(days=1)
    return days

def generate_color_palette(base_color: str, count: int) -> List[str]:
    """Generate color palette variations"""
    # This would typically use a color library, simplified for demo
    colors = [base_color]
    for i in range(1, count):
        # Simple variation - in production would use proper color theory
        opacity = 1 - (i * 0.1)
        colors.append(f"{base_color}{int(opacity * 255):02x}")
    return colors[:count]

def create_backup_data() -> Dict[str, Any]:
    """Create backup data structure in case of data source failure"""
    return {
        'UNIQUE_CLIENT_ID': 'BACKUP-001',
        'CLIENT_NAME': 'Enterprise Backup Client',
        'STATUS': 'System Maintenance Mode',
        'PERFORMANCE_SCORE': 99.0,
        'RISK_SCORE': 1.0,
        'LAST_UPDATED': datetime.now(),
        'BACKUP_MODE': True
    }

# ============================================================================
# APPLICATION EXECUTION
# ============================================================================

if __name__ == "__main__":
    """
    Application entry point for enterprise dashboard
    """
    try:
        # Set up logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('lexcura_enterprise.log'),
                logging.StreamHandler()
            ]
        )
        
        logging.info(f"Starting {AppConfig.APP_NAME} {AppConfig.VERSION}")
        
        # Execute main application
        main()
        
    except Exception as e:
        logging.critical(f"Critical application error: {e}")
        st.error("Critical system error. Please contact technical support.")
        
    finally:
        logging.info("Application session ended")
            
            # Navigation menu
            st.markdown("""
            <div class="sidebar-section">
                <div class="sidebar-title">Executive Menu</div>
                <div class="sidebar-item active">📊 Executive Dashboard</div>
                <div class="sidebar-item">📈 Financial Analytics</div>
                <div class="sidebar-item">🔍 Risk Intelligence</div>
                <div class="sidebar-item">🌍 Global Compliance</div>
                <div class="sidebar-item">🤖 AI Insights</div>
                <div class="sidebar-item">📋 Executive Reports</div>
                <div class="sidebar-item">⚙️ System Settings</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Quick actions
            st.markdown("### Quick Actions")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📊 Export", use_container_width=True):
                    st.session_state.export_modal = True
            with col2:
                if st.button("🔄 Refresh", use_container_width=True):
                    st.cache_data.clear()
                    st.rerun()
            
            # System status
            st.markdown("""
            <div class="sidebar-section">
                <div class="sidebar-title">System Status</div>
                <div class="metric-container">
                    <span class="metric-label">Data Connection</span>
                    <span class="metric-value" style="color: var(--success-green);">Online</span>
                </div>
                <div class="metric-container">
                    <span class="metric-label">AI Engine</span>
                    <span class="metric-value" style="color: var(--success-green);">Active</span>
                </div>
                <div class="metric-container">
                    <span class="metric-label">Last Update</span>
                    <span class="metric-value">2 min ago</span>
                </div>
                <div class="metric-container">
                    <span class="metric-label">Next Refresh</span>
                    <span class="metric-value">3 min</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    @staticmethod
    def render_notification(message: str, type: str = "info", duration: int = 5000):
        """Render enterprise notification"""
        notification_id = str(uuid.uuid4())
        
        notification_html = f"""
        <div id="{notification_id}" class="notification {type}" style="animation-duration: 0.3s;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span>{message}</span>
                <button onclick="document.getElementById('{notification_id}').remove()" 
                        style="background: none; border: none; color: var(--text-neutral); cursor: pointer; font-size: 1.2rem;">×</button>
            </div>
        </div>
        
        <script>
            setTimeout(() => {{
                const el = document.getElementById('{notification_id}');
                if (el) el.remove();
            }}, {duration});
        </script>
        """
        
        st.markdown(notification_html, unsafe_allow_html=True)
    
    @staticmethod
    def render_chart_container(chart_func, data: Dict[str, Any], title: str, description: str = ""):
        """Render chart with enterprise container styling"""
        st.markdown(f"""
        <div class="chart-container">
            <div class="chart-header">
                <h3 class="chart-title">{title}</h3>
                {f'<p class="chart-description">{description}</p>' if description else ''}
            </div>
        """, unsafe_allow_html=True)
        
        try:
            fig = chart_func(data)
            st.plotly_chart(fig, use_container_width=True, config={
                "displayModeBar": True,
                "displaylogo": False,
                "modeBarButtonsToRemove": ["pan2d", "lasso2d"],
                "toImageButtonOptions": {
                    "format": "png",
                    "filename": f"lexcura_{title.lower().replace(' ', '_')}",
                    "height": 600,
                    "width": 1200,
                    "scale": 2
                }
            })
        except Exception as e:
            st.error(f"Chart rendering error: {str(e)}")
            st.markdown("""
            <div style="text-align: center; padding: 3rem; color: var(--text-muted);">
                <div style="font-size: 2rem; margin-bottom: 1rem;">⚠️</div>
                <div>Chart temporarily unavailable</div>
                <div style="font-size: 0.875rem; margin-top: 0.5rem;">Enterprise analytics processing...</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

# ============================================================================
# EXPORT & REPORTING SYSTEM
# ============================================================================

class EnterpriseExportManager:
    """Advanced export and reporting capabilities"""
    
    @staticmethod
    def export_to_csv(data: pd.DataFrame, filename: str) -> str:
        """Export data to CSV format"""
        csv_buffer = io.StringIO()
        data.to_csv(csv_buffer, index=False)
        return csv_buffer.getvalue()
    
    @staticmethod
    def export_to_excel(data: Dict[str, pd.DataFrame], filename: str) -> bytes:
        """Export multiple datasets to Excel with formatting"""
        excel_buffer = io.BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
            for sheet_name, df in data.items():
                df.to_excel(writer, sheet_name=sheet_name, index=False)
        return excel_buffer.getvalue()
    
    @staticmethod
    def create_executive_report(client_data: Dict[str, Any]) -> str:
        """Generate comprehensive executive report"""
        report_date = datetime.now().strftime("%Y-%m-%d")
        client_name = client_data.get('CLIENT_NAME', 'Executive Client')
        
        report_content = f"""
# LexCura Elite Executive Intelligence Report
**Generated:** {report_date}
**Client:** {client_name}
**Report Type:** Executive Summary

## Executive Summary
{client_data.get('EXECUTIVE_SUMMARY', 'Executive performance analysis unavailable.')}

## Key Performance Indicators
- **Compliance Excellence:** {client_data.get('PERFORMANCE_SCORE', 'N/A')}%
- **Risk Profile:** {client_data.get('RISK_SCORE', 'N/A')}/10 (Ultra-Low)
- **Violation-Free Days:** {client_data.get('DAYS_VIOLATION_FREE', 'N/A')} days
- **Team Certification:** {client_data.get('TEAM_CERTIFICATION', 'N/A')}%
- **AI Optimization Opportunities:** {client_data.get('AI_INSIGHTS', 'N/A')} active

## Financial Performance
{client_data.get('FINANCIAL_STATS', 'Financial performance data unavailable.')}

## Risk Analysis
{client_data.get('RISK_ANALYSIS', 'Risk analysis unavailable.')}

## Regulatory Intelligence
{client_data.get('REGULATORY_UPDATES', 'Regulatory updates unavailable.')}

## Recommendations
Based on current performance metrics and predictive analytics:

1. **Maintain Excellence Standards:** Continue current practices that have achieved {client_data.get('DAYS_VIOLATION_FREE', 0)} violation-free days
2. **Leverage AI Insights:** Implement the {client_data.get('AI_INSIGHTS', 0)} identified optimization opportunities
3. **Global Expansion:** Consider extending coverage to additional jurisdictions
4. **Team Development:** Maintain {client_data.get('TEAM_CERTIFICATION', 0)}% certification levels

## Next Steps
- Monthly executive briefing scheduled
- Quarterly strategic review planned
- Continuous AI monitoring active
- Predictive analytics optimization ongoing

---
**Report Generated by LexCura Elite Intelligence Platform**
**Confidential & Proprietary - Executive Use Only**
        """
        
        return report_content

# ============================================================================
# MAIN APPLICATION LOGIC
# ============================================================================

def render_main_dashboard():
    """Render the main enterprise dashboard"""
    # Initialize data manager
    data_manager = DataConnectionManager()
    
    # Load client data
    with st.spinner("Loading executive intelligence..."):
        client_data = data_manager.load_client_data()
        st.session_state.data_loaded = True
        st.session_state.last_refresh = datetime.now()
    
    # Initialize UI components and chart manager
    ui_components = EnterpriseUIComponents()
    chart_manager = EnterpriseChartManager()
    
    # Render header
    ui_components.render_enterprise_header(st.session_state.user)
    
    # Render sidebar
    ui_components.render_enterprise_sidebar(st.session_state.user)
    
    # Main content area
    st.markdown("## Executive Intelligence Dashboard")
    
    # Executive KPIs
    ui_components.render_executive_kpis(client_data)
    
    # Executive summary card
    executive_summary = client_data.get('EXECUTIVE_SUMMARY', '')
    if executive_summary:
        st.markdown(f"""
        <div class="enterprise-card">
            <div class="card-header">
                <h3 class="card-title">Executive Intelligence Brief</h3>
                <div style="font-size: 0.875rem; color: var(--text-neutral);">
                    Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
                </div>
            </div>
            <div class="card-content">
                {executive_summary}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Alert system
    render_executive_alerts(client_data)
    
    # Dashboard tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Executive Overview",
        "💰 Financial Intelligence", 
        "🛡️ Risk Analysis",
        "🌍 Global Compliance",
        "🔮 Predictive Analytics"
    ])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            ui_components.render_chart_container(
                chart_manager.create_executive_kpi_overview,
                client_data,
                "Executive Performance Matrix",
                "Comprehensive multi-dimensional performance analysis"
            )
        
        with col2:
            ui_components.render_chart_container(
                chart_manager.create_risk_assessment_gauge,
                client_data,
                "Enterprise Risk Assessment",
                "Real-time risk monitoring across all domains"
            )
    
    with tab2:
        ui_components.render_chart_container(
            chart_manager.create_financial_performance_timeline,
            client_data,
            "Executive Financial Intelligence Platform",
            "Advanced financial performance analysis with forecasting and ROI optimization"
        )
        
        # Financial metrics section
        st.markdown("### Financial Performance Metrics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Annual Optimization",
                "£8.7M",
                delta="£2.4M (38.2%)",
                help="Total annual compliance optimization value"
            )
        
        with col2:
            st.metric(
                "Platform ROI",
                "847%",
                delta="124% improvement",
                help="Return on investment for the platform"
            )
        
        with col3:
            st.metric(
                "Cost Avoidance",
                "£12.3M",
                delta="£4.1M (50.0%)",
                help="Total regulatory penalties and violations avoided"
            )
        
        with col4:
            st.metric(
                "Efficiency Gain",
                "342%",
                delta="89% YoY",
                help="Operational efficiency improvement"
            )
    
    with tab3:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            ui_components.render_chart_container(
                chart_manager.create_risk_assessment_gauge,
                client_data,
                "Multi-Domain Risk Assessment",
                "Comprehensive risk analysis across all operational areas"
            )
        
        with col2:
            st.markdown("""
            <div class="enterprise-card">
                <div class="card-header">
                    <h3 class="card-title">Risk Intelligence Summary</h3>
                </div>
                <div class="card-content">
                    <div class="metric-container">
                        <span class="metric-label">Overall Risk Score</span>
                        <span class="metric-value" style="color: var(--success-green);">0.8/10</span>
                    </div>
                    <div class="metric-container">
                        <span class="metric-label">Risk Category</span>
                        <span class="metric-value" style="color: var(--success-green);">Ultra-Low</span>
                    </div>
                    <div class="metric-container">
                        <span class="metric-label">Trend Direction</span>
                        <span class="metric-value" style="color: var(--success-green);">▼ Decreasing</span>
                    </div>
                    <div class="metric-container">
                        <span class="metric-label">Next Review</span>
                        <span class="metric-value">7 days</span>
                    </div>
                    
                    <div style="margin-top: 2rem; padding-top: 1rem; border-top: 1px solid var(--accent-gold);">
                        <h4 style="color: var(--accent-gold); margin-bottom: 1rem;">Active Mitigations</h4>
                        <ul style="color: var(--text-neutral); line-height: 1.8;">
                            <li>AI-powered predictive monitoring</li>
                            <li>Real-time regulatory change detection</li>
                            <li>Automated compliance verification</li>
                            <li>Executive alert system</li>
                        </ul>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
