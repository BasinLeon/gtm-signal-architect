# Streamlit Cloud Deployment Guide

This guide will help you deploy the Basin Signal Architect to Streamlit Cloud for a live demo.

## Prerequisites

- GitHub account
- Streamlit Cloud account (free tier available at [share.streamlit.io](https://share.streamlit.io))
- gtm-signal-architect repository pushed to GitHub

## Step 1: Push Repository to GitHub

```bash
cd ~/Documents/GitHub/gtm-signal-architect

# Initialize git repository (if not already done)
git init

# Add all files
git add .

# Create first commit
git commit -m "Initial commit: Basin Signal Architect"

# Create GitHub repository (via GitHub website or CLI)
# Then push to remote
git remote add origin https://github.com/BasinLeon/gtm-signal-architect.git
git branch -M main
git push -u origin main
```

## Step 2: Deploy to Streamlit Cloud

### Automatic Deployment (Recommended)

1. **Go to Streamlit Cloud**: Visit [share.streamlit.io](https://share.streamlit.io)
2. **Sign in** with your GitHub account
3. **Click "New app"**
4. **Select your repository**:
   - Repository: `BasinLeon/gtm-signal-architect`
   - Branch: `main`
   - Main file path: `app.py`
5. **Click "Deploy"**

That's it! Streamlit Cloud will:
- Install dependencies from `requirements.txt`
- Start the app
- Provide you with a public URL like `https://basinleon-gtm-signal-architect.streamlit.app`

### Configuration Options

**Custom Domain** (Optional):
- Go to app settings in Streamlit Cloud
- Add custom domain (requires DNS configuration)

**Privacy Controls** (Recommended for IP Protection):

Add this to your repository as `.streamlit/config.toml`:

```toml
[server]
enableCORS = false
enableXsrfProtection = true

[browser]
gatherUsageStats = false
```

**Environment Variables** (if needed):
- Set in Streamlit Cloud dashboard under "Advanced settings"
- Example: API keys, database credentials

## Step 3: Gating Options for IP Protection

If you want to show the tool but protect your full logic:

### Option A: Demo Mode with Limited Data
Add to `app.py`:

```python
# At the top Const
DEMO_MODE = True
MAX_ROWS_IN_DEMO = 100

# In processing section
if DEMO_MODE and len(df) > MAX_ROWS_IN_DEMO:
    st.warning(f"⚠️ Demo mode: Processing first {MAX_ROWS_IN_DEMO} rows only")
    df = df.head(MAX_ROWS_IN_DEMO)
```

### Option B: Email Gate
Add email collection before processing:

```python
user_email = st.text_input("Enter your email to process leads:")
if not user_email or '@' not in user_email:
    st.stop()
```

### Option C: Password Protection
Simple password gate:

```python
password = st.text_input("Enter access code:", type="password")
if password != "your-secret-password":
    st.error("Invalid access code")
    st.stop()
```

## Step 4: Update Portfolio Links

Once deployed, update your portfolio:

1. **GitHub README**: Add live demo link
```markdown
## Live Demo
Try it out: [Basin Signal Architect](https://basinleon-gtm-signal-architect.streamlit.app)
```

2. **Portfolio Website**: Update the link in `index.html`
```html
<a href="https://basinleon-gtm-signal-architect.streamlit.app" target="_blank" class="btn">
    Try Live Demo →
</a>
```

3. **LinkedIn Bio**: Add to your profile
```
🏗️ Built: Basin Signal Architect (Live Demo: link-in-bio)
```

## Step 5: Monitoring & Maintenance

**View Analytics**:
- Streamlit Cloud dashboard shows usage stats
- Monitor app performance and errors

**Update the App**:
```bash
git add .
git commit -m "Update: [description]"
git push
```
Streamlit Cloud auto-deploys on push to main branch.

**Troubleshooting**:
- Check logs in Streamlit Cloud dashboard
- Verify `requirements.txt` has correct versions
- Test locally first: `streamlit run app.py`

## Optional: Local Development

```bash
cd ~/Documents/GitHub/gtm-signal-architect

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run locally
streamlit run app.py
```

Access at: `http://localhost:8501`

---

**Next Steps**: Once deployed, use this in your outreach:
- LinkedIn comments: "Don't believe me? Upload your lead list here and see what my system finds."
- Portfolio showcases: Live demo proves you're a technical operator
- Sales conversations: Interactive walkthrough instead of static slides
