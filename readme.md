text
# Simple Gas Pipeline Data Analysis

A minimal, API-free Python project for analyzing gas pipeline delivery data. Includes basic analytics, anomaly detection, and plotting. Designed for use in Jupyter, Colab, or as a simple Python script.

## Features

- Seasonal pattern analysis and time series visualization
- Basic anomaly detection (z-score method)
- Throughput and capacity summary stats
- Geographic plotting (if lat/lon available)
- Fully local, no API or cloud dependencies

## Setup

1. Install dependencies:
pip install pandas numpy matplotlib seaborn

text
2. (Optional) For notebooks, install Jupyter or run in Colab.

## Usage

- Run example analyses using the included notebook.
- Or run directly:
python pipeline_analysis.py

text

## Data

The provided `gas_pipeline_sample.csv` is for demonstration. Use your own data by matching its structure:
- pipeline_name, loc_name, eff_gas_day, scheduled_quantity, latitude, longitude

## Extending

Add new analysis or plotting functions in `pipeline_analysis.py`.

## License

MIT
data/gas_pipeline_sample.csv
Example with synthetic data:

text
pipeline_name,loc_name,eff_gas_day,scheduled_quantity,latitude,longitude
Alpha,StationA,2023-01-01,1050,40.7128,-74.0060
Alpha,StationA,2023-01-02,970,40.7128,-74.0060
Alpha,StationA,2023-01-03,985,40.7128,-74.0060
Beta,StationB,2023-01-01,800,34.0522,-118.2437
Beta,StationB,2023-01-02,810,34.0522,-118.2437
Beta,StationB,2023-01-03,780,34.0522,-118.2437
pipeline_analysis.py
python
"""
Simple Gas Pipeline Data Analysis: basic stats, anomaly detection, and plots.
Author: [your name]
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def load_data(filepath):
    """Load pipeline data from CSV."""
    df = pd.read_csv(filepath, parse_dates=["eff_gas_day"])
    return df

def summary_statistics(df):
    """Show capacity and throughput stats."""
    print("---- SUMMARY STATISTICS ----")
    print(df.groupby('pipeline_name')["scheduled_quantity"].describe())

def plot_time_series(df):
    """Plot time series for each pipeline/location."""
    for (pipeline, loc), group in df.groupby(['pipeline_name', 'loc_name']):
        plt.figure(figsize=(8, 4))
        plt.plot(group['eff_gas_day'], group['scheduled_quantity'])
        plt.title(f"{pipeline} / {loc} Delivery Over Time")
        plt.xlabel("Date")
        plt.ylabel("Scheduled Quantity")
        plt.show()

def detect_anomalies(df, threshold=2.5):
    """Flag days where delivery quantity is far from mean (z-score method)."""
    df['zscore'] = (df['scheduled_quantity'] - df['scheduled_quantity'].mean()) / df['scheduled_quantity'].std()
    anomalies = df[np.abs(df['zscore']) > threshold]
    print("---- ANOMALIES (by z-score > {:.1f}) ----".format(threshold))
    print(anomalies[['pipeline_name', 'loc_name', 'eff_gas_day', 'scheduled_quantity', 'zscore']])
    return anomalies

def plot_geographic(df):
    """Simple scatterplot of locations (if lat/lon available)."""
    plt.figure(figsize=(6, 4))
    sns.scatterplot(x='longitude', y='latitude', hue='pipeline_name', data=df)
    plt.title("Pipeline Station Locations")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.show()

def main():
    df = load_data("data/gas_pipeline_sample.csv")
    summary_statistics(df)
    plot_time_series(df)
    detect_anomalies(df)
    plot_geographic(df)

if __name__ == "__main__":
    main()
example_notebook.ipynb
Use a Jupyter Notebook for step-by-step exploration. Below is a description; actual cells should follow this sequence:

Cell 1: Install packages (if needed)

python
!pip install pandas numpy matplotlib seaborn
Cell 2: Import code and load data

python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("data/gas_pipeline_sample.csv", parse_dates=["eff_gas_day"])
Cell 3: Explore statistics

python
df.groupby('pipeline_name')["scheduled_quantity"].describe()
Cell 4: Plot time series

python
for (pipeline, loc), group in df.groupby(['pipeline_name', 'loc_name']):
    plt.figure(figsize=(8, 4))
    plt.plot(group['eff_gas_day'], group['scheduled_quantity'])
    plt.title(f"{pipeline} / {loc} Delivery Over Time")
    plt.xlabel("Date")
    plt.ylabel("Scheduled Quantity")
    plt.show()
Cell 5: Detect anomalies

python
df['zscore'] = (df['scheduled_quantity'] - df['scheduled_quantity'].mean()) / df['scheduled_quantity'].std()
anomalies = df[np.abs(df['zscore']) > 2.5]
anomalies
Cell 6: Plot station locations

python
sns.scatterplot(x='longitude', y='latitude', hue='pipeline_name', data=df)
plt.title("Pipeline Station Locations")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.show()
