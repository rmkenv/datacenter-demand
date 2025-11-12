"""
Datacenter Power Demand Prediction Engine
Adapted from datacenter-demand repository for Streamlit
"""
import numpy as np
from dataclasses import dataclass
from typing import Dict

@dataclass
class DatacenterSpecs:
    """Datacenter technical specifications"""
    server_count: int
    rack_density: float       # kW per rack
    gpu_percentage: float     # fraction [0-1]
    pue_rating: float
    building_sqft: int
    cooling_type: str         # 'Air' or 'Liquid'
    state: str

@dataclass
class BusinessContext:
    """Nearby business context within radius"""
    manufacturing_count: int = 0
    healthcare_count: int = 0
    education_count: int = 0
    commercial_office_count: int = 0
    retail_count: int = 0
    technology_hub_count: int = 0
    warehousing_count: int = 0
    financial_count: int = 0
    radius_km: float = 5.0

@dataclass
class GridInfrastructure:
    """Local electrical grid information"""
    grid_capacity: float  # MW
    transmission_rating: float = 345.0  # kV
    substation_distance: float = 2.0
    reliability_score: float = 0.95
    renewable_percentage: float = 0.25

@dataclass
class EnvironmentalData:
    """Environmental conditions"""
    temp_avg: float
    humidity_avg: float = 50.0
    seasonal_variation: float = 15.0
    altitude: float = 0.0


class DatacenterImpactPredictor:
    """Predicts datacenter power demand and community impact"""
    
    # US State-level datacenter statistics (from research)
    STATE_DATA = {
        'Virginia': {'percentage': 25.6, 'pue': 1.35, 'region': 'Southeast', 'grid_capacity': 850},
        'Texas': {'percentage': 4.6, 'pue': 1.42, 'region': 'South', 'grid_capacity': 450},
        'California': {'percentage': 3.7, 'pue': 1.28, 'region': 'West', 'grid_capacity': 500},
        'Illinois': {'percentage': 5.5, 'pue': 1.38, 'region': 'Midwest', 'grid_capacity': 400},
        'Oregon': {'percentage': 11.4, 'pue': 1.25, 'region': 'West', 'grid_capacity': 350},
        'Arizona': {'percentage': 7.4, 'pue': 1.45, 'region': 'Southwest', 'grid_capacity': 380},
        'Iowa': {'percentage': 11.4, 'pue': 1.32, 'region': 'Midwest', 'grid_capacity': 320},
        'Georgia': {'percentage': 4.3, 'pue': 1.36, 'region': 'Southeast', 'grid_capacity': 420},
        'Washington': {'percentage': 5.7, 'pue': 1.22, 'region': 'West', 'grid_capacity': 380},
        'Pennsylvania': {'percentage': 3.2, 'pue': 1.41, 'region': 'Northeast', 'grid_capacity': 430},
        'New Jersey': {'percentage': 5.4, 'pue': 1.43, 'region': 'Northeast', 'grid_capacity': 410},
        'Nebraska': {'percentage': 11.7, 'pue': 1.34, 'region': 'Midwest', 'grid_capacity': 290},
        'North Dakota': {'percentage': 4.4, 'pue': 1.39, 'region': 'Midwest', 'grid_capacity': 260},
        'Nevada': {'percentage': 8.7, 'pue': 1.41, 'region': 'West', 'grid_capacity': 340},
    }
    
    def __init__(self):
        self.model_uncertainty = 0.126  # 12.6% MAPE from Neural Network model
    
    def calculate_base_consumption(self, specs: DatacenterSpecs) -> float:
        """
        Calculate base power consumption in MW
        Based on server hardware and facility design
        """
        # Estimate servers per rack (assuming 2U servers)
        servers_per_rack = 42 / 2  # 21 servers per rack
        total_racks = specs.server_count / servers_per_rack
        
        # Base server power from rack density
        base_server_power = total_racks * specs.rack_density
        
        # GPU multiplier (GPUs significantly increase power)
        gpu_multiplier = 1 + (specs.gpu_percentage * 2.5)
        server_power_kw = base_server_power * gpu_multiplier
        
        # Cooling power depends on cooling type
        cooling_efficiency = 0.25 if specs.cooling_type.lower() == 'liquid' else 0.4
        cooling_power_kw = server_power_kw * cooling_efficiency
        
        # Infrastructure overhead (UPS, networking, lighting, etc.)
        infrastructure_power_kw = (server_power_kw + cooling_power_kw) * 0.15
        
        # Apply PUE (Power Usage Effectiveness)
        total_power_kw = (server_power_kw + cooling_power_kw + infrastructure_power_kw) * specs.pue_rating
        
        # Convert to MW
        return total_power_kw / 1000.0
    
    def calculate_business_context_multiplier(self, ctx: BusinessContext) -> float:
        """
        Calculate demand multiplier based on nearby businesses
        Nearby tech hubs, manufacturing, etc. increase demand
        """
        base = 1.0
        
        # Impact factors for different business types
        impact_factors = {
            'manufacturing': 0.15,
            'healthcare': 0.10,
            'education': 0.08,
            'commercial_office': 0.05,
            'retail': 0.07,
            'technology_hub': 0.20,
            'warehousing': 0.04,
            'financial': 0.06
        }
        
        for field, coefficient in impact_factors.items():
            count = getattr(ctx, field + '_count')
            # Distance factor (closer businesses have more impact)
            distance_factor = 1.0 / (1 + ctx.radius_km / 5.0)
            base += count * coefficient * distance_factor * 0.02
        
        # Cap at 1.6x (60% increase maximum)
        return min(base, 1.6)
    
    def calculate_seasonal_factor(self, env: EnvironmentalData) -> float:
        """
        Calculate seasonal/environmental impact on cooling demand
        Higher temperatures increase cooling needs
        """
        factor = 0.85
        
        # Temperature impact (higher temp = more cooling needed)
        factor += max(env.temp_avg - 60, 0) * 0.008
        
        # Humidity impact (slight effect)
        factor += (env.humidity_avg - 50) * 0.001
        
        # Seasonal variation impact
        factor += env.seasonal_variation * 0.002
        
        return np.clip(factor, 0.8, 1.3)
    
    def assess_grid_impact(self, pred_demand: float, grid_info: GridInfrastructure) -> str:
        """Categorize grid impact level"""
        utilization = pred_demand / grid_info.grid_capacity
        
        if utilization > 0.8:
            return 'HIGH_STRAIN'
        elif utilization > 0.6:
            return 'MODERATE_IMPACT'
        else:
            return 'LOW_IMPACT'
    
    def predict_impact(
        self, 
        specs: DatacenterSpecs,
        context: BusinessContext,
        grid: GridInfrastructure,
        environment: EnvironmentalData
    ) -> Dict:
        """
        Main prediction function
        Returns comprehensive impact analysis
        """
        # Calculate base consumption
        base_consumption = self.calculate_base_consumption(specs)
        
        # Apply business context multiplier
        business_multiplier = self.calculate_business_context_multiplier(context)
        
        # Apply seasonal/environmental factor
        seasonal_factor = self.calculate_seasonal_factor(environment)
        
        # Final predicted demand
        predicted_demand = base_consumption * business_multiplier * seasonal_factor
        
        # Grid impact assessment
        grid_impact = self.assess_grid_impact(predicted_demand, grid)
        grid_utilization = predicted_demand / grid.grid_capacity
        
        # Uncertainty range (based on model MAPE)
        uncertainty_lower = predicted_demand * (1 - self.model_uncertainty)
        uncertainty_upper = predicted_demand * (1 + self.model_uncertainty)
        
        # Additional impact metrics
        annual_energy_mwh = predicted_demand * 8760  # hours per year
        co2_emissions_tons = annual_energy_mwh * 0.4  # approximate kg CO2/kWh * 1000
        
        # Economic estimates
        estimated_jobs = int(specs.server_count / 500)  # rough estimate
        annual_energy_cost = annual_energy_mwh * 50  # $50/MWh average
        
        # State comparison
        state_info = self.STATE_DATA.get(specs.state, {'percentage': 0, 'pue': 1.4, 'region': 'Unknown'})
        
        return {
            'base_consumption_mw': round(base_consumption, 2),
            'business_multiplier': round(business_multiplier, 3),
            'seasonal_factor': round(seasonal_factor, 3),
            'predicted_demand_mw': round(predicted_demand, 2),
            'uncertainty_range_mw': [round(uncertainty_lower, 2), round(uncertainty_upper, 2)],
            'grid_impact': grid_impact,
            'grid_utilization': round(grid_utilization, 3),
            'grid_utilization_percent': round(grid_utilization * 100, 1),
            'confidence_score': round(1 - self.model_uncertainty, 2),
            'annual_energy_mwh': round(annual_energy_mwh, 0),
            'co2_emissions_tons': round(co2_emissions_tons, 0),
            'estimated_jobs': estimated_jobs,
            'annual_energy_cost_usd': round(annual_energy_cost, 0),
            'state_datacenter_percentage': state_info['percentage'],
            'state_region': state_info['region'],
            'state_typical_pue': state_info['pue']
        }
    
    @classmethod
    def get_state_list(cls):
        """Return list of available states"""
        return sorted(cls.STATE_DATA.keys())
    
    @classmethod
    def get_state_info(cls, state: str):
        """Get information about a specific state"""
        return cls.STATE_DATA.get(state, None)
