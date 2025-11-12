# 🏢 Datacenter Community Impact Calculator

A Streamlit web application that helps communities understand the potential impact of datacenters on their local electrical grid, environment, and economy.

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)

## 🎯 Overview

This tool uses machine learning models trained on US datacenter data to predict:
- **Power demand** in megawatts (MW)
- **Grid utilization** and strain levels
- **Environmental impact** (CO₂ emissions, energy consumption)
- **Economic effects** (jobs, energy costs)

### Based on Research

This application is built on the research from [datacenter-demand](https://github.com/rmkenv/datacenter-demand), featuring:
- **96% accuracy** (R² score)
- **12.6% mean error** (MAPE)
- Neural network model trained on 2,000+ datacenter scenarios
- Calibrated to US state-level statistics

## ✨ Features

### 📍 Community Profile
- State selection with pre-loaded datacenter statistics
- Local grid infrastructure details
- Nearby business context (manufacturing, tech hubs, retail, etc.)
- Environmental conditions (temperature, humidity)

### 🖥️ Datacenter Specifications
- Server count and configuration
- Rack density and GPU percentage
- Building size and cooling system type
- PUE (Power Usage Effectiveness) rating

### 📊 Impact Analysis
- **Interactive visualizations** using Plotly
- Grid utilization gauge with color-coded impact levels
- Power demand breakdown charts
- State-by-state comparison
- Prediction uncertainty ranges
- Environmental and economic metrics
- Downloadable analysis reports

### 📚 Educational Resources
- Comprehensive guides on datacenter impacts
- Explanations of key metrics (PUE, rack density, etc.)
- Mitigation strategies for environmental concerns
- Community action steps

## 🚀 Quick Start

### Local Installation

1. **Clone or download this repository**
```bash
cd streamlit_app
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
streamlit run app.py
```

4. **Open in browser**
The app will automatically open at `http://localhost:8501`

## ☁️ Deploy to Streamlit Cloud

### Option 1: GitHub Deployment (Recommended)

1. **Create a GitHub repository**
   - Create a new repository on GitHub
   - Upload all files from the `streamlit_app` folder

2. **Connect to Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Set main file path: `app.py`
   - Click "Deploy"

3. **Your app will be live in minutes!**
   - URL format: `https://[your-username]-[repo-name].streamlit.app`

### Option 2: Direct Deployment

1. **Visit Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)

2. **Upload your app**
   - Use the "Paste GitHub URL" option
   - Or drag and drop your files

3. **Configure settings**
   - Python version: 3.8+
   - Main file: `app.py`

4. **Deploy!**

## 📁 Project Structure

```
streamlit_app/
├── app.py                  # Main Streamlit application
├── predictor.py            # ML prediction engine
├── visualizations.py       # Plotly chart functions
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## 🔧 Configuration

### Customizing State Data

Edit the `STATE_DATA` dictionary in `predictor.py` to add more states or update statistics:

```python
STATE_DATA = {
    'YourState': {
        'percentage': 5.0,      # % of state electricity used by datacenters
        'pue': 1.35,            # Typical PUE for the state
        'region': 'Region',     # Geographic region
        'grid_capacity': 400    # Typical grid capacity (MW)
    }
}
```

### Adjusting Model Parameters

Modify uncertainty and calculation factors in `predictor.py`:

```python
self.model_uncertainty = 0.126  # MAPE from neural network model
```

## 📊 Understanding the Predictions

### Grid Impact Levels

- **LOW_IMPACT** (<60% utilization): Minimal strain on infrastructure
- **MODERATE_IMPACT** (60-80% utilization): Noticeable load, may need improvements
- **HIGH_STRAIN** (>80% utilization): Significant concerns, requires upgrades

### Key Metrics

- **PUE (Power Usage Effectiveness)**: Ratio of total facility power to IT power
  - 1.0 = Perfect (theoretical)
  - 1.2-1.4 = Excellent
  - 1.5 = Industry average
  - 2.0+ = Inefficient

- **Rack Density**: Power per server rack (kW)
  - 5-8 kW = Traditional
  - 12-20 kW = Modern
  - 30+ kW = High-performance AI

## 🛠️ Troubleshooting

### Common Issues

**App won't start:**
- Check Python version (3.8+ required)
- Verify all dependencies installed: `pip install -r requirements.txt`

**Charts not displaying:**
- Ensure Plotly is installed: `pip install plotly>=5.17.0`
- Clear browser cache

**Data not saving between tabs:**
- This is normal - Streamlit uses session state
- Complete tabs in order: Community Profile → Datacenter Specs → Impact Analysis

### Deployment Issues

**Streamlit Cloud errors:**
- Check `requirements.txt` formatting
- Ensure all files uploaded correctly
- Verify Python version in settings (3.8+)

## 📈 Technical Details

### Machine Learning Model

The prediction engine uses algorithms from the original research:
- **Architecture**: Physics-based calculation + ML multipliers
- **Features**: Server specs, facility design, business context, environmental factors
- **Validation**: Cross-validated on synthetic datasets calibrated to real US statistics

### Calculation Flow

1. **Base Consumption**: Hardware specs + PUE → Base MW
2. **Business Multiplier**: Nearby businesses → 1.0-1.6x adjustment
3. **Seasonal Factor**: Temperature/humidity → 0.8-1.3x adjustment
4. **Final Prediction**: Base × Business × Seasonal
5. **Uncertainty**: ±12.6% range from model MAPE

## 🤝 Contributing

This tool is based on open research. Suggestions for improvements:

1. **Additional States**: Submit state-level datacenter statistics
2. **Enhanced Visualizations**: New chart types or metrics
3. **Educational Content**: Clearer explanations or additional resources
4. **Localization**: Support for other countries/regions

## 📄 License

This project adapts code from [datacenter-demand](https://github.com/rmkenv/datacenter-demand) which is under MIT License.

## 🙏 Acknowledgments

- Original research: [rmkenv/datacenter-demand](https://github.com/rmkenv/datacenter-demand)
- Data sources: U.S. Department of Energy, Lawrence Berkeley National Laboratory
- Visualization: Plotly
- Framework: Streamlit

## 📞 Support

For issues or questions:
- Check the "Learn More" tab in the app
- Review the original research repository
- Consult with energy professionals for specific projects

## ⚠️ Disclaimer

This tool is for educational and planning purposes only. Predictions are estimates based on machine learning models with inherent uncertainty. For critical infrastructure decisions, consult with professional engineers and energy experts.

---

**Built with ❤️ for communities concerned about datacenter impacts**

*Last updated: November 2024*
