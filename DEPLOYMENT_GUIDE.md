# Quick Deployment Guide

## 🚀 Deploy to Streamlit Cloud in 5 Minutes

### Step 1: Prepare Your Files
You have everything ready in the `streamlit_app` folder:
- ✅ app.py (main application)
- ✅ predictor.py (prediction engine)
- ✅ visualizations.py (charts)
- ✅ requirements.txt (dependencies)
- ✅ README.md (documentation)
- ✅ .streamlit/config.toml (styling)

### Step 2: Upload to GitHub

**Option A: Create New Repository**
1. Go to https://github.com/new
2. Create repository (e.g., "datacenter-impact-calculator")
3. Upload all files from `streamlit_app` folder
4. Commit and push

**Option B: Use GitHub Desktop**
1. Download GitHub Desktop
2. Create new repository
3. Add files from `streamlit_app`
4. Publish to GitHub

### Step 3: Deploy to Streamlit Cloud

1. **Visit Streamlit Cloud**
   - Go to https://share.streamlit.io
   - Sign in with GitHub

2. **Create New App**
   - Click "New app" button
   - Select your repository
   - Main file path: `app.py`
   - Click "Deploy"

3. **Wait for Deployment** (2-3 minutes)
   - Streamlit will install dependencies
   - App will start automatically

4. **Get Your URL**
   - Format: `https://[username]-[repo-name].streamlit.app`
   - Share with your community!

### Step 4: Test Your App

Visit your app and test:
- [ ] Home tab loads correctly
- [ ] Community Profile inputs work
- [ ] Datacenter Specs inputs work
- [ ] Impact Analysis generates charts
- [ ] Learn More content displays

## 🖥️ Local Testing (Optional)

Before deploying, test locally:

```bash
# Navigate to folder
cd streamlit_app

# Install dependencies
pip install -r requirements.txt

# Run app
streamlit run app.py
```

Opens at: http://localhost:8501

## 🔧 Troubleshooting

### Deployment Fails
- Check requirements.txt format (no extra spaces)
- Ensure all .py files are uploaded
- Verify Python 3.8+ selected in Streamlit settings

### Charts Don't Display
- Check Plotly installed in requirements.txt
- Clear browser cache
- Try different browser

### App is Slow
- Normal for first load (cold start)
- Subsequent loads are faster
- Consider Streamlit caching for large datasets

## 📱 Sharing Your App

Once deployed, share the URL with:
- Community members
- Local government
- Environmental groups
- Planning committees

## 🎨 Customization

### Change Colors
Edit `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#YOUR_COLOR"
backgroundColor = "#YOUR_COLOR"
```

### Add Your Logo
Replace placeholder in `app.py` sidebar:
```python
st.image("your_logo.png", use_container_width=True)
```

### Add More States
Edit `STATE_DATA` in `predictor.py`

## 📊 Example Usage

1. **Community Meeting**
   - Project app on screen
   - Input proposed datacenter specs live
   - Show impact visualizations
   - Discuss results with attendees

2. **Planning Commission**
   - Generate reports beforehand
   - Download analysis as TXT
   - Include in meeting materials

3. **Public Education**
   - Share app link online
   - Let residents explore scenarios
   - Gather feedback and concerns

## 🆘 Need Help?

- Review README.md for details
- Check original research: https://github.com/rmkenv/datacenter-demand
- Streamlit docs: https://docs.streamlit.io
- Contact local energy professionals

---

**You're ready to deploy! 🚀**
