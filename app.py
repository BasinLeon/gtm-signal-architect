"""
Basin Signal Architect
A GTM Operating System for Technical Founders

This tool processes raw lead lists through the Basin Priority Logic:
1. Friction Filter - Identifies high-intent signals
2. DNA Analysis - Matches founder backgrounds
3. Script Generation - Creates engineer-to-engineer outreach
"""

import streamlit as st
import pandas as pd
import io
from datetime import datetime

# Configure page
st.set_page_config(
    page_title="Basin Signal Architect",
    page_icon="🏗️",
    layout="wide"
)

# Custom CSS for terminal aesthetic
st.markdown("""
<style>
    .main {
        background-color: #0a0a0a;
        color: #00ff00;
    }
    .stButton>button {
        background-color: #1a1a1a;
        color: #00ff00;
        border: 1px solid #00ff00;
        font-family: monospace;
    }
    .metric-card {
        background-color: #111;
        padding: 20px;
        border-radius: 5px;
        border: 1px solid #333;
    }
</style>
""", unsafe_allow_html=True)

def analyze_friction(row):
    """
    Friction Filter: Identifies companies actively hiring for Sales/GTM roles.
    High friction = High intent to build sales infrastructure.
    """
    score = 0
    signals = []
    
    # Check for sales hiring keywords in job descriptions/company info
    hiring_keywords = ['sales', 'account executive', 'ae ', 'sdr', 'bdr', 'business development', 'revenue']
    
    # Analyze available fields (adjust based on your CSV structure)
    row_text = ' '.join([str(val).lower() for val in row.values if pd.notna(val)])
    
    for keyword in hiring_keywords:
        if keyword in row_text:
            score += 1
            signals.append(f"Hiring for {keyword}")
    
    return score, signals

def analyze_dna(row):
    """
    DNA Analysis: Matches founder/leadership backgrounds.
    Technical/Security background = Higher alignment with "engineer-to-engineer" approach.
    """
    dna_type = "Unknown"
    confidence = 0
    
    row_text = ' '.join([str(val).lower() for val in row.values if pd.notna(val)])
    
    # Technical DNA indicators
    tech_keywords = ['engineer', 'cto', 'vp engineering', 'developer', 'technical founder', 'phd', 'security', 'infosec']
    tech_score = sum(1 for keyword in tech_keywords if keyword in row_text)
    
    # Sales DNA indicators
    sales_keywords = ['vp sales', 'cro', 'chief revenue', 'sales leader', 'head of sales']
    sales_score = sum(1 for keyword in sales_keywords if keyword in row_text)
    
    if tech_score > sales_score:
        dna_type = "Technical DNA"
        confidence = min(tech_score * 20, 100)
    elif sales_score > tech_score:
        dna_type = "Sales DNA"
        confidence = min(sales_score * 20, 100)
    else:
        dna_type = "Mixed DNA"
        confidence = 50
    
    return dna_type, confidence

def calculate_priority(friction_score, dna_type, dna_confidence):
    """
    Basin Priority Logic: Combines friction and DNA signals.
    Priority tiers: P0 (Highest), P1, P2, P3 (Lowest)
    """
    if friction_score >= 3 and dna_type == "Technical DNA" and dna_confidence >= 60:
        return "P0"
    elif friction_score >= 2 and dna_type == "Technical DNA":
        return "P1"
    elif friction_score >= 2 or dna_type == "Technical DNA":
        return "P2"
    else:
        return "P3"

def generate_outreach_script(row, priority, dna_type):
    """
    Script Generation: Creates personalized outreach based on signals.
    Engineer-to-engineer approach for Technical DNA.
    """
    company_name = row.get('Company', row.get('company', 'the company'))
    contact_name = row.get('Name', row.get('name', row.get('Contact Name', 'there')))
    
    if dna_type == "Technical DNA":
        subject = f"Re: {company_name}'s GTM Architecture"
        email_body = f"""Hi {contact_name},

I noticed {company_name} is scaling the sales team. Most technical founders hire the Rolodex before building the road—you end up with high activity, low signal.

I built a different approach: GTM as an operating system. Signal prioritization, not spray-and-pray.

Would you be open to a 15-minute technical walkthrough of how we deploy this for seed/Series A teams?

Best,
Leon Basin
Architecture > Activity"""

        linkedin_msg = f"""Hi {contact_name} - saw {company_name} is hiring for sales. Built a signal-based GTM system for technical founders. Worth a quick sync?"""
    
    else:
        subject = f"GTM System for {company_name}"
        email_body = f"""Hi {contact_name},

I help technical founders operationalize GTM before scaling headcount.

Instead of building a team first, we build the architecture: lead scoring, signal detection, and systematic outreach.

Open to exploring this for {company_name}?

Best,
Leon"""

        linkedin_msg = f"""Hi {contact_name} - helping technical founders systematize GTM. Worth exploring for {company_name}?"""
    
    return subject, email_body, linkedin_msg

# Main App
st.title("🏗️ Basin Signal Architect")
st.markdown("### Rule-based signal review for GTM teams")
st.markdown("---")

# Instructions
with st.expander("📋 How to Use"):
    st.markdown("""
    1. **Export** your lead list from Apollo/Clay as CSV
    2. **Upload** the CSV below
    3. **Review** the signal analysis and priority assignments
    4. **Export** the processed `Basin_Attack_List.csv`
    
    **Expected CSV Columns**: Company, Name, Title, Description, or similar fields containing company/contact data.
    """)

# File upload
uploaded_file = st.file_uploader("Upload Lead List (CSV)", type=['csv'])

if uploaded_file is not None:
    # Load data
    df = pd.read_csv(uploaded_file)
    st.success(f"✅ Loaded {len(df)} leads")
    
    # Process leads
    with st.spinner("🔍 Analyzing signals..."):
        results = []
        
        for idx, row in df.iterrows():
            # Run analysis
            friction_score, friction_signals = analyze_friction(row)
            dna_type, dna_confidence = analyze_dna(row)
            priority = calculate_priority(friction_score, dna_type, dna_confidence)
            subject, email_body, linkedin_msg = generate_outreach_script(row, priority, dna_type)
            
            # Compile results
            result = row.to_dict()
            result['Friction_Score'] = friction_score
            result['Friction_Signals'] = ' | '.join(friction_signals) if friction_signals else 'None'
            result['Company_DNA'] = dna_type
            result['DNA_Confidence'] = dna_confidence
            result['Basin_Priority'] = priority
            result['Email_Subject'] = subject
            result['Email_Body'] = email_body
            result['LinkedIn_Message'] = linkedin_msg
            
            results.append(result)
        
        results_df = pd.DataFrame(results)
    
    # Display metrics
    st.markdown("### 📊 Signal Analysis")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Leads", len(results_df))
    with col2:
        p0_count = len(results_df[results_df['Basin_Priority'] == 'P0'])
        st.metric("P0 Priority", p0_count)
    with col3:
        tech_dna_count = len(results_df[results_df['Company_DNA'] == 'Technical DNA'])
        st.metric("Technical DNA", tech_dna_count)
    with col4:
        high_friction = len(results_df[results_df['Friction_Score'] >= 2])
        st.metric("High Friction", high_friction)
    
    # Priority distribution
    st.markdown("### 🎯 Priority Distribution")
    priority_dist = results_df['Basin_Priority'].value_counts()
    st.bar_chart(priority_dist)
    
    # Sample results
    st.markdown("### 🔬 Sample Results (Top 10 by Priority)")
    display_cols = ['Basin_Priority', 'Company_DNA', 'Friction_Score', 'Email_Subject']
    # Add any original columns that exist
    for col in ['Company', 'Name', 'Title']:
        if col in results_df.columns:
            display_cols.insert(0, col)
    
    st.dataframe(results_df[display_cols].head(10))
    
    # Export
    st.markdown("### 💾 Export Attack List")
    
    # Filter options
    col1, col2 = st.columns(2)
    with col1:
        priority_filter = st.multiselect(
            "Filter by Priority",
            options=['P0', 'P1', 'P2', 'P3'],
            default=['P0', 'P1']
        )
    with col2:
        min_friction = st.slider("Minimum Friction Score", 0, 10, 1)
    
    filtered_df = results_df[
        (results_df['Basin_Priority'].isin(priority_filter)) &
        (results_df['Friction_Score'] >= min_friction)
    ]
    
    st.info(f"📤 Exporting {len(filtered_df)} leads matching criteria")
    
    # Download button
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="⬇️ Download Basin_Attack_List.csv",
        data=csv,
        file_name=f"Basin_Attack_List_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

else:
    st.info("👆 Upload a CSV to begin signal analysis")
    
    # Demo section
    st.markdown("### 🎬 Demo")
    st.markdown("""
    Try `examples/synthetic-leads.csv` from this repository.

    Its three fictional companies produce P0, P2, and P3 tiers using the visible keyword rules.
    Review the checked-in `examples/synthetic-results.csv` alongside the app.

    Scores are heuristics, not verified buying intent. No response-rate or time-savings result is claimed for this demo.
    """)

# Footer
st.markdown("---")
st.markdown("*Built by Leon Basin • Architecture > Activity*")
