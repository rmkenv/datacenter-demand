# 🚀 QUICK START GUIDE

## Your Datacenter Impact Calculator is Ready!

### 📁 Location
All files are in: `/workspace/streamlit_app/`

### ✅ What You Have

**Application Files:**
- `app.py` - Main Streamlit application (run this!)
- `predictor.py` - Prediction engine
- `visualizations.py` - Interactive charts
- `requirements.txt` - Dependencies
- `.streamlit/config.toml` - Styling

**Documentation:**
- `README.md` - Complete guide
- `DEPLOYMENT_GUIDE.md` - Deployment steps
- `SAMPLE_SCENARIOS.md` - Example scenarios
- `PROJECT_SUMMARY.md` - Full overview

---

## 🏃 Option 1: Test Locally (2 minutes)

```bash
# Navigate to folder
cd /workspace/streamlit_app

# Install dependencies (if not already done)
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

Opens automatically at: **http://localhost:8501**

---

## ☁️ Option 2: Deploy to Streamlit Cloud (5 minutes)

### Step 1: Create GitHub Repository
1. Go to https://github.com/new
2. Name it: `datacenter-impact-calculator`
3. Make it public
4. Create repository

### Step 2: Upload Files
Upload these files from `/workspace/streamlit_app/`:
- ✅ app.py
- ✅ predictor.py
- ✅ visualizations.py
- ✅ requirements.txt
- ✅ README.md
- ✅ .streamlit/config.toml (keep folder structure)

### Step 3: Deploy
1. Go to https://share.streamlit.io
2. Sign in with GitHub
3. Click "New app"
4. Select your repository
5. Main file: `app.py`
6. Click "Deploy"

### Step 4: Share Your URL
Format: `https://[username]-datacenter-impact-calculator.streamlit.app`

---

## 🎮 How to Use the App

### Tab 1: Home
- Read introduction
- Understand what the tool does

### Tab 2: Community Profile
- Select your state (14 options)
- Enter grid capacity (MW)
- Count nearby businesses
- Set temperature

### Tab 3: Datacenter Specs
- Server count (100-100,000)
- Rack density (5-30 kW)
- GPU percentage (0-100%)
- Cooling type (Air/Liquid)
- PUE rating (1.0-2.5)

### Tab 4: Impact Analysis
- See grid utilization gauge
- View power breakdown
- Compare to other states
- Read environmental impact
- Download report

### Tab 5: Learn More
- Understand datacenters
- Environmental concerns
- Economic effects
- Mitigation strategies

---

## 📊 Try These Scenarios

**Small Business Datacenter:**
- Servers: 1,000
- Rack: 10 kW
- GPU: 10%
- PUE: 1.5
- Result: ~2-3 MW

**Mid-Size Cloud:**
- Servers: 5,000
- Rack: 15 kW
- GPU: 40%
- PUE: 1.3
- Result: ~12-15 MW

**Hyperscale Facility:**
- Servers: 50,000
- Rack: 18 kW
- GPU: 30%
- PUE: 1.1
- Result: ~150-180 MW

---

## 🎯 Key Features

✅ **14 US States** - Pre-loaded with real statistics
✅ **Interactive Charts** - Hover for details
✅ **Grid Impact** - Color-coded warnings
✅ **Environmental** - CO₂ and energy estimates
✅ **Economic** - Job and cost projections
✅ **Download** - Export reports as TXT
✅ **Educational** - Learn about impacts
✅ **Mobile Ready** - Works on all devices

---

## 🆘 Need Help?

**Local Issues:**
- Dependencies: `pip install -r requirements.txt`
- Port in use: `streamlit run app.py --server.port 8502`

**Deployment Issues:**
- Check all files uploaded
- Verify requirements.txt format
- Ensure .streamlit folder included

**Questions:**
- Read README.md
- Check DEPLOYMENT_GUIDE.md
- See SAMPLE_SCENARIOS.md

---

## 🎉 You're All Set!

Your datacenter impact calculator is:
✅ Fully functional
✅ Well documented
✅ Ready to deploy
✅ Based on peer-reviewed research

**Deploy now and help your community make informed decisions!**

---

*Questions? Check PROJECT_SUMMARY.md for complete details*
