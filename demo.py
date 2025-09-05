
"""Datacenter Power Demand Estimation Demo"""

# Clone repository
!git clone https://github.com/rmkenv/datacenter-demand.git
# %cd datacenter-demand   # (Uncomment in Colab to change directory)

# Install dependencies
!pip install -r requirements.txt

# Generate synthetic dataset
!python dcpower.py generate

# Train ML models
!python dcpower.py train

# Predict datacenter power demand
!python dcpower.py predict --servers 5000 --rack-density 15 --gpu 0.4 --pue 1.3 \
--sqft 200000 --cooling Liquid --state Virginia --grid-capacity 850 --temp 65

# Run unit tests
!pytest --maxfail=1 --disable-warnings -q

# Visualization example
from visualization_utils import plot_state_consumption_bar
plot_state_consumption_bar()
