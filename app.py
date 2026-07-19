import os
import asyncio
import streamlit as st
import re
import datetime
from dotenv import load_dotenv

# Import capstone modules
from security import validate_text, validate_image_file, LOG_FILE
from tools import get_weather, BANGLADESH_SIMULATED_WEATHER
from orchestrator import AgriGuardianOrchestrator
from pdf_generator import generate_report_pdf
from skills.disease_knowledge import DISEASES, list_all_diseases, get_disease_details
from skills.treatment_knowledge import TREATMENTS, get_treatment_recs
from skills.weather_analysis import calculate_disease_risks, generate_weather_farming_advice

# Load environment variables
load_dotenv()

# Streamlit Page Configuration
st.set_page_config(
    page_title="AgriGuardian AI — Smart Crop Health Guard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium Look & Feel (Inter font, Forest Green/Gold palette, Glassmorphism, Micro-animations)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Header Gradient & Banner */
    .banner-container {
        background: linear-gradient(135deg, #113025 0%, #1B4D3E 50%, #2A6855 100%);
        padding: 2.5rem;
        border-radius: 16px;
        box-shadow: 0 8px 32px rgba(27, 77, 62, 0.15);
        color: white;
        margin-bottom: 2rem;
        border: 1px solid rgba(197, 160, 89, 0.2);
        position: relative;
        overflow: hidden;
    }
    .banner-container::after {
        content: '';
        position: absolute;
        top: 0; right: 0; width: 300px; height: 300px;
        background: radial-gradient(circle, rgba(197,160,89,0.1) 0%, transparent 70%);
        border-radius: 50%;
    }
    .banner-title {
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
        font-size: 2.5rem;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .banner-subtitle {
        font-size: 1.1rem;
        opacity: 0.9;
        margin-top: 0.5rem;
        font-weight: 300;
    }
    
    /* Sleek Cards */
    .card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        border: 1px solid #E2E8F0;
        margin-bottom: 1rem;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
    }
    
    .card-title {
        color: #1B4D3E;
        font-family: 'Outfit', sans-serif;
        font-weight: 600;
        font-size: 1.25rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        border-bottom: 1.5px solid #F4F6F4;
        padding-bottom: 0.5rem;
    }
    
    /* Styled Badges */
    .badge {
        display: inline-block;
        padding: 0.25rem 0.6rem;
        font-size: 0.75rem;
        font-weight: 600;
        border-radius: 50px;
        margin-right: 0.5rem;
    }
    .badge-primary { background-color: #E2ECE9; color: #1B4D3E; border: 1px solid #1B4D3E; }
    .badge-warning { background-color: #FEF3C7; color: #D97706; border: 1px solid #F59E0B; }
    .badge-danger { background-color: #FEE2E2; color: #DC2626; border: 1px solid #EF4444; }
    .badge-success { background-color: #DCFCE7; color: #15803D; border: 1px solid #22C55E; }
    
    /* Custom Sidebar Header */
    .sidebar-header {
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
        color: #1B4D3E;
        font-size: 1.4rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# App Title & Subtitle Banner
st.markdown("""
<div class="banner-container">
    <div class="banner-title">🛡️ AgriGuardian AI</div>
    <div class="banner-subtitle">Secure Multi-Agent Decision Orchestration for Bangladeshi Farmers & Extension Workers</div>
</div>
""", unsafe_allow_html=True)

# ----------------- SESSION STATE & INITIALIZATION -----------------
if "orchestrator" not in st.session_state:
    st.session_state.orchestrator = AgriGuardianOrchestrator(demo_mode=False)

if "api_key_valid" not in st.session_state:
    # Check environment variable
    st.session_state.api_key_valid = "GEMINI_API_KEY" in os.environ and os.environ["GEMINI_API_KEY"] != "DUMMY_KEY"

# ----------------- SIDEBAR CONFIGURATION -----------------
with st.sidebar:
    st.markdown('<div class="sidebar-header">🛡️ AgriGuardian Panel</div>', unsafe_allow_html=True)
    
    st.write("Config and calibrate the guardrails and agent orchestration settings below:")
    st.markdown("---")
    
    # API Settings & Modes
    st.subheader("⚙️ System Configuration")
    
    # Override Mode
    mode_option = st.radio(
        "Execution Engine",
        ["Demo Simulation", "Live AI Agents (Gemini 2.5)"],
        index=0 if not st.session_state.api_key_valid else 1,
        help="Demo mode simulates the multi-agent system using the localized knowledge database and BARC rule engines. Live mode accesses Google Gemini models."
    )
    
    st.session_state.orchestrator.demo_mode = (mode_option == "Demo Simulation")
    
    # Custom API Key Option
    custom_key = st.text_input(
        "Gemini API Key (Optional Override)",
        type="password",
        help="Input a custom Gemini API key to run in live agentic mode. If empty, the system checks the environment variable."
    )
    
    if custom_key:
        os.environ["GEMINI_API_KEY"] = custom_key
        st.session_state.api_key_valid = True
        st.session_state.orchestrator.api_key_valid = True
    else:
        # Check original Env
        st.session_state.api_key_valid = "GEMINI_API_KEY" in os.environ and os.environ["GEMINI_API_KEY"] != "DUMMY_KEY"
        st.session_state.orchestrator.api_key_valid = st.session_state.api_key_valid

    # Status indicators
    st.markdown("---")
    st.subheader("🛡️ System Guardrail Status")
    
    status_color = "green" if st.session_state.api_key_valid or st.session_state.orchestrator.demo_mode else "orange"
    status_text = "Simulated Fallback Mode" if st.session_state.orchestrator.demo_mode else "Live Agentic Active"
    
    st.markdown(f"**Orchestrator Mode:** :{status_color}[{status_text}]")
    st.markdown("**Guardrail Level:** :green[High (Strict Input Validation)]")
    st.markdown("**Weather Engine:** :green[BARC & OpenWeather API]")
    st.markdown("**Approved Chemicals:** :green[Bangladesh BARC 2026]")
    
    st.markdown("---")
    st.info("💡 **Tip:** Try typing keywords like 'potato late blight' or 'rice blast' in the symptom box to see the high-fidelity demo database match correctly.")

# ----------------- TABS SETUP -----------------
tab1, tab2, tab3, tab4 = st.tabs([
    "🔍 Crop Diagnostics", 
    "📚 Disease Library", 
    "🌦️ Weather Analytics", 
    "🛡️ Security Logs"
])

# ----------------- TAB 1: CROP DIAGNOSTICS -----------------
with tab1:
    st.subheader("Run Agentic Diagnostic Workflow")
    
    col_input, col_info = st.columns([2, 1])
    
    with col_input:
        st.markdown('<div class="card"><div class="card-title">📝 Field Data Input</div>', unsafe_allow_html=True)
        
        # Location Selection
        district_list = list(BANGLADESH_SIMULATED_WEATHER.keys())
        district_list = [d.capitalize() for d in district_list] + ["Other (Bangladesh Custom)"]
        
        selected_district = st.selectbox(
            "Select District (Bangladesh Location)",
            district_list,
            index=0
        )
        
        # User input description
        text_desc = st.text_area(
            "Describe the observed crop symptoms in detail:",
            value="",
            max_chars=500,
            height=120,
            placeholder="e.g. My potato plants are showing dark brown spots on the leaves with light green borders. Some leaves have white fuzzy growth on the underside."
        )
        
        # Image Upload
        uploaded_image = st.file_uploader(
            "Upload crop leaf symptom image (Optional - JPG, JPEG, PNG only)",
            type=["jpg", "jpeg", "png"]
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Submit Button
        btn_run = st.button("🚀 Analyze Crop & Generate Report")

    with col_info:
        st.markdown('<div class="card"><div class="card-title">🔬 Diagnostic Scope</div>', unsafe_allow_html=True)
        st.markdown("""
        **AgriGuardian AI** operates as a coordinate chain of five distinct specialist agents:
        1. 🔍 **Disease Detector:** Extracts symptoms and crop names.
        2. 🩺 **Diagnosis Agent:** References pathogen profiles and provides diagnoses.
        3. 💊 **Treatment Agent:** Designs organic, bio, and BARC-approved chemical recommendations.
        4. ☀️ **Weather Advisor:** Correlates local climate forecasts with disease propagation dynamics.
        5. 📋 **Report Compiler:** Packages the information into a professional downloadable document.
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        if uploaded_image:
            st.image(uploaded_image, caption="Uploaded Leaf Specimen", width="stretch")

    # Execution Phase
    if btn_run:
        if not text_desc.strip():
            st.error("⚠️ Please provide a text description of the crop symptoms.")
        else:
            with st.spinner("Initiating Guardrail Verification and Agent Workflow..."):
                # Setup logs/progress area
                log_placeholder = st.empty()
                progress_bar = st.progress(0)
                
                # Check text guardrails locally first for immediate UI response
                is_safe, text_err = validate_text(text_desc)
                if not is_safe:
                    st.error(f"🛡️ **Security Rejection:** {text_err}")
                    progress_bar.empty()
                else:
                    # Save uploaded image file temporarily if provided
                    temp_img_path = None
                    if uploaded_image:
                        # Validate image metadata
                        is_img_safe, img_err = validate_image_file(uploaded_image.name)
                        if not is_img_safe:
                            st.error(f"🛡️ **Security Rejection (Image):** {img_err}")
                            st.stop()
                        
                        temp_img_path = uploaded_image.name
                        # Write the uploaded file bytes to disk so validator/orchestrator can access it
                        with open(temp_img_path, "wb") as f:
                            f.write(uploaded_image.getbuffer())
                            
                    # Run the async orchestrator workflow
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    try:
                        # Call orchestrator
                        location_val = selected_district
                        result = loop.run_until_complete(
                            st.session_state.orchestrator.run_workflow(
                                location=location_val,
                                text_description=text_desc,
                                image_name=temp_img_path
                            )
                        )
                        
                        # Clean up temp image
                        if temp_img_path and os.path.exists(temp_img_path):
                            os.remove(temp_img_path)
                            
                        if not result.get("success"):
                            st.error(f"❌ Workflow Rejected: {result.get('error')}")
                            # Show security logs if any
                            with st.expander("🛡️ Security Violation Details"):
                                for l in result.get("logs", []):
                                    st.write(l)
                        else:
                            progress_bar.progress(100)
                            st.success("✅ AgriGuardian Diagnostics Complete!")
                            
                            # Render Agent Execution logs beautifully
                            with st.expander("🔗 Click to view Multi-Agent Trace & Handoff Logs", expanded=True):
                                for log in result.get("logs", []):
                                    st.markdown(f"{log}")
                                    
                            # Main Result Display
                            st.markdown("### 📋 Final Health & Treatment Dossier")
                            
                            # Compute HTML presentation strings to avoid backslashes inside f-string expressions in Python < 3.12
                            det_html = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', result['detector_output']).replace("\n", "<br/>")
                            wea_html = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', result['weather_output']).replace("\n", "<br/>")
                            diag_html = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', result['diagnosis_output']).replace("\n", "<br/>")

                            col_res1, col_res2 = st.columns([1, 1])

                            with col_res1:
                                # Symptom card
                                st.markdown(f"""
                                <div class="card">
                                    <div class="card-title">🔍 Crop Profile & Symptoms</div>
                                    {det_html}
                                </div>
                                """, unsafe_allow_html=True)
                                
                                # Weather advisories card
                                st.markdown(f"""
                                <div class="card">
                                    <div class="card-title">🌦️ Local Weather & Outbreak Risks</div>
                                    {wea_html}
                                </div>
                                """, unsafe_allow_html=True)
                                
                            with col_res2:
                                # Diagnosis Card
                                st.markdown(f"""
                                <div class="card">
                                    <div class="card-title">🩺 Clinical Diagnosis</div>
                                    {diag_html}
                                </div>
                                """, unsafe_allow_html=True)
                                
                                # Safety checklist
                                st.markdown(f"""
                                <div class="card">
                                    <div class="card-title">🛡️ Farmer Safety Guidelines</div>
                                    <b>Strict Application Protocols:</b><br/>
                                    - Wear protective face masks and rubber gloves.<br/>
                                    - Do not spray chemicals against the wind direction.<br/>
                                    - Keep a 14-day Pre-Harvest Interval (PHI).<br/>
                                    - Dispose of chemical containers away from cattle and fish ponds.
                                </div>
                                """, unsafe_allow_html=True)
                                
                            # Treatments in full width
                            st.markdown("### 💊 Tiered Management Plan")
                            treatment_lines = result['treatment_output'].split("\n\n")
                            t_cols = st.columns(len(treatment_lines))
                            for idx, t_section in enumerate(treatment_lines):
                                if t_section.strip():
                                    t_sec_html = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', t_section).replace("\n", "<br/>")
                                    with t_cols[min(idx, len(t_cols)-1)]:
                                        st.markdown(f"""
                                        <div class="card" style="height: 100%;">
                                            {t_sec_html}
                                        </div>
                                        """, unsafe_allow_html=True)
                                        
                            # Add locations to result for PDF generation
                            result["location"] = selected_district
                            
                            # PDF Generation
                            pdf_bytes = generate_report_pdf(result)
                            
                            st.markdown("---")
                            st.subheader("📥 Export Agricultural Report")
                            st.download_button(
                                label="💾 Download PDF Health Report",
                                data=pdf_bytes,
                                file_name=f"AgriGuardian_Report_{selected_district.replace(' ', '_')}.pdf",
                                mime="application/pdf"
                            )
                            
                    except Exception as ex:
                        st.error(f"System Error running workflow: {ex}")
                        progress_bar.empty()

# ----------------- TAB 2: DISEASE LIBRARY -----------------
with tab2:
    st.subheader("Bangladesh Crop Disease Knowledge Database")
    st.write("Browse details of primary agricultural threats in Bangladesh:")
    
    search_q = st.text_input("🔍 Search disease profiles by keyword (e.g. Rice, late blight):")
    
    for key, info in DISEASES.items():
        # Match keyword
        if (not search_q) or (search_q.lower() in info["name"].lower() or 
                              search_q.lower() in info["crop"].lower() or
                              search_q.lower() in info["scientific_name"].lower()):
            
            with st.expander(f"🌿 {info['crop']} — {info['name']} ({info['scientific_name']})", expanded=True):
                col_info1, col_info2 = st.columns([1, 1])
                
                with col_info1:
                    st.write(f"**Pathogen Type:** {info['pathogen_type']}")
                    st.write(f"**Environmental Conditions:** {info['environmental_factors']}")
                    st.write("**Observed Symptoms:**")
                    for sym in info["symptoms"]:
                        st.write(f"- {sym}")
                        
                with col_info2:
                    trecs = get_treatment_recs(key)
                    if trecs:
                        st.write("**Organic Protocols:**")
                        for org in trecs["organic"]:
                            st.write(f"- {org}")
                        st.write("**Biological Controls:**")
                        for bio in trecs["biological"]:
                            st.write(f"- {bio}")
                        st.write("**BARC Chemical Options:**")
                        for chem in trecs["chemical"]:
                            st.write(f"- {chem}")
                        st.write(f"⚠️ *Safety:* {trecs['safety_notes']}")

# ----------------- TAB 3: WEATHER ANALYTICS -----------------
with tab3:
    st.subheader("Climate & Disease Outbreak Risk Calculator")
    st.write("Calculate dynamic outbreak propagation risk indices based on local weather conditions:")
    
    col_w1, col_w2 = st.columns([1, 2])
    
    with col_w1:
        st.markdown('<div class="card"><div class="card-title">🌦️ Custom Climate Input</div>', unsafe_allow_html=True)
        # We can enter custom temperature and humidity or load from a district profile
        preset = st.selectbox("Load Weather Profile Preset:", ["Custom"] + list(BANGLADESH_SIMULATED_WEATHER.keys()))
        
        if preset != "Custom":
            default_t = BANGLADESH_SIMULATED_WEATHER[preset]["temp"]
            default_h = BANGLADESH_SIMULATED_WEATHER[preset]["humidity"]
            default_r = BANGLADESH_SIMULATED_WEATHER[preset]["rain_prob"]
        else:
            default_t = 28.0
            default_h = 75.0
            default_r = 30.0
            
        custom_t = st.slider("Temperature (°C):", 5.0, 45.0, default_t, 0.5)
        custom_h = st.slider("Relative Humidity (%):", 10.0, 100.0, default_h, 1.0)
        custom_r = st.slider("Rain Probability (%):", 0.0, 100.0, default_r, 5.0)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_w2:
        # Calculate Risk and Advisories
        risks = calculate_disease_risks(custom_t, custom_h)
        advisories = generate_weather_farming_advice(custom_t, custom_h, custom_r)
        
        st.markdown('<div class="card"><div class="card-title">📊 Calculated Outbreak Propagation Risk Indices</div>', unsafe_allow_html=True)
        
        cols_risk = st.columns(len(risks))
        for idx, (disease_key, risk_level) in enumerate(risks.items()):
            disease_name = DISEASES.get(disease_key, {}).get("name", disease_key.replace("_", " ").title())
            with cols_risk[idx]:
                if risk_level == "High":
                    badge_html = '<span class="badge badge-danger">High Risk</span>'
                elif risk_level == "Medium":
                    badge_html = '<span class="badge badge-warning">Medium Risk</span>'
                else:
                    badge_html = '<span class="badge badge-success">Low Risk</span>'
                    
                st.markdown(f"**{disease_name}**<br/>{badge_html}", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Display Advisories
        st.markdown('<div class="card"><div class="card-title">🚜 Local Farming Advisories</div>', unsafe_allow_html=True)
        for adv in advisories:
            st.write(f"- {adv}")
        st.markdown('</div>', unsafe_allow_html=True)

# ----------------- TAB 4: SECURITY CENTER -----------------
with tab4:
    st.subheader("🛡️ Input Security Guardrail & Sandbox")
    st.write("AgriGuardian AI applies active input filters to prevent prompt injection and hazardous query profiles:")
    
    col_sec1, col_sec2 = st.columns([1, 1])
    
    with col_sec1:
        st.markdown('<div class="card"><div class="card-title">🧪 Guardrail Sandbox</div>', unsafe_allow_html=True)
        st.write("Test the input filter manually by entering test strings below:")
        
        test_input = st.text_input("Enter test query (e.g. try typing 'anthrax' or 'ignore prior instructions'):")
        
        if test_input:
            is_valid, err_msg = validate_text(test_input)
            if is_valid:
                st.success("✅ Input passed security check.")
            else:
                st.error(f"❌ Input Rejected: {err_msg}")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_sec2:
        st.markdown('<div class="card"><div class="card-title">📜 Security Violation Log (Live Tail)</div>', unsafe_allow_html=True)
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                log_lines = f.readlines()
            
            if log_lines:
                # Show last 15 lines
                tail_lines = log_lines[-15:]
                st.code("".join(tail_lines), language="text")
            else:
                st.info("No security violations logged yet.")
        else:
            st.info("Log file is empty or has not been created yet.")
        st.markdown('</div>', unsafe_allow_html=True)
