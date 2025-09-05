"""
Test suite using pytest
"""
from datacenter_power_predictor import DatacenterPowerDemandPredictor, DatacenterSpecs, BusinessContext, GridInfrastructure, EnvironmentalData

def test_prediction_pipeline_smoke():
    specs = DatacenterSpecs(5000, 15, 0.4, 1.3, 200000, 'Liquid', 'Virginia')
    ctx = BusinessContext(2, 1, 0, 5, 3, 1, 2, 1)
    grid = GridInfrastructure(850, 345.0)
    env = EnvironmentalData(65, 60, 15)
    predictor = DatacenterPowerDemandPredictor()
    result = predictor.predict_single_facility(specs, ctx, grid, env)
    assert result['predicted_demand_mw'] > 0

def test_training_pipeline():
    from data_utils import USDatacenterDataGenerator
    import pandas as pd
    df = USDatacenterDataGenerator().generate_dataset(n_samples=100)
    predictor = DatacenterPowerDemandPredictor()
    results = predictor.train_models(df)
    assert 'random_forest' in results
    assert results['random_forest']['r2'] >= 0
