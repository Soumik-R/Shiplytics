import streamlit as st
import pandas as pd
import plotly.express as px

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Shiplytics | Profit Optimizer",
    page_icon="🚢",
    layout="wide"
)

# --- 1. DATA LOADING & PROCESSING ---
@st.cache_data
def load_and_prep_data():
    try:
        # Load Data
        orders = pd.read_csv('datasets/orders.csv')
        costs = pd.read_csv('datasets/cost_breakdown.csv')
        perf = pd.read_csv('datasets/delivery_performance.csv')
        routes = pd.read_csv('datasets/routes_distance.csv')
        
        # Merging Strategy
        # 1. Order + Costs
        df = pd.merge(orders, costs, on='Order_ID')
        # 2. Add Performance (Carrier info)
        df = pd.merge(df, perf[['Order_ID', 'Carrier', 'Actual_Delivery_Days', 'Delivery_Status']], on='Order_ID')
        # 3. Add Route info
        df = pd.merge(df, routes[['Order_ID', 'Route', 'Distance_KM']], on='Order_ID')
        
        # --- PROFITABILITY ENGINE ---
        # Calculate Total Operational Cost per Order
        cost_cols = ['Fuel_Cost', 'Labor_Cost', 'Vehicle_Maintenance', 'Insurance', 
                     'Packaging_Cost', 'Technology_Platform_Fee', 'Other_Overhead']
        df['Total_Cost'] = df[cost_cols].sum(axis=1)
        
        # Net Profit = Revenue - Cost
        df['Net_Profit'] = df['Order_Value_INR'] - df['Total_Cost']
        
        # Margin %
        df['Margin_Percent'] = (df['Net_Profit'] / df['Order_Value_INR']) * 100
        
        return df
    except FileNotFoundError as e:
        return None

df = load_and_prep_data()

if df is None:
    st.error("🚨 Error: CSV files not found. Please make sure all 7 CSV files are in the 'Shiplytics' folder.")
    st.stop()

# --- SIDEBAR FILTERS ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2830/2830305.png", width=50)
st.sidebar.title("Shiplytics Control")
st.sidebar.markdown("---")
selected_route = st.sidebar.selectbox("📍 Select Route to Optimize", df['Route'].unique())

# --- MAIN DASHBOARD ---
st.title("💰 Shiplytics: Vendor Profit Optimizer")
st.markdown("### *Identify bleeding routes and switch carriers to save costs instantly.*")
st.markdown("---")

# Filter Data Based on Selection
route_df = df[df['Route'] == selected_route]

# KPI ROW
col1, col2, col3, col4 = st.columns(4)
total_profit = route_df['Net_Profit'].sum()
avg_margin = route_df['Margin_Percent'].mean()
order_count = len(route_df)
bleeding_orders = len(route_df[route_df['Net_Profit'] < 0])

col1.metric("Total Route Profit", f"₹{total_profit:,.0f}", delta_color="normal")
col2.metric("Avg Margin %", f"{avg_margin:.1f}%", delta="-2.4%" if avg_margin < 15 else "1.2%")
col3.metric("Order Volume", order_count)
col4.metric("Loss-Making Orders", bleeding_orders, delta_color="inverse")

# --- TABBED INTERFACE ---
tab1, tab2, tab3 = st.tabs(["📊 Carrier Analysis", "🤖 Switch Simulator", "📝 Data View"])

# === TAB 1: CARRIER ANALYSIS ===
with tab1:
    st.subheader(f"Carrier Performance on {selected_route}")
    
    # Aggregate Data by Carrier
    carrier_stats = route_df.groupby('Carrier').agg({
        'Order_ID': 'count',
        'Net_Profit': 'mean',
        'Actual_Delivery_Days': 'mean',
        'Margin_Percent': 'mean'
    }).reset_index()
    
    # Scatter Plot: Cost vs Speed
    fig = px.scatter(carrier_stats, x='Actual_Delivery_Days', y='Net_Profit',
                     size='Order_ID', color='Carrier',
                     title="Carrier Efficiency Matrix (Size = Volume)",
                     labels={'Actual_Delivery_Days': 'Avg Delivery Time (Days)', 'Net_Profit': 'Avg Profit per Order (₹)'},
                     hover_data=['Margin_Percent'])
    
    # Add Reference Lines
    fig.add_hline(y=0, line_dash="dash", line_color="red", annotation_text="Break-even Point")
    st.plotly_chart(fig, use_container_width=True)
    
    st.info("💡 **Insight:** Carriers below the red line are destroying value. Carriers in the top-left are your 'Stars' (Fast & Profitable).")

# === TAB 2: SWITCH SIMULATOR ===
with tab2:
    st.subheader("🤖 AI Recommendation Engine")
    
    # Identify Best & Worst
    try:
        best_carrier = carrier_stats.sort_values('Net_Profit', ascending=False).iloc[0]
        worst_carrier = carrier_stats.sort_values('Net_Profit', ascending=True).iloc[0]
        
        if len(carrier_stats) > 1:
            col_a, col_b = st.columns(2)
            
            with col_a:
                st.error(f"📉 **Underperformer: {worst_carrier['Carrier']}**")
                st.write(f"Avg Profit: **₹{worst_carrier['Net_Profit']:.2f}**")
                st.write(f"Volume: {worst_carrier['Order_ID']} orders")
                
            with col_b:
                st.success(f"📈 **Recommended Switch: {best_carrier['Carrier']}**")
                st.write(f"Avg Profit: **₹{best_carrier['Net_Profit']:.2f}**")
                st.write(f"Potential Uplift: **+₹{best_carrier['Net_Profit'] - worst_carrier['Net_Profit']:.2f}/order**")
                
            # The Simulation
            st.markdown("#### 🛠️ Simulation Control")
            if worst_carrier['Carrier'] != best_carrier['Carrier']:
                percent_switch = st.slider(f"Shift volume from {worst_carrier['Carrier']} to {best_carrier['Carrier']}", 0, 100, 50)
                
                # Calculate Impact
                orders_to_move = int(worst_carrier['Order_ID'] * (percent_switch / 100))
                profit_gain_per_order = best_carrier['Net_Profit'] - worst_carrier['Net_Profit']
                total_savings = orders_to_move * profit_gain_per_order
                
                st.markdown(f"""
                <div style="padding: 20px; background-color: #d4edda; border-radius: 10px; border: 1px solid #c3e6cb;">
                    <h3 style="color: #155724; margin:0;">💰 Projected Monthly Savings: ₹{total_savings:,.2f}</h3>
                    <p style="color: #155724; margin:0;">By moving <b>{orders_to_move} orders</b>, you improve total route margin by significantly.</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("Only one carrier operates on this route. No switching opportunities available.")
            
    except Exception as e:
        st.write("Not enough data to generate recommendations for this route.")

# === TAB 3: DATA VIEW ===
with tab3:
    st.subheader("Raw Data Breakdown")
    # Conditional Formatting for Dataframe
    def color_negative_red(val):
        color = 'red' if val < 0 else 'green'
        return f'color: {color}'

    display_cols = ['Order_ID', 'Carrier', 'Net_Profit', 'Margin_Percent', 'Actual_Delivery_Days']
    try:
        st.dataframe(route_df[display_cols].style.map(color_negative_red, subset=['Net_Profit', 'Margin_Percent']))
    except:
        st.dataframe(route_df[display_cols]) # Fallback if style fails