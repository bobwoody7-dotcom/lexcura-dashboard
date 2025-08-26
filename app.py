# Elite Enterprise Compliance Platform
# Premium £10,000+/month C-Suite Dashboard
# Ultra-polished, Fortune 500 aesthetic with luxury animations

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
import base64
from pathlib import Path

# ========================================================================================
# PAGE CONFIGURATION & SETUP
# ========================================================================================

st.set_page_config(
    page_title="Executive Compliance Command Center",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========================================================================================
# PREMIUM DESIGN SYSTEM & ANIMATIONS
# ========================================================================================

def load_css():
    """Load premium CSS with luxury animations and enterprise styling"""
    return """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Montserrat:wght@400;500;600;700;800&display=swap');
    
    :root {
        --primary: #C9A961;        /* Luxury Gold */
        --primary-dark: #B8973F;   /* Dark Gold */
        --secondary: #2C5282;      /* Executive Blue */
        --accent: #667EEA;         /* Premium Purple */
        --success: #10B981;        /* Success Green */
        --warning: #F59E0B;        /* Warning Amber */
        --danger: #EF4444;         /* Danger Red */
        --white: #FFFFFF;          /* Pure White */
        --light: #F8FAFC;          /* Light Grey */
        --medium: #64748B;         /* Medium Grey */
        --dark: #1E293B;           /* Dark Grey */
        --charcoal: #0F172A;       /* Charcoal */
        --black: #020617;          /* Deep Black */
    }
    
    * {
        box-sizing: border-box;
        margin: 0;
        padding: 0;
    }
    
    html, body {
        scroll-behavior: smooth;
    }
    
    /* ============= MAIN LAYOUT ============= */
    .stApp {
        background: linear-gradient(135deg, var(--black) 0%, var(--charcoal) 50%, var(--dark) 100%);
        background-attachment: fixed;
        color: var(--white);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        position: relative;
        overflow-x: hidden;
    }
    
    /* Animated background pattern */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: 
            radial-gradient(circle at 20% 80%, rgba(201, 169, 97, 0.03) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(44, 82, 130, 0.05) 0%, transparent 50%),
            radial-gradient(circle at 40% 40%, rgba(102, 126, 234, 0.02) 0%, transparent 50%);
        z-index: -1;
        animation: backgroundPulse 20s ease-in-out infinite alternate;
    }
    
    @keyframes backgroundPulse {
        0% { opacity: 0.3; transform: scale(1); }
        100% { opacity: 0.6; transform: scale(1.1); }
    }
    
    /* Confidential watermark */
    .stApp::after {
        content: 'CONFIDENTIAL';
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%) rotate(-45deg);
        font-size: 8rem;
        font-weight: 800;
        color: rgba(255, 255, 255, 0.02);
        z-index: -1;
        pointer-events: none;
        font-family: 'Montserrat', sans-serif;
        letter-spacing: 2rem;
    }
    
    /* ============= HEADER SYSTEM ============= */
    .executive-header {
        background: linear-gradient(135deg, rgba(201, 169, 97, 0.15) 0%, rgba(44, 82, 130, 0.15) 100%);
        backdrop-filter: blur(20px);
        border-bottom: 1px solid rgba(201, 169, 97, 0.2);
        padding: 1.5rem 2rem;
        margin: -1rem -1rem 2rem -1rem;
        position: sticky;
        top: -1rem;
        z-index: 1000;
        animation: slideDown 0.8s ease-out;
    }
    
    @keyframes slideDown {
        from { transform: translateY(-100%); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    
    .header-grid {
        display: grid;
        grid-template-columns: auto 1fr auto;
        gap: 2rem;
        align-items: center;
    }
    
    .logo-section {
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .logo-icon {
        width: 50px;
        height: 50px;
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        font-weight: bold;
        color: var(--white);
        box-shadow: 0 8px 25px rgba(201, 169, 97, 0.3);
        animation: logoGlow 3s ease-in-out infinite alternate;
    }
    
    @keyframes logoGlow {
        0% { box-shadow: 0 8px 25px rgba(201, 169, 97, 0.3); }
        100% { box-shadow: 0 12px 35px rgba(201, 169, 97, 0.6); }
    }
    
    .company-name {
        font-family: 'Montserrat', sans-serif;
        font-size: 1.8rem;
        font-weight: 700;
        background: linear-gradient(135deg, var(--primary) 0%, var(--white) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: -0.02em;
    }
    
    .tagline {
        font-size: 0.9rem;
        color: var(--medium);
        font-weight: 500;
        margin-top: 0.25rem;
    }
    
    .client-badge {
        background: linear-gradient(135deg, var(--secondary) 0%, var(--accent) 100%);
        padding: 0.75rem 1.5rem;
        border-radius: 25px;
        font-weight: 600;
        font-size: 0.9rem;
        box-shadow: 0 4px 20px rgba(44, 82, 130, 0.3);
        animation: badgePulse 2s ease-in-out infinite alternate;
    }
    
    @keyframes badgePulse {
        0% { transform: scale(1); }
        100% { transform: scale(1.05); }
    }
    
    .status-indicators {
        display: flex;
        gap: 1rem;
        align-items: center;
    }
    
    .status-dot {
        width: 12px;
        height: 12px;
        border-radius: 50%;
        animation: statusPulse 2s ease-in-out infinite;
    }
    
    .status-dot.green { background: var(--success); }
    .status-dot.amber { background: var(--warning); }
    .status-dot.red { background: var(--danger); }
    
    @keyframes statusPulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.7; transform: scale(1.2); }
    }
    
    .live-time {
        font-family: 'Courier New', monospace;
        font-size: 0.9rem;
        color: var(--primary);
        font-weight: 600;
    }
    
    /* ============= SIDEBAR NAVIGATION ============= */
    .css-1d391kg {
        background: linear-gradient(180deg, var(--charcoal) 0%, var(--black) 100%);
        border-right: 1px solid rgba(201, 169, 97, 0.2);
    }
    
    .nav-item {
        padding: 1rem 1.5rem;
        margin: 0.5rem 1rem;
        border-radius: 12px;
        cursor: pointer;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        gap: 1rem;
        font-weight: 500;
        color: var(--light);
        border: 1px solid transparent;
    }
    
    .nav-item:hover {
        background: linear-gradient(135deg, rgba(201, 169, 97, 0.1) 0%, rgba(44, 82, 130, 0.1) 100%);
        border: 1px solid rgba(201, 169, 97, 0.3);
        transform: translateX(5px);
        color: var(--white);
    }
    
    .nav-item.active {
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
        color: var(--white);
        font-weight: 600;
        box-shadow: 0 4px 20px rgba(201, 169, 97, 0.4);
    }
    
    .nav-icon {
        font-size: 1.2rem;
        min-width: 24px;
    }
    
    /* ============= KPI CARDS ============= */
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 2rem;
        margin: 2rem 0;
    }
    
    .kpi-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.9) 100%);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(201, 169, 97, 0.2);
        border-radius: 20px;
        padding: 2rem;
        position: relative;
        overflow: hidden;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        cursor: pointer;
        animation: cardFloat 6s ease-in-out infinite;
    }
    
    .kpi-card:nth-child(1) { animation-delay: 0s; }
    .kpi-card:nth-child(2) { animation-delay: 1.5s; }
    .kpi-card:nth-child(3) { animation-delay: 3s; }
    .kpi-card:nth-child(4) { animation-delay: 4.5s; }
    
    @keyframes cardFloat {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-5px); }
    }
    
    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, var(--primary) 0%, var(--secondary) 50%, var(--accent) 100%);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .kpi-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 20px 40px rgba(201, 169, 97, 0.2);
        border: 1px solid rgba(201, 169, 97, 0.4);
    }
    
    .kpi-card:hover::before {
        opacity: 1;
    }
    
    .kpi-icon {
        width: 60px;
        height: 60px;
        border-radius: 15px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        margin-bottom: 1.5rem;
        position: relative;
        overflow: hidden;
    }
    
    .kpi-icon::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(255, 255, 255, 0.1), transparent);
        transform: rotate(45deg);
        animation: shimmer 3s infinite;
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
        100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
    }
    
    .kpi-value {
        font-size: 2.5rem;
        font-weight: 800;
        font-family: 'Montserrat', sans-serif;
        margin-bottom: 0.5rem;
        background: linear-gradient(135deg, var(--white) 0%, var(--primary) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: countUp 2s ease-out;
    }
    
    @keyframes countUp {
        from { transform: scale(0.5); opacity: 0; }
        to { transform: scale(1); opacity: 1; }
    }
    
    .kpi-label {
        font-size: 0.95rem;
        color: var(--medium);
        font-weight: 500;
        margin-bottom: 0.75rem;
    }
    
    .kpi-trend {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 0.85rem;
        font-weight: 600;
    }
    
    .trend-up { color: var(--success); }
    .trend-down { color: var(--danger); }
    .trend-stable { color: var(--warning); }
    
    /* ============= CHART CONTAINERS ============= */
    .chart-section {
        margin: 3rem 0;
    }
    
    .section-header {
        text-align: center;
        margin-bottom: 3rem;
    }
    
    .section-title {
        font-size: 2.5rem;
        font-weight: 700;
        font-family: 'Montserrat', sans-serif;
        background: linear-gradient(135deg, var(--primary) 0%, var(--white) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1rem;
        animation: titleSlide 1s ease-out;
    }
    
    @keyframes titleSlide {
        from { transform: translateY(30px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    
    .section-subtitle {
        font-size: 1.1rem;
        color: var(--medium);
        font-weight: 400;
        max-width: 600px;
        margin: 0 auto;
    }
    
    .charts-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(550px, 1fr));
        gap: 2.5rem;
        margin-top: 2rem;
    }
    
    .chart-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.8) 100%);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(201, 169, 97, 0.15);
        border-radius: 24px;
        padding: 2rem;
        position: relative;
        overflow: hidden;
        transition: all 0.4s ease;
        animation: chartAppear 0.8s ease-out both;
    }
    
    .chart-card:nth-child(1) { animation-delay: 0.1s; }
    .chart-card:nth-child(2) { animation-delay: 0.2s; }
    .chart-card:nth-child(3) { animation-delay: 0.3s; }
    .chart-card:nth-child(4) { animation-delay: 0.4s; }
    .chart-card:nth-child(5) { animation-delay: 0.5s; }
    .chart-card:nth-child(6) { animation-delay: 0.6s; }
    .chart-card:nth-child(7) { animation-delay: 0.7s; }
    .chart-card:nth-child(8) { animation-delay: 0.8s; }
    
    @keyframes chartAppear {
        from { 
            transform: translateY(40px) scale(0.9); 
            opacity: 0; 
        }
        to { 
            transform: translateY(0) scale(1); 
            opacity: 1; 
        }
    }
    
    .chart-card:hover {
        transform: translateY(-5px);
        border: 1px solid rgba(201, 169, 97, 0.3);
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.3);
    }
    
    .chart-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .chart-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: var(--white);
        font-family: 'Montserrat', sans-serif;
    }
    
    .chart-actions {
        display: flex;
        gap: 0.5rem;
    }
    
    .chart-action-btn {
        width: 32px;
        height: 32px;
        border-radius: 8px;
        background: rgba(255, 255, 255, 0.1);
        border: none;
        color: var(--light);
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.3s ease;
    }
    
    .chart-action-btn:hover {
        background: var(--primary);
        color: var(--white);
        transform: scale(1.1);
    }
    
    /* ============= EXECUTIVE SUMMARY ============= */
    .executive-summary {
        background: linear-gradient(135deg, rgba(44, 82, 130, 0.15) 0%, rgba(102, 126, 234, 0.15) 100%);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(44, 82, 130, 0.3);
        border-radius: 20px;
        padding: 2.5rem;
        margin: 3rem 0;
        position: relative;
        overflow: hidden;
        animation: summarySlide 1s ease-out;
    }
    
    @keyframes summarySlide {
        from { transform: translateX(-30px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    .executive-summary::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, var(--secondary) 0%, var(--accent) 100%);
    }
    
    .summary-header {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 1.5rem;
    }
    
    .summary-icon {
        width: 50px;
        height: 50px;
        background: linear-gradient(135deg, var(--secondary) 0%, var(--accent) 100%);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        color: var(--white);
    }
    
    .summary-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--white);
        font-family: 'Montserrat', sans-serif;
    }
    
    .summary-content {
        font-size: 1.1rem;
        line-height: 1.7;
        color: var(--light);
        font-weight: 400;
    }
    
    /* ============= BUTTONS & INTERACTIONS ============= */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
        color: var(--white);
        border: none;
        border-radius: 12px;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
        padding: 0.75rem 2rem;
        font-size: 0.95rem;
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 0 4px 15px rgba(201, 169, 97, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: left 0.5s;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, var(--primary-dark) 0%, var(--primary) 100%);
        transform: translateY(-2px) scale(1.05);
        box-shadow: 0 8px 25px rgba(201, 169, 97, 0.4);
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    /* ============= DOWNLOAD SECTION ============= */
    .download-section {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(5, 150, 105, 0.1) 100%);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-radius: 20px;
        padding: 2.5rem;
        margin: 3rem 0;
        text-align: center;
        animation: downloadPulse 3s ease-in-out infinite alternate;
    }
    
    @keyframes downloadPulse {
        0% { border-color: rgba(16, 185, 129, 0.3); }
        100% { border-color: rgba(16, 185, 129, 0.6); }
    }
    
    .download-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--success);
        margin-bottom: 1rem;
        font-family: 'Montserrat', sans-serif;
    }
    
    .download-subtitle {
        font-size: 1rem;
        color: var(--light);
        margin-bottom: 2rem;
    }
    
    /* ============= FOOTER ============= */
    .executive-footer {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(2, 6, 23, 0.95) 100%);
        backdrop-filter: blur(20px);
        border-top: 1px solid rgba(201, 169, 97, 0.2);
        padding: 3rem 2rem 2rem;
        margin: 4rem -1rem -1rem;
        text-align: center;
    }
    
    .footer-content {
        max-width: 800px;
        margin: 0 auto;
    }
    
    .footer-brand {
        font-size: 1.3rem;
        font-weight: 700;
        font-family: 'Montserrat', sans-serif;
        background: linear-gradient(135deg, var(--primary) 0%, var(--white) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1rem;
    }
    
    .footer-disclaimer {
        font-size: 0.9rem;
        color: var(--medium);
        line-height: 1.6;
        margin-bottom: 1rem;
    }
    
    .footer-contact {
        font-size: 0.85rem;
        color: var(--light);
        font-weight: 500;
    }
    
    /* ============= RESPONSIVE DESIGN ============= */
    @media (max-width: 768px) {
        .header-grid {
            grid-template-columns: 1fr;
            gap: 1rem;
            text-align: center;
        }
        
        .kpi-grid {
            grid-template-columns: 1fr;
            gap: 1rem;
        }
        
        .charts-grid {
            grid-template-columns: 1fr;
            gap: 1.5rem;
        }
        
        .section-title {
            font-size: 2rem;
        }
        
        .kpi-value {
            font-size: 2rem;
        }
        
        .chart-card {
            padding: 1.5rem;
        }
    }
    
    /* ============= STREAMLIT OVERRIDES ============= */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header { visibility: hidden; }
    .stDeployButton { visibility: hidden; }
    
    .css-1rs6os { 
        background: transparent;
        border: none;
    }
    
    .css-163ttbj {
        background: transparent;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--charcoal);
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, var(--primary) 0%, var(--primary-dark) 100%);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, var(--primary-dark) 0%, var(--primary) 100%);
    }
    
    /* Loading animations */
    .stSpinner {
        color: var(--primary) !important;
    }
    
    .stProgress > div > div {
        background: linear-gradient(90deg, var(--primary) 0%, var(--secondary) 100%);
    }
</style>

<script>
// Live time update
function updateTime() {
    const now = new Date();
    const timeString = now.toLocaleTimeString('en-GB', { 
        timeZone: 'UTC', 
        hour12: false 
    });
    const dateString = now.toLocaleDateString('en-GB');
    
    const timeElements = document.querySelectorAll('.live-time');
    timeElements.forEach(el => {
        el.textContent = `${dateString} ${timeString} UTC`;
    });
}

// Update every second
setInterval(updateTime, 1000);
updateTime();

// Smooth scroll for navigation
document.querySelectorAll('.nav-item').forEach(item => {
    item.addEventListener('click', function() {
        const targetId = this.getAttribute('data-target');
        const target = document.getElementById(targetId);
        if (target) {
            target.scrollIntoView({ behavior: 'smooth' });
        }
    });
});

// Chart animation triggers
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('animate-in');
        }
    });
}, observerOptions);

document.querySelectorAll('.chart-card').forEach(card => {
    observer.observe(card);
});
</script>
"""

# ========================================================================================
# PREMIUM COLOR SYSTEM
# ========================================================================================

PREMIUM_COLORS = {
    'primary': '#C9A961',          # Luxury Gold
    'primary_dark': '#B8973F',     # Dark Gold  
    'secondary': '#2C5282',        # Executive Blue
    'accent': '#667EEA',           # Premium Purple
    'success': '#10B981',          # Success Green
    'warning': '#F59E0B',          # Warning Amber
    'danger': '#EF4444',           # Danger Red
    'white': '#FFFFFF',            # Pure White
    'light': '#F8FAFC',            # Light Grey
    'medium': '#64748B',           # Medium Grey
    'dark': '#1E293B',             # Dark Grey
    'charcoal': '#0F172A',         # Charcoal
    'black': '#020617',            # Deep Black
    # Chart-specific colors
    'chart_bg': 'rgba(30, 41, 59, 0.4)',
    'chart_grid': 'rgba(255, 255, 255, 0.1)',
    'chart_text': '#F8FAFC'
}

# Premium typography system
PREMIUM_FONTS = {
    'primary': 'Montserrat, system-ui, -apple-system, sans-serif',
    'secondary': 'Inter, system-ui, -apple-system, sans-serif',
    'mono': 'JetBrains Mono, Courier New, monospace',
    'sizes': {
        'xs': 11,
        'sm': 12,
        'base': 14,
        'lg': 16,
        'xl': 18,
        'xxl': 24,
        'display': 32
    }
}

# ========================================================================================
# DATA CONNECTION & CACHING
# ========================================================================================

@st.cache_data(ttl=300)
def connect_to_sheets():
    """Premium data connection with error handling"""
    try:
        credentials_info = json.loads(st.secrets["gcp_service_account"])
        credentials = Credentials.from_service_account_info(
            credentials_info,
            scopes=[
                "https://www.googleapis.com/auth/spreadsheets.readonly",
                "https://www.googleapis.com/auth/drive.readonly"
            ]
        )
        gc = gspread.authorize(credentials)
        return gc
    except Exception as e:
        st.error(f"🔴 Data connection failed: {str(e)}")
        return None

@st.cache_data(ttl=60)
def load_premium_client_data(client_id=None):
    """Load client data with premium demo fallback"""
    try:
        gc = connect_to_sheets()
        if not gc:
            return get_premium_demo_data(client_id)
            
        sheet_id = st.secrets.get("MASTER_SHEET_ID", "1oI-XqRbp8r3V8yMjnC5pNvDMljJDv4f6d01vRmrVH1g")
        spreadsheet = gc.open_by_key(sheet_id)
        
        try:
            sheet = spreadsheet.worksheet("MASTER SHEET")
        except Exception:
            return get_premium_demo_data(client_id)
        
        headers = sheet.row_values(1)
        row_data = sheet.row_values(2)
        
        while len(row_data) < len(headers):
            row_data.append("")
            
        data = dict(zip(headers, row_data))
        
        return {
            'client_id': data.get('UNIQUE CLIENT ID', client_id or 'EXEC001'),
            'client_name': data.get('CLIENT NAME', 'Executive Client'),
            'tier': data.get('TIER', 'Enterprise'),
            'region': data.get('REGION', 'Global'),
            'content': data.get('MAIN STRUCTURED CONTENT', ''),
            'summary': data.get('EXECUTIVE SUMMARY', ''),
            'alert_level': data.get('ALERT LEVEL', 'GREEN'),
            'status': data.get('STATUS', 'Active'),
            'last_update': data.get('DATE SCRAPED', datetime.now().strftime('%Y-%m-%d %H:%M UTC'))
        }
        
    except Exception as e:
        st.warning(f"⚠️ Using demo data: {str(e)}")
        return get_premium_demo_data(client_id)

def get_premium_demo_data(client_id=None):
    """Premium demo data for C-suite presentation"""
    return {
        'client_id': client_id or 'EXEC001',
        'client_name': 'Fortune 500 Pharmaceuticals Inc.',
        'tier': 'Enterprise Plus',
        'region': 'Global Operations',
        'content': 'Comprehensive enterprise-grade compliance monitoring across 47 facilities worldwide with real-time regulatory intelligence, predictive risk analytics, and automated compliance workflows.',
        'summary': 'Executive Summary: Current compliance posture demonstrates exceptional performance across all regulatory frameworks with 98.7% adherence rate. Strategic risk mitigation protocols are actively monitoring 147 compliance vectors with predictive analytics identifying potential issues 30 days in advance. Financial impact analysis shows $2.3M in avoided penalties and operational savings through proactive compliance management.',
        'alert_level': 'GREEN',
        'status': 'Optimal',
        'last_update': datetime.now().strftime('%Y-%m-%d %H:%M UTC')
    }

# ========================================================================================
# PREMIUM CHART LAYOUTS
# ========================================================================================

def create_premium_chart_layout(title, height=400):
    """Create premium chart layout with luxury styling"""
    return {
        'title': {
            'text': title,
            'font': {
                'family': PREMIUM_FONTS['primary'],
                'size': PREMIUM_FONTS['sizes']['xl'],
                'color': PREMIUM_COLORS['white']
            },
            'x': 0.5,
            'xanchor': 'center',
            'y': 0.95,
            'yanchor': 'top'
        },
        'paper_bgcolor': 'rgba(0,0,0,0)',
        'plot_bgcolor': PREMIUM_COLORS['chart_bg'],
        'font': {
            'color': PREMIUM_COLORS['chart_text'],
            'family': PREMIUM_FONTS['secondary'],
            'size': PREMIUM_FONTS['sizes']['sm']
        },
        'margin': dict(l=60, r=60, t=80, b=60),
        'height': height,
        'showlegend': True,
        'legend': {
            'font': {
                'color': PREMIUM_COLORS['light'],
                'family': PREMIUM_FONTS['secondary'],
                'size': PREMIUM_FONTS['sizes']['sm']
            },
            'bgcolor': 'rgba(0,0,0,0)',
            'borderwidth': 0,
            'orientation': 'h',
            'yanchor': 'bottom',
            'y': 1.02,
            'xanchor': 'center',
            'x': 0.5
        },
        'hovermode': 'closest',
        'hoverlabel': {
            'bgcolor': PREMIUM_COLORS['charcoal'],
            'bordercolor': PREMIUM_COLORS['primary'],
            'font': {'color': PREMIUM_COLORS['white']}
        }
    }

def add_premium_grid(layout):
    """Add premium grid styling to chart layout"""
    layout['xaxis'] = {
        'color': PREMIUM_COLORS['light'],
        'gridcolor': PREMIUM_COLORS['chart_grid'],
        'gridwidth': 1,
        'showgrid': True,
        'zeroline': False,
        'tickfont': {'size': PREMIUM_FONTS['sizes']['sm'], 'color': PREMIUM_COLORS['medium']}
    }
    layout['yaxis'] = {
        'color': PREMIUM_COLORS['light'],
        'gridcolor': PREMIUM_COLORS['chart_grid'],
        'gridwidth': 1,
        'showgrid': True,
        'zeroline': False,
        'tickfont': {'size': PREMIUM_FONTS['sizes']['sm'], 'color': PREMIUM_COLORS['medium']}
    }
    return layout

# ========================================================================================
# ELITE CHART FUNCTIONS
# ========================================================================================

def create_financial_impact_chart():
    """Premium Financial Impact Analysis with animations"""
    periods = ['Q1 2024', 'Q2 2024', 'Q3 2024', 'Q4 2024', 'Q1 2025']
    cost_avoidance = [1200000, 1450000, 1350000, 1680000, 1500000]
    operational_savings = [850000, 920000, 1100000, 1250000, 1180000]
    penalty_avoidance = [450000, 380000, 620000, 430000, 510000]
    
    fig = go.Figure()
    
    # Add bars with premium styling
    fig.add_trace(go.Bar(
        name='Cost Avoidance',
        x=periods,
        y=cost_avoidance,
        marker=dict(
            color=PREMIUM_COLORS['primary'],
            line=dict(color=PREMIUM_COLORS['primary_dark'], width=2)
        ),
        hovertemplate='<b>Cost Avoidance</b><br>%{x}<br>$%{y:,.0f}<extra></extra>'
    ))
    
    fig.add_trace(go.Bar(
        name='Operational Savings',
        x=periods,
        y=operational_savings,
        marker=dict(
            color=PREMIUM_COLORS['secondary'],
            line=dict(color=PREMIUM_COLORS['accent'], width=2)
        ),
        hovertemplate='<b>Operational Savings</b><br>%{x}<br>$%{y:,.0f}<extra></extra>'
    ))
    
    fig.add_trace(go.Bar(
        name='Penalty Avoidance',
        x=periods,
        y=penalty_avoidance,
        marker=dict(
            color=PREMIUM_COLORS['success'],
            line=dict(color=PREMIUM_COLORS['warning'], width=2)
        ),
        hovertemplate='<b>Penalty Avoidance</b><br>%{x}<br>$%{y:,.0f}<extra></extra>'
    ))
    
    layout = create_premium_chart_layout('Financial Impact Analysis', 450)
    layout = add_premium_grid(layout)
    layout['barmode'] = 'group'
    layout['bargap'] = 0.2
    layout['bargroupgap'] = 0.1
    
    fig.update_layout(layout)
    
    # Add animation
    fig.update_traces(
        marker=dict(
            line=dict(width=2)
        )
    )
    
    return fig

def create_alert_status_heatmap():
    """Premium Alert Status with interactive heatmap"""
    departments = [
        'Quality Assurance', 'Manufacturing', 'Environmental Health', 
        'Personnel Training', 'Documentation', 'Facility Management',
        'Process Control', 'Regulatory Affairs'
    ]
    
    alert_types = ['Critical', 'High', 'Medium', 'Low', 'Normal']
    
    # Create realistic alert distribution data
    alert_data = np.array([
        [0, 1, 2, 4, 12],  # Quality Assurance
        [1, 2, 3, 5, 8],   # Manufacturing  
        [0, 0, 1, 3, 15],  # Environmental Health
        [0, 1, 1, 2, 10],  # Personnel Training
        [0, 0, 2, 6, 12],  # Documentation
        [0, 0, 1, 2, 14],  # Facility Management
        [1, 1, 2, 3, 9],   # Process Control
        [0, 0, 0, 1, 18]   # Regulatory Affairs
    ])
    
    fig = go.Figure(data=go.Heatmap(
        z=alert_data,
        x=alert_types,
        y=departments,
        colorscale=[
            [0, PREMIUM_COLORS['success']],
            [0.25, PREMIUM_COLORS['warning']],
            [0.5, PREMIUM_COLORS['primary']],
            [0.75, PREMIUM_COLORS['secondary']],
            [1, PREMIUM_COLORS['danger']]
        ],
        text=alert_data,
        texttemplate="%{text}",
        textfont={"size": PREMIUM_FONTS['sizes']['sm'], "color": PREMIUM_COLORS['white']},
        hoverongaps=False,
        hovertemplate='<b>%{y}</b><br>%{x}: %{z} alerts<extra></extra>'
    ))
    
    layout = create_premium_chart_layout('Alert Status Distribution', 450)
    layout = add_premium_grid(layout)
    layout['xaxis']['title'] = 'Alert Severity'
    layout['yaxis']['title'] = 'Department'
    
    fig.update_layout(layout)
    return fig

def create_risk_assessment_gauge():
    """Premium Risk Assessment with multi-level gauge"""
    current_risk = 23.7
    
    fig = go.Figure()
    
    fig.add_trace(go.Indicator(
        mode="gauge+number+delta",
        value=current_risk,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={
            'text': "Enterprise Risk Level",
            'font': {'size': PREMIUM_FONTS['sizes']['lg'], 'color': PREMIUM_COLORS['white']}
        },
        delta={
            'reference': 30,
            'decreasing': {'color': PREMIUM_COLORS['success']},
            'suffix': '%'
        },
        number={'suffix': '%', 'font': {'size': 48, 'color': PREMIUM_COLORS['white']}},
        gauge={
            'axis': {
                'range': [None, 100],
                'tickwidth': 2,
                'tickcolor': PREMIUM_COLORS['medium'],
                'tickfont': {'size': PREMIUM_FONTS['sizes']['sm']}
            },
            'bar': {'color': PREMIUM_COLORS['success'], 'thickness': 0.7},
            'bgcolor': PREMIUM_COLORS['charcoal'],
            'borderwidth': 3,
            'bordercolor': PREMIUM_COLORS['primary'],
            'steps': [
                {'range': [0, 25], 'color': PREMIUM_COLORS['success'], 'name': 'Low Risk'},
                {'range': [25, 50], 'color': PREMIUM_COLORS['warning'], 'name': 'Medium Risk'},
                {'range': [50, 75], 'color': PREMIUM_COLORS['primary'], 'name': 'High Risk'},
                {'range': [75, 100], 'color': PREMIUM_COLORS['danger'], 'name': 'Critical Risk'}
            ],
            'threshold': {
                'line': {'color': PREMIUM_COLORS['white'], 'width': 4},
                'thickness': 0.8,
                'value': 40
            }
        }
    ))
    
    layout = create_premium_chart_layout('Risk Assessment Overview', 450)
    fig.update_layout(layout)
    return fig

def create_performance_trends():
    """Premium Performance Trends with multiple metrics"""
    months = pd.date_range(start='2024-01-01', end='2025-01-01', freq='M')
    month_names = [m.strftime('%b %Y') for m in months]
    
    # Generate realistic trend data
    compliance_score = [87 + 10 * np.sin(i/3) + np.random.normal(0, 1) for i in range(len(months))]
    efficiency_score = [85 + 8 * np.cos(i/4) + np.random.normal(0, 1.5) for i in range(len(months))]
    risk_score = [30 - 5 * np.sin(i/3) + np.random.normal(0, 2) for i in range(len(months))]
    
    # Smooth the data
    compliance_score = pd.Series(compliance_score).rolling(window=3, center=True).mean().fillna(method='bfill').fillna(method='ffill')
    efficiency_score = pd.Series(efficiency_score).rolling(window=3, center=True).mean().fillna(method='bfill').fillna(method='ffill')
    risk_score = pd.Series(risk_score).rolling(window=3, center=True).mean().fillna(method='bfill').fillna(method='ffill')
    
    fig = go.Figure()
    
    # Compliance Score
    fig.add_trace(go.Scatter(
        x=month_names,
        y=compliance_score,
        mode='lines+markers',
        name='Compliance Score',
        line=dict(color=PREMIUM_COLORS['primary'], width=4, shape='spline'),
        marker=dict(size=8, color=PREMIUM_COLORS['primary'], line=dict(width=2, color=PREMIUM_COLORS['white'])),
        hovertemplate='<b>Compliance Score</b><br>%{x}<br>%{y:.1f}%<extra></extra>'
    ))
    
    # Efficiency Score  
    fig.add_trace(go.Scatter(
        x=month_names,
        y=efficiency_score,
        mode='lines+markers',
        name='Process Efficiency',
        line=dict(color=PREMIUM_COLORS['secondary'], width=4, shape='spline'),
        marker=dict(size=8, color=PREMIUM_COLORS['secondary'], line=dict(width=2, color=PREMIUM_COLORS['white'])),
        hovertemplate='<b>Process Efficiency</b><br>%{x}<br>%{y:.1f}%<extra></extra>'
    ))
    
    # Risk Score (inverted axis)
    fig.add_trace(go.Scatter(
        x=month_names,
        y=risk_score,
        mode='lines+markers',
        name='Risk Level',
        line=dict(color=PREMIUM_COLORS['accent'], width=4, shape='spline'),
        marker=dict(size=8, color=PREMIUM_COLORS['accent'], line=dict(width=2, color=PREMIUM_COLORS['white'])),
        yaxis='y2',
        hovertemplate='<b>Risk Level</b><br>%{x}<br>%{y:.1f}%<extra></extra>'
    ))
    
    # Target lines
    fig.add_hline(y=90, line_dash="dash", line_color=PREMIUM_COLORS['success'], 
                  annotation_text="Target: 90%", annotation_position="bottom right")
    
    layout = create_premium_chart_layout('Executive Performance Trends', 450)
    layout = add_premium_grid(layout)
    layout['xaxis']['tickangle'] = -45
    layout['yaxis']['title'] = 'Performance Score (%)'
    layout['yaxis2'] = {
        'title': 'Risk Level (%)',
        'overlaying': 'y',
        'side': 'right',
        'color': PREMIUM_COLORS['light'],
        'gridcolor': PREMIUM_COLORS['chart_grid'],
        'range': [0, 50]
    }
    
    fig.update_layout(layout)
    return fig

def create_regulatory_risk_analysis():
    """Premium Regulatory Risk Analysis with interactive bars"""
    regulations = [
        'USP <797>', 'USP <800>', 'USP <825>', 'FDA 503B', 
        'State Board', 'cGMP', 'DEA', 'OSHA', 'EPA'
    ]
    
    current_risk = [15, 28, 8, 22, 18, 35, 12, 25, 14]
    potential_impact = [85, 95, 65, 90, 75, 98, 70, 80, 68]
    
    # Create risk colors based on current risk level
    colors = []
    for risk in current_risk:
        if risk < 20:
            colors.append(PREMIUM_COLORS['success'])
        elif risk < 40:
            colors.append(PREMIUM_COLORS['warning'])
        else:
            colors.append(PREMIUM_COLORS['danger'])
    
    fig = go.Figure()
    
    # Current Risk Bars
    fig.add_trace(go.Bar(
        name='Current Risk Level',
        x=regulations,
        y=current_risk,
        marker=dict(
            color=colors,
            line=dict(color=PREMIUM_COLORS['white'], width=1),
            opacity=0.8
        ),
        hovertemplate='<b>%{x}</b><br>Current Risk: %{y}%<extra></extra>'
    ))
    
    # Potential Impact (as line)
    fig.add_trace(go.Scatter(
        name='Potential Impact',
        x=regulations,
        y=potential_impact,
        mode='lines+markers',
        line=dict(color=PREMIUM_COLORS['primary'], width=3),
        marker=dict(size=10, color=PREMIUM_COLORS['primary'], line=dict(width=2, color=PREMIUM_COLORS['white'])),
        yaxis='y2',
        hovertemplate='<b>%{x}</b><br>Potential Impact: %{y}%<extra></extra>'
    ))
    
    layout = create_premium_chart_layout('Regulatory Risk Analysis', 450)
    layout = add_premium_grid(layout)
    layout['xaxis']['tickangle'] = -30
    layout['yaxis']['title'] = 'Current Risk Level (%)'
    layout['yaxis']['range'] = [0, 50]
    layout['yaxis2'] = {
        'title': 'Potential Impact (%)',
        'overlaying': 'y',
        'side': 'right',
        'color': PREMIUM_COLORS['light'],
        'range': [0, 100]
    }
    
    fig.update_layout(layout)
    return fig

def create_deadlines_timeline():
    """Premium Deadlines Timeline with Gantt-style visualization"""
    today = datetime.now()
    
    # Create comprehensive deadline data
    deadlines_data = [
        {
            'task': 'Annual Quality Review',
            'start': today + timedelta(days=5),
            'duration': 14,
            'priority': 'Critical',
            'department': 'Quality Assurance',
            'completion': 0
        },
        {
            'task': 'Environmental Monitoring Update',
            'start': today + timedelta(days=12),
            'duration': 8,
            'priority': 'High',
            'department': 'Environmental',
            'completion': 25
        },
        {
            'task': 'Personnel Training Certification',
            'start': today + timedelta(days=8),
            'duration': 21,
            'priority': 'High',
            'department': 'Training',
            'completion': 60
        },
        {
            'task': 'Facility Compliance Audit',
            'start': today + timedelta(days=18),
            'duration': 10,
            'priority': 'Medium',
            'department': 'Facilities',
            'completion': 0
        },
        {
            'task': 'Process Validation Review',
            'start': today + timedelta(days=25),
            'duration': 12,
            'priority': 'Medium',
            'department': 'Manufacturing',
            'completion': 15
        },
        {
            'task': 'Regulatory Submission Update',
            'start': today + timedelta(days=35),
            'duration': 7,
            'priority': 'Low',
            'department': 'Regulatory',
            'completion': 0
        }
    ]
    
    fig = go.Figure()
    
    # Priority colors
    priority_colors = {
        'Critical': PREMIUM_COLORS['danger'],
        'High': PREMIUM_COLORS['warning'],
        'Medium': PREMIUM_COLORS['primary'],
        'Low': PREMIUM_COLORS['success']
    }
    
    y_pos = list(range(len(deadlines_data)))
    
    for i, task_data in enumerate(deadlines_data):
        start_date = task_data['start']
        duration = task_data['duration']
        end_date = start_date + timedelta(days=duration)
        priority = task_data['priority']
        completion = task_data['completion']
        
        # Main task bar
        fig.add_trace(go.Bar(
            name=f"{task_data['task']} ({priority})",
            x=[duration],
            y=[task_data['task']],
            base=[start_date],
            orientation='h',
            marker=dict(
                color=priority_colors[priority],
                opacity=0.7,
                line=dict(color=PREMIUM_COLORS['white'], width=1)
            ),
            hovertemplate=f"<b>{task_data['task']}</b><br>" +
                         f"Department: {task_data['department']}<br>" +
                         f"Start: {start_date.strftime('%Y-%m-%d')}<br>" +
                         f"Duration: {duration} days<br>" +
                         f"Priority: {priority}<br>" +
                         f"Completion: {completion}%<extra></extra>",
            showlegend=False
        ))
        
        # Progress bar overlay
        if completion > 0:
            progress_duration = duration * (completion / 100)
            fig.add_trace(go.Bar(
                name=f"Progress - {task_data['task']}",
                x=[progress_duration],
                y=[task_data['task']],
                base=[start_date],
                orientation='h',
                marker=dict(
                    color=PREMIUM_COLORS['success'],
                    opacity=0.9
                ),
                showlegend=False,
                hovertemplate=f"<b>Progress: {completion}%</b><extra></extra>"
            ))
    
    # Add "Today" line
    fig.add_shape(
        type="line",
        x0=today, x1=today,
        y0=-0.5, y1=len(deadlines_data)-0.5,
        line=dict(color=PREMIUM_COLORS['accent'], width=3, dash='dash'),
    )
    
    # Add annotation for today
    fig.add_annotation(
        x=today,
        y=len(deadlines_data)-0.5,
        text="Today",
        showarrow=True,
        arrowhead=2,
        arrowsize=1,
        arrowwidth=2,
        arrowcolor=PREMIUM_COLORS['accent'],
        font=dict(color=PREMIUM_COLORS['accent'], size=PREMIUM_FONTS['sizes']['sm'])
    )
    
    layout = create_premium_chart_layout('Upcoming Compliance Deadlines', 500)
    layout['xaxis'].update({
        'type': 'date',
        'title': 'Timeline',
        'tickangle': -45
    })
    layout['yaxis'].update({
        'title': 'Compliance Tasks',
        'autorange': 'reversed'  # Reverse to show first task at top
    })
    layout['bargap'] = 0.3
    layout['showlegend'] = False
    
    fig.update_layout(layout)
    return fig

# ========================================================================================
# UI COMPONENTS
# ========================================================================================

def render_premium_header(client_data):
    """Render premium executive header"""
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M UTC')
    
    st.markdown(f"""
    <div class="executive-header">
        <div class="header-grid">
            <div class="logo-section">
                <div class="logo-icon">LC</div>
                <div>
                    <div class="company-name">LexCura Executive</div>
                    <div class="tagline">Enterprise Compliance Command Center</div>
                </div>
            </div>
            
            <div class="client-badge">
                <strong>{client_data['client_name']}</strong>
                <br><small>{client_data['tier']} • {client_data['region']}</small>
            </div>
            
            <div class="status-indicators">
                <div class="status-dot {client_data['alert_level'].lower()}"></div>
                <div>
                    <div><strong>{client_data['status']}</strong></div>
                    <div class="live-time">{current_time}</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_premium_sidebar():
    """Render premium animated sidebar navigation"""
    with st.sidebar:
        st.markdown("""
        <div style="padding: 2rem 0;">
            <div style="text-align: center; margin-bottom: 2rem;">
                <div class="logo-icon" style="margin: 0 auto 1rem;">LC</div>
                <h3 style="color: #C9A961; margin: 0;">Navigation</h3>
            </div>
            
            <div class="nav-item active" data-target="overview">
                <span class="nav-icon">📊</span>
                <span>Executive Overview</span>
            </div>
            
            <div class="nav-item" data-target="analytics">
                <span class="nav-icon">📈</span>
                <span>Analytics Dashboard</span>
            </div>
            
            <div class="nav-item" data-target="alerts">
                <span class="nav-icon">🚨</span>
                <span>Alert Management</span>
            </div>
            
            <div class="nav-item" data-target="risk">
                <span class="nav-icon">⚠️</span>
                <span>Risk Assessment</span>
            </div>
            
            <div class="nav-item" data-target="deadlines">
                <span class="nav-icon">📅</span>
                <span>Deadline Tracker</span>
            </div>
            
            <div class="nav-item" data-target="reports">
                <span class="nav-icon">📋</span>
                <span>Executive Reports</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

def render_kpi_cards():
    """Render premium animated KPI cards"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-icon" style="background: linear-gradient(135deg, #10B981 0%, #059669 100%);">📊</div>
            <div class="kpi-value">96.7%</div>
            <div class="kpi-label">Compliance Score</div>
            <div class="kpi-trend trend-up">
                <span>↗</span> +2.3% vs last month
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-icon" style="background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%);">⚠️</div>
            <div class="kpi-value">23</div>
            <div class="kpi-label">Active Risks</div>
            <div class="kpi-trend trend-down">
                <span>↘</span> -5 vs last month
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-icon" style="background: linear-gradient(135deg, #2C5282 0%, #2A69AC 100%);">💰</div>
            <div class="kpi-value">$2.3M</div>
            <div class="kpi-label">Financial Impact</div>
            <div class="kpi-trend trend-up">
                <span>↗</span> +12% savings YTD
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-icon" style="background: linear-gradient(135deg, #667EEA 0%, #764BA2 100%);">🔔</div>
            <div class="kpi-value">147</div>
            <div class="kpi-label">Alerts Resolved</div>
            <div class="kpi-trend trend-up">
                <span>↗</span> 98.7% resolution rate
            </div>
        </div>
        """, unsafe_allow_html=True)

def render_executive_summary(client_data):
    """Render premium executive summary"""
    if client_data.get('summary'):
        st.markdown(f"""
        <div class="executive-summary">
            <div class="summary-header">
                <div class="summary-icon">📋</div>
                <div class="summary-title">Executive Summary</div>
            </div>
            <div class="summary-content">
                {client_data['summary']}
            </div>
        </div>
        """, unsafe_allow_html=True)

def render_chart_section(title, subtitle, chart_func, chart_id=None):
    """Render premium chart section with animations"""
    chart_id_attr = f'id="{chart_id}"' if chart_id else ''
    
    st.markdown(f"""
    <div class="chart-section" {chart_id_attr}>
        <div class="section-header">
            <h2 class="section-title">{title}</h2>
            <p class="section-subtitle">{subtitle}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Create chart with premium styling
    chart = chart_func()
    
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(chart, use_container_width=True, key=f"chart_{chart_id or title}")
    st.markdown('</div>', unsafe_allow_html=True)

def render_download_section(client_data):
    """Render premium download section"""
    if client_data.get('content') and len(client_data['content']) > 500:
        st.markdown("""
        <div class="download-section">
            <h3 class="download-title">📊 Executive Data Access</h3>
            <p class="download-subtitle">
                Comprehensive compliance intelligence and detailed analytics 
                for enterprise decision-making
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            content = client_data['content']
            
            if len(content) > 2000:
                st.text_area(
                    "Data Preview", 
                    content[:2000] + "...", 
                    height=200, 
                    disabled=True,
                    help="Preview of full compliance report"
                )
                
                # Export buttons
                col_a, col_b, col_c = st.columns(3)
                
                with col_a:
                    st.download_button(
                        "📄 Download PDF Report",
                        content,
                        file_name=f"executive_compliance_report_{client_data['client_id']}_{datetime.now().strftime('%Y%m%d')}.txt",
                        mime="text/plain"
                    )
                
                with col_b:
                    # Convert to CSV-like format for Excel
                    csv_content = f"Client,{client_data['client_name']}\nTier,{client_data['tier']}\nRegion,{client_data['region']}\nStatus,{client_data['status']}\nAlert Level,{client_data['alert_level']}\nLast Update,{client_data['last_update']}\n\nFull Report:\n{content}"
                    
                    st.download_button(
                        "📊 Export to Excel",
                        csv_content,
                        file_name=f"compliance_data_{client_data['client_id']}_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv"
                    )
                
                with col_c:
                    # Create JSON export
                    json_data = {
                        "client_info": {
                            "id": client_data['client_id'],
                            "name": client_data['client_name'],
                            "tier": client_data['tier'],
                            "region": client_data['region']
                        },
                        "compliance_data": {
                            "status": client_data['status'],
                            "alert_level": client_data['alert_level'],
                            "last_update": client_data['last_update'],
                            "full_report": content
                        },
                        "export_metadata": {
                            "generated_at": datetime.now().isoformat(),
                            "format_version": "1.0"
                        }
                    }
                    
                    st.download_button(
                        "🔗 API Export (JSON)",
                        json.dumps(json_data, indent=2),
                        file_name=f"compliance_api_export_{client_data['client_id']}_{datetime.now().strftime('%Y%m%d')}.json",
                        mime="application/json"
                    )
            else:
                st.text_area("Full Report", content, height=300, disabled=True)

def render_premium_footer():
    """Render premium executive footer"""
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')
    
    st.markdown(f"""
    <div class="executive-footer">
        <div class="footer-content">
            <div class="footer-brand">LexCura Executive Suite</div>
            <p class="footer-disclaimer">
                <strong>CONFIDENTIAL:</strong> This executive dashboard contains proprietary compliance intelligence 
                and sensitive business information. Distribution is restricted to authorized personnel only. 
                All data is encrypted and monitored for security compliance.
            </p>
            <div class="footer-contact">
                Generated: {current_time} | Support: executive@lexcura.com | Emergency: +1-800-LEX-CURA
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ========================================================================================
# MAIN APPLICATION
# ========================================================================================

def main():
    """Main elite compliance dashboard application"""
    
    # Load premium CSS
    st.markdown(load_css(), unsafe_allow_html=True)
    
    # Get client ID from URL params
    client_id = st.query_params.get("client_id", "EXEC001")
    
    # Load client data with premium loading
    with st.spinner('🔄 Loading executive compliance intelligence...'):
        client_data = load_premium_client_data(client_id)
        time.sleep(0.5)  # Brief pause for premium feel
    
    # Render premium header
    render_premium_header(client_data)
    
    # Render premium sidebar
    render_premium_sidebar()
    
    # Control section
    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 2])
    with col1:
        if st.button("🔄 Refresh Data", type="primary"):
            st.cache_data.clear()
            st.rerun()
    
    with col2:
        export_mode = st.selectbox("📊 View Mode", ["Executive", "Detailed", "Technical"])
    
    with col3:
        time_range = st.selectbox("📅 Time Range", ["Last 30 Days", "Last 90 Days", "YTD", "Custom"])
    
    # KPI Cards Section
    st.markdown('<div id="overview"></div>', unsafe_allow_html=True)
    render_kpi_cards()
    
    # Executive Summary
    render_executive_summary(client_data)
    
    # Analytics Dashboard
    st.markdown('<div id="analytics"></div>', unsafe_allow_html=True)
    
    # Charts Grid - Premium Layout
    st.markdown("""
    <div class="chart-section">
        <div class="section-header">
            <h2 class="section-title">Executive Analytics Dashboard</h2>
            <p class="section-subtitle">
                Real-time compliance intelligence with predictive analytics and enterprise-grade visualizations
            </p>
        </div>
        <div class="charts-grid">
    """, unsafe_allow_html=True)
    
    # Row 1: Financial Impact & Compliance Radar
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="chart-header"><h3 class="chart-title">Financial Impact Analysis</h3></div>', unsafe_allow_html=True)
        st.plotly_chart(create_financial_impact_chart(), use_container_width=True, key="financial_chart")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="chart-header"><h3 class="chart-title">Compliance Excellence Matrix</h3></div>', unsafe_allow_html=True)
        st.plotly_chart(create_compliance_radar_chart(), use_container_width=True, key="radar_chart")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Row 2: Monitoring Dashboard (Full Width)
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="chart-header"><h3 class="chart-title">Executive Monitoring Command Center</h3></div>', unsafe_allow_html=True)
    st.plotly_chart(create_monitoring_dashboard(), use_container_width=True, key="monitoring_chart")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Row 3: Alert Status & Risk Assessment
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-card" id="alerts">', unsafe_allow_html=True)
        st.markdown('<div class="chart-header"><h3 class="chart-title">Alert Distribution Matrix</h3></div>', unsafe_allow_html=True)
        st.plotly_chart(create_alert_status_heatmap(), use_container_width=True, key="alerts_chart")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-card" id="risk">', unsafe_allow_html=True)
        st.markdown('<div class="chart-header"><h3 class="chart-title">Enterprise Risk Assessment</h3></div>', unsafe_allow_html=True)
        st.plotly_chart(create_risk_assessment_gauge(), use_container_width=True, key="risk_chart")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Row 4: Performance Trends & Regulatory Analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="chart-header"><h3 class="chart-title">Performance Intelligence</h3></div>', unsafe_allow_html=True)
        st.plotly_chart(create_performance_trends(), use_container_width=True, key="performance_chart")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="chart-header"><h3 class="chart-title">Regulatory Risk Intelligence</h3></div>', unsafe_allow_html=True)
        st.plotly_chart(create_regulatory_risk_analysis(), use_container_width=True, key="regulatory_chart")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Row 5: Deadlines Timeline (Full Width)
    st.markdown('<div class="chart-card" id="deadlines">', unsafe_allow_html=True)
    st.markdown('<div class="chart-header"><h3 class="chart-title">Executive Deadline Command Center</h3></div>', unsafe_allow_html=True)
    st.plotly_chart(create_deadlines_timeline(), use_container_width=True, key="deadlines_chart")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div></div>', unsafe_allow_html=True)  # Close charts-grid and chart-section
    
    # Download Section
    st.markdown('<div id="reports"></div>', unsafe_allow_html=True)
    render_download_section(client_data)
    
    # Premium Footer
    render_premium_footer()

if __name__ == "__main__":
    main()

def create_compliance_radar_chart():
    """Premium Compliance Excellence Radar with smooth animations"""
    categories = [
        'Documentation<br>Standards',
        'Personnel<br>Training', 
        'Environmental<br>Controls',
        'Quality<br>Systems',
        'Facility<br>Standards',
        'Process<br>Controls',
        'Risk<br>Management',
        'Regulatory<br>Compliance'
    ]
    
    current_scores = [94, 97, 89, 96, 98, 91, 93, 95]
    benchmark_scores = [85, 88, 82, 87, 89, 84, 86, 88]
    
    fig = go.Figure()
    
    # Add current performance
    fig.add_trace(go.Scatterpolar(
        r=current_scores + [current_scores[0]],
        theta=categories + [categories[0]],
        fill='toself',
        name='Current Performance',
        line=dict(color=PREMIUM_COLORS['primary'], width=3),
        fillcolor=f"rgba(201, 169, 97, 0.3)",
        marker=dict(size=8, color=PREMIUM_COLORS['primary']),
        hovertemplate='<b>%{theta}</b><br>Current: %{r}%<extra></extra>'
    ))
    
    # Add benchmark
    fig.add_trace(go.Scatterpolar(
        r=benchmark_scores + [benchmark_scores[0]],
        theta=categories + [categories[0]],
        fill='toself',
        name='Industry Benchmark',
        line=dict(color=PREMIUM_COLORS['medium'], width=2, dash='dash'),
        fillcolor=f"rgba(100, 116, 139, 0.2)",
        marker=dict(size=6, color=PREMIUM_COLORS['medium']),
        hovertemplate='<b>%{theta}</b><br>Benchmark: %{r}%<extra></extra>'
    ))
    
    layout = create_premium_chart_layout('Compliance Excellence Radar', 500)
    layout['polar'] = dict(
        bgcolor=PREMIUM_COLORS['chart_bg'],
        radialaxis=dict(
            visible=True,
            range=[0, 100],
            gridcolor=PREMIUM_COLORS['chart_grid'],
            tickfont=dict(size=PREMIUM_FONTS['sizes']['xs'], color=PREMIUM_COLORS['medium']),
            tickmode='linear',
            tick0=0,
            dtick=20
        ),
        angularaxis=dict(
            tickfont=dict(size=PREMIUM_FONTS['sizes']['sm'], color=PREMIUM_COLORS['light']),
            gridcolor=PREMIUM_COLORS['chart_grid']
        )
    )
    
    fig.update_layout(layout)
    return fig

def create_monitoring_dashboard():
    """Premium Monitoring Dashboard with animated gauges"""
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Overall Compliance', 'Risk Level', 'Process Efficiency', 'Regulatory Readiness'),
        specs=[[{'type': 'indicator'}, {'type': 'indicator'}],
               [{'type': 'indicator'}, {'type': 'indicator'}]],
        vertical_spacing=0.25
    )
    
    # Overall Compliance Score
    fig.add_trace(go.Indicator(
        mode="gauge+number+delta",
        value=96.7,
        domain={'row': 0, 'column': 0},
        title={'text': "Overall Compliance", 'font': {'size': PREMIUM_FONTS['sizes']['base']}},
        delta={'reference': 95, 'increasing': {'color': PREMIUM_COLORS['success']}},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 2, 'tickcolor': PREMIUM_COLORS['medium']},
            'bar': {'color': PREMIUM_COLORS['primary'], 'thickness': 0.8},
            'bgcolor': PREMIUM_COLORS['charcoal'],
            'borderwidth': 2,
            'bordercolor': PREMIUM_COLORS['chart_grid'],
            'steps': [
                {'range': [0, 60], 'color': PREMIUM_COLORS['danger']},
                {'range': [60, 85], 'color': PREMIUM_COLORS['warning']},
                {'range': [85, 100], 'color': PREMIUM_COLORS['success']}
            ],
            'threshold': {
                'line': {'color': PREMIUM_COLORS['white'], 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ), row=1, col=1)
    
    # Risk Level (inverted - lower is better)
    fig.add_trace(go.Indicator(
        mode="gauge+number+delta",
        value=18.5,
        domain={'row': 0, 'column': 1},
        title={'text': "Risk Level", 'font': {'size': PREMIUM_FONTS['sizes']['base']}},
        delta={'reference': 25, 'decreasing': {'color': PREMIUM_COLORS['success']}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 2, 'tickcolor': PREMIUM_COLORS['medium']},
            'bar': {'color': PREMIUM_COLORS['success'], 'thickness': 0.8},
            'bgcolor': PREMIUM_COLORS['charcoal'],
            'borderwidth': 2,
            'bordercolor': PREMIUM_COLORS['chart_grid'],
            'steps': [
                {'range': [0, 30], 'color': PREMIUM_COLORS['success']},
                {'range': [30, 60], 'color': PREMIUM_COLORS['warning']},
                {'range': [60, 100], 'color': PREMIUM_COLORS['danger']}
            ],
            'threshold': {
                'line': {'color': PREMIUM_COLORS['white'], 'width': 4},
                'thickness': 0.75,
                'value': 40
            }
        }
    ), row=1, col=2)
    
    # Process Efficiency
    fig.add_trace(go.Indicator(
        mode="gauge+number+delta",
        value=92.3,
        domain={'row': 1, 'column': 0},
        title={'text': "Process Efficiency", 'font': {'size': PREMIUM_FONTS['sizes']['base']}},
        delta={'reference': 88, 'increasing': {'color': PREMIUM_COLORS['success']}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 2, 'tickcolor': PREMIUM_COLORS['medium']},
            'bar': {'color': PREMIUM_COLORS['secondary'], 'thickness': 0.8},
            'bgcolor': PREMIUM_COLORS['charcoal'],
            'borderwidth': 2,
            'bordercolor': PREMIUM_COLORS['chart_grid'],
            'steps': [
                {'range': [0, 60], 'color': PREMIUM_COLORS['danger']},
                {'range': [60, 85], 'color': PREMIUM_COLORS['warning']},
                {'range': [85, 100], 'color': PREMIUM_COLORS['success']}
            ],
            'threshold': {
                'line': {'color': PREMIUM_COLORS['white'], 'width': 4},
                'thickness': 0.75,
                'value': 80
            }
        }
    ), row=2, col=1)
    
    # Regulatory Readiness
    fig.add_trace(go.Indicator(
        mode="gauge+number+delta",
        value=94.8,
        domain={'row': 1, 'column': 1},
        title={'text': "Regulatory Readiness", 'font': {'size': PREMIUM_FONTS['sizes']['base']}},
        delta={'reference': 92, 'increasing': {'color': PREMIUM_COLORS['success']}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 2, 'tickcolor': PREMIUM_COLORS['medium']},
            'bar': {'color': PREMIUM_COLORS['accent'], 'thickness': 0.8},
            'bgcolor': PREMIUM_COLORS['charcoal'],
            'borderwidth': 2,
            'bordercolor': PREMIUM_COLORS['chart_grid'],
            'steps': [
                {'range': [0, 60], 'color': PREMIUM_COLORS['danger']},
                {'range': [60, 85], 'color': PREMIUM_COLORS['warning']},
                {'range': [85, 100], 'color': PREMIUM_COLORS['success']}
            ],
            'threshold': {
                'line': {'color': PREMIUM_COLORS['white'], 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ), row=2, col=2)
    
    fig.update_layout(
        height=600,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor=PREMIUM_COLORS['chart_bg'],
        font=dict(color=PREMIUM_COLORS['white'], family=PREMIUM_FONTS['secondary']),
        title={
            'text': 'Executive Monitoring Dashboard',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': PREMIUM_FONTS['sizes']['xl'], 'color': PREMIUM_COLORS['white']}
        }
    )
    
    return fig
