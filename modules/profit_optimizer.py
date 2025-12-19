import streamlit as st
import plotly.express as px

def render_page(df_profit):
    # Header with better styling
    st.markdown("""<h1 style='text-align: center;'>Vendor Profit Analysis</h1>""", unsafe_allow_html=True)
    st.markdown("""<p style='font-size: 1.1rem; color: #7f8c8d; margin-bottom: 2rem; text-align: center;'>Optimize carrier selection and maximize profit margins</p>""", unsafe_allow_html=True)
    
    # 1. Sidebar Control (Local to this module)
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Filter Options")
    routes = df_profit['Route'].unique()
    selected_route = st.sidebar.selectbox("Select Route", routes)
    
    # Filter Data
    route_df = df_profit[df_profit['Route'] == selected_route]
    
    # 2. KPI Section with enhanced styling
    st.markdown("<div style='margin: 2rem 0;'>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center;'>Key Performance Indicators</h4>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    
    total_profit = route_df['Net_Profit'].sum()
    avg_margin = route_df['Margin_Percent'].mean()
    bleeding_orders = len(route_df[route_df['Net_Profit'] < 0])
    total_orders = len(route_df)
    
    with c1:
        st.metric(
            "Total Profit", 
            f"₹{total_profit:,.0f}",
            delta=f"{total_profit/total_orders:.0f} per order" if total_orders > 0 else "N/A"
        )
    with c2:
        st.metric(
            "Avg Margin", 
            f"{avg_margin:.1f}%",
            delta="Healthy" if avg_margin > 10 else "Low",
            delta_color="normal" if avg_margin > 10 else "inverse"
        )
    with c3:
        st.metric(
            "Loss-Making Orders", 
            bleeding_orders,
            delta=f"{(bleeding_orders/total_orders*100):.1f}% of total" if total_orders > 0 else "N/A",
            delta_color="inverse" if bleeding_orders > 0 else "normal"
        )
    with c4:
        st.metric(
            "Total Orders", 
            total_orders,
            delta=f"{selected_route}"
        )
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("---")
    
    # 3. Main Analysis Tabs
    tab1, tab2 = st.tabs(["Performance Analysis", "Optimization Engine"])
    
    with tab1:
        st.markdown("#### Carrier Performance Matrix")
        st.markdown("<p style='color: #7f8c8d; margin-bottom: 1.5rem;'>Analyze carrier efficiency: profit vs delivery speed</p>", unsafe_allow_html=True)
        
        carrier_stats = route_df.groupby('Carrier').agg({
            'Net_Profit': 'mean', 
            'Actual_Delivery_Days': 'mean', 
            'Order_ID': 'count'
        }).reset_index()
        
        fig = px.scatter(
            carrier_stats, 
            x='Actual_Delivery_Days', 
            y='Net_Profit', 
            size='Order_ID', 
            color='Carrier',
            title="Carrier Performance: Profit vs Speed",
            labels={
                'Actual_Delivery_Days': 'Delivery Time (Days)',
                'Net_Profit': 'Average Profit (₹)',
                'Order_ID': 'Order Volume'
            },
            template="plotly_white"
        )
        fig.add_hline(y=0, line_dash="dash", line_color="#e74c3c", annotation_text="Break-even Point")
        fig.update_layout(
            height=500,
            font=dict(family="Arial, sans-serif", size=12),
            title_font=dict(size=18, color="#2c3e50"),
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig, use_container_width=True)
        
    with tab2:
        st.markdown("#### Carrier Optimization Simulator")
        st.markdown("<p style='color: #7f8c8d; margin-bottom: 1.5rem;'>Simulate carrier switches to maximize profitability</p>", unsafe_allow_html=True)
        
        best = carrier_stats.sort_values('Net_Profit', ascending=False).iloc[0]
        worst = carrier_stats.sort_values('Net_Profit', ascending=True).iloc[0]
        
        if worst['Carrier'] != best['Carrier']:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                    <div style='padding: 1.5rem; background-color: #fee; border-left: 4px solid #e74c3c; border-radius: 8px;'>
                        <h4 style='color: #c0392b; margin-top: 0;'>Underperforming Carrier</h4>
                        <p style='font-size: 1.5rem; font-weight: 700; margin: 0.5rem 0; color: #2c3e50;'>{}</p>
                        <p style='color: #5a6c7d; margin: 0; font-weight: 500;'>Avg Profit: ₹{:,.2f}</p>
                    </div>
                """.format(worst['Carrier'], worst['Net_Profit']), unsafe_allow_html=True)
                
            with col2:
                st.markdown("""
                    <div style='padding: 1.5rem; background-color: #efd; border-left: 4px solid #27ae60; border-radius: 8px;'>
                        <h4 style='color: #27ae60; margin-top: 0;'>Top Performing Carrier</h4>
                        <p style='font-size: 1.5rem; font-weight: 700; margin: 0.5rem 0; color: #2c3e50;'>{}</p>
                        <p style='color: #5a6c7d; margin: 0; font-weight: 500;'>Avg Profit: ₹{:,.2f}</p>
                    </div>
                """.format(best['Carrier'], best['Net_Profit']), unsafe_allow_html=True)
            
            st.markdown("<div style='margin: 2rem 0;'>", unsafe_allow_html=True)
            st.markdown("##### Switching Simulation")
            pct = st.slider(
                "Percentage of orders to switch from {} to {}".format(worst['Carrier'], best['Carrier']), 
                0, 100, 50,
                help="Adjust the slider to see potential savings"
            )
            
            savings = (best['Net_Profit'] - worst['Net_Profit']) * (worst['Order_ID'] * pct/100)
            
            st.markdown("""
                <div style='padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px; text-align: center; margin-top: 1.5rem;'>
                    <p style='color: rgba(255,255,255,0.9); margin: 0; font-size: 1rem;'>PROJECTED MONTHLY SAVINGS</p>
                    <p style='color: white; font-size: 3rem; font-weight: 700; margin: 0.5rem 0;'>₹{:,.2f}</p>
                    <p style='color: rgba(255,255,255,0.8); margin: 0; font-size: 0.9rem;'>By switching {}% of orders ({} orders)</p>
                </div>
            """.format(savings, pct, int(worst['Order_ID'] * pct/100)), unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info("This route is already using the optimal carrier. No switching recommendations available.")
