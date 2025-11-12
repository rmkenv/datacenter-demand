"""
Visualization utilities for Datacenter Impact Application
Creates interactive Plotly charts and graphs
"""
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List

def create_grid_utilization_gauge(utilization_percent: float, impact_level: str) -> go.Figure:
    """
    Create a gauge chart showing grid utilization percentage
    """
    # Color based on impact level
    color_map = {
        'LOW_IMPACT': '#2ecc71',
        'MODERATE_IMPACT': '#f39c12',
        'HIGH_STRAIN': '#e74c3c'
    }
    color = color_map.get(impact_level, '#95a5a6')
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=utilization_percent,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Grid Utilization", 'font': {'size': 24}},
        number={'suffix': "%", 'font': {'size': 40}},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkgray"},
            'bar': {'color': color},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 60], 'color': '#d5f4e6'},
                {'range': [60, 80], 'color': '#ffeaa7'},
                {'range': [80, 100], 'color': '#fab1a0'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 80
            }
        }
    ))
    
    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=60, b=20),
        paper_bgcolor="white",
        font={'family': "Arial"}
    )
    
    return fig


def create_power_breakdown_chart(results: Dict) -> go.Figure:
    """
    Create a bar chart showing power demand breakdown
    """
    categories = ['Base Consumption', 'With Business Impact', 'With Seasonal Factors']
    values = [
        results['base_consumption_mw'],
        results['base_consumption_mw'] * results['business_multiplier'],
        results['predicted_demand_mw']
    ]
    
    colors = ['#3498db', '#9b59b6', '#e74c3c']
    
    fig = go.Figure(data=[
        go.Bar(
            x=categories,
            y=values,
            text=[f"{v:.1f} MW" for v in values],
            textposition='auto',
            marker_color=colors,
            hovertemplate='<b>%{x}</b><br>Power: %{y:.2f} MW<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title="Power Demand Breakdown",
        xaxis_title="",
        yaxis_title="Power Demand (MW)",
        height=400,
        showlegend=False,
        paper_bgcolor="white",
        plot_bgcolor="white",
        font={'family': "Arial", 'size': 12}
    )
    
    fig.update_yaxis(showgrid=True, gridcolor='lightgray')
    
    return fig


def create_state_comparison_chart(current_state: str, current_percentage: float, predictor_class) -> go.Figure:
    """
    Compare datacenter electricity usage across states
    """
    states = []
    percentages = []
    
    for state, data in predictor_class.STATE_DATA.items():
        states.append(state)
        percentages.append(data['percentage'])
    
    # Sort by percentage
    sorted_data = sorted(zip(states, percentages), key=lambda x: x[1], reverse=True)
    states, percentages = zip(*sorted_data)
    
    # Highlight current state
    colors = ['#e74c3c' if state == current_state else '#3498db' for state in states]
    
    fig = go.Figure(data=[
        go.Bar(
            x=list(percentages),
            y=list(states),
            orientation='h',
            marker_color=colors,
            text=[f"{p:.1f}%" for p in percentages],
            textposition='auto',
            hovertemplate='<b>%{y}</b><br>Datacenter Usage: %{x:.1f}%<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title="Datacenter Electricity Usage by State<br><sub>% of State's Total Electricity</sub>",
        xaxis_title="Percentage of State Electricity (%)",
        yaxis_title="",
        height=500,
        showlegend=False,
        paper_bgcolor="white",
        plot_bgcolor="white",
        font={'family': "Arial", 'size': 11}
    )
    
    fig.update_xaxis(showgrid=True, gridcolor='lightgray')
    
    return fig


def create_impact_summary_metrics(results: Dict) -> go.Figure:
    """
    Create a summary metrics visualization
    """
    metrics = [
        {
            'title': 'Power Demand',
            'value': f"{results['predicted_demand_mw']:.1f}",
            'unit': 'MW',
            'icon': '⚡'
        },
        {
            'title': 'Annual Energy',
            'value': f"{results['annual_energy_mwh']:,.0f}",
            'unit': 'MWh/year',
            'icon': '🔋'
        },
        {
            'title': 'CO₂ Emissions',
            'value': f"{results['co2_emissions_tons']:,.0f}",
            'unit': 'tons/year',
            'icon': '🌍'
        },
        {
            'title': 'Estimated Jobs',
            'value': f"{results['estimated_jobs']}",
            'unit': 'positions',
            'icon': '👥'
        }
    ]
    
    # Create subplot structure
    from plotly.subplots import make_subplots
    
    fig = make_subplots(
        rows=1, cols=4,
        specs=[[{'type': 'indicator'}, {'type': 'indicator'}, 
                {'type': 'indicator'}, {'type': 'indicator'}]],
        horizontal_spacing=0.1
    )
    
    for i, metric in enumerate(metrics):
        fig.add_trace(
            go.Indicator(
                mode="number",
                value=float(metric['value'].replace(',', '')),
                title={'text': f"{metric['icon']}<br>{metric['title']}<br><span style='font-size:0.8em'>{metric['unit']}</span>"},
                number={'font': {'size': 30}},
            ),
            row=1, col=i+1
        )
    
    fig.update_layout(
        height=200,
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor="white"
    )
    
    return fig


def create_uncertainty_range_chart(results: Dict) -> go.Figure:
    """
    Visualize prediction uncertainty range
    """
    predicted = results['predicted_demand_mw']
    lower, upper = results['uncertainty_range_mw']
    
    fig = go.Figure()
    
    # Add uncertainty range as a horizontal bar
    fig.add_trace(go.Scatter(
        x=[lower, upper],
        y=['Predicted Demand', 'Predicted Demand'],
        mode='lines+markers',
        line=dict(color='rgba(52, 152, 219, 0.3)', width=20),
        marker=dict(size=10, color=['#3498db', '#3498db']),
        name='Uncertainty Range',
        hovertemplate='Range: %{x:.2f} MW<extra></extra>'
    ))
    
    # Add predicted value
    fig.add_trace(go.Scatter(
        x=[predicted],
        y=['Predicted Demand'],
        mode='markers',
        marker=dict(size=15, color='#e74c3c', symbol='diamond'),
        name='Predicted',
        hovertemplate='Predicted: %{x:.2f} MW<extra></extra>'
    ))
    
    fig.update_layout(
        title=f"Prediction Uncertainty (±{results['confidence_score']*100:.0f}% Confidence)",
        xaxis_title="Power Demand (MW)",
        yaxis_title="",
        height=200,
        showlegend=True,
        paper_bgcolor="white",
        plot_bgcolor="white",
        font={'family': "Arial"}
    )
    
    fig.update_xaxis(showgrid=True, gridcolor='lightgray')
    fig.update_yaxis(showticklabels=False)
    
    return fig


def create_multiplier_visualization(business_mult: float, seasonal_mult: float) -> go.Figure:
    """
    Show multiplier effects as a funnel
    """
    stages = ['Base Power', 'Business Impact', 'Seasonal/Environmental']
    values = [1.0, business_mult, business_mult * seasonal_mult]
    
    fig = go.Figure(go.Funnel(
        y=stages,
        x=values,
        textposition="inside",
        textinfo="value+percent initial",
        marker={"color": ["#3498db", "#9b59b6", "#e74c3c"]},
        hovertemplate='<b>%{y}</b><br>Multiplier: %{x:.3f}x<extra></extra>'
    ))
    
    fig.update_layout(
        title="Impact Multipliers",
        height=300,
        paper_bgcolor="white",
        font={'family': "Arial"}
    )
    
    return fig
