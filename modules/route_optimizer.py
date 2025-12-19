import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# City coordinates for map visualization
CITY_COORDS = {
    "Mumbai": {"lat": 19.0760, "lon": 72.8777},
    "Delhi": {"lat": 28.7041, "lon": 77.1025},
    "Bangalore": {"lat": 12.9716, "lon": 77.5946},
    "Chennai": {"lat": 13.0827, "lon": 80.2707},
    "Kolkata": {"lat": 22.5726, "lon": 88.3639},
    "Hyderabad": {"lat": 17.3850, "lon": 78.4867},
    "Ahmedabad": {"lat": 23.0225, "lon": 72.5714},
    "Pune": {"lat": 18.5204, "lon": 73.8567},
    "Dubai": {"lat": 25.2048, "lon": 55.2708},
    "Singapore": {"lat": 1.3521, "lon": 103.8198},
    "Bangkok": {"lat": 13.7563, "lon": 100.5018},
    "Hong Kong": {"lat": 22.3193, "lon": 114.1694}
}

def parse_route_data(df_routes):
    """Parse route data to create origin-destination pairs with statistics"""
    route_stats = []
    
    for _, row in df_routes.iterrows():
        route = row['Route']
        if '-' in route:
            parts = route.split('-')
            origin = parts[0].strip()
            destination = parts[1].strip()
            
            route_stats.append({
                'Origin': origin,
                'Destination': destination,
                'Distance_KM': row['Distance_KM'],
                'Fuel_Consumption_L': row['Fuel_Consumption_L'],
                'Toll_Charges_INR': row['Toll_Charges_INR'],
                'Traffic_Delay_Minutes': row['Traffic_Delay_Minutes'],
                'Weather_Impact': row['Weather_Impact']
            })
    
    return pd.DataFrame(route_stats)

def render_page(df_routes, df_vehicles):
    # Header with professional styling
    st.markdown("""<h1 style='text-align: center;'>Smart Route Optimizer</h1>""", unsafe_allow_html=True)
    st.markdown("""<p style='font-size: 1.1rem; color: #7f8c8d; margin-bottom: 2rem; text-align: center;'>Find the shortest, most efficient, and cost-effective delivery routes</p>""", unsafe_allow_html=True)
    
    # Parse route data
    route_df = parse_route_data(df_routes)
    
    # Get unique cities (only Indian cities for domestic routes)
    indian_cities = ['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Kolkata', 
                     'Hyderabad', 'Ahmedabad', 'Pune']
    all_cities = list(set(route_df['Origin'].unique()) | set(route_df['Destination'].unique()))
    
    # Filter options with sidebar
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Route Configuration")
    route_type = st.sidebar.selectbox("Route Type", ["Domestic (India)", "International", "All Routes"])
    
    if route_type == "Domestic (India)":
        available_cities = [c for c in indian_cities if c in all_cities]
    else:
        available_cities = sorted(all_cities)
    
    # City selection
    st.markdown("<h4 style='text-align: center;'>Route Selection</h4>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        origin = st.selectbox("Origin City", available_cities, index=0, help="Select the starting point of your route", key="route_origin")
    
    with col2:
        dest_options = [c for c in available_cities if c != origin]
        destination = st.selectbox("Destination City", dest_options, 
                                   index=min(1, len(dest_options)-1) if dest_options else 0,
                                   help="Select the destination", key="route_dest")
    
    with col3:
        st.markdown("<br>", unsafe_allow_html=True)
        search_button = st.button("Find Routes", type="primary", use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Find all routes between selected cities
    routes_found = route_df[
        ((route_df['Origin'] == origin) & (route_df['Destination'] == destination)) |
        ((route_df['Origin'] == destination) & (route_df['Destination'] == origin))
    ]
    
    if len(routes_found) > 0:
        st.markdown("---")
        
        # Show shortest route
        shortest = routes_found.loc[routes_found['Distance_KM'].idxmin()]
        
        # KPIs with enhanced card design
        st.markdown("#### Optimal Route Metrics")
        st.markdown("<div style='margin-bottom: 2rem;'>", unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
                <div style='padding: 1.5rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; text-align: center;'>
                    <p style='color: rgba(255,255,255,0.8); margin: 0; font-size: 0.85rem;'>DISTANCE</p>
                    <p style='color: white; font-size: 2rem; font-weight: 700; margin: 0.5rem 0;'>{:.1f}</p>
                    <p style='color: rgba(255,255,255,0.8); margin: 0; font-size: 0.85rem;'>kilometers</p>
                </div>
            """.format(shortest['Distance_KM']), unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
                <div style='padding: 1.5rem; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); border-radius: 10px; text-align: center;'>
                    <p style='color: rgba(255,255,255,0.8); margin: 0; font-size: 0.85rem;'>FUEL</p>
                    <p style='color: white; font-size: 2rem; font-weight: 700; margin: 0.5rem 0;'>{:.1f}</p>
                    <p style='color: rgba(255,255,255,0.8); margin: 0; font-size: 0.85rem;'>liters</p>
                </div>
            """.format(shortest['Fuel_Consumption_L']), unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
                <div style='padding: 1.5rem; background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); border-radius: 10px; text-align: center;'>
                    <p style='color: rgba(255,255,255,0.8); margin: 0; font-size: 0.85rem;'>TOLL</p>
                    <p style='color: white; font-size: 2rem; font-weight: 700; margin: 0.5rem 0;'>₹{:.0f}</p>
                    <p style='color: rgba(255,255,255,0.8); margin: 0; font-size: 0.85rem;'>charges</p>
                </div>
            """.format(shortest['Toll_Charges_INR']), unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
                <div style='padding: 1.5rem; background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); border-radius: 10px; text-align: center;'>
                    <p style='color: rgba(255,255,255,0.8); margin: 0; font-size: 0.85rem;'>DELAY</p>
                    <p style='color: white; font-size: 2rem; font-weight: 700; margin: 0.5rem 0;'>{:.0f}</p>
                    <p style='color: rgba(255,255,255,0.8); margin: 0; font-size: 0.85rem;'>minutes</p>
                </div>
            """.format(shortest['Traffic_Delay_Minutes']), unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("---")
        
        # VEHICLE RECOMMENDATION SECTION
        st.markdown("#### 🚛 Smart Vehicle Recommendation")
        st.markdown("<p style='color: #7f8c8d; margin-bottom: 1.5rem;'>AI-powered vehicle selection based on route distance, fuel efficiency, and emissions</p>", unsafe_allow_html=True)
        
        # Calculate vehicle suitability scores
        distance = shortest['Distance_KM']
        fuel_needed = shortest['Fuel_Consumption_L']
        
        # Filter available vehicles
        available_vehicles = df_vehicles[df_vehicles['Status'] == 'Available'].copy()
        
        if len(available_vehicles) > 0:
            # Calculate efficiency scores
            available_vehicles['Fuel_Cost'] = (distance / available_vehicles['Fuel_Efficiency_KM_per_L']) * 100  # ₹100 per liter
            available_vehicles['CO2_Total'] = available_vehicles['CO2_Emissions_Kg_per_KM'] * distance
            available_vehicles['Age_Score'] = 10 - available_vehicles['Age_Years']  # Newer is better
            
            # Normalize and calculate composite score (lower is better)
            available_vehicles['Efficiency_Score'] = (
                (available_vehicles['Fuel_Cost'] / available_vehicles['Fuel_Cost'].max() * 0.4) +
                (available_vehicles['CO2_Total'] / available_vehicles['CO2_Total'].max() * 0.4) +
                (1 - available_vehicles['Age_Score'] / 10 * 0.2)
            )
            
            # Sort by efficiency score
            available_vehicles = available_vehicles.sort_values('Efficiency_Score')
            
            # Get top 3 recommendations
            top_vehicles = available_vehicles.head(3)
            
            # Display recommendations in cards
            cols = st.columns(3)
            for idx, (i, vehicle) in enumerate(top_vehicles.iterrows()):
                with cols[idx]:
                    if idx == 0:
                        border_color = "#27ae60"  # Green for best
                        badge = "🏆 BEST CHOICE"
                    elif idx == 1:
                        border_color = "#3498db"  # Blue for second
                        badge = "⭐ GOOD"
                    else:
                        border_color = "#95a5a6"  # Gray for third
                        badge = "✓ VIABLE"
                    
                    st.markdown(f"""
                        <div style='padding: 1.5rem; background-color: #ffffff; border-left: 5px solid {border_color}; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
                            <p style='color: {border_color}; font-weight: 700; font-size: 0.85rem; margin: 0 0 1rem 0;'>{badge}</p>
                            <p style='color: #2c3e50; font-size: 1.3rem; font-weight: 700; margin: 0.5rem 0;'>{vehicle['Vehicle_ID']}</p>
                            <p style='color: #7f8c8d; font-size: 0.9rem; margin: 0 0 1rem 0;'>{vehicle['Vehicle_Type'].replace('_', ' ')}</p>
                            <hr style='margin: 0.5rem 0; border: none; border-top: 1px solid #ecf0f1;'>
                            <p style='color: #34495e; font-size: 0.85rem; margin: 0.3rem 0;'><strong>Capacity:</strong> {vehicle['Capacity_KG']:.0f} kg</p>
                            <p style='color: #34495e; font-size: 0.85rem; margin: 0.3rem 0;'><strong>Fuel Cost:</strong> ₹{vehicle['Fuel_Cost']:.0f}</p>
                            <p style='color: #34495e; font-size: 0.85rem; margin: 0.3rem 0;'><strong>CO2:</strong> {vehicle['CO2_Total']:.1f} kg</p>
                            <p style='color: #34495e; font-size: 0.85rem; margin: 0.3rem 0;'><strong>Location:</strong> {vehicle['Current_Location']}</p>
                            <p style='color: #34495e; font-size: 0.85rem; margin: 0.3rem 0;'><strong>Efficiency:</strong> {vehicle['Fuel_Efficiency_KM_per_L']:.1f} km/L</p>
                        </div>
                    """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Cost & Emission Comparison
            st.markdown("##### 💰 Cost & Environmental Impact Comparison")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Cost comparison chart
                import plotly.express as px
                cost_comparison = top_vehicles[['Vehicle_ID', 'Fuel_Cost']].copy()
                cost_comparison['Savings'] = cost_comparison['Fuel_Cost'].max() - cost_comparison['Fuel_Cost']
                
                fig_cost = px.bar(
                    cost_comparison,
                    x='Vehicle_ID',
                    y='Fuel_Cost',
                    title='Fuel Cost Comparison',
                    labels={'Fuel_Cost': 'Fuel Cost (₹)', 'Vehicle_ID': 'Vehicle'},
                    color='Fuel_Cost',
                    color_continuous_scale=['#27ae60', '#f39c12', '#e74c3c'],
                    text='Fuel_Cost'
                )
                fig_cost.update_traces(texttemplate='₹%{text:.0f}', textposition='outside')
                fig_cost.update_layout(showlegend=False, height=350)
                st.plotly_chart(fig_cost, use_container_width=True)
            
            with col2:
                # CO2 comparison chart
                co2_comparison = top_vehicles[['Vehicle_ID', 'CO2_Total']].copy()
                
                fig_co2 = px.bar(
                    co2_comparison,
                    x='Vehicle_ID',
                    y='CO2_Total',
                    title='CO2 Emissions Comparison',
                    labels={'CO2_Total': 'CO2 Emissions (kg)', 'Vehicle_ID': 'Vehicle'},
                    color='CO2_Total',
                    color_continuous_scale=['#27ae60', '#f39c12', '#e74c3c'],
                    text='CO2_Total'
                )
                fig_co2.update_traces(texttemplate='%{text:.1f} kg', textposition='outside')
                fig_co2.update_layout(showlegend=False, height=350)
                st.plotly_chart(fig_co2, use_container_width=True)
            
            # Savings Summary
            best_vehicle = top_vehicles.iloc[0]
            worst_cost = available_vehicles['Fuel_Cost'].max()
            savings = worst_cost - best_vehicle['Fuel_Cost']
            co2_reduction = available_vehicles['CO2_Total'].max() - best_vehicle['CO2_Total']
            
            st.markdown(f"""
                <div style='padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px; text-align: center; margin: 1.5rem 0;'>
                    <p style='color: rgba(255,255,255,0.9); margin: 0; font-size: 1rem;'>🎯 POTENTIAL SAVINGS WITH {best_vehicle['Vehicle_ID']}</p>
                    <div style='display: flex; justify-content: space-around; margin-top: 1.5rem;'>
                        <div>
                            <p style='color: white; font-size: 2.5rem; font-weight: 700; margin: 0;'>₹{savings:.0f}</p>
                            <p style='color: rgba(255,255,255,0.8); margin: 0; font-size: 0.9rem;'>Cost Savings</p>
                        </div>
                        <div>
                            <p style='color: white; font-size: 2.5rem; font-weight: 700; margin: 0;'>{co2_reduction:.1f} kg</p>
                            <p style='color: rgba(255,255,255,0.8); margin: 0; font-size: 0.9rem;'>CO2 Reduction</p>
                        </div>
                        <div>
                            <p style='color: white; font-size: 2.5rem; font-weight: 700; margin: 0;'>{(savings/worst_cost*100):.1f}%</p>
                            <p style='color: rgba(255,255,255,0.8); margin: 0; font-size: 0.9rem;'>Efficiency Gain</p>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
        else:
            st.warning("⚠️ No vehicles currently available for this route. All fleet vehicles are in transit.")
        
        st.markdown("---")
        
        # Show all available routes if multiple exist
        if len(routes_found) > 1:
            st.markdown("#### Available Route Options")
            
            display_df = routes_found[['Origin', 'Destination', 'Distance_KM', 
                                       'Fuel_Consumption_L', 'Toll_Charges_INR', 
                                       'Traffic_Delay_Minutes', 'Weather_Impact']].copy()
            display_df['Total_Cost_INR'] = (display_df['Fuel_Consumption_L'] * 100) + display_df['Toll_Charges_INR']
            display_df = display_df.sort_values('Distance_KM')
            
            # Rename columns for better readability
            display_df = display_df.rename(columns={
                'Distance_KM': 'Distance (km)',
                'Fuel_Consumption_L': 'Fuel (L)',
                'Toll_Charges_INR': 'Toll (₹)',
                'Traffic_Delay_Minutes': 'Delay (min)',
                'Weather_Impact': 'Weather',
                'Total_Cost_INR': 'Total Cost (₹)'
            })
            
            # Highlight the shortest route
            st.dataframe(
                display_df.style.highlight_min(subset=['Distance (km)'], color='#d4edda').format({
                    'Distance (km)': '{:.2f}',
                    'Fuel (L)': '{:.2f}',
                    'Toll (₹)': '{:,.2f}',
                    'Total Cost (₹)': '{:,.2f}'
                }),
                use_container_width=True,
                hide_index=True
            )
            st.markdown("<br>", unsafe_allow_html=True)
        
        # Map visualization with enhanced title
        st.markdown("#### Interactive Route Map")
        st.markdown("<p style='color: #7f8c8d; margin-bottom: 1rem;'>Visual representation of available routes</p>", unsafe_allow_html=True)
        
        fig = go.Figure()
        
        # Plot all found routes
        for idx, route in routes_found.iterrows():
            origin_coords = CITY_COORDS.get(route['Origin'], {"lat": 20, "lon": 78})
            dest_coords = CITY_COORDS.get(route['Destination'], {"lat": 20, "lon": 78})
            
            is_shortest = (idx == shortest.name)
            
            # Draw route line
            fig.add_trace(go.Scattergeo(
                lon=[origin_coords['lon'], dest_coords['lon']],
                lat=[origin_coords['lat'], dest_coords['lat']],
                mode='lines+markers',
                line=dict(width=3 if is_shortest else 1, 
                         color='green' if is_shortest else 'blue'),
                marker=dict(size=10 if is_shortest else 6),
                name=f"{route['Origin']} → {route['Destination']} ({route['Distance_KM']:.0f} km)" + 
                     (" [SHORTEST]" if is_shortest else ""),
                text=f"{route['Distance_KM']:.2f} km",
                hovertemplate='<b>%{text}</b><br>Fuel: ' + f"{route['Fuel_Consumption_L']:.2f}L<br>" +
                             f"Toll: ₹{route['Toll_Charges_INR']:.2f}<extra></extra>"
            ))
        
        # Update map layout
        if origin in CITY_COORDS and destination in CITY_COORDS:
            # Center map between the two cities
            center_lat = (CITY_COORDS[origin]['lat'] + CITY_COORDS[destination]['lat']) / 2
            center_lon = (CITY_COORDS[origin]['lon'] + CITY_COORDS[destination]['lon']) / 2
            
            fig.update_layout(
                geo=dict(
                    scope='asia',
                    projection_type='natural earth',
                    showland=True,
                    landcolor='rgb(243, 243, 243)',
                    coastlinecolor='rgb(204, 204, 204)',
                    center=dict(lat=center_lat, lon=center_lon),
                    projection_scale=3
                ),
                height=500,
                margin={"r": 0, "t": 30, "l": 0, "b": 0},
                showlegend=True
            )
        else:
            fig.update_layout(
                geo_scope='asia',
                height=500,
                margin={"r": 0, "t": 30, "l": 0, "b": 0}
            )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Cost comparison
        if len(routes_found) > 1:
            st.markdown("### Cost Comparison")
            
            cost_df = routes_found.copy()
            cost_df['Fuel_Cost_INR'] = cost_df['Fuel_Consumption_L'] * 100  # ₹100 per liter
            cost_df['Total_Cost_INR'] = cost_df['Fuel_Cost_INR'] + cost_df['Toll_Charges_INR']
            cost_df['Route_Label'] = cost_df['Origin'] + ' → ' + cost_df['Destination']
            
            import plotly.express as px
            fig_cost = px.bar(cost_df, x='Route_Label', y=['Fuel_Cost_INR', 'Toll_Charges_INR'],
                             title="Cost Breakdown by Route",
                             labels={'value': 'Cost (INR)', 'Route_Label': 'Route'},
                             barmode='stack',
                             color_discrete_map={'Fuel_Cost_INR': '#FF6B6B', 'Toll_Charges_INR': '#4ECDC4'})
            st.plotly_chart(fig_cost, use_container_width=True)
    
    else:
        st.warning(f"No direct routes found between {origin} and {destination} in the dataset.")
        st.info("Try selecting different cities or check if the route exists in your data.")
    
    # Additional statistics
    st.markdown("---")
    st.markdown("### Overall Route Statistics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Total Routes in Database", len(route_df))
        st.metric("Average Distance", f"{route_df['Distance_KM'].mean():.2f} km")
        st.metric("Longest Route", f"{route_df['Distance_KM'].max():.2f} km")
    
    with col2:
        st.metric("Cities Covered", len(all_cities))
        st.metric("Average Fuel Consumption", f"{route_df['Fuel_Consumption_L'].mean():.2f} L")
        st.metric("Average Toll Charges", f"₹{route_df['Toll_Charges_INR'].mean():.2f}")
