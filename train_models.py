"""
Train and Validate ML Models for Datacenter Power Demand
"""
from datacenter_power_predictor import DatacenterPowerDemandPredictor
from data_utils import DataProcessor
import pandas as pd

def train_and_report(datafile='us_datacenter_power_demand_dataset.csv'):
    df = DataProcessor.load_and_validate_data(datafile)
    predictor = DatacenterPowerDemandPredictor()
    results = predictor.train_models(df)
    print("\nModel Performance:")
    for name, m in results.items():
        if isinstance(m, dict) and 'r2' in m:
            print(f"{name:16s} | R2: {m['r2']:.3f} | MAPE: {m['mape']:.2f}% | MAE: {m['mae']:.2f} MW | RMSE: {m['rmse']:.2f} MW")
    return predictor, results

if __name__ == '__main__':
    train_and_report()
