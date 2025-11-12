# Sample Datacenter Scenarios

Use these example scenarios to understand different types of datacenters and their impacts.

## 🏢 Scenario 1: Small Enterprise Datacenter

**Location:** Pennsylvania
**Purpose:** Regional business services

### Specifications
- Servers: 1,000
- Rack Density: 10 kW/rack
- GPU Percentage: 10%
- Cooling: Air
- PUE: 1.5
- Building Size: 50,000 sq ft

### Context
- Small city with mixed businesses
- Manufacturing: 3
- Commercial offices: 8
- Retail: 5
- Grid capacity: 430 MW

### Expected Impact
- Power demand: ~2-3 MW
- Grid utilization: <1%
- Impact level: LOW
- Jobs: 5-10

---

## 🌐 Scenario 2: Mid-Size Cloud Datacenter

**Location:** Virginia
**Purpose:** Cloud computing services (AWS-style)

### Specifications
- Servers: 5,000
- Rack Density: 15 kW/rack
- GPU Percentage: 40%
- Cooling: Liquid
- PUE: 1.3
- Building Size: 200,000 sq ft

### Context
- Tech hub area
- Technology hubs: 8
- Commercial offices: 15
- Manufacturing: 5
- Grid capacity: 850 MW

### Expected Impact
- Power demand: ~12-15 MW
- Grid utilization: 1.5-2%
- Impact level: LOW
- Jobs: 10-20

---

## 🤖 Scenario 3: AI/ML Training Datacenter

**Location:** California
**Purpose:** Artificial intelligence and machine learning

### Specifications
- Servers: 3,000
- Rack Density: 25 kW/rack
- GPU Percentage: 90%
- Cooling: Liquid
- PUE: 1.2
- Building Size: 150,000 sq ft

### Context
- Silicon Valley area
- Technology hubs: 20
- Commercial offices: 30
- Education: 5
- Grid capacity: 500 MW

### Expected Impact
- Power demand: ~25-30 MW
- Grid utilization: 5-6%
- Impact level: LOW-MODERATE
- Jobs: 15-25

---

## 🏭 Scenario 4: Hyperscale Datacenter

**Location:** Iowa
**Purpose:** Large cloud provider (Meta, Google, Microsoft)

### Specifications
- Servers: 50,000
- Rack Density: 18 kW/rack
- GPU Percentage: 30%
- Cooling: Liquid
- PUE: 1.1
- Building Size: 1,000,000 sq ft

### Context
- Rural area with renewable energy
- Manufacturing: 2
- Technology hubs: 1
- Grid capacity: 320 MW

### Expected Impact
- Power demand: ~150-180 MW
- Grid utilization: 50-55%
- Impact level: MODERATE-HIGH
- Jobs: 100-200

---

## ⚡ Scenario 5: High-Density GPU Cluster

**Location:** Texas
**Purpose:** Cryptocurrency mining or AI inference

### Specifications
- Servers: 10,000
- Rack Density: 30 kW/rack
- GPU Percentage: 100%
- Cooling: Liquid
- PUE: 1.4
- Building Size: 300,000 sq ft

### Context
- Industrial area
- Manufacturing: 10
- Warehousing: 8
- Grid capacity: 450 MW

### Expected Impact
- Power demand: ~80-100 MW
- Grid utilization: 18-22%
- Impact level: MODERATE
- Jobs: 20-40

---

## 📊 Comparison Table

| Scenario | Servers | Power (MW) | Grid % | Impact | Jobs |
|----------|---------|------------|--------|--------|------|
| Small Enterprise | 1,000 | 2-3 | <1% | LOW | 5-10 |
| Mid-Size Cloud | 5,000 | 12-15 | 1.5% | LOW | 10-20 |
| AI/ML Training | 3,000 | 25-30 | 5-6% | LOW-MOD | 15-25 |
| Hyperscale | 50,000 | 150-180 | 50-55% | MOD-HIGH | 100-200 |
| GPU Cluster | 10,000 | 80-100 | 18-22% | MODERATE | 20-40 |

---

## 💡 Key Insights

### Power Efficiency
- **Liquid cooling** reduces consumption by 15-25% vs air
- **Lower PUE** significantly reduces overall power draw
- **GPU workloads** can triple power consumption

### Grid Impact
- **Location matters**: States with higher grid capacity handle datacenters better
- **Business context**: Tech hubs add 10-20% to demand
- **Temperature**: Hot climates increase cooling needs by 15-30%

### Economic Trade-offs
- **Small datacenters**: Low impact, few jobs
- **Hyperscale**: Major grid impact, substantial job creation
- **Best balance**: Mid-size facilities in high-capacity grids

---

## 🎯 How to Use These Scenarios

1. **Compare to your situation**: Find the closest match to your proposed datacenter
2. **Adjust parameters**: Modify specifications in the app
3. **See the difference**: Note how changes affect predictions
4. **Inform decisions**: Use realistic scenarios in planning discussions

---

## ⚠️ Important Notes

- These are **illustrative examples**, not real facilities
- Actual impacts depend on many local factors
- Always consult with energy professionals
- Grid capacity varies significantly by region
- Job estimates include only direct employment

---

*Use the Streamlit app to explore these scenarios interactively!*
