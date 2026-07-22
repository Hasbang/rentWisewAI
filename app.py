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
            "Total Cash Available Today (NLE)",
            min_value=1000,
            max_value=10000000,
            value=80000,
            step=1000,
            help="How much cash do you have available right now to pay upfront?"
        )
    with col2:
        currency = st.selectbox("Currency", ["NLE", "USD"])

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

    # FIX 3: Clear previous results immediately when a new search starts.
    # This prevents the user from seeing stale results during the new run.
    if "result" in st.session_state:
        del st.session_state["result"]
    if "requirements" in st.session_state:
        del st.session_state["requirements"]

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
        # Package
        requirements = {
            "budget": budget,
            "currency": currency,
            "location": location.strip(),
            "bedrooms": bedrooms,
            "bathrooms": bathrooms,
            "property_type": property_type,
            "notes": notes.strip() or "No additional notes provided.",
        }

        # FIX 2: Multi-stage progress feedback.
        # The user sees exactly what is happening at each stage.
        progress_bar = st.progress(0)
        status_text = st.empty()

        try:
            status_text.info("🔍 Stage 1 of 3 — Loading property listings...")
            progress_bar.progress(15)
            time.sleep(0.5)

            status_text.info("🧠 Stage 2 of 3 — Property Analyst is filtering and ranking properties...")
            progress_bar.progress(40)

            result = run_rentwise_crew(requirements)

            progress_bar.progress(85)
            status_text.info("✍️ Stage 3 of 3 — Rental Advisor is preparing your report...")
            time.sleep(0.5)

            progress_bar.progress(100)
            status_text.empty()
            progress_bar.empty()

            # Store in session state
            st.session_state["result"] = result
            st.session_state["requirements"] = requirements
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
if "result" in st.session_state:
    result = st.session_state["result"]
    requirements = st.session_state["requirements"]

    # FIX 4: Search summary metrics — scannable at a glance
    st.markdown('<div class="section-header">📊 Search Summary</div>',
                unsafe_allow_html=True)

    col_a, col_b, col_c, col_d = st.columns(4)
    col_a.metric("Your Budget", f"{requirements['currency']} {requirements['budget']:,}")
    col_b.metric("Bedrooms", requirements["bedrooms"])
    col_c.metric("Property Type", requirements["property_type"].title())
    col_d.metric("Location", requirements["location"])

    if requirements["notes"] != "No additional notes provided.":
        st.caption(f"📝 Notes: {requirements['notes']}")

    st.divider()

    # FIX 2: Detect no-results scenario and show helpful guidance
    no_results_signals = [
        "no properties",
        "no affordable",
        "no suitable",
        "no available",
        "none of the properties",
        "could not find",
    ]

    result_lower = result.lower()
    no_results = any(signal in result_lower for signal in no_results_signals)

    if no_results:
        # Show a structured no-results message with actionable suggestions
        st.markdown('<div class="section-header">⚠️ No Matching Properties Found</div>',
                    unsafe_allow_html=True)
        st.markdown("""
        <div class="no-results-box">
            <h4>Here's what you can try:</h4>
            <ul>
                <li>💰 <strong>Increase your budget</strong> — some properties require 2 years advance</li>
                <li>📍 <strong>Broaden your location</strong> — try nearby areas like Wilberforce or Congo Cross</li>
                <li>🛏️ <strong>Reduce bedroom count</strong> — fewer bedrooms means lower advance costs</li>
                <li>🏠 <strong>Change property type</strong> — try "any" to see all available types</li>
            </ul>
            <p>The AI's full analysis is below to help you understand why properties were rejected.</p>
        </div>
        """, unsafe_allow_html=True)

    # Always show the full advisory report
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