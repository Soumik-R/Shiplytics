import streamlit as st
from utils.data_loader import load_and_process_data
import modules.profit_optimizer as profit_optimizer
import modules.inventory_bot as inventory_bot
import modules.route_optimizer as route_optimizer

# --- APP CONFIG ---
st.set_page_config(page_title="Shiplytics | Logistics AI", page_icon="📊", layout="wide", initial_sidebar_state="expanded")

# --- CUSTOM CSS FOR PROFESSIONAL LOOK ---
st.markdown("""
    <style>
    /* Main styling */
    .main {
        padding: 2rem;
    }
    
    /* Header styling */
    h1 {
        color: #1f77b4;
        font-weight: 700;
        padding-bottom: 1rem;
        border-bottom: 3px solid #1f77b4;
    }
    
    h2 {
        color: #2c3e50;
        font-weight: 600;
        margin-top: 1.5rem;
    }
    
    h3 {
        color: #34495e;
        font-weight: 500;
        font-style: italic;
        margin-bottom: 1rem;
    }
    
    /* Metric styling */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1f77b4 0%, #2c3e50 100%);
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        color: white;
    }
    
    [data-testid="stSidebar"] .stRadio > label {
        color: white;
        font-weight: 600;
        font-size: 1.1rem;
    }
    
    [data-testid="stSidebar"] .stRadio > div {
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        padding: 0.5rem;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(90deg, #1f77b4 0%, #2980b9 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(31, 119, 180, 0.4);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border-bottom: 3px solid transparent;
        color: #34495e;
        font-weight: 600;
        padding: 1rem 2rem;
    }
    
    .stTabs [aria-selected="true"] {
        border-bottom: 3px solid #1f77b4;
        color: #1f77b4;
    }
    
    /* Card-like containers */
    .block-container {
        padding: 2rem 3rem;
    }
    
    /* Dataframe styling */
    .stDataFrame {
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        overflow: hidden;
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div {
        background-color: #ffffff;
        border: 2px solid #d1d5db;
        border-radius: 8px;
    }
    
    .stSelectbox [data-baseweb="select"] {
        background-color: #ffffff;
    }
    
    .stSelectbox [data-baseweb="select"] > div {
        background-color: #ffffff;
        color: #1f2937;
        font-weight: 500;
    }
    
    .stSelectbox input {
        color: #1f2937 !important;
    }
    
    .stSelectbox div[role="button"] {
        color: #1f2937 !important;
    }
    
    /* Dropdown menu items */
    [data-baseweb="menu"] {
        background-color: #ffffff !important;
    }
    
    [data-baseweb="menu"] li {
        color: #1f2937 !important;
    }
    
    [data-baseweb="menu"] li:hover {
        background-color: #f3f4f6 !important;
    }
    
    /* Sidebar selectbox */
    [data-testid="stSidebar"] .stSelectbox > div > div {
        background-color: #ffffff !important;
        border: 2px solid #e5e7eb !important;
        border-radius: 8px;
    }
    
    [data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] {
        background-color: #ffffff !important;
    }
    
    [data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] > div {
        background-color: #ffffff !important;
        color: #1f2937 !important;
        font-weight: 500;
    }
    
    [data-testid="stSidebar"] .stSelectbox input {
        color: #1f2937 !important;
    }
    
    [data-testid="stSidebar"] .stSelectbox div[role="button"] {
        color: #1f2937 !important;
    }
    
    [data-testid="stSidebar"] .stSelectbox label {
        color: white !important;
        font-weight: 600;
    }
    
    [data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] svg {
        fill: #1f2937 !important;
    }
    
    /* Alert styling */
    .stAlert {
        border-radius: 8px;
        border-left: 4px solid;
    }
    
    /* Slider styling */
    .stSlider > div > div > div {
        background-color: #1f77b4;
    }
    </style>
""", unsafe_allow_html=True)

# --- DATA LOADING (Centralized) ---
df_profit, df_inventory, df_orders, df_routes, df_vehicles = load_and_process_data()

if df_profit is None:
    st.error("Critical Error: CSV files not found. Please check your folder.")
    st.stop()

# --- SIDEBAR NAVIGATION ---
st.sidebar.markdown("""
    <div style='text-align: center; padding: 1.5rem 0; margin-bottom: 2rem;'>
        <h1 style='color: white; margin: 0; font-size: 2rem; border: none;'>SHIPLYTICS</h1>
        <p style='color: rgba(255,255,255,0.8); margin: 0.5rem 0 0 0; font-size: 0.9rem;'>Logistics Intelligence Platform</p>
    </div>
""", unsafe_allow_html=True)

st.sidebar.markdown("<p style='color: white; font-weight: 600; font-size: 1.1rem; margin-bottom: 1rem;'>Navigation</p>", unsafe_allow_html=True)
page = st.sidebar.radio("Select Module", ["Vendor Profit Analysis", "Inventory Management", "Route Optimizer"], label_visibility="collapsed")

# --- PAGE ROUTING ---
if page == "Vendor Profit Analysis":
    profit_optimizer.render_page(df_profit)
    
elif page == "Inventory Management":
    inventory_bot.render_page(df_inventory, df_orders)
    
elif page == "Route Optimizer":
    route_optimizer.render_page(df_routes, df_vehicles)

# --- VERSION INFO AT BOTTOM OF SIDEBAR ---
st.sidebar.markdown("---")
st.sidebar.markdown("""
    <div style='padding: 1rem; background: rgba(255,255,255,0.1); border-radius: 8px; margin-top: 2rem; text-align: center;'>
        <p style='color: rgba(255,255,255,0.95); font-size: 0.9rem; margin: 0; font-weight: 500;'>
            Developed By<br>
            <strong style='font-size: 1.1rem;'>Soumik Roy</strong>
        </p>
    </div>
""", unsafe_allow_html=True)