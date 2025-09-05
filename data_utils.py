"""
Data Utilities for US Datacenter Power Algorithm
Generates synthetic data for the ML pipeline
"""
import numpy as np
import pandas as pd
import logging

logger = logging.getLogger(__name__)

class USDatacenterDataGenerator:
    """Generate synthetic datacenter data as per US patterns"""

    def __init__(self, seed: int = 42):
        np.random.seed(seed)
        self.state_data = {
            'Virginia': {'percentage': 25.6, 'pue': 1.35, 'region': 'Southeast'},
            'Texas': {'percentage': 4.6, 'pue': 1.42, 'region': 'South'},
            'California': {'percentage': 3.7, 'pue': 1.28, 'region': 'West'},
            'Illinois': {'percentage': 5.5, 'pue': 1.38, 'region': 'Midwest'},
            'Oregon': {'percentage': 11.4, 'pue': 1.25, 'region': 'West'},
            'Arizona': {'percentage': 7.4, 'pue': 1.45, 'region': 'Southwest'},
            'Iowa': {'percentage': 11.4, 'pue': 1.32, 'region': 'Midwest'},
            'Georgia': {'percentage': 4.3, 'pue': 1.36, 'region': 'Southeast'},
            'Washington': {'percentage': 5.7, 'pue': 1.22, 'region': 'West'},
            'Pennsylvania': {'percentage': 3.2, 'pue': 1.41, 'region': 'Northeast'},
            'New Jersey': {'percentage': 5.4, 'pue': 1.43, 'region': 'Northeast'},
            'Nebraska': {'percentage': 11.7, 'pue': 1.34, 'region': 'Midwest'},
            'North Dakota': {'percentage': 4.4, 'pue': 1.39, 'region': 'Midwest'},
            'Nevada': {'percentage': 8.7, 'pue': 1.41, 'region': 'West'},
        }
        self.business_types = [
            'Manufacturing', 'Healthcare', 'Education', 'Commercial_Office',
            'Retail', 'Technology_Hub', 'Warehousing', 'Financial'
        ]

    def generate_dataset(self, n_samples=2000, output_file='us_datacenter_power_demand_dataset.csv'):
        """Main data generation routine"""
        data = []
        state_names = list(self.state_data.keys())
        weights = np.array([self.state_data[s]['percentage'] for s in state_names])
        weights = weights / np.sum(weights)
        for _ in range(n_samples):
            state = np.random.choice(state_names, p=weights)
            sdat = self.state_data[state]
            server_count = int(np.random.lognormal(7.5, 1.2))
            rack_density = np.random.normal(12.5, 3.2)
            gpu_pct = np.random.beta(2, 8)
            pue = np.random.normal(sdat['pue'], 0.15)
            building_sqft = int(server_count * np.random.uniform(80, 120))
            cooling_type = np.random.choice(['Air', 'Liquid'], p=[0.75, 0.25])
            temp_avg = np.random.normal(75, 15)
            humidity_avg = np.random.uniform(40, 70)
            business_counts = {f"{b}_count": np.random.poisson(4) for b in self.business_types}
            grid_capacity = np.random.normal(850 if state == 'Virginia' else 400, 150)
            transmission_rating = np.random.normal(345, 50)
            base_server_power = (server_count / 21) * rack_density
            gpu_mult = 1 + (gpu_pct * 2.5)
            server_power = base_server_power * gpu_mult
            cooling_efficiency = 0.25 if cooling_type == 'Liquid' else 0.4
            cooling_power = server_power * cooling_efficiency
            infrastructure_power = (server_power + cooling_power) * 0.15
            base_consumption_mw = (server_power + cooling_power + infrastructure_power) * pue / 1000
            # context multiplier
            business_multiplier = 1.0 + sum(np.random.uniform(0, 0.01) * business_counts[k]
                                            for k in business_counts)
            business_multiplier = min(business_multiplier, 1.6)
            seasonal_factor = 0.85 + max(temp_avg - 60, 0) * 0.008
            predicted_demand = base_consumption_mw * business_multiplier * seasonal_factor
            actual_demand = predicted_demand * np.random.normal(1.0, 0.08)
            item = {
                'state': state, 'region': sdat['region'], 'server_count': server_count,
                'rack_density': max(rack_density, 5), 'gpu_percentage': gpu_pct,
                'pue_rating': max(pue, 1.0), 'building_sqft': building_sqft, 'cooling_type': cooling_type,
                'temp_avg': temp_avg, 'humidity_avg': humidity_avg,
                'grid_capacity': grid_capacity, 'transmission_rating': transmission_rating,
                'base_consumption_mw': base_consumption_mw, 'business_multiplier': business_multiplier,
                'seasonal_factor': seasonal_factor, 'predicted_demand_mw': predicted_demand,
                'actual_demand_mw': actual_demand
            }
            item.update(business_counts)
            data.append(item)
        df = pd.DataFrame(data)
        if output_file:
            df.to_csv(output_file, index=False)
        return df

class DataProcessor:
    """Basic loader/validator (stub)"""
    @staticmethod
    def load_and_validate_data(filename):
        return pd.read_csv(filename)
