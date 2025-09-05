#!/usr/bin/env python3
"""
CLI for US Datacenter Power Demand Estimation
"""
import click
from datacenter_power_predictor import DatacenterSpecs, BusinessContext, GridInfrastructure, EnvironmentalData, DatacenterPowerDemandPredictor
from data_utils import USDatacenterDataGenerator
from train_models import train_and_report
import pandas as pd

@click.group()
def cli():
    "Datacenter Power Demand CLI"
    pass

@cli.command()
def generate():
    "Generate synthetic datacenter dataset"
    df = USDatacenterDataGenerator().generate_dataset()
    print(f"Generated {len(df)} rows")

@cli.command()
def train():
    "Train and evaluate machine learning models"
    train_and_report()

@cli.command()
@click.option('--servers', type=int, required=True)
@click.option('--rack-density', type=float, required=True)
@click.option('--gpu', type=float, default=0.2)
@click.option('--pue', type=float, default=1.4)
@click.option('--sqft', type=int, required=True)
@click.option('--cooling', type=click.Choice(['Air', 'Liquid']), default='Air')
@click.option('--state', type=str, required=True)
@click.option('--grid-capacity', type=float, default=500.0)
@click.option('--temp', type=float, default=70.0)
def predict(servers, rack_density, gpu, pue, sqft, cooling, state, grid_capacity, temp):
    "Estimate power for single facility"
    specs = DatacenterSpecs(servers, rack_density, gpu, pue, sqft, cooling, state)
    context = BusinessContext(2, 1, 1, 5, 3, 1, 2, 1)
    grid = GridInfrastructure(grid_capacity, 230.0)
    env = EnvironmentalData(temp, 50.0, 15.0)
    predictor = DatacenterPowerDemandPredictor()
    result = predictor.predict_single_facility(specs, context, grid, env)
    for k, v in result.items():
        print(f"{k}: {v}")

if __name__ == '__main__':
    cli()
