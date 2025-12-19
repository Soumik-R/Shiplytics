import pandas as pd
import streamlit as st

@st.cache_data
def load_and_process_data():
    try:
        # Load Raw Data
        orders = pd.read_csv('datasets/orders.csv')
        costs = pd.read_csv('datasets/cost_breakdown.csv')
        perf = pd.read_csv('datasets/delivery_performance.csv')
        routes = pd.read_csv('datasets/routes_distance.csv')
        inventory = pd.read_csv('datasets/warehouse_inventory.csv')
        vehicles = pd.read_csv('datasets/vehicle_fleet.csv')
        
        # --- PROCESS PROFIT DATA ---
        # Merge: Orders + Costs + Performance + Routes
        df_profit = pd.merge(orders, costs, on='Order_ID')
        df_profit = pd.merge(df_profit, perf[['Order_ID', 'Carrier', 'Actual_Delivery_Days']], on='Order_ID')
        df_profit = pd.merge(df_profit, routes[['Order_ID', 'Route']], on='Order_ID')
        
        # Calculate Financials
        cost_cols = ['Fuel_Cost', 'Labor_Cost', 'Vehicle_Maintenance', 'Insurance', 
                     'Packaging_Cost', 'Technology_Platform_Fee', 'Other_Overhead']
        df_profit['Total_Cost'] = df_profit[cost_cols].sum(axis=1)
        df_profit['Net_Profit'] = df_profit['Order_Value_INR'] - df_profit['Total_Cost']
        df_profit['Margin_Percent'] = (df_profit['Net_Profit'] / df_profit['Order_Value_INR']) * 100
        
        return df_profit, inventory, orders, routes, vehicles
        
    except FileNotFoundError:
        return None, None, None, None, None