"""
US Datacenter Power Demand Estimation Algorithm

Implements single-facility demand prediction and model training.
"""
import numpy as np
import logging
from typing import Dict, List
from dataclasses import dataclass
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Logging config
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class DatacenterSpecs:
    server_count: int
    rack_density: float       # kW per rack
    gpu_percentage: float     # fraction [0-1]
    pue_rating: float
    building_sqft: int
    cooling_type: str         # 'Air' or 'Liquid'
    state: str                # e.g. 'Virginia'

@dataclass
class BusinessContext:
    manufacturing_count: int
    healthcare_count: int
    education_count: int
    commercial_office_count: int
    retail_count: int
    technology_hub_count: int
    warehousing_count: int
    financial_count: int
    radius_km: float = 5.0

@dataclass
class GridInfrastructure:
    grid_capacity: float  # MW
    transmission_rating: float  # kV
    substation_distance: float = 2.0
    reliability_score: float = 0.95
    renewable_percentage: float = 0.25

@dataclass
class EnvironmentalData:
    temp_avg: float
    humidity_avg: float
    seasonal_variation: float
    altitude: float = 0.0

class DatacenterPowerDemandPredictor:
    """Main class for prediction and model training"""

    def __init__(self, config: Dict = None):
        self.config = config or {
            'rf_n_estimators': 100,
            'gb_n_estimators': 100,
            'nn_hidden_layers': (100, 50),
            'nn_max_iter': 500,
            'validation_split': 0.2,
            'cv_folds': 5
        }
        self.models = {
            'random_forest': RandomForestRegressor(
                n_estimators=self.config['rf_n_estimators'], random_state=42, n_jobs=-1),
            'gradient_boosting': GradientBoostingRegressor(
                n_estimators=self.config['gb_n_estimators'], random_state=42),
            'neural_network': MLPRegressor(
                hidden_layer_sizes=self.config['nn_hidden_layers'], max_iter=self.config['nn_max_iter'], random_state=42)
        }
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.feature_columns = []
        self.is_trained = False

    def calculate_base_consumption(self, specs: DatacenterSpecs) -> float:
        # Basic physical calculation for MW
        servers_per_rack = 42 / 2  # Approximate 2U servers/rack
        total_racks = specs.server_count / servers_per_rack
        base_server_power = total_racks * specs.rack_density
        gpu_multiplier = 1 + (specs.gpu_percentage * 2.5)
        server_power_kw = base_server_power * gpu_multiplier
        cooling_efficiency = 0.25 if specs.cooling_type.lower() == 'liquid' else 0.4
        cooling_power_kw = server_power_kw * cooling_efficiency
        infrastructure_power_kw = (server_power_kw + cooling_power_kw) * 0.15
        total_power_kw = (server_power_kw + cooling_power_kw + infrastructure_power_kw) * specs.pue_rating
        return total_power_kw / 1000.0

    def calculate_business_context_multiplier(self, ctx: BusinessContext) -> float:
        base = 1.0
        impact_factors = {
            'manufacturing': 0.15, 'healthcare': 0.10, 'education': 0.08, 'commercial_office': 0.05,
            'retail': 0.07, 'technology_hub': 0.20, 'warehousing': 0.04, 'financial': 0.06}
        for field, coef in impact_factors.items():
            count = getattr(ctx, field + '_count')
            dist_factor = 1.0 / (1 + ctx.radius_km / 5.0)
            base += count * coef * dist_factor * 0.02
        return min(base, 1.6)

    def calculate_seasonal_factor(self, env: EnvironmentalData) -> float:
        factor = 0.85 + max(env.temp_avg - 60, 0) * 0.008
        factor += (env.humidity_avg - 50) * 0.001
        factor += env.seasonal_variation * 0.002
        return np.clip(factor, 0.8, 1.3)

    def assess_grid_impact(self, pred_demand: float, grid_info: GridInfrastructure) -> str:
        utilization = pred_demand / grid_info.grid_capacity
        if utilization > 0.8: return 'HIGH_STRAIN'
        elif utilization > 0.6: return 'MODERATE_IMPACT'
        else: return 'LOW_IMPACT'

    def predict_single_facility(self, specs, ctx, grid, env) -> Dict:
        base = self.calculate_base_consumption(specs)
        bus_multiplier = self.calculate_business_context_multiplier(ctx)
        s_factor = self.calculate_seasonal_factor(env)
        predicted = base * bus_multiplier * s_factor
        grid_impact = self.assess_grid_impact(predicted, grid)
        uncertainty = 0.12
        return {
            'base_consumption_mw': round(base, 2),
            'business_multiplier': round(bus_multiplier, 3),
            'seasonal_factor': round(s_factor, 3),
            'predicted_demand_mw': round(predicted, 2),
            'uncertainty_range_mw': [round(predicted * (1 - uncertainty), 2), round(predicted * (1 + uncertainty), 2)],
            'grid_impact': grid_impact,
            'grid_utilization': round(predicted / grid.grid_capacity, 3),
            'confidence_score': 0.88
        }

    def prepare_training_features(self, df):
        numeric = [
            'server_count', 'rack_density', 'gpu_percentage', 'pue_rating',
            'building_sqft', 'temp_avg', 'humidity_avg', 'grid_capacity',
            'transmission_rating', 'business_multiplier', 'seasonal_factor'
        ]
        business = [c for c in df.columns if c.endswith('_count')]
        cat = ['state', 'region', 'cooling_type']
        df_encoded = df.copy()
        for c in cat:
            enc = LabelEncoder()
            df_encoded[f'{c}_encoded'] = enc.fit_transform(df[c])
            self.label_encoders[c] = enc
        features = numeric + business + [f'{v}_encoded' for v in cat]
        self.feature_columns = features
        X = df_encoded[features].fillna(0).values
        y = df_encoded['actual_demand_mw'].values
        return X, y, features

    def train_models(self, df):
        X, y, features = self.prepare_training_features(df)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=self.config['validation_split'], random_state=42)
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        results = {}
        for name, model in self.models.items():
            if name == 'neural_network':
                model.fit(X_train_scaled, y_train)
                y_pred = model.predict(X_test_scaled)
                cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=self.config['cv_folds'], scoring='r2')
            else:
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
                cv_scores = cross_val_score(model, X_train, y_train, cv=self.config['cv_folds'], scoring='r2')
            mae = mean_absolute_error(y_test, y_pred)
            rmse = np.sqrt(mean_squared_error(y_test, y_pred))
            r2s = r2_score(y_test, y_pred)
            mape = np.mean(np.abs((y_test - y_pred) / y_test)) * 100
            results[name] = {
                'mae': mae, 'rmse': rmse, 'r2': r2s, 'mape': mape,
                'cv_r2_mean': cv_scores.mean(), 'cv_r2_std': cv_scores.std(),
                'predictions': y_pred, 'actual': y_test
            }
        # Feature importance (Random Forest)
        if 'random_forest' in results:
            model = self.models['random_forest']
            import pandas as pd
            results['feature_importance'] = pd.DataFrame({
                'feature': features,
                'importance': model.feature_importances_
            }).sort_values('importance', ascending=False)
        self.is_trained = True
        return results
