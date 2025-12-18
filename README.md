# 🚢 Shiplytics - Logistics Intelligence Platform

> **Transforming Logistics Operations through Data-Driven Decision Making**

## 📋 Table of Contents
- [Project Overview](#project-overview)
- [Business Context](#business-context)
- [Problem Statement](#problem-statement)
- [Solution Architecture](#solution-architecture)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Features & Modules](#features--modules)
- [Data Flow & Workflow](#data-flow--workflow)
- [Installation & Setup](#installation--setup)
- [Usage Guide](#usage-guide)
- [Key Insights](#key-insights)
- [Future Enhancements](#future-enhancements)
- [Developer](#developer)

---

## 🎯 Project Overview

**Shiplytics** is an intelligent logistics analytics platform developed for **NexGen Logistics Pvt. Ltd.**, a mid-sized logistics company operating across India with international connections. The platform addresses critical operational challenges through data analytics, providing actionable insights for:

- 📊 **Vendor Profit Optimization** - Carrier performance analysis and cost reduction
- 📦 **Inventory Management** - Inter-warehouse stock balancing
- 🗺️ **Route Optimization** - Shortest and most cost-effective route discovery

### Project Objectives
✅ Transform reactive operations into predictive, data-driven workflows  
✅ Reduce operational costs by 15-20%  
✅ Improve customer experience through better delivery performance  
✅ Build sustainable, scalable logistics intelligence  

---

## 🏢 Business Context

### Company Profile: NexGen Logistics Pvt. Ltd.

**Operations:**
- 📍 5 Major Warehouses: Mumbai, Delhi, Bangalore, Chennai, Kolkata
- 🚚 50-Vehicle Fleet: Vans, trucks, refrigerated units, express bikes
- 🤝 5 Carrier Partnerships for extended reach
- 📦 200+ Monthly Orders across multiple product categories
- 🌏 International Connections: Singapore, Dubai, Hong Kong, Bangkok

**Product Categories:**
Electronics | Fashion | Food & Beverage | Healthcare | Industrial Goods | Books | Home Goods

**Customer Segments:**
Enterprise | SMB | Individual

**Delivery Priorities:**
Express | Standard | Economy

---

## ⚠️ Problem Statement

NexGen Logistics faces critical challenges:

### 1. Delivery Performance Issues
- Inconsistent on-time delivery rates
- Customer dissatisfaction
- Lack of predictive capabilities

### 2. Operational Inefficiencies
- Suboptimal route planning
- Poor fleet utilization
- Manual decision-making processes

### 3. Cost Pressures
- Rising fuel and operational costs
- Vendor contract inefficiencies
- Cost leakage across operations

### 4. Inventory Management
- Stock imbalances across warehouses
- Overstocking and stockouts
- High storage costs

---

## 🏗️ Solution Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     SHIPLYTICS PLATFORM                         │
│                  Logistics Intelligence System                   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
        ┌─────────────────────────────────────────┐
        │         DATA INGESTION LAYER            │
        │  ┌────────────────────────────────────┐ │
        │  │ 7 CSV Datasets                     │ │
        │  │ • orders.csv                       │ │
        │  │ • delivery_performance.csv         │ │
        │  │ • routes_distance.csv             │ │
        │  │ • vehicle_fleet.csv               │ │
        │  │ • warehouse_inventory.csv         │ │
        │  │ • customer_feedback.csv           │ │
        │  │ • cost_breakdown.csv              │ │
        │  └────────────────────────────────────┘ │
        └─────────────────────────────────────────┘
                              │
                              ▼
        ┌─────────────────────────────────────────┐
        │      DATA PROCESSING LAYER              │
        │  ┌────────────────────────────────────┐ │
        │  │ utils/data_loader.py               │ │
        │  │ • Data loading & validation        │ │
        │  │ • Data merging & transformation    │ │
        │  │ • Metric calculation               │ │
        │  │ • Caching (@st.cache_data)         │ │
        │  └────────────────────────────────────┘ │
        └─────────────────────────────────────────┘
                              │
                              ▼
        ┌─────────────────────────────────────────┐
        │      ANALYTICS & LOGIC LAYER            │
        │                                         │
        │  ┌──────────────────────────────────┐  │
        │  │ modules/profit_optimizer.py      │  │
        │  │ • Carrier performance analysis   │  │
        │  │ • Profit vs speed optimization   │  │
        │  │ • Cost simulation engine         │  │
        │  └──────────────────────────────────┘  │
        │                                         │
        │  ┌──────────────────────────────────┐  │
        │  │ modules/inventory_bot.py         │  │
        │  │ • Stock health monitoring        │  │
        │  │ • Inter-warehouse balancing      │  │
        │  │ • Transfer recommendations       │  │
        │  └──────────────────────────────────┘  │
        │                                         │
        │  ┌──────────────────────────────────┐  │
        │  │ modules/route_optimizer.py       │  │
        │  │ • Route comparison & analysis    │  │
        │  │ • Distance optimization          │  │
        │  │ • Cost breakdown calculation     │  │
        │  └──────────────────────────────────┘  │
        └─────────────────────────────────────────┘
                              │
                              ▼
        ┌─────────────────────────────────────────┐
        │     VISUALIZATION & UI LAYER            │
        │  ┌────────────────────────────────────┐ │
        │  │ Streamlit Web Application          │ │
        │  │ • Interactive dashboards           │ │
        │  │ • Real-time filtering              │ │
        │  │ • Plotly visualizations            │ │
        │  │ • Responsive design                │ │
        │  └────────────────────────────────────┘ │
        └─────────────────────────────────────────┘
                              │
                              ▼
        ┌─────────────────────────────────────────┐
        │         USER INTERFACE                  │
        │  ┌────────────────────────────────────┐ │
        │  │ Decision Makers & Analysts         │ │
        │  │ • Executive Dashboard              │ │
        │  │ • Operational Insights             │ │
        │  │ • Actionable Recommendations       │ │
        │  └────────────────────────────────────┘ │
        └─────────────────────────────────────────┘
```

---

## 💻 Technology Stack

### Core Technologies
| Technology | Purpose | Version |
|------------|---------|---------|
| **Python** | Primary programming language | 3.8+ |
| **Streamlit** | Web application framework | Latest |
| **Pandas** | Data manipulation & analysis | Latest |
| **Plotly** | Interactive visualizations | Latest |
| **NumPy** | Numerical computing | Latest |

### Visualization Libraries
- **Plotly Express** - Quick interactive charts
- **Plotly Graph Objects** - Advanced visualizations (maps, custom charts)
- **Streamlit Components** - UI elements and metrics

### Data Processing
- **Pandas DataFrames** - Structured data handling
- **Streamlit Caching** - Performance optimization
- **Python datetime** - Time-based analysis

---

## 📁 Project Structure

```
Shiplytics/
│
├── app.py                          # Main application entry point
│   ├── Configuration & styling
│   ├── Data loading orchestration
│   ├── Navigation & routing
│   └── Global UI components
│
├── datasets/                       # Data storage
│   ├── orders.csv                 # Order information (200 records)
│   ├── delivery_performance.csv   # Delivery metrics (150 records)
│   ├── routes_distance.csv        # Route data (150 records)
│   ├── vehicle_fleet.csv          # Fleet information (50 records)
│   ├── warehouse_inventory.csv    # Inventory data (35 records)
│   ├── customer_feedback.csv      # Customer reviews (83 records)
│   └── cost_breakdown.csv         # Cost components (150 records)
│
├── utils/                         # Utility functions
│   └── data_loader.py            # Centralized data processing
│       ├── load_and_process_data()
│       ├── Data merging logic
│       ├── Metric calculations
│       └── Error handling
│
├── modules/                       # Feature modules
│   ├── __init__.py               # Module initialization
│   │
│   ├── profit_optimizer.py       # Vendor Profit Analysis
│   │   ├── render_page()
│   │   ├── KPI calculations
│   │   ├── Carrier performance matrix
│   │   └── Switching simulation
│   │
│   ├── inventory_bot.py          # Inventory Management
│   │   ├── render_page()
│   │   ├── Stock health analysis
│   │   ├── Transfer logic
│   │   └── Map visualization
│   │
│   └── route_optimizer.py        # Route Optimization
│       ├── render_page()
│       ├── parse_route_data()
│       ├── Route comparison
│       └── Cost analysis
│
└── README.md                      # Project documentation
```

---

## 🎨 Features & Modules

### 1. 💰 Vendor Profit Analysis

**Purpose:** Optimize carrier selection and maximize profit margins

**Key Features:**
- ✅ **Performance KPIs**
  - Total Profit by route
  - Average Margin percentage
  - Loss-making orders count
  - Orders per route
  
- ✅ **Carrier Performance Matrix**
  - Scatter plot: Profit vs Delivery Speed
  - Bubble size represents order volume
  - Break-even point indicator
  
- ✅ **Optimization Engine**
  - Best vs Worst carrier comparison
  - Interactive switching simulation
  - Projected monthly savings calculator
  - Visual cost impact analysis

**Business Impact:**
- Identify underperforming carriers
- Optimize vendor contracts
- Reduce delivery costs by 15-20%
- Improve profit margins

---

### 2. 📦 Inventory Management System

**Purpose:** Intelligent inter-warehouse stock balancing

**Key Features:**
- ✅ **Stock Health Overview**
  - Critical Low inventory alerts
  - Overstocked locations
  - Healthy stock indicators
  
- ✅ **Visual Analytics**
  - Bar chart comparison (Current vs Reorder levels)
  - Interactive geographic map
  - Status-based color coding
  
- ✅ **Smart Recommendations**
  - Automatic deficit-surplus matching
  - Transfer route visualization
  - Quantity recommendations
  - Detailed transfer table

**Business Impact:**
- Reduce stockouts and overstocking
- Optimize storage costs
- Improve order fulfillment rates
- Balance inventory across network

---

### 3. 🗺️ Smart Route Optimizer

**Purpose:** Find shortest, most efficient routes

**Key Features:**
- ✅ **Route Discovery**
  - Domestic and International filtering
  - Origin-Destination selection
  - Multiple route comparison
  
- ✅ **Optimal Route Metrics**
  - Distance (kilometers)
  - Fuel consumption (liters)
  - Toll charges (₹)
  - Traffic delays (minutes)
  
- ✅ **Interactive Visualization**
  - Geographic route mapping
  - Shortest route highlighting
  - Cost breakdown charts
  - Route comparison tables

**Business Impact:**
- Reduce fuel consumption
- Minimize delivery time
- Lower operational costs
- Improve delivery reliability

---

## 🔄 Data Flow & Workflow

### System Workflow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    USER INTERACTION                             │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │  Select Module   │
                    │  from Sidebar    │
                    └──────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│ Vendor Profit │    │  Inventory    │    │     Route     │
│   Analysis    │    │  Management   │    │  Optimizer    │
└───────────────┘    └───────────────┘    └───────────────┘
        │                     │                     │
        ▼                     ▼                     ▼
┌─────────────────────────────────────────────────────────┐
│              DATA PROCESSING LAYER                      │
│                                                         │
│  load_and_process_data()                               │
│  ├─ Load 7 CSV files                                   │
│  ├─ Merge related datasets                             │
│  ├─ Calculate derived metrics                          │
│  ├─ Handle missing data                                │
│  └─ Cache results for performance                      │
└─────────────────────────────────────────────────────────┘
        │                     │                     │
        ▼                     ▼                     ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│  Filter by    │    │  Filter by    │    │  Filter by    │
│    Route      │    │   Category    │    │  Route Type   │
└───────────────┘    └───────────────┘    └───────────────┘
        │                     │                     │
        ▼                     ▼                     ▼
┌─────────────────────────────────────────────────────────┐
│           ANALYTICS & CALCULATIONS                      │
│                                                         │
│  Profit Module          Inventory Module   Route Module│
│  ├─ Group by carrier   ├─ Stock status    ├─ Parse     │
│  ├─ Aggregate stats    ├─ Match surplus   │   routes   │
│  ├─ Calculate savings  ├─ Find deficit    ├─ Compare   │
│  └─ Simulate switches  └─ Recommend moves │   costs    │
└─────────────────────────────────────────────────────────┘
        │                     │                     │
        ▼                     ▼                     ▼
┌─────────────────────────────────────────────────────────┐
│              VISUALIZATION LAYER                        │
│                                                         │
│  ├─ Plotly Charts (Scatter, Bar, Line)                 │
│  ├─ Geographic Maps (Scattergeo)                       │
│  ├─ Metrics & KPIs (st.metric)                         │
│  ├─ Tables & DataFrames                                │
│  └─ Interactive Filters                                │
└─────────────────────────────────────────────────────────┘
        │                     │                     │
        ▼                     ▼                     ▼
┌─────────────────────────────────────────────────────────┐
│                  BUSINESS DECISIONS                     │
│                                                         │
│  ├─ Switch to better carriers                          │
│  ├─ Rebalance inventory                                │
│  ├─ Optimize delivery routes                           │
│  └─ Reduce operational costs                           │
└─────────────────────────────────────────────────────────┘
```

### Data Processing Pipeline

```
CSV Files → Pandas DataFrames → Data Validation → Merging
                                                      │
                                                      ▼
                                          Metric Calculation
                                                      │
                                                      ▼
                                          Streamlit Cache
                                                      │
                                                      ▼
                                          Module Rendering
                                                      │
                                                      ▼
                                          User Interface
```

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git (optional)

### Step 1: Clone or Download Repository
```bash
# Clone repository okay
git clone <repository-url>
cd Shiplytics

# OR download and extract ZIP file
```

### Step 2: Install Dependencies
```bash
# Install required packages
pip install streamlit pandas plotly numpy
```

### Step 3: Verify Data Files
Ensure all datasets are in the `datasets/` folder:
```
datasets/
├── orders.csv
├── delivery_performance.csv
├── routes_distance.csv
├── vehicle_fleet.csv
├── warehouse_inventory.csv
├── customer_feedback.csv
└── cost_breakdown.csv
```

### Step 4: Run the Application
```bash
# Start Streamlit server
streamlit run app.py
```

### Step 5: Access the Dashboard
Open your browser and navigate to:
```
http://localhost:8501
```

---

## 📖 Usage Guide

### Navigation

1. **Sidebar Navigation**
   - Select module from navigation menu
   - Apply filters specific to each module
   - View developer information at bottom

2. **Vendor Profit Analysis**
   - Select route from dropdown
   - View KPIs and metrics
   - Switch between Analysis and Optimizer tabs
   - Use slider to simulate carrier switches

3. **Inventory Management**
   - Select product category
   - Review stock status cards
   - Examine bar charts and maps
   - Check transfer recommendations

4. **Route Optimizer**
   - Choose route type (Domestic/International/All)
   - Select origin and destination cities
   - Click "Find Routes" button
   - Review optimal metrics and visualizations

### Key Interactions

- **Filters:** Change selections to update dashboards dynamically
- **Charts:** Hover for detailed information
- **Maps:** Interactive zoom and pan
- **Tables:** Sort and review detailed data
- **Buttons:** Trigger calculations and updates

---

## 💡 Key Insights

### Business Value Delivered

1. **Cost Reduction**
   - Identified 15-20% savings potential through carrier optimization
   - Highlighted fuel and toll cost inefficiencies
   - Reduced inventory holding costs

2. **Operational Efficiency**
   - Automated route selection process
   - Real-time inventory balancing recommendations
   - Data-driven carrier performance metrics

3. **Customer Experience**
   - Improved delivery time predictions
   - Better inventory availability
   - Reduced stockouts through proactive balancing

4. **Decision Support**
   - Clear visualization of trade-offs
   - Quantified business impact
   - Actionable recommendations

---

## 🔮 Future Enhancements

### Planned Features

1. **Predictive Analytics**
   - ML model for delivery delay prediction
   - Demand forecasting
   - Seasonal trend analysis

2. **Advanced Optimization**
   - Multi-objective route optimization
   - Dynamic pricing recommendations
   - Fleet utilization optimization

3. **Real-time Integration**
   - Live GPS tracking integration
   - Real-time inventory updates
   - API endpoints for mobile apps

4. **Sustainability Metrics**
   - Carbon footprint tracking
   - Green route recommendations
   - Environmental impact dashboard

5. **Customer Analytics**
   - Sentiment analysis on feedback
   - Customer satisfaction prediction
   - Churn risk identification

6. **Enhanced Visualizations**
   - 3D route visualization
   - Animated flow diagrams
   - Advanced geospatial analytics

---

## 📊 Technical Highlights

### Code Quality Features
✅ Modular architecture for maintainability  
✅ Centralized data loading with caching  
✅ Professional UI/UX design  
✅ Error handling and data validation  
✅ Responsive layouts  
✅ Performance optimization  

### Visualization Techniques
✅ Interactive scatter plots  
✅ Geographic mapping (Scattergeo)  
✅ Gradient-styled metric cards  
✅ Multi-axis charts  
✅ Dynamic filtering  
✅ Color-coded status indicators    

---

## 👨‍💻 Developer

**Developed By: Soumik Roy**

### Technologies Demonstrated
- Python Programming
- Data Analysis & Visualization
- Streamlit Web Development
- Business Intelligence
- UI/UX Design

<div align="center">

### 🌟 Built with Innovation, Powered by Data 🌟

**Transforming Logistics, One Insight at a Time**

</div>
