import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Hardcoded Coords for the Map
CITY_COORDS = {
    "Mumbai": {"lat": 19.0760, "lon": 72.8777},
    "Delhi": {"lat": 28.7041, "lon": 77.1025},
    "Bangalore": {"lat": 12.9716, "lon": 77.5946},
    "Chennai": {"lat": 13.0827, "lon": 80.2707},
    "Kolkata": {"lat": 22.5726, "lon": 88.3639},
    "Hyderabad": {"lat": 17.3850, "lon": 78.4867},
    "Ahmedabad": {"lat": 23.0225, "lon": 72.5714},
    "Pune": {"lat": 18.5204, "lon": 73.8567}
}

def render_page(df_inventory, df_orders):
    # Header with professional styling
    st.markdown("""<h1 style='text-align: center;'>Inventory Management System</h1>""", unsafe_allow_html=True)
    st.markdown("""<p style='font-size: 1.1rem; color: #7f8c8d; margin-bottom: 2rem; text-align: center;'>Intelligent inter-warehouse stock balancing and optimization</p>""", unsafe_allow_html=True)
    
    # 1. Data Prep
    demand_df = df_orders.groupby(['Origin', 'Product_Category']).size().reset_index(name='Demand_Count')
    stock_df = df_inventory[['Location', 'Product_Category', 'Current_Stock_Units', 'Reorder_Level']].copy()
    
    analysis_df = pd.merge(stock_df, demand_df, left_on=['Location', 'Product_Category'], right_on=['Origin', 'Product_Category'], how='left')
    analysis_df['Demand_Count'] = analysis_df['Demand_Count'].fillna(0)
    
    # Logic: Status Flagging
    analysis_df['Status'] = 'Healthy'
    analysis_df.loc[analysis_df['Current_Stock_Units'] < analysis_df['Reorder_Level'], 'Status'] = 'CRITICAL LOW'
    analysis_df.loc[analysis_df['Current_Stock_Units'] > (analysis_df['Reorder_Level'] * 3), 'Status'] = 'Overstocked'
    
    # 2. Filters with enhanced sidebar
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Filter Options")
    categories = analysis_df['Product_Category'].unique()
    selected_cat = st.sidebar.selectbox("Product Category", categories)
    cat_data = analysis_df[analysis_df['Product_Category'] == selected_cat]
    
    # Status Overview Cards
    critical_count = len(cat_data[cat_data['Status'] == 'CRITICAL LOW'])
    overstock_count = len(cat_data[cat_data['Status'] == 'Overstocked'])
    healthy_count = len(cat_data[cat_data['Status'] == 'Healthy'])
    
    st.markdown("#### Inventory Status Overview")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div style='padding: 1.5rem; background-color: #fee; border-left: 4px solid #e74c3c; border-radius: 8px; text-align: center;'>
                <p style='color: #7f8c8d; margin: 0; font-size: 0.9rem;'>Critical Low</p>
                <p style='font-size: 2.5rem; font-weight: 700; margin: 0.5rem 0; color: #e74c3c;'>{}</p>
                <p style='color: #95a5a6; margin: 0; font-size: 0.85rem;'>Locations</p>
            </div>
        """.format(critical_count), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div style='padding: 1.5rem; background-color: #fef9e7; border-left: 4px solid #f39c12; border-radius: 8px; text-align: center;'>
                <p style='color: #7f8c8d; margin: 0; font-size: 0.9rem;'>Overstocked</p>
                <p style='font-size: 2.5rem; font-weight: 700; margin: 0.5rem 0; color: #f39c12;'>{}</p>
                <p style='color: #95a5a6; margin: 0; font-size: 0.85rem;'>Locations</p>
            </div>
        """.format(overstock_count), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div style='padding: 1.5rem; background-color: #efd; border-left: 4px solid #27ae60; border-radius: 8px; text-align: center;'>
                <p style='color: #7f8c8d; margin: 0; font-size: 0.9rem;'>Healthy Stock</p>
                <p style='font-size: 2.5rem; font-weight: 700; margin: 0.5rem 0; color: #27ae60;'>{}</p>
                <p style='color: #95a5a6; margin: 0; font-size: 0.85rem;'>Locations</p>
            </div>
        """.format(healthy_count), unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("<div style='margin: 2rem 0;'>", unsafe_allow_html=True)
    
    # 3. Visualization with enhanced layout
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("#### Stock Health Analysis")
        fig_bar = px.bar(
            cat_data, 
            x='Location', 
            y=['Current_Stock_Units', 'Reorder_Level'], 
            barmode='group',
            color_discrete_map={'Current_Stock_Units': '#3498db', 'Reorder_Level': '#e74c3c'},
            labels={'value': 'Units', 'variable': 'Metric'},
            template="plotly_white"
        )
        fig_bar.update_layout(
            height=400,
            font=dict(family="Arial, sans-serif", size=11),
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            xaxis_title="",
            yaxis_title="Stock Units"
        )
        st.plotly_chart(fig_bar, use_container_width=True)
        
    with col2:
        st.markdown("#### Transfer Recommendations")
        
        # Transfer Logic
        deficits = cat_data[cat_data['Status'] == 'CRITICAL LOW']
        surpluses = cat_data[cat_data['Status'] == 'Overstocked']
        
        fig_map = go.Figure()
        
        if len(deficits) > 0 and len(surpluses) > 0:
            recommendations = []
            for idx, need in deficits.iterrows():
                if len(surpluses) > 0:
                    donor = surpluses.iloc[0]
                    
                    # Draw Line
                    start = CITY_COORDS.get(donor['Location'], {'lat':20, 'lon':78})
                    end = CITY_COORDS.get(need['Location'], {'lat':20, 'lon':78})
                    
                    fig_map.add_trace(go.Scattergeo(
                        lon = [start['lon'], end['lon']], 
                        lat = [start['lat'], end['lat']],
                        mode = 'lines+markers', 
                        line = dict(width=3, color='#3498db'),
                        marker = dict(size=12, color=['#f39c12', '#e74c3c']),
                        name = f"{donor['Location']} → {need['Location']}",
                        showlegend=True
                    ))
                    recommendations.append({
                        'From': donor['Location'],
                        'To': need['Location'],
                        'Available': int(donor['Current_Stock_Units']),
                        'Needed': int(need['Reorder_Level'] - need['Current_Stock_Units'])
                    })
            
            fig_map.update_layout(
                geo=dict(
                    scope='asia',
                    showland=True,
                    landcolor='rgb(243, 243, 243)',
                    coastlinecolor='rgb(204, 204, 204)',
                    projection_type='natural earth'
                ),
                height=400,
                margin={"r":0,"t":0,"l":0,"b":0},
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5)
            )
            st.plotly_chart(fig_map, use_container_width=True)
            
            # Show recommendations table
            if recommendations:
                st.markdown("##### Recommended Transfers")
                rec_df = pd.DataFrame(recommendations)
                st.dataframe(rec_df, use_container_width=True, hide_index=True)
        else:
            st.info("No stock transfers needed. All locations have balanced inventory levels.")
            
    st.markdown("</div>", unsafe_allow_html=True)
