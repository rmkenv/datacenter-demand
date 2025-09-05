"""
Publication-ready Visualizations for Datacenter Power Demand
"""
import matplotlib.pyplot as plt
import pandas as pd

def plot_state_consumption_bar():
    # Replace with chart as needed
    states = ['Virginia', 'Nebraska', 'Oregon', 'Iowa', 'Nevada']
    percentages = [25.6, 11.7, 11.4, 11.4, 8.7]
    plt.bar(states, percentages)
    plt.ylabel("Datacenter % State Electr.")
    plt.title("Top 5 US States by Datacenter Electricity Use")
    plt.tight_layout()
    plt.show()
