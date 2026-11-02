import os
import io
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from datetime import datetime
from data import (
    load_data,
    add_student_record,
    update_student_record,
    delete_student_record
)
from generate_report import generate_pdf_report, get_grade_and_status

Username=st.secrets["auth"]["username"]
Password=st.secrets["auth"]["password"]

# Global Matplotlib dark theme styling for high-contrast crisp text & legends
plt.rcParams['text.color'] = '#f8fafc'
plt.rcParams['axes.labelcolor'] = '#94a3b8'
plt.rcParams['xtick.color'] = '#cbd5e1'
plt.rcParams['ytick.color'] = '#cbd5e1'
plt.rcParams['legend.facecolor'] = '#1e293b'
plt.rcParams['legend.edgecolor'] = '#475569'
plt.rcParams['legend.labelcolor'] = '#f8fafc'
plt.rcParams['legend.fontsize'] = 9

st.set_page_config(
    page_title="MST Analytics & Management Portal",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.markdown("""
<style>
    /* Global Apple SF Pro Font & Smoothing */
    html, body, [class*="css"] {
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text", "Helvetica Neue", Arial, sans-serif !important;
        -webkit-font-smoothing: antialiased !important;
        -moz-osx-font-smoothing: grayscale !important;
    }

    /* macOS Window Header Bar */
    .apple-window-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.5rem 0.2rem 1.2rem 0.2rem;
        margin-bottom: 0.8rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    }
    .apple-title-group {
        display: flex;
        flex-direction: column;
    }
    .apple-title {
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: -0.035em;
        color: #ffffff;
        margin-bottom: 0.25rem;
        line-height: 1.2;
    }
    .apple-subtitle {
        font-size: 0.96rem;
        color: #94a3b8;
        font-weight: 400;
        letter-spacing: -0.01em;
    }

    /* Apple System Status Pill */
    .apple-status-pill {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.82rem;
        font-weight: 600;
        color: #cbd5e1;
        backdrop-filter: blur(12px);
    }
    .apple-status-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background-color: #34d399;
        box-shadow: 0 0 8px #34d399;
    }

    /* Apple Frosted Glassmorphism Card Containers */
    .apple-card {
        background: rgba(22, 28, 45, 0.65);
        border: 1px solid rgba(255, 255, 255, 0.09);
        border-radius: 20px;
        padding: 1.5rem 1.8rem;
        backdrop-filter: blur(28px) saturate(180%);
        -webkit-backdrop-filter: blur(28px) saturate(180%);
        box-shadow: 0 10px 32px -4px rgba(0, 0, 0, 0.45), inset 0 1px 0 rgba(255, 255, 255, 0.08);
        margin-bottom: 1.3rem;
        transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .apple-card:hover {
        border-color: rgba(255, 255, 255, 0.15);
    }

    .apple-card-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 1.1rem;
        padding-bottom: 0.75rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.06);
    }
    .apple-card-title {
        font-size: 1.12rem;
        font-weight: 700;
        color: #f8fafc;
        letter-spacing: -0.02em;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .apple-card-caption {
        font-size: 0.82rem;
        color: #94a3b8;
        font-weight: 500;
    }

    /* Apple Widget-Style Metric Cards (st.metric) */
    div[data-testid="stMetric"] {
        background: rgba(22, 28, 45, 0.65) !important;
        border: 1px solid rgba(255, 255, 255, 0.09) !important;
        border-radius: 18px !important;
        padding: 1.15rem 1.35rem !important;
        backdrop-filter: blur(24px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(24px) saturate(180%) !important;
        box-shadow: 0 8px 24px -4px rgba(0, 0, 0, 0.35), inset 0 1px 0 rgba(255, 255, 255, 0.08) !important;
        transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-2.5px) !important;
        border-color: rgba(56, 189, 248, 0.4) !important;
        box-shadow: 0 12px 28px -4px rgba(0, 0, 0, 0.45), 0 0 16px rgba(56, 189, 248, 0.15) !important;
    }
    div[data-testid="stMetric"] label[data-testid="stMetricLabel"] {
        font-size: 0.78rem !important;
        font-weight: 700 !important;
        color: #94a3b8 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.8px !important;
    }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        font-size: 2.05rem !important;
        font-weight: 800 !important;
        color: #ffffff !important;
        letter-spacing: -0.03em !important;
        margin-top: 0.2rem !important;
    }
    div[data-testid="stMetric"] div[data-testid="stMetricDelta"] {
        font-size: 0.82rem !important;
        font-weight: 600 !important;
        color: #cbd5e1 !important;
    }

    /* Apple Metallic Frosted Podium Topper Cards */
    .apple-topper-gold {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.18) 0%, rgba(180, 83, 9, 0.08) 100%);
        border: 1px solid rgba(245, 158, 11, 0.4);
        border-radius: 16px;
        padding: 1.15rem 1.3rem;
        margin-bottom: 0.8rem;
        backdrop-filter: blur(16px);
        box-shadow: 0 4px 16px rgba(245, 158, 11, 0.12);
        transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .apple-topper-gold:hover {
        transform: translateY(-2.5px);
        box-shadow: 0 8px 24px rgba(245, 158, 11, 0.25);
        border-color: rgba(245, 158, 11, 0.6);
    }
    .apple-topper-silver {
        background: linear-gradient(135deg, rgba(148, 163, 184, 0.18) 0%, rgba(71, 85, 105, 0.08) 100%);
        border: 1px solid rgba(148, 163, 184, 0.4);
        border-radius: 16px;
        padding: 1.15rem 1.3rem;
        margin-bottom: 0.8rem;
        backdrop-filter: blur(16px);
        box-shadow: 0 4px 16px rgba(148, 163, 184, 0.12);
        transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .apple-topper-silver:hover {
        transform: translateY(-2.5px);
        box-shadow: 0 8px 24px rgba(148, 163, 184, 0.25);
        border-color: rgba(148, 163, 184, 0.6);
    }
    .apple-topper-bronze {
        background: linear-gradient(135deg, rgba(217, 119, 6, 0.18) 0%, rgba(146, 64, 14, 0.08) 100%);
        border: 1px solid rgba(217, 119, 6, 0.4);
        border-radius: 16px;
        padding: 1.15rem 1.3rem;
        margin-bottom: 0.8rem;
        backdrop-filter: blur(16px);
        box-shadow: 0 4px 16px rgba(217, 119, 6, 0.12);
        transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .apple-topper-bronze:hover {
        transform: translateY(-2.5px);
        box-shadow: 0 8px 24px rgba(217, 119, 6, 0.25);
        border-color: rgba(217, 119, 6, 0.6);
    }

    /* Apple macOS Segmented Control Tabs (st.tabs) */
    div[data-baseweb="tab-list"] {
        background: rgba(20, 26, 42, 0.7) !important;
        padding: 6px !important;
        border-radius: 16px !important;
        border: 1px solid rgba(255, 255, 255, 0.09) !important;
        gap: 6px !important;
        margin-bottom: 1.6rem !important;
        box-shadow: inset 0 2px 6px rgba(0, 0, 0, 0.3) !important;
    }
    button[data-baseweb="tab"] {
        border-radius: 11px !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        padding: 8px 20px !important;
        border: none !important;
        color: #94a3b8 !important;
        transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }
    button[data-baseweb="tab"]:hover {
        color: #ffffff !important;
        background: rgba(255, 255, 255, 0.08) !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        background: rgba(255, 255, 255, 0.18) !important;
        color: #ffffff !important;
        box-shadow: 0 3px 12px rgba(0, 0, 0, 0.35), inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
        border: 1px solid rgba(255, 255, 255, 0.14) !important;
    }
    div[data-baseweb="tab-border"], div[data-baseweb="tab-highlight"] {
        display: none !important;
    }

    /* Apple-style Form Controls & Inputs */
    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div {
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        background: rgba(15, 23, 42, 0.65) !important;
        color: #f8fafc !important;
        position: relative !important;
        transition: all 0.2s ease !important;
    }
    div[data-baseweb="input"] input,
    div[data-baseweb="base-input"] input {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        color: #f8fafc !important;
    }
    div[data-baseweb="select"] > div:hover,
    div[data-baseweb="input"] > div:hover {
        border-color: rgba(56, 189, 248, 0.5) !important;
    }
    div[data-baseweb="select"] > div:focus-within,
    div[data-baseweb="input"] > div:focus-within {
        border-color: #38bdf8 !important;
        box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.25) !important;
    }

    /* Apple-style Primary Buttons */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(180deg, #0a84ff 0%, #0071e3 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        font-size: 0.98rem !important;
        padding: 0.65rem 1.6rem !important;
        box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.25), 0 4px 16px rgba(0, 113, 227, 0.35) !important;
        transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }
    div.stButton > button[kind="primary"]:hover {
        transform: translateY(-1.5px) !important;
        box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.3), 0 6px 22px rgba(0, 113, 227, 0.55) !important;
    }
    div.stButton > button[kind="primary"]:active {
        transform: translateY(0.5px) !important;
    }

    /* Apple-style Download Buttons */
    div.stDownloadButton > button {
        background: rgba(30, 41, 59, 0.8) !important;
        color: #38bdf8 !important;
        border: 1px solid rgba(56, 189, 248, 0.35) !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        padding: 0.65rem 1.5rem !important;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.25) !important;
        transition: all 0.2s ease !important;
    }
    div.stDownloadButton > button:hover {
        background: rgba(56, 189, 248, 0.18) !important;
        color: #ffffff !important;
        border-color: #38bdf8 !important;
        transform: translateY(-1.5px) !important;
        box-shadow: 0 6px 20px rgba(56, 189, 248, 0.25) !important;
    }

    /* Password Input Container: reserve room for right-side eye button */
    div[data-testid="stTextInput"]:has(input[type="password"]) div[data-baseweb="input"] > div,
    div[data-baseweb="input"]:has(button) > div,
    div[data-baseweb="base-input"]:has(button) {
        position: relative !important;
        padding-right: 100px !important;
    }

    /* Password Eye Button - Pinned to right: 0, full height, centered eye icon */
    div[data-baseweb="input"] button,
    div[data-baseweb="base-input"] button,
    button[aria-label*="password"],
    button[title*="password"] {
        position: absolute !important;
        top: 0 !important;
        bottom: 0 !important;
        right: -20px !important;
        height: 100% !important;
        width: 58px !important;
        min-width: 58px !important;
        max-width: 58px !important;
        transform: translateX(0) !important;
        background: #facc15 !important;
        background-color: #facc15 !important;
        border: none !important;
        margin: 0 !important;
        padding: 0 !important;
        border-radius: 0 11px 11px 0 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        box-shadow: none !important;
        cursor: pointer !important;
        z-index: 5 !important;
    }
    div[data-baseweb="input"] button:hover,
    div[data-baseweb="base-input"] button:hover,
    button[aria-label*="password"]:hover {
        background: #eab308 !important;
        background-color: #eab308 !important;
        transform: none !important;
    }
    div[data-baseweb="input"] button svg,
    div[data-baseweb="base-input"] button svg,
    button[aria-label*="password"] svg {
        fill: #0f172a !important;
        color: #0f172a !important;
        width: 22px !important;
        height: 22px !important;
        display: block !important;
        margin: auto !important;
    }

    /* Yellow Login Form Submit Button */
    div[data-testid="stFormSubmitButton"] button,
    div[data-testid="stFormSubmitButton"] > button,
    button[kind="primaryFormSubmit"],
    button[data-testid="baseButton-primaryFormSubmit"],
    div.stFormSubmitButton button {
        background: #facc15 !important;
        background-color: #facc15 !important;
        color: #0f172a !important;
        border: none !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
        border-radius: 8px !important;
        padding: 0.65rem 1.4rem !important;
        box-shadow: 0 3px 12px rgba(250, 204, 21, 0.3) !important;
        transition: all 0.2s ease-in-out !important;
    }
    div[data-testid="stFormSubmitButton"] button:hover,
    div[data-testid="stFormSubmitButton"] > button:hover,
    button[kind="primaryFormSubmit"]:hover,
    button[data-testid="baseButton-primaryFormSubmit"]:hover,
    div.stFormSubmitButton button:hover {
        background: #eab308 !important;
        background-color: #eab308 !important;
        color: #000000 !important;
        box-shadow: 0 5px 18px rgba(234, 179, 8, 0.45) !important;
        transform: translateY(-1px) !important;
    }
    div[data-testid="stFormSubmitButton"] button p,
    div[data-testid="stFormSubmitButton"] button span,
    button[kind="primaryFormSubmit"] p,
    button[kind="primaryFormSubmit"] span {
        color: #0f172a !important;
        font-weight: 700 !important;
    }

    /* Record Management Form Submit Buttons (Tabs) - Apple Blue */
    div[data-testid="stTabs"] div[data-testid="stFormSubmitButton"] button,
    div[data-testid="stTabs"] button[kind="primaryFormSubmit"] {
        background: linear-gradient(180deg, #0a84ff 0%, #0071e3 100%) !important;
        background-color: #0071e3 !important;
        color: #ffffff !important;
        box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.25), 0 4px 16px rgba(0, 113, 227, 0.35) !important;
    }
    div[data-testid="stTabs"] div[data-testid="stFormSubmitButton"] button p,
    div[data-testid="stTabs"] button[kind="primaryFormSubmit"] p {
        color: #ffffff !important;
    }

    /* Apple macOS Style Sidebar Navigation */
    section[data-testid="stSidebar"] {
        background-color: #1E2638 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
    }
    section[data-testid="stSidebar"] div[role="radiogroup"] {
        gap: 6px !important;
    }
    section[data-testid="stSidebar"] div[role="radiogroup"] > label {
        padding: 0.72rem 1rem !important;
        border-radius: 12px !important;
        font-size: 1.04rem !important;
        font-weight: 500 !important;
        letter-spacing: -0.2px !important;
        transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
        margin-bottom: 0.25rem !important;
        cursor: pointer !important;
        display: flex !important;
        align-items: center !important;
        border: 1px solid transparent !important;
    }
    /* Hide default radio circle for clean Apple-style sidebar buttons */
    section[data-testid="stSidebar"] div[role="radiogroup"] > label > div:first-child {
        display: none !important;
    }
    section[data-testid="stSidebar"] div[role="radiogroup"] > label > div:last-child {
        width: 100% !important;
    }
    section[data-testid="stSidebar"] div[role="radiogroup"] > label:hover {
        background: rgba(255, 255, 255, 0.08) !important;
        transform: translateX(4px) !important;
    }
    /* Active selected navigation item */
    section[data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:checked),
    section[data-testid="stSidebar"] div[role="radiogroup"] > label[data-checked="true"] {
        background: rgba(59, 130, 246, 0.2) !important;
        color: #60a5fa !important;
        font-weight: 700 !important;
        border: 1px solid rgba(59, 130, 246, 0.4) !important;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2) !important;
    }

    /* Sleek Apple-style Logout Button */
    div.sidebar-logout div.stButton > button {
        background: rgba(239, 68, 68, 0.12) !important;
        color: #f87171 !important;
        border: 1px solid rgba(239, 68, 68, 0.25) !important;
        border-radius: 11px !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        padding: 0.6rem 1rem !important;
        transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }
    div.sidebar-logout div.stButton > button:hover {
        background: rgba(239, 68, 68, 0.25) !important;
        color: #ffffff !important;
        border-color: rgba(239, 68, 68, 0.5) !important;
        box-shadow: 0 4px 12px rgba(239, 68, 68, 0.25) !important;
        transform: translateY(-1px) !important;
    }

    /* Apple-style Expanders */
    details[data-testid="stExpander"] {
        background: rgba(22, 28, 45, 0.5) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 14px !important;
        margin-top: 0.6rem !important;
    }

    /* Apple Dataframe Containers */
    div[data-testid="stDataFrame"] {
        border: 1px solid rgba(255, 255, 255, 0.09) !important;
        border-radius: 16px !important;
        overflow: hidden !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25) !important;
    }

    /* Apple Custom Pill Badges */
    .apple-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.3px;
    }
    .apple-pill-blue {
        background: rgba(56, 189, 248, 0.15);
        border: 1px solid rgba(56, 189, 248, 0.35);
        color: #38bdf8;
    }
    .apple-pill-green {
        background: rgba(52, 211, 153, 0.15);
        border: 1px solid rgba(52, 211, 153, 0.35);
        color: #34d399;
    }
    .apple-pill-amber {
        background: rgba(251, 191, 36, 0.15);
        border: 1px solid rgba(251, 191, 36, 0.35);
        color: #fbbf24;
    }
    .apple-pill-red {
        background: rgba(248, 113, 113, 0.15);
        border: 1px solid rgba(248, 113, 113, 0.35);
        color: #f87171;
    }
</style>
""", unsafe_allow_html=True)


def check_login():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if not st.session_state["logged_in"]:
        col1, col2, col3 = st.columns([1, 1.6, 1])
        with col2:
            st.write("")
            st.write("")
            st.markdown("<h2 style='text-align: center; font-weight: 800; color: #60a5fa; margin-bottom: 0px;'>🎓 MST Analytics Portal</h2>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 0.92rem; margin-top: 4px; margin-bottom: 2rem;'>MST MARKS ANALYZER - Analysis of Mid Semester Test marks</p>", unsafe_allow_html=True)

            with st.form("login_form", border=False):
                st.markdown("<h3 style='margin-bottom: 1.2rem; font-weight: 700;'>🔐 USER Login</h3>", unsafe_allow_html=True)
                username = st.text_input("Username", placeholder="enter username")
                password = st.text_input("Password", type="password", placeholder="enter password")

                st.write("")
                login_btn = st.form_submit_button("Sign In →", type="primary", use_container_width=True)

                st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 0.78rem; margin-top: 0.85rem; letter-spacing: 0.4px;'>Authorized access only | Contact Administrator to access</p>", unsafe_allow_html=True)

                if login_btn:
                    if username == Username and password == Password:
                        st.session_state["logged_in"] = True
                        st.session_state["username"] = username
                        st.success("Login successful! Redirecting...")
                        st.rerun()
                    else:
                        st.error("Invalid Username or Password! Please try again.")
        return False
    return True

if not check_login():
    st.stop()


def get_data():
    return load_data()

df = get_data()
subject_cols = list(df.columns[2:7])


with st.sidebar:
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 12px; padding: 0.6rem 0.2rem 1.2rem 0.2rem; border-bottom: 1px solid rgba(255, 255, 255, 0.08); margin-bottom: 1.2rem;">
        <div style="background: linear-gradient(135deg, #3b82f6, #1d4ed8); width: 44px; height: 44px; border-radius: 14px; display: flex; align-items: center; justify-content: center; font-size: 1.5rem; box-shadow: 0 4px 14px rgba(59, 130, 246, 0.4);">
            🎓
        </div>
        <div>
            <div style="font-size: 1.25rem; font-weight: 800; letter-spacing: -0.3px; line-height: 1.2; color: #ffffff;">MST Portal</div>
            <div style="font-size: 0.76rem; color: #94a3b8; font-weight: 500;">Academic Analytics Suite</div>
        </div>
    </div>
    <div style="font-size: 0.72rem; font-weight: 700; color: #64748b; letter-spacing: 0.8px; text-transform: uppercase; margin-bottom: 0.6rem; padding-left: 0.4rem;">
        Platform Menu
    </div>
    """, unsafe_allow_html=True)

    menu = st.radio(
        "Navigation Menu",
        [
            "🏠 Dashboard",
            "👤 Student Analysis",
            "🏫 Class Analysis",
            "📊 Visualizations",
            "📝 Record Management",
            "📄 Report Card Generator"
        ],
        label_visibility="collapsed"
    )

    st.markdown("<div style='margin-top: 2.2rem;'></div>", unsafe_allow_html=True)

    st.markdown("<div class='sidebar-logout'>", unsafe_allow_html=True)
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state["logged_in"] = False
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<p style='text-align: center; color: #64748b; font-size: 0.74rem; margin-top: 1.2rem;'>MST Management System v2.0</p>", unsafe_allow_html=True)


if menu == "🏠 Dashboard":
    st.markdown("""
    <div class='apple-window-header'>
        <div class='apple-title-group'>
            <div class='apple-title'>🏠 MST Performance Dashboard</div>
            <div class='apple-subtitle'>High-level executive overview of class performance and key academic indicators</div>
        </div>
        <div class='apple-status-pill'>
            <div class='apple-status-dot'></div>
            Academic Session 2025-26 • Active
        </div>
    </div>
    """, unsafe_allow_html=True)

    total_students = len(df)
    class_avg = df["Average"].mean()
    highest_total = df["Total"].max()
    lowest_total = df["Total"].min()
    pass_count = len(df[df["Total"] >= 40])
    pass_pct = (pass_count / total_students) * 100 if total_students > 0 else 0

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Students", f"{total_students}", help="Total enrolled students in class")
    m2.metric("Class Average", f"{class_avg:.2f} / 20", f"Total Avg: {df['Total'].mean():.1f} / 100")
    m3.metric("Highest Total", f"{highest_total:.1f} / 100", f"Topper: {df.loc[df['Total']==highest_total, 'Name'].values[0]}")
    m4.metric("Passing Rate", f"{pass_pct:.1f}%", f"{pass_count} Passed (≥40%)")

    st.markdown("<div style='margin-top: 1.2rem;'></div>", unsafe_allow_html=True)

    col_left, col_right = st.columns([1.15, 1.85])

    with col_left:
        st.markdown("""
        <div class='apple-card'>
            <div class='apple-card-header'>
                <div class='apple-card-title'>🏆 Top 3 Class Toppers</div>
                <div class='apple-card-caption'>Merit Standings</div>
            </div>
        """, unsafe_allow_html=True)

        toppers = df.sort_values(by="Total", ascending=False).head(3).reset_index(drop=True)
        card_classes = ["apple-topper-gold", "apple-topper-silver", "apple-topper-bronze"]
        badge_titles = ["🥇 1st Position", "🥈 2nd Position", "🥉 3rd Position"]
        badge_colors = ["#f59e0b", "#94a3b8", "#d97706"]

        for i, row in toppers.iterrows():
            c_class = card_classes[i] if i < len(card_classes) else "apple-topper-bronze"
            b_title = badge_titles[i] if i < len(badge_titles) else f"Rank {i+1}"
            b_color = badge_colors[i] if i < len(badge_colors) else "#94a3b8"

            st.markdown(f"""
            <div class='{c_class}'>
                <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.25rem;'>
                    <span style='font-weight: 700; color: {b_color}; font-size: 0.82rem; text-transform: uppercase; letter-spacing: 0.6px;'>{b_title}</span>
                    <span style='background: rgba(255, 255, 255, 0.12); border-radius: 12px; padding: 2px 10px; font-weight: 800; color: #ffffff; font-size: 0.95rem;'>{row['Total']} / 100</span>
                </div>
                <div style='font-size: 1.22rem; font-weight: 800; color: #ffffff; letter-spacing: -0.02em;'>{row['Name']}</div>
                <div style='font-size: 0.84rem; color: #cbd5e1; margin-top: 4px;'>
                    Roll: <b style="color: #ffffff;">{row['Enrollment_Number']}</b> &nbsp;•&nbsp; Avg: <b style="color: #38bdf8;">{row['Average']:.1f}/20</b>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    with col_right:
        st.markdown("""
        <div class='apple-card'>
            <div class='apple-card-header'>
                <div class='apple-card-title'>📊 Subject-wise Class Average</div>
                <div class='apple-card-caption'>Benchmark (out of 20)</div>
            </div>
        """, unsafe_allow_html=True)

        sub_avgs = [round(df[s].mean(), 2) for s in subject_cols]
        clean_subs = [s.replace("_", " ") for s in subject_cols]

        fig, ax = plt.subplots(figsize=(8, 4.2))
        fig.patch.set_facecolor('none')
        ax.set_facecolor('none')

        bars = ax.bar(clean_subs, sub_avgs, color="#38bdf8", edgecolor="none", width=0.46, zorder=3)
        ax.set_ylim(0, 22)
        ax.set_ylabel("Average Marks (out of 20)", fontsize=9, color="#94a3b8")
        ax.grid(axis='y', linestyle=':', color="#5D6E8D", alpha=0.5, zorder=0)

        ax.tick_params(colors="#cbd5e1", labelsize=9)
        for spine in ax.spines.values():
            spine.set_color("#334155")
            spine.set_linewidth(0.8)

        for bar in bars:
            h = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, h + 0.45, f"{h:.2f}", ha='center', fontsize=9, fontweight="bold", color="#ffffff")

        plt.xticks(rotation=10)
        plt.tight_layout()
        st.pyplot(fig)

        # Quick Performance Highlights below the chart to perfectly balance the layout
        sub_averages = {s: df[s].mean() for s in subject_cols}
        best_sub = max(sub_averages, key=sub_averages.get)
        toughest_sub = min(sub_averages, key=sub_averages.get)

        st.markdown(f"""
        <div style="display: flex; gap: 12px; margin-top: 0.85rem;">
            <div style="flex: 1; background: rgba(52, 211, 153, 0.1); border: 1px solid rgba(52, 211, 153, 0.3); border-radius: 14px; padding: 0.85rem 1rem;">
                <div style="font-size: 0.72rem; color: #34d399; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;">🌟 Best Scoring Subject</div>
                <div style="font-size: 1.08rem; font-weight: 800; color: #ffffff; margin-top: 2px;">{best_sub.replace('_', ' ')}</div>
                <div style="font-size: 0.82rem; color: #cbd5e1; margin-top: 2px;">Class Avg: <b style="color: #34d399;">{sub_averages[best_sub]:.2f} / 20</b></div>
            </div>
            <div style="flex: 1; background: rgba(248, 113, 113, 0.1); border: 1px solid rgba(248, 113, 113, 0.3); border-radius: 14px; padding: 0.85rem 1rem;">
                <div style="font-size: 0.72rem; color: #f87171; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;">▲ Needs Focus (Toughest)</div>
                <div style="font-size: 1.08rem; font-weight: 800; color: #ffffff; margin-top: 2px;">{toughest_sub.replace('_', ' ')}</div>
                <div style="font-size: 0.82rem; color: #cbd5e1; margin-top: 2px;">Class Avg: <b style="color: #f87171;">{sub_averages[toughest_sub]:.2f} / 20</b></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class='apple-card'>
        <div class='apple-card-header'>
            <div class='apple-card-title'>📋 Student Master Directory</div>
            <div class='apple-card-caption'>Instant Lookup & Export</div>
        </div>
    """, unsafe_allow_html=True)

    search_query = st.text_input("Search student by name or roll number...", placeholder="🔍 Type student name or 4-digit roll number...", label_visibility="collapsed")

    if search_query:
        filtered_df = df[
            df["Name"].str.contains(search_query, case=False, na=False) |
            df["Enrollment_Number"].astype(str).str.contains(search_query, na=False)
        ]
    else:
        filtered_df = df

    st.dataframe(filtered_df, use_container_width=True, hide_index=True)

    csv_bytes = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Master Marks CSV",
        data=csv_bytes,
        file_name="MST_Student_Marks.csv",
        mime="text/csv"
    )
    st.markdown("</div>", unsafe_allow_html=True)


elif menu == "👤 Student Analysis":
    st.markdown("""
    <div class='apple-window-header'>
        <div class='apple-title-group'>
            <div class='apple-title'>👤 Individual Student Performance Analysis</div>
            <div class='apple-subtitle'>Deep dive into student marks, growth targets, and class benchmarks</div>
        </div>
        <div class='apple-status-pill'>
            <div class='apple-status-dot'></div>
            Student Diagnostic Center
        </div>
    </div>
    """, unsafe_allow_html=True)

    student_options = [f"{row['Name']} (Roll: {row['Enrollment_Number']})" for _, row in df.iterrows()]
    selected_option = st.selectbox("Select Student:", student_options)

    if selected_option:
        roll_selected = selected_option.split("Roll: ")[1].replace(")", "").strip()
        student_data = df[df["Enrollment_Number"].astype(str) == str(roll_selected)]
        if student_data.empty:
            st.error("Student record not found in database!")
            st.stop()

        student = student_data.iloc[0]

        df_temp = df.copy()
        df_temp["Rank"] = df_temp["Total"].rank(ascending=False, method="min")
        rank_data = df_temp.loc[df_temp["Enrollment_Number"].astype(str) == str(roll_selected),"Rank"]
        if rank_data.empty:
            st.error("Student rank not found!")
            st.stop()

        rank = int(rank_data.iloc[0])

        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Student Name", student["Name"], f"Roll: {student['Enrollment_Number']}")
        k2.metric("Total Marks", f"{student['Total']} / 100", f"Percentage: {student['Total']:.1f}%")
        k3.metric("Average Score", f"{student['Average']:.2f} / 20", f"Out of 20 max")
        k4.metric("Class Standing", f"Rank #{rank}", f"Out of {len(df)} students")

        st.markdown("<div style='margin-top: 1.2rem;'></div>", unsafe_allow_html=True)

        c1, c2 = st.columns([1.15, 1.85])

        with c1:
            st.markdown("""
            <div class='apple-card'>
                <div class='apple-card-header'>
                    <div class='apple-card-title'>📑 Subject Performance Breakdown</div>
                    <div class='apple-card-caption'>Status & Remarks</div>
                </div>
            """, unsafe_allow_html=True)

            subject_analysis_data = []
            priority_subjects = []

            for sub in subject_cols:
                raw_m = student[sub]
                clean_name = sub.replace("_", " ")
                if pd.isna(raw_m):
                    status = "Absent"
                    remark = "Needs Improvement (Absent)"
                    priority_subjects.append((clean_name, -1, "Absent", 14))
                else:
                    m = float(raw_m)
                    if m >= 17:
                        remark = "Strong"
                    elif m >= 14:
                        remark = "Good"
                    elif m >= 10:
                        remark = "Average"
                        priority_subjects.append((clean_name, m, f"{m}", 15))
                    else:
                        remark = "Needs Improvement"
                        priority_subjects.append((clean_name, m, f"{m}", 14))
                    status = f"{m:.1f} / 20"

                subject_analysis_data.append({"Subject": clean_name, "Marks": status, "Remark": remark})

            st.dataframe(pd.DataFrame(subject_analysis_data), use_container_width=True, hide_index=True)

            st.markdown("<div style='font-size: 1.02rem; font-weight: 700; margin-top: 1.2rem; margin-bottom: 0.6rem; color: #f8fafc;'>🎯 Growth Targets & Recommendations</div>", unsafe_allow_html=True)
            priority_subjects.sort(key=lambda x: x[1])

            if priority_subjects:
                for idx, (psub, _, p_mstr, p_target) in enumerate(priority_subjects, 1):
                    st.warning(f"**{idx}. {psub}**: Current: `{p_mstr}` ➔ **Suggested Target: `{p_target}/20`**")
            else:
                st.success("🎉 Outstanding consistency! All subjects are at Good or Strong level.")

            st.markdown("</div>", unsafe_allow_html=True)

        with c2:
            st.markdown("""
            <div class='apple-card'>
                <div class='apple-card-header'>
                    <div class='apple-card-title'>📈 Marks vs Class Average Benchmark</div>
                    <div class='apple-card-caption'>Comparative Visual</div>
                </div>
            """, unsafe_allow_html=True)

            std_scores = [0 if pd.isna(student[s]) else float(student[s]) for s in subject_cols]
            class_avgs = [round(df[s].mean(), 2) for s in subject_cols]
            clean_names = [s.replace("_", " ") for s in subject_cols]

            x_idx = np.arange(len(subject_cols))
            w = 0.35

            fig, ax = plt.subplots(figsize=(7.5, 4.5))
            fig.patch.set_facecolor('none')
            ax.set_facecolor('none')

            b1 = ax.bar(x_idx - w/2, std_scores, width=w, label=f"{student['Name']}'s Marks", color='#38bdf8', edgecolor='none', zorder=3)
            b2 = ax.bar(x_idx + w/2, class_avgs, width=w, label="Class Average", color='#fbbf24', edgecolor='none', zorder=3)

            ax.set_xticks(x_idx)
            ax.set_xticklabels(clean_names, rotation=12, fontsize=8.5)
            ax.set_ylim(0, 22)
            ax.set_ylabel("Marks (out of 20)", color="#94a3b8")
            ax.legend(frameon=True, facecolor="#1e293b", edgecolor="#334155")
            ax.set_ylabel("Marks (out of 20) -->", color="#94a3b8")
            ax.set_xlabel("Subjects -->", color="#94a3b8")
            ax.legend(frameon=True, facecolor="#1e293b", edgecolor="#475569", labelcolor="#f8fafc", fontsize=9)
            ax.grid(axis='y', linestyle=':', color="#334155", alpha=0.5, zorder=0)

            ax.tick_params(colors="#cbd5e1")
            for spine in ax.spines.values():
                spine.set_color("#334155")

            for b in b1:
                h = b.get_height()
                ax.text(b.get_x() + b.get_width()/2, h + 0.35, f"{h:.1f}", ha='center', fontsize=8, fontweight='bold', color="#ffffff")
            for b in b2:
                h = b.get_height()
                ax.text(b.get_x() + b.get_width()/2, h + 0.35, f"{h:.1f}", ha='center', fontsize=8, color="#cbd5e1")

            plt.tight_layout()
            st.pyplot(fig)
            st.markdown("</div>", unsafe_allow_html=True)


elif menu == "🏫 Class Analysis":
    st.markdown("""
    <div class='apple-window-header'>
        <div class='apple-title-group'>
            <div class='apple-title'>🏫 Class-wide Analytical Insights</div>
            <div class='apple-subtitle'>Deep dive into overall performance, best/toughest subjects, and benchmarks</div>
        </div>
        <div class='apple-status-pill'>
            <div class='apple-status-dot'></div>
            Class Analytics Engine
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class='apple-card'>
            <div class='apple-card-header'>
                <div class='apple-card-title'>📊 Performance Segregation</div>
                <div class='apple-card-caption'>Above / Below Class Average</div>
            </div>
        """, unsafe_allow_html=True)

        class_avg = df["Average"].mean()
        above_avg_df = df[df["Average"] >= class_avg]
        below_avg_df = df[df["Average"] < class_avg]

        st.success(f"**Students ≥ Class Average ({class_avg:.2f})**: {len(above_avg_df)} students")
        with st.expander("View Students Above Average"):
            for _, r in above_avg_df.iterrows():
                st.write(f"• **{r['Name']}** (Roll: {r['Enrollment_Number']}) - Total: `{r['Total']}` | Avg: `{r['Average']:.2f}`")

        st.error(f"**Students < Class Average ({class_avg:.2f})**: {len(below_avg_df)} students")
        with st.expander("View Students Below Average"):
            for _, r in below_avg_df.iterrows():
                st.write(f"• **{r['Name']}** (Roll: {r['Enrollment_Number']}) - Total: `{r['Total']}` | Avg: `{r['Average']:.2f}`")

        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class='apple-card'>
            <div class='apple-card-header'>
                <div class='apple-card-title'>🌟 Subject Highlights & Difficulty</div>
                <div class='apple-card-caption'>Curriculum Metrics</div>
            </div>
        """, unsafe_allow_html=True)

        sub_averages = {s: df[s].mean() for s in subject_cols}
        best_sub = max(sub_averages, key=sub_averages.get)
        toughest_sub = min(sub_averages, key=sub_averages.get)

        st.info(f"★ **Highest Scoring Subject**: `{best_sub.replace('_', ' ')}`\n\nClass Average: **{sub_averages[best_sub]:.2f} / 20**")
        st.warning(f"▲ **Toughest Subject**: `{toughest_sub.replace('_', ' ')}`\n\nClass Average: **{sub_averages[toughest_sub]:.2f} / 20**")

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class='apple-card'>
        <div class='apple-card-header'>
            <div class='apple-card-title'>🔍 Subject-Specific Class Inspection</div>
            <div class='apple-card-caption'>Student Score Distribution</div>
        </div>
    """, unsafe_allow_html=True)

    chosen_sub = st.selectbox("Select Subject for Inspection:", [s.replace("_", " ") for s in subject_cols])
    orig_sub = chosen_sub.replace(" ", "_")

    s_col1, s_col2, s_col3 = st.columns(3)
    s_series = pd.to_numeric(df[orig_sub], errors='coerce')
    s_avg = s_series.mean()
    s_max = s_series.max()
    s_min = s_series.min()

    highest_stds = df.loc[df[orig_sub] == s_max, "Name"].tolist()
    lowest_stds = df.loc[df[orig_sub] == s_min, "Name"].tolist()

    s_col1.metric(f"{chosen_sub} Average", f"{s_avg:.2f} / 20")
    s_col2.metric("Highest Score", f"{s_max:.1f}", f"Scored by: {', '.join(highest_stds)}")
    s_col3.metric("Lowest Score", f"{s_min:.1f}", f"Scored by: {', '.join(lowest_stds)}")

    st.write("")
    fig, ax = plt.subplots(figsize=(9, 4))
    fig.patch.set_facecolor('none')
    ax.set_facecolor('none')

    st_scores = s_series.fillna(0)
    bars = ax.bar(df["Name"], st_scores, color="#a78bfa", edgecolor="none", width=0.48, zorder=3)
    ax.axhline(s_avg, color="#f43f5e", linestyle="--", linewidth=1.5, label=f"Subject Avg ({s_avg:.2f})", zorder=4)
    ax.set_ylim(0, 22)
    ax.set_ylabel("Marks (out of 20) -->", color="#94a3b8")
    ax.set_xlabel("Students -->", color="#94a3b8")
    ax.legend(frameon=True, facecolor="#B8CBDC", edgecolor="#5D6E8B")
    ax.legend(frameon=True, facecolor="#1e293b", edgecolor="#475569", labelcolor="#f8fafc", fontsize=9)
    ax.grid(axis='y', linestyle=':', color="#5D6E8B", alpha=0.5, zorder=0)

    ax.tick_params(colors="#cbd5e1")
    for spine in ax.spines.values():
        spine.set_color("#334155")

    for i, bar in enumerate(bars):
        h = bar.get_height()
        label = "Absent" if pd.isna(df.loc[i, orig_sub]) else f"{h:.1f}"
        ax.text(bar.get_x() + bar.get_width() / 2, h + 0.35, label, ha='center', fontsize=8.5, fontweight='bold', color="#ffffff")

    plt.xticks(rotation=12)
    plt.tight_layout()
    st.pyplot(fig)
    st.markdown("</div>", unsafe_allow_html=True)


elif menu == "📊 Visualizations":
    st.markdown("""
    <div class='apple-window-header'>
        <div class='apple-title-group'>
            <div class='apple-title'>📊 Interactive Visual Analytics Gallery</div>
            <div class='apple-subtitle'>Explore comprehensive graphs, student comparisons, and distributions</div>
        </div>
        <div class='apple-status-pill'>
            <div class='apple-status-dot'></div>
            Visual Studio Engine
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='apple-card'>
        <div class='apple-card-header'>
            <div class='apple-card-title'>🎨 Visualization Selector</div>
            <div class='apple-card-caption'>Select Analytical Perspective</div>
        </div>
    """, unsafe_allow_html=True)

    viz_choice = st.selectbox(
        "Choose Chart to View:",
        [
            "1. Total Marks of Every Student",
            "2. Marks in Each Subject (Grouped Bar Chart)",
            "3. Marks Obtained by Specific Student",
            "4. Average Performance of All Students",
            "5. Subject-wise Class Average Comparison",
            "6. Marks of All Students in a Specific Subject",
            "7. Student vs Class Average Benchmark Comparison",
            "8. Class Overall Grade Distribution (Pie Chart)"
        ]
    )

    st.markdown("</div>", unsafe_allow_html=True)


    if viz_choice.startswith("1."):
        st.markdown("""
        <div class='apple-card-header'>
            <div class='apple-card-title'>📊 Total Marks Scored by Students</div>
            <div class='apple-card-caption'>Out of 100 Maximum Marks</div>
        </div>
        """, unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(9, 4.5))
        fig.patch.set_facecolor('none')
        ax.set_facecolor('none')

        bars = ax.bar(df["Name"], df["Total"], color="#38bdf8", edgecolor="none", width=0.48, zorder=3)
        ax.set_yticks(np.arange(0, 101, 10))
        ax.set_ylabel("Total Marks -->", color="#94a3b8")
        ax.set_xlabel("Students -->", color="#94a3b8")
        ax.grid(axis='y', linestyle=':', color="#334155", alpha=0.5, zorder=0)
        ax.tick_params(colors="#cbd5e1")
        for s in ax.spines.values():
            s.set_color("#334155")

        for b in bars:
            h = b.get_height()
            ax.text(b.get_x() + b.get_width() / 2, h + 1, f"{h:.1f}", ha='center', fontsize=9, fontweight='bold', color="#ffffff")
        plt.tight_layout()
        st.pyplot(fig)

    elif viz_choice.startswith("2."):
        st.markdown("""
        <div class='apple-card-header'>
            <div class='apple-card-title'>📊 All Subject Marks for Each Student</div>
            <div class='apple-card-caption'>Grouped Multi-Subject Comparison</div>
        </div>
        """, unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(11, 5.5))
        fig.patch.set_facecolor('none')
        ax.set_facecolor('none')

        clean_sub_names = [s.replace("_", " ") for s in subject_cols]
        df_plot = df.set_index("Name")[subject_cols]
        df_plot.columns = clean_sub_names

        df_plot.plot(kind="bar", ax=ax, width=0.75, colormap="viridis", edgecolor="none")
        ax.set_yticks(np.arange(0, 21, 2))
        ax.set_ylabel("Marks -->", color="#94a3b8")
        ax.set_xlabel("Students -->", color="#94a3b8")
        plt.xticks(rotation=0)
        ax.legend(title="Subjects", frameon=True, facecolor="#1e293b", edgecolor="#334155")
        ax.grid(axis='y', linestyle=':', color="#334155", alpha=0.5)
        ax.tick_params(colors="#cbd5e1")
        for s in ax.spines.values():
            s.set_color("#334155")
        plt.tight_layout()
        st.pyplot(fig)

    elif viz_choice.startswith("3."):
        st.markdown("""
        <div class='apple-card-header'>
            <div class='apple-card-title'>📊 Marks Obtained by Specific Student</div>
            <div class='apple-card-caption'>Subject Breakdown (out of 20)</div>
        </div>
        """, unsafe_allow_html=True)
        sname_opt3 = st.selectbox(
            "Select Student:",
            [f"{r['Name']} (Roll: {r['Enrollment_Number']})" for _, r in df.iterrows()],
            key="viz_opt3_student"
        )
        if sname_opt3:
            roll_val = int(sname_opt3.split("Roll: ")[1].replace(")", "").strip())
            st_row = df[df["Enrollment_Number"] == roll_val].iloc[0]
            clean_names = [sub.replace("_", " ") for sub in subject_cols]
            marks_raw = [pd.to_numeric(st_row[s], errors='coerce') for s in subject_cols]
            marks_plot = [0 if pd.isna(m) else m for m in marks_raw]

            fig, ax = plt.subplots(figsize=(9, 4.5))
            fig.patch.set_facecolor('none')
            ax.set_facecolor('none')

            bars = ax.bar(clean_names, marks_plot, color='#38bdf8', edgecolor='none', width=0.48, zorder=3)
            ax.set_yticks(np.arange(0, 21, 2))
            ax.set_ylim(0, 22)
            ax.set_ylabel("Marks (out of 20) -->", color="#94a3b8")
            ax.set_xlabel("Subjects -->", color="#94a3b8")
            ax.grid(axis='y', linestyle=':', color="#334155", alpha=0.5, zorder=0)
            ax.tick_params(colors="#cbd5e1")
            for s in ax.spines.values():
                s.set_color("#334155")

            for idx, bar in enumerate(bars):
                h = bar.get_height()
                label = "Absent" if pd.isna(marks_raw[idx]) else f"{h:.1f}"
                ax.text(bar.get_x() + bar.get_width() / 2, h + 0.35, label, ha='center', fontsize=9, fontweight='bold', color="#ffffff")

            plt.xticks(rotation=12)
            plt.tight_layout()
            st.pyplot(fig)

    elif viz_choice.startswith("4."):
        st.markdown("""
        <div class='apple-card-header'>
            <div class='apple-card-title'>📊 Average Performance of Every Student</div>
            <div class='apple-card-caption'>Student Averages (out of 20)</div>
        </div>
        """, unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(9, 4.5))
        fig.patch.set_facecolor('none')
        ax.set_facecolor('none')

        bars = ax.bar(df["Name"], df["Average"], color="#fbbf24", edgecolor="none", width=0.48, zorder=3)
        ax.set_yticks(np.arange(0, 21, 2))
        ax.set_ylabel("Average Marks (out of 20) -->", color="#94a3b8")
        ax.set_xlabel("Students -->", color="#94a3b8")
        ax.grid(axis='y', linestyle=':', color="#334155", alpha=0.5, zorder=0)
        ax.tick_params(colors="#cbd5e1")
        for s in ax.spines.values():
            s.set_color("#334155")

        for b in bars:
            h = b.get_height()
            ax.text(b.get_x() + b.get_width() / 2, h + 0.35, f"{h:.2f}", ha='center', fontsize=9, fontweight='bold', color="#ffffff")
        plt.tight_layout()
        st.pyplot(fig)

    elif viz_choice.startswith("5."):
        st.markdown("""
        <div class='apple-card-header'>
            <div class='apple-card-title'>📊 Subject-wise Class Average Marks</div>
            <div class='apple-card-caption'>Curriculum Benchmarks</div>
        </div>
        """, unsafe_allow_html=True)
        avg_marks = [df[sub].mean() for sub in subject_cols]
        clean_names = [sub.replace("_", " ") for sub in subject_cols]

        fig, ax = plt.subplots(figsize=(9, 4.5))
        fig.patch.set_facecolor('none')
        ax.set_facecolor('none')

        bars = ax.bar(clean_names, avg_marks, color="#34d399", edgecolor="none", width=0.48, zorder=3)
        ax.set_yticks(np.arange(0, 21, 2))
        ax.set_ylabel("Average Marks -->", color="#94a3b8")
        ax.set_xlabel("Subjects -->", color="#94a3b8")
        ax.grid(axis='y', linestyle=':', color="#334155", alpha=0.5, zorder=0)
        ax.tick_params(colors="#cbd5e1")
        for s in ax.spines.values():
            s.set_color("#334155")

        for b in bars:
            h = b.get_height()
            ax.text(b.get_x() + b.get_width() / 2, h + 0.35, f"{h:.2f}", ha='center', fontsize=9, fontweight='bold', color="#ffffff")
        plt.tight_layout()
        st.pyplot(fig)

    elif viz_choice.startswith("6."):
        st.markdown("""
        <div class='apple-card-header'>
            <div class='apple-card-title'>📊 Marks Scored by All Students in Specific Subject</div>
            <div class='apple-card-caption'>With Subject Class Average Benchmark</div>
        </div>
        """, unsafe_allow_html=True)
        chosen_sub_opt6 = st.selectbox(
            "Select Subject:",
            [s.replace("_", " ") for s in subject_cols],
            key="viz_opt6_subject"
        )
        if chosen_sub_opt6:
            orig_sub = chosen_sub_opt6.replace(" ", "_")
            sub_series = pd.to_numeric(df[orig_sub], errors='coerce')
            sub_avg_val = sub_series.mean()
            sub_plot_scores = sub_series.fillna(0)

            fig, ax = plt.subplots(figsize=(9, 4.5))
            fig.patch.set_facecolor('none')
            ax.set_facecolor('none')

            bars = ax.bar(df["Name"], sub_plot_scores, color='#a78bfa', edgecolor='none', width=0.48, zorder=3)
            ax.axhline(sub_avg_val, color='#f43f5e', linestyle='--', linewidth=1.5, label=f"Class Avg ({sub_avg_val:.2f})", zorder=4)
            ax.set_yticks(np.arange(0, 21, 2))
            ax.set_ylim(0, 22)
            ax.set_ylabel("Marks (out of 20) -->", color="#94a3b8")
            ax.set_xlabel("Students -->", color="#94a3b8")
            ax.legend(frameon=True, facecolor="#1e293b", edgecolor="#334155")
            ax.legend(frameon=True, facecolor="#1e293b", edgecolor="#475569", labelcolor="#f8fafc", fontsize=9)
            ax.grid(axis='y', linestyle=':', color="#334155", alpha=0.5, zorder=0)
            ax.tick_params(colors="#cbd5e1")
            for s in ax.spines.values():
                s.set_color("#334155")

            for i, bar in enumerate(bars):
                h = bar.get_height()
                label = "Absent" if pd.isna(df.loc[i, orig_sub]) else f"{h:.1f}"
                ax.text(bar.get_x() + bar.get_width() / 2, h + 0.35, label, ha='center', fontsize=8.5, fontweight='bold', color="#ffffff")

            plt.xticks(rotation=12)
            plt.tight_layout()
            st.pyplot(fig)

    elif viz_choice.startswith("7."):
        st.markdown("""
        <div class='apple-card-header'>
            <div class='apple-card-title'>📊 Student vs Class Average Benchmark Comparison</div>
            <div class='apple-card-caption'>Dual-Series Subject Evaluation</div>
        </div>
        """, unsafe_allow_html=True)
        sname = st.selectbox("Select Student to Compare:", df["Name"].tolist(), key="viz_opt7_student")
        student_row = df[df["Name"] == sname].iloc[0]

        std_marks = [pd.to_numeric(student_row[sub], errors='coerce') for sub in subject_cols]
        std_marks_plot = [0 if pd.isna(m) else m for m in std_marks]
        class_avgs = [round(df[sub].mean(), 2) for sub in subject_cols]
        clean_names = [s.replace("_", " ") for s in subject_cols]

        x_indices = np.arange(len(subject_cols))
        width = 0.35

        fig, ax = plt.subplots(figsize=(10, 5))
        fig.patch.set_facecolor('none')
        ax.set_facecolor('none')

        bars1 = ax.bar(x_indices - width/2, std_marks_plot, width=width, label=f"{sname}'s Marks", color='#38bdf8', edgecolor='none', zorder=3)
        bars2 = ax.bar(x_indices + width/2, class_avgs, width=width, label="Class Average", color='#fbbf24', edgecolor='none', zorder=3)

        ax.set_xticks(x_indices)
        ax.set_xticklabels(clean_names, rotation=12)
        ax.set_yticks(np.arange(0, 21, 2))
        ax.set_ylabel("Marks -->", color="#94a3b8")
        ax.set_xlabel("Subjects -->", color="#94a3b8")
        ax.legend(frameon=True, facecolor="#1e293b", edgecolor="#334155")
        ax.grid(axis='y', linestyle=':', color="#334155", alpha=0.5, zorder=0)
        ax.tick_params(colors="#cbd5e1")
        for s in ax.spines.values():
            s.set_color("#334155")

        for idx, bar in enumerate(bars1):
            h = bar.get_height()
            label = "Absent" if pd.isna(std_marks[idx]) else f"{h:.1f}"
            ax.text(bar.get_x() + bar.get_width()/2, h + 0.35, label, ha='center', fontsize=8, fontweight='bold', color="#ffffff")

        for bar in bars2:
            h = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, h + 0.35, f"{h:.1f}", ha='center', fontsize=8, color="#cbd5e1")

        plt.tight_layout()
        st.pyplot(fig)

    elif viz_choice.startswith("8."):
        st.markdown("""
        <div class='apple-card-header'>
            <div class='apple-card-title'>📊 Overall Class Grade Distribution</div>
            <div class='apple-card-caption'>Academic Tier Breakdown</div>
        </div>
        """, unsafe_allow_html=True)
        grade_a = df[df["Total"] >= 80]
        grade_b = df[(df["Total"] >= 60) & (df["Total"] < 80)]
        grade_c = df[(df["Total"] >= 40) & (df["Total"] < 60)]
        needs_imp = df[df["Total"] < 40]

        grades_config = [
            ("Grade A (≥80%)", grade_a, '#34d399'),
            ("Grade B (60-79%)", grade_b, '#38bdf8'),
            ("Grade C (40-59%)", grade_c, '#fbbf24'),
            ("Needs Improvement (<40%)", needs_imp, '#f43f5e'),
        ]

        active_grades = [(t, s, c) for t, s, c in grades_config if len(s) > 0]
        sizes = [len(s) for _, s, _ in active_grades]
        colors = [c for _, _, c in active_grades]
        explode = [0.05] * len(sizes)
        slice_labels = [f"{t}\n({len(s)} std)" for t, s, _ in active_grades]

        legend_labels = []
        for t, s, _ in active_grades:
            names = ", ".join([f"{r['Name']}" for _, r in s.iterrows()])
            legend_labels.append(f"{t} ({len(s)}): {names}")

        fig, ax = plt.subplots(figsize=(10, 5.5))
        fig.patch.set_facecolor('none')
        ax.set_facecolor('none')

        wedges, texts, autotexts = ax.pie(
            sizes,
            labels=slice_labels,
            autopct='%1.1f%%',
            startangle=140,
            colors=colors,
            explode=explode,
            shadow=True,
            textprops={'fontsize': 10, 'fontweight': 'bold', 'color': '#cbd5e1'}
        )

        for at in autotexts:
            at.set_fontsize(10)
            at.set_color('#0f172a')
            at.set_fontweight('bold')

        ax.legend(
            wedges,
            legend_labels,
            title="Student Breakdown",
            loc="center left",
            bbox_to_anchor=(1.05, 0.5),
            fontsize=9,
            frameon=True,
            facecolor="#1e293b",
            edgecolor="#334155"
        )
        plt.tight_layout()
        st.pyplot(fig)

    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "📝 Record Management":
    st.markdown("""
    <div class='apple-window-header'>
        <div class='apple-title-group'>
            <div class='apple-title'>📝 Student Marks Management (CRUD)</div>
            <div class='apple-subtitle'>Add new student records, modify marks, or safely purge entries</div>
        </div>
        <div class='apple-status-pill'>
            <div class='apple-status-dot'></div>
            Live Database Sync
        </div>
    </div>
    """, unsafe_allow_html=True)

    tab_add, tab_edit, tab_del, tab_view = st.tabs(["➕ Add Student", "✏️ Update Marks", "🗑️ Delete Record", "📋 Master Records"])

    with tab_add:
        st.markdown("""
        <div class='apple-card'>
            <div class='apple-card-header'>
                <div class='apple-card-title'>➕ Register New Student</div>
                <div class='apple-card-caption'>Full Record Creation</div>
            </div>
        """, unsafe_allow_html=True)

        with st.form("add_student_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            new_name = col1.text_input("Student Full Name *", placeholder="e.g. Rahul Sharma")
            new_roll = col2.number_input("4-digit Enrollment Number *", min_value=1000, max_value=9999, step=1, value=1080)

            st.write("**Subject Marks (Maximum 20):**")
            m_cols = st.columns(5)
            new_marks = {}
            for i, sub in enumerate(subject_cols):
                new_marks[sub] = m_cols[i].number_input(f"{sub.replace('_', ' ')}", min_value=0.0, max_value=20.0, step=0.5, value=15.0)

            st.write("")
            submitted = st.form_submit_button("Save Student Record", type="primary")

            if submitted:
                if not new_name.strip():
                    st.error("Student Name cannot be empty!")
                elif str(new_roll) in df["Enrollment_Number"].astype(str).values:
                    st.error(f"Enrollment Number {new_roll} already exists for {df.loc[df['Enrollment_Number']==new_roll, 'Name'].values[0]}!")
                else:
                    tot = round(sum(new_marks.values()), 2)
                    avg = round(tot / len(subject_cols), 2)
                    new_entry = {
                        "Name": new_name.strip(),
                        "Enrollment_Number": new_roll,
                        **new_marks,
                        "Total": tot,
                        "Average": avg
                    }
                    new_entry["Enrollment_Number"] = str(new_roll)
                    try:
                        add_student_record(new_entry)
                        st.success(f"✅ Record for **{new_name}** added successfully!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Failed to add student record: {e}")

        st.markdown("</div>", unsafe_allow_html=True)

    with tab_edit:
        st.markdown("""
        <div class='apple-card'>
            <div class='apple-card-header'>
                <div class='apple-card-title'>✏️ Update Student Marks</div>
                <div class='apple-card-caption'>Modify Existing Records</div>
            </div>
        """, unsafe_allow_html=True)

        student_to_edit = st.selectbox("Select Student to Update:", [f"{r['Name']} (Roll: {r['Enrollment_Number']})" for _, r in df.iterrows()], key="edit_selector")

        if student_to_edit:
            edit_roll = student_to_edit.split("Roll: ")[1].replace(")", "").strip()
            curr_row = df[df["Enrollment_Number"].astype(str) == edit_roll].iloc[0]
            curr_idx = df[df["Enrollment_Number"].astype(str) == edit_roll].index[0]

            with st.form("edit_student_form"):
                e_name = st.text_input("Student Name", value=curr_row["Name"])

                st.write("**Edit Marks (Maximum 20):**")
                em_cols = st.columns(5)
                updated_marks = {}
                for i, sub in enumerate(subject_cols):
                    default_val = 0.0 if pd.isna(curr_row[sub]) else float(curr_row[sub])
                    updated_marks[sub] = em_cols[i].number_input(f"{sub.replace('_', ' ')}", min_value=0.0, max_value=20.0, step=0.5, value=default_val)

                st.write("")
                update_btn = st.form_submit_button("Update Changes", type="primary")

                if update_btn:
                    new_tot = round(sum(updated_marks.values()), 2)
                    new_avg = round(new_tot / len(subject_cols), 2)

                    df.loc[curr_idx, "Name"] = e_name.strip()
                    for sub in subject_cols:
                        df.loc[curr_idx, sub] = updated_marks[sub]
                    df.loc[curr_idx, "Total"] = new_tot
                    df.loc[curr_idx, "Average"] = new_avg

                    student_data = df.loc[curr_idx].to_dict()
                    update_student_record(edit_roll, student_data)
                    st.success(f"✅ Marks updated for **{e_name}**! New Total: {new_tot}, Avg: {new_avg}")
                    st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    with tab_del:
        st.markdown("""
        <div class='apple-card'>
            <div class='apple-card-header'>
                <div class='apple-card-title'>🗑️ Delete Student Record</div>
                <div class='apple-card-caption'>Permanent Removal Action</div>
            </div>
        """, unsafe_allow_html=True)

        del_target = st.selectbox("Select Student to Delete:", [f"{r['Name']} (Roll: {r['Enrollment_Number']})" for _, r in df.iterrows()], key="del_selector")

        if del_target:
            del_roll = del_target.split("Roll: ")[1].replace(")", "").strip()
            row_to_del = df[df["Enrollment_Number"].astype(str) == del_roll].iloc[0]

            st.warning(f"Are you sure you want to permanently remove **{row_to_del['Name']}** (Roll: {del_roll}) with Total Marks: `{row_to_del['Total']}`?")
            confirm_del = st.checkbox("Yes, I confirm deletion.")

            if st.button("Delete Permanently", type="primary", disabled=not confirm_del):
                deleted = delete_student_record(del_roll)
                if deleted:
                    st.success(f"✅ Record for Roll {del_roll} deleted successfully!")
                else :
                    st.error("❌ Record not found in database!")
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    with tab_view:
        st.markdown("""
        <div class='apple-card'>
            <div class='apple-card-header'>
                <div class='apple-card-title'>📋 Master Database Records</div>
                <div class='apple-card-caption'>Full Academic Ledger</div>
            </div>
        """, unsafe_allow_html=True)
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)


elif menu == "📄 Report Card Generator":
    st.markdown("""
    <div class='apple-window-header'>
        <div class='apple-title-group'>
            <div class='apple-title'>📄 Official College Report Card Generator</div>
            <div class='apple-subtitle'>Generate, preview, and download formal PDF marksheet certificates</div>
        </div>
        <div class='apple-status-pill'>
            <div class='apple-status-dot'></div>
            PDF Vector Engine
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='apple-card'>
        <div class='apple-card-header'>
            <div class='apple-card-title'>🎯 Marksheet Student Selection</div>
            <div class='apple-card-caption'>Pick Candidate</div>
        </div>
    """, unsafe_allow_html=True)

    c_sel, _ = st.columns([2, 1])
    target_student_name = c_sel.selectbox("Select Student for Marksheet:", df["Name"].tolist(), label_visibility="collapsed")
    st.markdown("</div>", unsafe_allow_html=True)

    if target_student_name:
        st_data = df[df["Name"] == target_student_name].iloc[0]

        grade_s, div_s = get_grade_and_status(st_data["Total"])
        df_temp = df.copy()
        df_temp["Rank"] = df_temp["Total"].rank(ascending=False, method="min")
        rank = int(df_temp.loc[df["Enrollment_Number"] == st_data["Enrollment_Number"], "Rank"].values[0])

        st.markdown(f"""
        <div class='apple-card'>
            <div style="text-align: center; border-bottom: 1px solid rgba(255, 255, 255, 0.1); padding-bottom: 1.1rem; margin-bottom: 1.4rem;">
                <div style="font-size: 1.35rem; font-weight: 800; color: #60a5fa; letter-spacing: -0.02em;">MARKS ANALYZER | REPORT CARD GENERATOR</div>
                <div style="color: #94a3b8; font-size: 0.92rem; margin: 3px 0; font-weight: 500;">DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING</div>
                <div style="display: inline-block; background: rgba(245, 158, 11, 0.15); border: 1px solid rgba(245, 158, 11, 0.35); color: #fbbf24; padding: 4px 16px; border-radius: 20px; font-weight: 700; font-size: 0.85rem; margin-top: 8px;">
                    MID SEMESTER TEST (MST) - STATEMENT OF MARKS
                </div>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 1.2rem; font-size: 0.95rem; line-height: 1.8;">
                <div>
                    <span style="color: #94a3b8;">Student Name:</span> <b style="color: #ffffff; font-size: 1.05rem;">{st_data['Name'].upper()}</b><br>
                    <span style="color: #94a3b8;">Enrollment No:</span> <b style="color: #ffffff;">{st_data['Enrollment_Number']}</b><br>
                    <span style="color: #94a3b8;">Class Standing:</span> <b style="color: #38bdf8;">Rank #{rank} out of {len(df)}</b>
                </div>
                <div style="text-align: right;">
                    <span style="color: #94a3b8;">Academic Session:</span> <b style="color: #ffffff;">2025-2026</b><br>
                    <span style="color: #94a3b8;">Semester / Branch:</span> <b style="color: #ffffff;">3rd Sem (CSE)</b><br>
                    <span style="color: #94a3b8;">Final Grade:</span> <b style="color: #34d399;">{grade_s}</b>
                </div>
            </div>
        """, unsafe_allow_html=True)

        sub_rows = []
        for s in subject_cols:
            val = st_data[s]
            score_str = "ABSENT" if pd.isna(val) else f"{float(val):.1f}"
            st_flag = "PASS" if (pd.notna(val) and float(val) >= 8.0) else "FAIL"
            sub_rows.append({
                "Subject Name": s.replace("_", " "),
                "Max Marks": 20,
                "Min Pass": 8,
                "Marks Obtained": score_str,
                "Result": st_flag
            })
        st.dataframe(pd.DataFrame(sub_rows), use_container_width=True, hide_index=True)

        st.write("")
        st.info(f"**Grand Total:** `{st_data['Total']}/100` &nbsp;•&nbsp; **Percentage:** `{st_data['Total']:.1f}%` &nbsp;•&nbsp; **Division:** `{div_s}`")

        st.markdown("<div style='margin-top: 1.2rem;'></div>", unsafe_allow_html=True)

        try:
            pdf_path = generate_pdf_report(st_data, df)
            with open(pdf_path, "rb") as f:
                pdf_bytes = f.read()

            st.download_button(
                label=f"⬇️ Download {st_data['Name']}'s Official PDF Marksheet",
                data=pdf_bytes,
                file_name=f"ReportCard_{st_data['Enrollment_Number']}_{st_data['Name']}.pdf",
                mime="application/pdf",
                type="primary",
                use_container_width=True
            )
            st.caption(f"📄 High-resolution vector PDF certificate • Local copy: `{pdf_path}`")
        except Exception as e:
            st.error(f"Could not prepare PDF: {e}")

        st.markdown("</div>", unsafe_allow_html=True)
