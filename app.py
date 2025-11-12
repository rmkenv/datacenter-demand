"""
Datacenter Community Impact Calculator
A Streamlit application to help communities understand datacenter impacts

Based on research from: https://github.com/rmkenv/datacenter-demand
"""
import streamlit as st
import numpy as np
from predictor import (
    DatacenterImpactPredictor,
    DatacenterSpecs,
    BusinessContext,
    GridInfrastructure,
    EnvironmentalData
)
from visualizations import (
    create_grid_utilization_gauge,
    create_power_breakdown_chart,
    create_state_comparison_chart,
    create_impact_summary_metrics,
    create_uncertainty_range_chart,
    create_multiplier_visualization
)

# Page configuration
st.set_page_config(
    page_title="Datacenter Community Impact Calculator",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #7f8c8d;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #ecf0f1;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .impact-high {
        color: #e74c3c;
        font-weight: bold;
    }
    .impact-moderate {
        color: #f39c12;
        font-weight: bold;
    }
    .impact-low {
        color: #2ecc71;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize predictor
@st.cache_resource
def get_predictor():
    return DatacenterImpactPredictor()

predictor = get_predictor()

# Main header
st.markdown('<h1 class="main-header">🏢 Datacenter Community Impact Calculator</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Understand how datacenters affect your local electrical grid, environment, and economy</p>', unsafe_allow_html=True)

# Create tabs for different sections
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🏠 Home",
    "📍 Community Profile",
    "🖥️ Datacenter Specs",
    "📊 Impact Analysis",
    "📚 Learn More"
])

# ============================================================================
# TAB 1: HOME / INTRODUCTION
# ============================================================================
with tab1:
    st.header("Welcome")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### What is this tool?
        
        This calculator helps communities understand the potential impact of datacenters on their local infrastructure,
        particularly the electrical grid. Using machine learning models trained on US datacenter data, it predicts:
        
        - **Power demand** in megawatts (MW)
        - **Grid utilization** and strain levels
        - **Environmental impact** (CO₂ emissions)
        - **Economic effects** (jobs, energy costs)
        
        ### How it works
        
        1. **Enter your community profile** - Tell us about your location and local businesses
        2. **Specify datacenter characteristics** - Enter details about the proposed or existing datacenter
        3. **View impact analysis** - See comprehensive visualizations and predictions
        4. **Learn and plan** - Understand implications and mitigation strategies
        
        ### Based on Research
        
        This tool is based on peer-reviewed research and uses a neural network model with:
        - **96% accuracy** (R² score)
        - **12.6% mean error** (MAPE)
        - Trained on US state-level datacenter statistics
        """)
    
    with col2:
        st.info("### Quick Facts\n\n"
                "🔌 Virginia dedicates **>25%** of its electricity to datacenters\n\n"
                "⚡ A mid-size datacenter can consume **50-100 MW** (equivalent to 40,000 homes)\n\n"
                "🌍 Datacenters account for **~2%** of global electricity use\n\n"
                "💼 Average datacenter creates **10-50** direct jobs")
        
        st.success("### Get Started\n\n"
                   "Click on the **Community Profile** tab above to begin!")

# ============================================================================
# TAB 2: COMMUNITY PROFILE
# ============================================================================
with tab2:
    st.header("📍 Community Profile")
    st.markdown("Tell us about your community's location and characteristics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Location")
        
        state = st.selectbox(
            "Select your state",
            options=predictor.get_state_list(),
            index=0,
            help="Choose the state where the datacenter is located"
        )
        
        state_info = predictor.get_state_info(state)
        if state_info:
            st.info(f"**{state}** - {state_info['region']} Region\n\n"
                    f"Current datacenter electricity usage: **{state_info['percentage']:.1f}%**\n\n"
                    f"Typical PUE: **{state_info['pue']:.2f}**")
        
        st.subheader("Local Grid Infrastructure")
        
        grid_capacity = st.number_input(
            "Grid Capacity (MW)",
            min_value=50.0,
            max_value=2000.0,
            value=float(state_info.get('grid_capacity', 400)) if state_info else 400.0,
            step=50.0,
            help="Total electrical grid capacity in your area (megawatts)"
        )
        
        transmission_rating = st.number_input(
            "Transmission Line Rating (kV)",
            min_value=69.0,
            max_value=765.0,
            value=345.0,
            step=50.0,
            help="Voltage rating of transmission lines"
        )
    
    with col2:
        st.subheader("Nearby Businesses (within 5 km)")
        st.markdown("*Count of each business type near the datacenter location*")
        
        manufacturing = st.number_input("Manufacturing Facilities", min_value=0, max_value=50, value=5)
        healthcare = st.number_input("Healthcare Facilities", min_value=0, max_value=50, value=3)
        education = st.number_input("Educational Institutions", min_value=0, max_value=50, value=2)
        commercial = st.number_input("Commercial Offices", min_value=0, max_value=100, value=10)
        retail = st.number_input("Retail Establishments", min_value=0, max_value=100, value=8)
        tech_hubs = st.number_input("Technology Hubs", min_value=0, max_value=50, value=4)
        warehousing = st.number_input("Warehouses", min_value=0, max_value=50, value=6)
        financial = st.number_input("Financial Institutions", min_value=0, max_value=50, value=2)
        
        st.subheader("Environmental Conditions")
        
        temp_avg = st.slider(
            "Average Temperature (°F)",
            min_value=30,
            max_value=100,
            value=65,
            help="Annual average temperature"
        )
        
        humidity_avg = st.slider(
            "Average Humidity (%)",
            min_value=20,
            max_value=90,
            value=50
        )
    
    # Store in session state
    if 'community_data' not in st.session_state:
        st.session_state.community_data = {}
    
    st.session_state.community_data = {
        'state': state,
        'grid_capacity': grid_capacity,
        'transmission_rating': transmission_rating,
        'manufacturing': manufacturing,
        'healthcare': healthcare,
        'education': education,
        'commercial': commercial,
        'retail': retail,
        'tech_hubs': tech_hubs,
        'warehousing': warehousing,
        'financial': financial,
        'temp_avg': temp_avg,
        'humidity_avg': humidity_avg
    }
    
    st.success("✅ Community profile saved! Continue to **Datacenter Specs** tab.")

# ============================================================================
# TAB 3: DATACENTER SPECIFICATIONS
# ============================================================================
with tab3:
    st.header("🖥️ Datacenter Specifications")
    st.markdown("Enter details about the proposed or existing datacenter")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Hardware Configuration")
        
        server_count = st.number_input(
            "Number of Servers",
            min_value=100,
            max_value=100000,
            value=5000,
            step=500,
            help="Total number of servers in the facility"
        )
        
        rack_density = st.number_input(
            "Rack Density (kW per rack)",
            min_value=5.0,
            max_value=30.0,
            value=15.0,
            step=1.0,
            help="Power consumption per server rack"
        )
        
        gpu_percentage = st.slider(
            "GPU Percentage",
            min_value=0.0,
            max_value=1.0,
            value=0.4,
            step=0.05,
            help="Fraction of servers with GPUs (AI/ML workloads increase power)"
        )
        
        st.info(f"**Configuration Summary:**\n\n"
                f"Estimated racks: **~{int(server_count/21)}**\n\n"
                f"GPU servers: **~{int(server_count*gpu_percentage)}**")
    
    with col2:
        st.subheader("Facility Design")
        
        building_sqft = st.number_input(
            "Building Size (sq ft)",
            min_value=10000,
            max_value=1000000,
            value=200000,
            step=10000,
            help="Total facility square footage"
        )
        
        cooling_type = st.selectbox(
            "Cooling System",
            options=["Air", "Liquid"],
            index=1,
            help="Liquid cooling is more efficient but less common"
        )
        
        pue_rating = st.number_input(
            "PUE Rating",
            min_value=1.0,
            max_value=2.5,
            value=1.3,
            step=0.05,
            help="Power Usage Effectiveness - Lower is better (1.0 = ideal, 1.5 = typical)"
        )
        
        efficiency_note = "Excellent" if pue_rating < 1.2 else "Good" if pue_rating < 1.4 else "Average" if pue_rating < 1.6 else "Poor"
        efficiency_color = "🟢" if pue_rating < 1.4 else "🟡" if pue_rating < 1.6 else "🔴"
        
        st.info(f"**Efficiency Assessment:**\n\n"
                f"{efficiency_color} PUE {pue_rating:.2f} = **{efficiency_note}**\n\n"
                f"Cooling type: **{cooling_type}** {'(25% overhead)' if cooling_type == 'Liquid' else '(40% overhead)'}")
    
    # Store in session state
    if 'datacenter_data' not in st.session_state:
        st.session_state.datacenter_data = {}
    
    st.session_state.datacenter_data = {
        'server_count': server_count,
        'rack_density': rack_density,
        'gpu_percentage': gpu_percentage,
        'building_sqft': building_sqft,
        'cooling_type': cooling_type,
        'pue_rating': pue_rating
    }
    
    st.success("✅ Datacenter specifications saved! Go to **Impact Analysis** tab to see results.")

# ============================================================================
# TAB 4: IMPACT ANALYSIS
# ============================================================================
with tab4:
    st.header("📊 Impact Analysis")
    
    # Check if we have all required data
    if 'community_data' not in st.session_state or 'datacenter_data' not in st.session_state:
        st.warning("⚠️ Please complete the **Community Profile** and **Datacenter Specs** tabs first.")
    else:
        # Prepare data objects
        community = st.session_state.community_data
        datacenter = st.session_state.datacenter_data
        
        specs = DatacenterSpecs(
            server_count=datacenter['server_count'],
            rack_density=datacenter['rack_density'],
            gpu_percentage=datacenter['gpu_percentage'],
            pue_rating=datacenter['pue_rating'],
            building_sqft=datacenter['building_sqft'],
            cooling_type=datacenter['cooling_type'],
            state=community['state']
        )
        
        context = BusinessContext(
            manufacturing_count=community['manufacturing'],
            healthcare_count=community['healthcare'],
            education_count=community['education'],
            commercial_office_count=community['commercial'],
            retail_count=community['retail'],
            technology_hub_count=community['tech_hubs'],
            warehousing_count=community['warehousing'],
            financial_count=community['financial']
        )
        
        grid = GridInfrastructure(
            grid_capacity=community['grid_capacity'],
            transmission_rating=community['transmission_rating']
        )
        
        environment = EnvironmentalData(
            temp_avg=community['temp_avg'],
            humidity_avg=community['humidity_avg']
        )
        
        # Run prediction
        with st.spinner("Calculating impact..."):
            results = predictor.predict_impact(specs, context, grid, environment)
        
        # Display results
        st.success("✅ Analysis complete!")
        
        # Key metrics at top
        st.subheader("Key Impact Metrics")
        st.plotly_chart(create_impact_summary_metrics(results), width='stretch')
        
        # Grid utilization gauge
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("Grid Utilization")
            st.plotly_chart(
                create_grid_utilization_gauge(
                    results['grid_utilization_percent'],
                    results['grid_impact']
                ),
                width='stretch'
            )
            
            # Impact level indicator
            impact_level = results['grid_impact']
            if impact_level == 'HIGH_STRAIN':
                st.error(f"⚠️ **{impact_level.replace('_', ' ')}** - This datacenter would significantly strain the local grid")
            elif impact_level == 'MODERATE_IMPACT':
                st.warning(f"⚡ **{impact_level.replace('_', ' ')}** - Noticeable impact on grid capacity")
            else:
                st.success(f"✅ **{impact_level.replace('_', ' ')}** - Manageable impact on local grid")
        
        with col2:
            st.subheader("Power Demand Breakdown")
            st.plotly_chart(create_power_breakdown_chart(results), width='stretch')
        
        # Detailed metrics
        st.subheader("Detailed Predictions")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Base Consumption",
                f"{results['base_consumption_mw']:.1f} MW",
                help="Pure hardware power draw"
            )
        
        with col2:
            st.metric(
                "Business Multiplier",
                f"{results['business_multiplier']:.2f}x",
                help="Impact from nearby businesses"
            )
        
        with col3:
            st.metric(
                "Seasonal Factor",
                f"{results['seasonal_factor']:.2f}x",
                help="Environmental impact on cooling"
            )
        
        with col4:
            st.metric(
                "Confidence",
                f"{results['confidence_score']*100:.0f}%",
                help="Model prediction confidence"
            )
        
        # Uncertainty range
        st.subheader("Prediction Uncertainty")
        st.plotly_chart(create_uncertainty_range_chart(results), width='stretch')
        st.caption(f"Predicted range: {results['uncertainty_range_mw'][0]:.1f} - {results['uncertainty_range_mw'][1]:.1f} MW "
                   f"(based on model accuracy of ±12.6%)")
        
        # State comparison
        st.subheader("State Comparison")
        st.plotly_chart(
            create_state_comparison_chart(
                community['state'],
                results['state_datacenter_percentage'],
                DatacenterImpactPredictor
            ),
            width='stretch'
        )
        
        # Environmental and Economic Impact
        st.subheader("Environmental & Economic Impact")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🌍 Environmental")
            st.metric("Annual Energy Consumption", f"{results['annual_energy_mwh']:,.0f} MWh")
            st.metric("CO₂ Emissions (estimated)", f"{results['co2_emissions_tons']:,.0f} tons/year")
            st.caption("*Based on average US grid carbon intensity of ~0.4 kg CO₂/kWh*")
            
            # Equivalencies
            homes_equivalent = int(results['annual_energy_mwh'] / 10.5)  # avg home uses ~10.5 MWh/year
            st.info(f"**Energy Equivalent:**\n\n"
                    f"This datacenter uses as much energy as approximately **{homes_equivalent:,}** US homes per year")
        
        with col2:
            st.markdown("### 💼 Economic")
            st.metric("Estimated Direct Jobs", results['estimated_jobs'])
            st.metric("Annual Energy Cost", f"${results['annual_energy_cost_usd']:,.0f}")
            st.caption("*Based on $50/MWh average commercial rate*")
            
            # Additional economic notes
            st.info(f"**Economic Notes:**\n\n"
                    f"• Datacenters typically create 2-3x indirect jobs\n\n"
                    f"• Average datacenter salary: $80,000-120,000\n\n"
                    f"• Property tax revenue varies by location")
        
        # Download results
        st.subheader("📥 Export Results")
        
        # Create summary text
        summary_text = f"""
DATACENTER COMMUNITY IMPACT ANALYSIS
Generated: {st.session_state.get('timestamp', 'N/A')}

LOCATION
State: {community['state']}
Grid Capacity: {community['grid_capacity']:.0f} MW

DATACENTER SPECIFICATIONS
Servers: {datacenter['server_count']:,}
Rack Density: {datacenter['rack_density']:.1f} kW/rack
GPU Percentage: {datacenter['gpu_percentage']:.1%}
Cooling: {datacenter['cooling_type']}
PUE: {datacenter['pue_rating']:.2f}
Building Size: {datacenter['building_sqft']:,} sq ft

IMPACT RESULTS
Predicted Power Demand: {results['predicted_demand_mw']:.2f} MW
Uncertainty Range: {results['uncertainty_range_mw'][0]:.2f} - {results['uncertainty_range_mw'][1]:.2f} MW
Grid Utilization: {results['grid_utilization_percent']:.1f}%
Grid Impact Level: {results['grid_impact']}

Annual Energy: {results['annual_energy_mwh']:,.0f} MWh
CO2 Emissions: {results['co2_emissions_tons']:,.0f} tons/year
Estimated Jobs: {results['estimated_jobs']}
Annual Energy Cost: ${results['annual_energy_cost_usd']:,.0f}

Model Confidence: {results['confidence_score']*100:.0f}%
        """
        
        st.download_button(
            label="Download Analysis Report (TXT)",
            data=summary_text,
            file_name="datacenter_impact_analysis.txt",
            mime="text/plain"
        )

# ============================================================================
# TAB 5: LEARN MORE
# ============================================================================
with tab5:
    st.header("📚 Learn More About Datacenters")
    
    st.markdown("""
    ## What are Datacenters?
    
    Datacenters are specialized facilities that house computer systems and associated components, such as 
    telecommunications and storage systems. They are critical infrastructure for:
    
    - Cloud computing services (AWS, Azure, Google Cloud)
    - Social media platforms (Facebook, Instagram, TikTok)
    - Streaming services (Netflix, YouTube, Spotify)
    - Artificial Intelligence and machine learning
    - Enterprise business operations
    - Scientific research and data analysis
    
    ---
    
    ## Environmental Impact
    
    ### Energy Consumption
    - Datacenters consume approximately **2% of global electricity**
    - A large datacenter can use **100+ MW** of power continuously
    - Cooling systems account for **30-40%** of total energy use
    
    ### Carbon Footprint
    - Emissions depend on local electricity grid composition
    - States with renewable energy (hydro, wind, solar) have lower impact
    - Industry goal: 100% renewable energy by 2030
    
    ### Mitigation Strategies
    - **Liquid cooling** reduces energy use by 25-40%
    - **Waste heat recovery** for district heating
    - **Renewable energy** power purchase agreements
    - **AI optimization** of cooling systems
    - **Higher PUE targets** (closer to 1.0)
    
    ---
    
    ## Economic Impact
    
    ### Positive Effects
    - **Job Creation**: 10-50 direct jobs per facility, plus 2-3x indirect jobs
    - **Tax Revenue**: Property taxes and business taxes
    - **Infrastructure**: Improved electrical grid and fiber optic networks
    - **Tech Ecosystem**: Attracts other technology companies
    
    ### Challenges
    - **Energy Costs**: Can increase electricity prices for residents
    - **Water Usage**: Cooling systems may strain water resources
    - **Grid Capacity**: May require expensive infrastructure upgrades
    - **Limited Local Employment**: Many jobs require specialized skills
    
    ---
    
    ## Grid Impact Explained
    
    ### LOW_IMPACT (<60% utilization)
    - Minimal strain on existing infrastructure
    - Grid can handle additional load comfortably
    - Unlikely to affect residential electricity
    
    ### MODERATE_IMPACT (60-80% utilization)
    - Noticeable load on grid capacity
    - May require some infrastructure improvements
    - Possible impact during peak demand periods
    
    ### HIGH_STRAIN (>80% utilization)
    - Significant grid capacity concerns
    - Requires major infrastructure upgrades
    - Risk of brownouts or increased electricity costs
    - May need dedicated substations or transmission lines
    
    ---
    
    ## Key Metrics Explained
    
    ### PUE (Power Usage Effectiveness)
    - Ratio of total facility power to IT equipment power
    - **1.0** = Perfect efficiency (theoretical minimum)
    - **1.2** = Excellent (top 10% of datacenters)
    - **1.5** = Industry average
    - **2.0+** = Inefficient (older facilities)
    
    ### Rack Density
    - Power consumption per server rack (measured in kW)
    - Traditional: 5-8 kW per rack
    - Modern: 12-20 kW per rack
    - High-performance AI: 30+ kW per rack
    
    ### GPU Percentage
    - Fraction of servers equipped with GPUs
    - AI/ML workloads require GPUs, which consume 2-3x more power
    - Traditional workloads: 0-20% GPUs
    - AI-focused datacenters: 50-100% GPUs
    
    ---
    
    ## About This Tool
    
    ### Methodology
    This calculator uses a machine learning model trained on US datacenter data:
    - **Neural Network** architecture
    - **R² = 0.96** (96% of variance explained)
    - **MAPE = 12.6%** (mean absolute percentage error)
    - Trained on 2,000+ synthetic datacenter scenarios
    - Calibrated to US state-level statistics
    
    ### Data Sources
    - U.S. Department of Energy datacenter statistics
    - Lawrence Berkeley National Laboratory research
    - Energy Systems Integration Group data
    - Academic research papers (see references below)
    
    ### Limitations
    - Predictions are estimates with ±12.6% uncertainty
    - Based on US electrical grid characteristics
    - Assumes modern datacenter design practices
    - Does not account for future grid improvements
    - Economic estimates are approximate
    
    ---
    
    ## References & Further Reading
    
    1. **Original Research Code**: [github.com/rmkenv/datacenter-demand](https://github.com/rmkenv/datacenter-demand)
    2. **U.S. Data Center Energy Usage Report** - Lawrence Berkeley National Laboratory
    3. **IEA Data Centre Energy Use** - International Energy Agency (2024)
    4. **Datacenter Efficiency Best Practices** - US Department of Energy
    5. **Google's Carbon-Free Energy Report** - Google Sustainability
    6. **Microsoft's Datacenter Sustainability** - Microsoft Environmental Report
    
    ---
    
    ## Community Action Steps
    
    If a datacenter is proposed in your community:
    
    1. **Request Transparency**
       - Power consumption estimates
       - Water usage projections
       - Cooling system design
       - Renewable energy commitments
    
    2. **Assess Grid Capacity**
       - Contact local utility company
       - Review grid infrastructure plans
       - Understand cost implications
    
    3. **Evaluate Environmental Impact**
       - Carbon footprint analysis
       - Water resource impact
       - Noise and heat pollution
    
    4. **Consider Economic Trade-offs**
       - Job creation vs. energy costs
       - Tax revenue vs. infrastructure costs
       - Long-term sustainability
    
    5. **Engage in Planning Process**
       - Attend public hearings
       - Request community benefit agreements
       - Advocate for renewable energy requirements
    """)
    
    st.info("💡 **Want to dive deeper?** Visit the [original research repository](https://github.com/rmkenv/datacenter-demand) for technical details and methodology.")

# ============================================================================
# SIDEBAR
# ============================================================================
with st.sidebar:
    st.image("https://via.placeholder.com/300x100/3498db/ffffff?text=Datacenter+Impact", width='stretch')
    
    st.markdown("### 🎯 Quick Navigation")
    st.markdown("""
    1. **Home** - Introduction and overview
    2. **Community Profile** - Enter location data
    3. **Datacenter Specs** - Enter facility details
    4. **Impact Analysis** - View predictions
    5. **Learn More** - Educational resources
    """)
    
    st.markdown("---")
    
    st.markdown("### 📊 Model Information")
    st.markdown("""
    - **Accuracy**: 96% (R²)
    - **Error Rate**: ±12.6%
    - **Training**: 2,000+ scenarios
    - **Coverage**: 14 US states
    """)
    
    st.markdown("---")
    
    st.markdown("### 🔗 Resources")
    st.markdown("""
    - [GitHub Repository](https://github.com/rmkenv/datacenter-demand)
    - [DOE Best Practices](https://www.energy.gov/eere/buildings/data-centers)
    - [IEA Energy Report](https://www.iea.org)
    """)
    
    st.markdown("---")
    
    st.caption("Built with Streamlit • Data from DOE, LBNL, and academic research")
    st.caption("⚠️ For educational purposes only. Consult with energy professionals for specific projects.")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #7f8c8d;'>
        <p>Datacenter Community Impact Calculator | Based on ML research from 
        <a href='https://github.com/rmkenv/datacenter-demand'>datacenter-demand</a></p>
        <p>Made with ❤️ for communities | © 2024</p>
    </div>
""", unsafe_allow_html=True)
