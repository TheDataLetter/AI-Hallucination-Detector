# BUSINESS DASHBOARD: How we show these results to non-technical stakeholders
#
# Not everyone understands code, but everyone understands charts.
#
# This dashboard translates our technical validation into visual insights that executives can use.
#
# This is the contextual audit layer from the article.

import streamlit as st
import pandas as pd
import plotly.express as px

# Set up the page so it looks professional
st.set_page_config(
    page_title="AI Validation Dashboard",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 AI Validation Dashboard")
st.markdown("*Contextual auditing for AI-generated business insights*")

st.info("""
**How to use this dashboard:**
Compare the AI's predictions against actual historical data.
Look for patterns that don't make business sense.
""")

# Load the real historical data
st.header("📈 Actual Revenue Trends")
st.caption("This is our ground truth - what actually happened")

actuals_df = pd.read_csv("data/sales-data.csv")
actuals_df['date'] = pd.to_datetime(actuals_df['date'])

# Create a simple revenue chart
fig = px.line(
    actuals_df,
    x='date',
    y='revenue',
    title='Monthly Revenue (Actuals)',
    labels={'revenue': 'Revenue ($)', 'date': 'Month'}
)

# Add some business context markers
fig.add_vrect(
    x0="2021-11-01", x1="2021-12-31",
    fillcolor="green", opacity=0.1,
    line_width=0,
    annotation_text="Holiday Season", annotation_position="top left"
)

fig.add_vrect(
    x0="2022-11-01", x1="2022-12-31",
    fillcolor="green", opacity=0.1,
    line_width=0
)

fig.add_vrect(
    x0="2023-11-01", x1="2023-12-31",
    fillcolor="green", opacity=0.1,
    line_width=0
)

st.plotly_chart(fig, width='stretch')

# Show the AI's segment claims
st.header("🧠 AI's Segment Analysis")
st.caption("These are the segments the AI reported on")

ai_reports_df = pd.read_csv("data/ai_reports.csv")
st.dataframe(ai_reports_df, width='stretch')

# Add some validation insights
st.header("🔍 Validation Insights")

col1, col2 = st.columns(2)

with col1:
    st.subheader("What We Checked")
    st.markdown("""
    - ✅ **Mathematical consistency**: Do the numbers add up?
    - ✅ **Segment existence**: Do these segments actually exist?
    - ✅ **Historical patterns**: Does this make sense given past trends?
    - ✅ **Business context**: Are there external factors we're missing?
    """)

with col2:
    st.subheader("Common Hallucination Patterns")
    st.markdown("""
    - ❌ **Invented segments**: 'European sales' when no Europe operations
    - ❌ **Impossible growth**: 200% growth in stable markets
    - ❌ **Seasonal blindness**: Missing holiday spikes or summer dips
    - ❌ **Context ignorance**: Not accounting for supply chain issues
    """)
    
st.warning("""
**Remember:** This dashboard is your last line of defense. 
The automated checks catch obvious errors, but you're looking for patterns
that only make sense if you understand the business.
""")
