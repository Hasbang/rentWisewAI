# app.py

import time
import streamlit as st
from crew.rentwise_crew import run_rentwise_crew

# ── PAGE CONFIGURATION ───────────────────────────────────────────
st.set_page_config(
    page_title="RentWise AI",
    page_icon="🏠",
    layout="wide",
)

# ── CUSTOM STYLES ────────────────────────────────────────────────
st.markdown("""
    <style>
        .main-title {
            font-size: 2.5rem;
            font-weight: 700;
            color: #1a1a2e;
        }
        .subtitle {
            font-size: 1.1rem;
            color: #555;
            margin-bottom: 2rem;
        }
        .section-header {
            font-size: 1.3rem;
            font-weight: 600;
            color: #1a1a2e;
            margin-top: 2rem;
            margin-bottom: 1rem;
            border-bottom: 2px solid #e0e0e0;
            padding-bottom: 0.5rem;
        }
        .property-card {
            background-color: #f8f9fa;
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            border-left: 5px solid #4CAF50;
        }
        .risk-card {
            background-color: #fff8e1;
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            border-left: 5px solid #FF9800;
        }
        .advisory-box {
            background-color: #f0f4ff;
            border-radius: 12px;
            padding: 2rem;
            margin-top: 1rem;
            border: 1px solid #c5d0f5;
        }
        .no-results-box {
            background-color: #fff3e0;
            border-radius: 12px;
            padding: 2rem;
            margin-top: 1rem;
            border-left: 5px solid #FF9800;
        }
        .footer {
            text-align: center;
            color: #aaa;
            font-size: 0.85rem;
            margin-top: 4rem;
            padding-top: 1rem;
            border-top: 1px solid #eee;
        }
    </style>
""", unsafe_allow_html=True)


# ── HEADER ───────────────────────────────────────────────────────
st.markdown('<div class="main-title">🏠 RentWise AI</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">AI-powered rental decision support for Freetown, Sierra Leone. '
    'Enter your requirements below and let our AI agents find your best options.</div>',
    unsafe_allow_html=True
)


# ── INPUT FORM ───────────────────────────────────────────────────
with st.form("search_form"):
    st.markdown('<div class="section-header">Your Requirements</div>',
                unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    with col1:
        budget = st.number_input(
    "Cash Budgeted for Housing (NLE)",
    min_value=1000,
    max_value=10000000,
    value=80000,
    step=1000,
    help="Enter the amount you have set aside specifically for advance rent and moving costs — not your total savings."
)
    with col2:
        # Currency selector kept as NLE only until conversion is built
        st.selectbox("Currency", ["NLE"])

    col3, col4 = st.columns(2)
    with col3:
        location = st.text_input(
            "Preferred Location",
            placeholder="e.g. Hill Station, Wilberforce, Lumley",
        )
    with col4:
        property_type = st.selectbox(
            "Property Type",
            ["apartment", "house", "bungalow", "studio", "any"]
        )

    col5, col6 = st.columns(2)
    with col5:
        bedrooms = st.selectbox("Bedrooms Needed", [1, 2, 3, 4, 5])
    with col6:
        bathrooms = st.selectbox("Bathrooms Needed", [1, 2, 3])

    notes = st.text_area(
        "Additional Notes or Preferences",
        placeholder="e.g. I want somewhere quiet with parking. I work at Hill Station.",
        height=100,
    )

    submitted = st.form_submit_button(
        "🔍 Find My Best Properties",
        use_container_width=True,
    )


# ── VALIDATION & CREW EXECUTION ──────────────────────────────────
if submitted:

    # Clear all previous results when a new search starts
    for key in ["result", "requirements", "filter_results"]:
        if key in st.session_state:
            del st.session_state[key]

    # Validate
    errors = []
    if not location.strip():
        errors.append("Please enter a preferred location.")
    if budget < 5000:
        errors.append("Budget seems too low. Please check your amount.")

    if errors:
        for error in errors:
            st.error(error)

    else:
        # Package requirements
        requirements = {
            "budget": budget,
            "location": location.strip(),
            "bedrooms": bedrooms,
            "bathrooms": bathrooms,
            "property_type": property_type,
            "notes": notes.strip() or "No additional notes provided.",
        }

        # Multi-stage progress feedback
        progress_bar = st.progress(0)
        status_text = st.empty()

        try:
            status_text.info("🔍 Stage 1 of 3 — Loading property listings from database...")
            progress_bar.progress(15)
            time.sleep(0.5)

            status_text.info("🧠 Stage 2 of 3 — Python is filtering and ranking properties...")
            progress_bar.progress(40)

            result_data = run_rentwise_crew(requirements)

            progress_bar.progress(85)
            status_text.info("✍️ Stage 3 of 3 — Rental Advisor is preparing your report...")
            time.sleep(0.5)

            progress_bar.progress(100)
            status_text.empty()
            progress_bar.empty()

            # Store all results in session state
            st.session_state["result"] = result_data["result"]
            st.session_state["requirements"] = requirements
            st.session_state["filter_results"] = result_data["filter_results"]
            st.success("✅ Analysis complete! Your report is ready below.")

        except Exception as e:
            progress_bar.empty()
            status_text.empty()
            st.error(
                "Something went wrong while running the analysis. "
                "Please check your internet connection and try again."
            )
            st.exception(e)


# ── RESULTS DISPLAY ──────────────────────────────────────────────
if "result" in st.session_state and "filter_results" in st.session_state:
    result = st.session_state["result"]
    requirements = st.session_state["requirements"]
    filter_results = st.session_state["filter_results"]

    shortlist = filter_results["shortlist"]
    rejected = filter_results["rejected"]

    # Search summary metrics
    st.markdown('<div class="section-header">📊 Search Summary</div>',
                unsafe_allow_html=True)

    col_a, col_b, col_c, col_d = st.columns(4)
    col_a.metric("Your Budget", f"NLE {requirements['budget']:,}")
    col_b.metric("Properties Analysed", len(shortlist) + len(rejected))
    col_c.metric("Shortlisted", len(shortlist))
    col_d.metric("Rejected", len(rejected))

    if requirements.get("notes") != "No additional notes provided.":
        st.caption(f"📝 Notes: {requirements['notes']}")

    st.divider()

    # Property cards built from Python data — reliable, not from LLM output
    if shortlist:
        st.markdown('<div class="section-header">🏠 Shortlisted Properties</div>',
                    unsafe_allow_html=True)

        for prop in shortlist:
            risk_label = "⚠️ High Upfront Capital Risk" if prop["highRisk"] else "✅ Financially Safe"
            card_style = "risk-card" if prop["highRisk"] else "property-card"

            st.markdown(f"""
            <div class="{card_style}">
                <h4>{prop['title']}</h4>
                <p>📍 {prop['location']} &nbsp;|&nbsp;
                   🛏 {prop['bedrooms']} bed &nbsp;|&nbsp;
                   🚿 {prop['bathrooms']} bath &nbsp;|&nbsp;
                   🏠 {prop['propertyType'].title()}</p>
                <p>💰 Yearly Rent: <strong>NLE {prop['yearlyRent']:,}</strong>
                   &nbsp;|&nbsp;
                   Move-in Cost: <strong>NLE {prop['moveInCost']:,}</strong></p>
                <p>Remaining Cash: <strong>NLE {prop['remainingCash']:,}</strong>
                   &nbsp;|&nbsp; {risk_label}</p>
                <p>🚗 Parking: {'Yes' if prop['parking'] else 'No'}
                   &nbsp;|&nbsp;
                   🛋 Furnished: {'Yes' if prop['furnished'] else 'No'}
                   &nbsp;|&nbsp;
                   💧 Water: {prop['waterSupply']}
                   &nbsp;|&nbsp;
                   ⚡ Electricity: {prop['electricity']}</p>
            </div>
            """, unsafe_allow_html=True)

    else:
        st.markdown("""
        <div class="no-results-box">
            <h4>⚠️ No matching properties found</h4>
            <ul>
                <li>💰 <strong>Increase your budget</strong> — some properties require 2 years advance</li>
                <li>📍 <strong>Broaden your location</strong> — try nearby areas</li>
                <li>🛏️ <strong>Reduce bedroom count</strong> — fewer bedrooms means lower advance costs</li>
                <li>🏠 <strong>Change property type</strong> — try "any" to see all available types</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # Full AI advisory report
    st.markdown('<div class="section-header">📋 AI Advisory Report</div>',
                unsafe_allow_html=True)
    st.markdown('<div class="advisory-box">', unsafe_allow_html=True)
    st.markdown(result)
    st.markdown('</div>', unsafe_allow_html=True)


# ── FOOTER ───────────────────────────────────────────────────────
st.markdown(
    '<div class="footer">RentWise AI · Built for Freetown, Sierra Leone · '
    'Powered by CrewAI & OpenRouter</div>',
    unsafe_allow_html=True
)