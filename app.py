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
import secrets
import time
import logging
from datetime import datetime, timedelta, date
from typing import Dict, List, Optional, Tuple, Any
import io
import base64
from pathlib import Path
import uuid
import re
from dataclasses import dataclass, asdict
from enum import Enum

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
        
        /* ===== NOTIFICATIONS & ALERTS ===== */
        
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
        
        /* ===== RESPONSIVE DESIGN ===== */
        
        @media (max-width: 1200px) {{
            .header-container {{
                grid-template-columns: auto 1fr;
                gap: var(--spacing-md);
            }}
            
            .kpi-grid {{
                grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            }}
        }}
        
        @media (max-width: 768px) {{
            .enterprise-header {{
                padding: var(--spacing-lg);
            }}
            
            .header-container {{
                grid-template-columns: 1fr;
                text-align: center;
            }}
            
            .kpi-grid {{
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            }}
        }}
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
                <p style="color: var(--text-neutral); margin: 0.5rem 0;">Executive Legal Intelligence Platform</p>
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
                time.sleep(1)
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

@st.cache_data(ttl=60, show_spinner=False)
def load_client_data(client_id: Optional[str] = None) -> Dict[str, Any]:
    """Load client data with comprehensive demo data"""
    return {
        'UNIQUE_CLIENT_ID': '11AA-EXEC',
        'CLIENT_NAME': 'Fortune Global Pharmaceuticals Inc.',
        'TIER': 'Executive Premium Elite',
        'REGION': 'Global Multi-Jurisdictional',
        'DELIVERY_FREQUENCY': 'Real-time Intelligence & Predictive Analytics',
        'EMAIL_ADDRESS': 'c-suite@fortuneglobalpharma.com',
        'MAIN_CONTENT': 'Comprehensive executive-grade regulatory intelligence with AI-powered risk prediction, real-time compliance monitoring, strategic legal advisory services, and C-suite executive briefings.',
        'FINANCIAL_STATS': '£8.7M annual compliance optimization, £1.2M platform investment, 847% ROI',
        'HISTORICAL_IMPACTS': 'ROI: 847% over 24 months, zero regulatory penalties, £12.3M in avoided violations',
        'EXECUTIVE_SUMMARY': 'Exceptional executive performance across all regulatory domains. Advanced AI-powered risk prediction has eliminated critical violations while optimizing operational efficiency by 847%. Current performance exceeds all industry benchmarks with 99.7% overall compliance score.',
        'COMPLIANCE_ALERTS': 'Zero critical violations (1,247 days violation-free), 5 proactive optimizations identified',
        'RISK_ANALYSIS': 'Ultra-low risk profile (0.8/10) with predictive monitoring and strategic AI controls',
        'REGULATORY_UPDATES': 'Global regulatory intelligence across 47 jurisdictions, AI-powered trend analysis, executive briefings',
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

# ============================================================================
# ADVANCED CHART CREATION SYSTEM
# ============================================================================

def create_executive_kpi_overview(data: Dict[str, Any]) -> go.Figure:
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
                tickfont=dict(color=BrandColors.HIGH_CONTRAST, size=12),
                gridcolor="rgba(212, 175, 55, 0.2)"
            )
        ),
        title="Executive Performance Matrix",
        showlegend=True
    )
    
    return apply_enterprise_styling(fig, height=450)

def create_financial_performance_timeline(data: Dict[str, Any]) -> go.Figure:
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

def create_compliance_heatmap(data: Dict[str, Any]) -> go.Figure:
    """Global compliance performance heatmap"""
    regulations = ['FDA 21 CFR 211', 'USP 797', 'USP 800', 'EU GMP Annex 1', 
                   'MHRA Orange Guide', 'Health Canada GUI-0104', 'TGA PIC/S', 
                   'ISO 13485', 'ICH Q7', 'ISPE Baseline']
    
    regions = ['North America', 'Europe', 'UK & Ireland', 'Asia Pacific', 
               'Latin America', 'Middle East']
    
    # Compliance scores matrix
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

def create_risk_assessment_gauge(data: Dict[str, Any]) -> go.Figure:
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

# ============================================================================
# PREMIUM UI COMPONENTS SYSTEM
# ============================================================================

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

def render_enterprise_sidebar(user: Optional[User] = None):
    """Render comprehensive enterprise sidebar"""
    with st.sidebar:
        # User profile section
        if user:
            st.markdown(f"""
            <div class="enterprise-card">
                <div class="card-header">
                    <h4 class="card-title">Executive Profile</h4>
                </div>
                <div class="card-content">
                    <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
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
        
        # Quick actions
        st.markdown("### Quick Actions")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📊 Export", use_container_width=True):
                st.success("Export initiated")
        with col2:
            if st.button("🔄 Refresh", use_container_width=True):
                st.cache_data.clear()
                st.rerun()
        
        # System status
        st.markdown("""
        <div class="enterprise-card">
            <div class="card-header">
                <h4 class="card-title">System Status</h4>
            </div>
            <div class="card-content">
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
            </div>
        </div>
        """, unsafe_allow_html=True)

def render_chart_container(chart_func, data: Dict[str, Any], title: str, description: str = ""):
    """Render chart with enterprise container styling"""
    st.markdown(f"""
    <div class="chart-container">
        <div class="chart-header">
            <h3 class="chart-title">{title}</h3>
            {f'<p style="color: var(--text-neutral); font-style: italic; text-align: center;">{description}</p>' if description else ''}
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
        <div style="text-align: center; padding: 3rem; color: var(--text-neutral);">
            <div style="font-size: 2rem; margin-bottom: 1rem;">⚠️</div>
            <div>Chart temporarily unavailable</div>
            <div style="font-size: 0.875rem; margin-top: 0.5rem;">Enterprise analytics processing...</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

def render_executive_alerts(client_data: Dict[str, Any]):
    """Render executive-grade alert system"""
    st.markdown("### Executive Status Intelligence")
    
    alert_level = client_data.get('ALERT_LEVEL', 'OPTIMAL')
    
    if alert_level == 'OPTIMAL EXCELLENCE':
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

# ============================================================================
# MAIN APPLICATION LOGIC
# ============================================================================

def render_main_dashboard():
    """Render the main enterprise dashboard"""
    
    # Load client data
    with st.spinner("Loading executive intelligence..."):
        client_data = load_client_data()
        st.session_state.data_loaded = True
        st.session_state.last_refresh = datetime.now()
    
    # Render header
    render_enterprise_header(st.session_state.user)
    
    # Render sidebar
    render_enterprise_sidebar(st.session_state.user)
    
    # Main content area
    st.markdown("## Executive Intelligence Dashboard")
    
    # Executive KPIs
    render_executive_kpis(client_data)
    
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
            render_chart_container(
                create_executive_kpi_overview,
                client_data,
                "Executive Performance Matrix",
                "Comprehensive multi-dimensional performance analysis"
            )
        
        with col2:
            render_chart_container(
                create_risk_assessment_gauge,
                client_data,
                "Enterprise Risk Assessment",
                "Real-time risk monitoring across all domains"
            )
    
    with tab2:
        render_chart_container(
            create_financial_performance_timeline,
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
            render_chart_container(
                create_risk_assessment_gauge,
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
    
    with tab4:
        render_chart_container(
            create_compliance_heatmap,
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
        st.markdown("### AI-Powered Predictive Intelligence")
        
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
    
    # Initialize Plotly theme
    create_enterprise_plotly_theme()
    
    # Main application logic for authenticated users
    try:
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
        
        # Logout button
        if st.sidebar.button("🚪 Logout", use_container_width=True):
            auth_manager = AuthenticationManager()
            auth_manager.logout_user()
        
    except Exception as e:
        st.error(f"Application error: {str(e)}")
        logging.error(f"Application error: {e}")

# ============================================================================
# APPLICATION EXECUTION
# ============================================================================

if __name__ == "__main__":
    """Application entry point for enterprise dashboard"""
    try:
        # Set up logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        logging.info(f"Starting {AppConfig.APP_NAME} {AppConfig.VERSION}")
        
        # Execute main application
        main()
        
    except Exception as e:
        logging.critical(f"Critical application error: {e}")
        st.error("Critical system error. Please contact technical support.")
    
    finally:
        logging.info("Application session ended")
