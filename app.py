import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os
import datetime

st.set_page_config(
    page_title="GemVal | Enterprise Diamond Valuation Engine",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Navigation state
if "page" not in st.session_state:
    st.session_state.page = "home"
if "active_nav" not in st.session_state:
    st.session_state.active_nav = None

# Custom styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    .block-container {
        padding-top: 0.6rem !important;
        padding-bottom: 0.5rem !important;
        padding-left: 1.8rem !important;
        padding-right: 1.8rem !important;
        max-width: 100% !important;
    }
    header[data-testid="stHeader"] {
        display: none !important;
    }
    #MainMenu, footer {
        visibility: hidden !important;
    }

    .stApp {
        background: radial-gradient(circle at 15% 10%, #0f172a 0%, #020617 100%);
        color: #f8fafc;
    }

    .luxury-navbar {
        background: rgba(15, 23, 42, 0.75);
        backdrop-filter: blur(24px);
        -webkit-backdrop-filter: blur(24px);
        border: 1px solid rgba(148, 163, 184, 0.15);
        border-radius: 18px;
        padding: 9px 24px;
        margin-bottom: 22px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5), 
                    0 0 20px -5px rgba(56, 189, 248, 0.08);
    }

    .brand-link {
        display: flex;
        align-items: center;
        gap: 12px;
        text-decoration: none !important;
        cursor: pointer;
        transition: transform 0.2s ease;
    }
    .brand-link:hover .logo-svg {
        filter: drop-shadow(0 0 14px rgba(56, 189, 248, 0.8));
        transform: scale(1.05);
    }
    .brand-link:hover .brand-name {
        color: #38bdf8;
    }
    .logo-svg {
        transition: all 0.25s ease;
        filter: drop-shadow(0 0 8px rgba(56, 189, 248, 0.45));
    }
    .brand-text-block {
        display: flex;
        flex-direction: column;
    }
    .brand-name {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.35rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        color: #ffffff;
        display: inline-flex;
        align-items: center;
        gap: 7px;
        transition: color 0.2s ease;
        line-height: 1.1;
    }
    .brand-badge {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 0.65rem;
        font-weight: 800;
        letter-spacing: 0.04em;
        background: linear-gradient(135deg, #38bdf8, #818cf8);
        color: #020617;
        padding: 2px 7px;
        border-radius: 6px;
        text-transform: uppercase;
        vertical-align: middle;
    }
    .brand-subtitle {
        font-size: 0.74rem;
        color: #94a3b8;
        font-weight: 500;
        margin-top: 2px;
        letter-spacing: -0.01em;
    }

    .navbar-right-cluster {
        display: flex;
        align-items: center;
        gap: 32px;
    }

    .nav-links-cluster {
        display: flex;
        align-items: center;
        gap: 28px;
    }
    .nav-item-link {
        font-size: 1.02rem;
        font-weight: 600;
        color: #94a3b8 !important;
        text-decoration: none !important;
        background: transparent !important;
        border: none !important;
        padding: 8px 2px;
        position: relative;
        transition: color 0.2s ease;
        cursor: pointer;
        display: inline-flex;
        align-items: center;
        gap: 8px;
    }
    .nav-item-link:hover {
        color: #38bdf8 !important;
    }
    .nav-item-link.active {
        color: #38bdf8 !important;
        font-weight: 700;
    }
    .nav-item-link.active::after {
        content: '';
        position: absolute;
        bottom: -2px;
        left: 0;
        width: 100%;
        height: 2.5px;
        background: linear-gradient(90deg, #38bdf8, #818cf8);
        border-radius: 2px;
        box-shadow: 0 0 12px rgba(56, 189, 248, 0.8);
    }

    .nav-back-link {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        color: #38bdf8 !important;
        font-size: 0.94rem;
        font-weight: 600;
        text-decoration: none !important;
        margin-bottom: 16px;
        padding: 8px 18px;
        border-radius: 10px;
        background: rgba(56, 189, 248, 0.1);
        border: 1px solid rgba(56, 189, 248, 0.3);
        transition: all 0.2s ease;
    }
    .nav-back-link:hover {
        background: rgba(56, 189, 248, 0.22);
        border-color: rgba(56, 189, 248, 0.6);
        transform: translateX(-3px);
        box-shadow: 0 4px 14px rgba(56, 189, 248, 0.25);
    }

    div[data-testid="stDataFrame"] {
        margin-top: 48px !important;
        margin-bottom: 30px !important;
        position: relative !important;
    }
    div[data-testid="stDataFrame"] div[data-testid="stElementToolbar"] {
        opacity: 1 !important;
        visibility: visible !important;
        display: flex !important;
        pointer-events: auto !important;
        position: absolute !important;
        top: -44px !important;
        right: 0px !important;
        height: 36px !important;
        z-index: 50 !important;
        background: rgba(15, 23, 42, 0.95) !important;
        backdrop-filter: blur(16px) !important;
        -webkit-backdrop-filter: blur(16px) !important;
        border: 1px solid rgba(56, 189, 248, 0.35) !important;
        border-radius: 8px !important;
        padding: 3px 6px !important;
        gap: 4px !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.5) !important;
    }
    div[data-testid="stDataFrame"] div[data-testid="stElementToolbar"] button {
        width: 30px !important;
        height: 30px !important;
        min-width: 30px !important;
        min-height: 30px !important;
        padding: 4px !important;
        margin: 0 !important;
        border-radius: 6px !important;
        background: rgba(30, 41, 59, 0.85) !important;
        border: 1px solid rgba(148, 163, 184, 0.25) !important;
        color: #f8fafc !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
        cursor: pointer !important;
    }
    div[data-testid="stDataFrame"] div[data-testid="stElementToolbar"] button:hover {
        background: rgba(56, 189, 248, 0.25) !important;
        border-color: rgba(56, 189, 248, 0.6) !important;
        color: #38bdf8 !important;
        transform: scale(1.1) !important;
    }
    div[data-testid="stDataFrame"] div[data-testid="stElementToolbar"] button svg {
        width: 17px !important;
        height: 17px !important;
        min-width: 17px !important;
        min-height: 17px !important;
        stroke-width: 2.2 !important;
    }

    div[data-testid="stElementToolbar"]:not(div[data-testid="stDataFrame"] div[data-testid="stElementToolbar"]),
    .vega-embed summary,
    details.vega-embed {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        pointer-events: none !important;
    }

    .section-title {
        margin-top: 8px !important;
        margin-bottom: 10px !important;
    }
    div[data-testid="stCaptionContainer"] {
        margin-bottom: 16px !important;
    }

    @keyframes pulse-glow {
        0% { box-shadow: 0 0 0 0 rgba(74, 222, 128, 0.6); }
        70% { box-shadow: 0 0 0 6px rgba(74, 222, 128, 0); }
        100% { box-shadow: 0 0 0 0 rgba(74, 222, 128, 0); }
    }
    .pulse-dot {
        width: 7px;
        height: 7px;
        background-color: #4ade80;
        border-radius: 50%;
        display: inline-block;
        animation: pulse-glow 2s infinite;
        vertical-align: middle;
        margin-right: 5px;
    }
    .status-capsule {
        background: rgba(34, 197, 94, 0.1);
        color: #4ade80;
        border: 1px solid rgba(34, 197, 94, 0.25);
        padding: 6px 14px;
        border-radius: 9999px;
        font-size: 0.74rem;
        font-weight: 700;
        letter-spacing: 0.02em;
        display: inline-flex;
        align-items: center;
        white-space: nowrap;
    }

    .section-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.05rem;
        font-weight: 700;
        color: #f1f5f9;
        letter-spacing: -0.01em;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .valuation-card {
        background: linear-gradient(145deg, rgba(30, 41, 59, 0.85) 0%, rgba(15, 23, 42, 0.95) 100%);
        border: 1px solid rgba(56, 189, 248, 0.3);
        border-radius: 16px;
        padding: 16px 20px;
        text-align: center;
        box-shadow: 0 12px 28px -10px rgba(56, 189, 248, 0.15);
        position: relative;
    }
    .valuation-label {
        color: #94a3b8;
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-weight: 600;
        margin-bottom: 2px;
    }
    .valuation-price {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2.7rem;
        font-weight: 700;
        color: #38bdf8;
        line-height: 1.05;
        margin-bottom: 4px;
        letter-spacing: -0.02em;
    }
    .valuation-range {
        color: #cbd5e1;
        font-size: 0.85rem;
        font-weight: 500;
        margin-bottom: 8px;
    }

    .badge-tier {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 9999px;
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }
    .badge-tier-luxury {
        background: rgba(192, 132, 252, 0.15);
        color: #c084fc;
        border: 1px solid rgba(192, 132, 252, 0.35);
    }
    .badge-tier-fine {
        background: rgba(56, 189, 248, 0.15);
        color: #38bdf8;
        border: 1px solid rgba(56, 189, 248, 0.35);
    }
    .badge-tier-commercial {
        background: rgba(74, 222, 128, 0.15);
        color: #4ade80;
        border: 1px solid rgba(74, 222, 128, 0.35);
    }

    .kpi-row {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 10px;
        margin-top: 10px;
    }
    .kpi-item {
        background: rgba(30, 41, 59, 0.5);
        border: 1px solid rgba(148, 163, 184, 0.1);
        border-radius: 10px;
        padding: 8px 10px;
        text-align: center;
    }
    .kpi-item-title {
        color: #94a3b8;
        font-size: 0.68rem;
        text-transform: uppercase;
        font-weight: 600;
    }
    .kpi-item-value {
        color: #f8fafc;
        font-size: 0.95rem;
        font-weight: 700;
    }

    div[data-testid="stSlider"] {
        margin-bottom: -10px;
    }
    div[data-testid="stSelectbox"] label, div[data-testid="stSlider"] label {
        font-size: 0.8rem !important;
        font-weight: 600 !important;
        color: #cbd5e1 !important;
    }
</style>
""", unsafe_allow_html=True)

# Load trained model artifact
@st.cache_resource
def load_production_model():
    candidates = [
        "diamond_price_model_hgb.pkl",
        "diamond_price_model_full_dataset.pkl",
        "diamond_price_model_100_instances.pkl"
    ]
    for fn in candidates:
        if os.path.exists(fn):
            with open(fn, "rb") as f:
                model = pickle.load(f)
            return model, fn
    return None, None

model, active_model_file = load_production_model()

# Navbar routing
current_page = st.query_params.get("page", "home")
st.session_state.page = current_page

home_active = "active" if current_page == "home" else ""
bench_active = "active" if current_page == "benchmark" else ""
guide_active = "active" if current_page == "guide" else ""

navbar_html = f"""<div class="luxury-navbar">
<a href="/" target="_self" class="brand-link" title="GemVal Home (Valuation Terminal)">
<svg width="34" height="34" viewBox="0 0 36 36" fill="none" class="logo-svg">
<defs>
<linearGradient id="gemGrad1" x1="0%" y1="0%" x2="100%" y2="100%">
<stop offset="0%" stop-color="#38bdf8"/>
<stop offset="100%" stop-color="#818cf8"/>
</linearGradient>
<linearGradient id="gemGrad2" x1="0%" y1="0%" x2="100%" y2="100%">
<stop offset="0%" stop-color="#818cf8"/>
<stop offset="100%" stop-color="#c084fc"/>
</linearGradient>
<linearGradient id="gemGrad3" x1="0%" y1="0%" x2="100%" y2="100%">
<stop offset="0%" stop-color="#38bdf8"/>
<stop offset="50%" stop-color="#60a5fa"/>
<stop offset="100%" stop-color="#3b82f6"/>
</linearGradient>
</defs>
<polygon points="10,6 26,6 31,14 5,14" fill="url(#gemGrad1)"/>
<polygon points="5,14 18,32 31,14" fill="url(#gemGrad3)"/>
<polygon points="10,6 18,14 5,14" fill="#bae6fd" opacity="0.6"/>
<polygon points="26,6 31,14 18,14" fill="#c7d2fe" opacity="0.6"/>
<polygon points="10,6 26,6 18,14" fill="#f0f9ff" opacity="0.85"/>
<polygon points="18,14 18,32 5,14" fill="#0369a1" opacity="0.4"/>
<polygon points="18,14 31,14 18,32" fill="#4338ca" opacity="0.4"/>
</svg>
<div class="brand-text-block">
<div class="brand-name">
GEMVAL <span class="brand-badge">PRO</span>
</div>
<div class="brand-subtitle">Institutional Diamond Valuation Engine</div>
</div>
</a>
<div class="navbar-right-cluster">
<div class="nav-links-cluster">
<a href="/" target="_self" class="nav-item-link {home_active}">Valuation Terminal</a>
<a href="?page=benchmark" target="_self" class="nav-item-link {bench_active}">Model Benchmark</a>
<a href="?page=guide" target="_self" class="nav-item-link {guide_active}">4Cs Market Guide</a>
</div>
<div class="status-capsule">
<span class="pulse-dot"></span> Engine Online
</div>
</div>
</div>"""

st.markdown(navbar_html, unsafe_allow_html=True)

# Valuation Terminal
if current_page == "home":
    # Preset selection
    col_p_label, col_p_choice = st.columns([1, 4.5])
    with col_p_label:
        st.markdown("<div style='font-size: 0.8rem; font-weight: 700; color: #94a3b8; padding-top: 6px;'>PRESET MARKET TIERS:</div>", unsafe_allow_html=True)
    with col_p_choice:
        preset = st.radio(
            "Presets",
            [
                "0.52 ct • Commercial Daily",
                "1.01 ct • Ideal Solitaire",
                "2.05 ct • High Luxury",
                "Custom Spec"
            ],
            horizontal=True,
            label_visibility="collapsed"
        )

    # Preset values
    if "0.52 ct" in preset:
        init_carat, init_cut, init_color, init_clarity = 0.52, "Very Good", "H", "SI1"
        init_depth, init_table = 62.8, 57.0
        init_x, init_y, init_z = 5.12, 5.15, 3.22
    elif "1.01 ct" in preset:
        init_carat, init_cut, init_color, init_clarity = 1.01, "Ideal", "G", "VS1"
        init_depth, init_table = 61.8, 56.0
        init_x, init_y, init_z = 6.44, 6.41, 3.97
    elif "2.05 ct" in preset:
        init_carat, init_cut, init_color, init_clarity = 2.05, "Premium", "D", "VVS1"
        init_depth, init_table = 62.2, 58.0
        init_x, init_y, init_z = 8.15, 8.11, 5.06
    else:
        init_carat, init_cut, init_color, init_clarity = 1.00, "Ideal", "E", "VS2"
        init_depth, init_table = 61.5, 57.0
        init_x, init_y, init_z = 6.42, 6.45, 3.96

    col_left, col_right = st.columns([1.1, 1], gap="medium")

    # Inputs
    with col_left:
        st.markdown('<div class="section-title"><span>💎</span> Diamond Specifications</div>', unsafe_allow_html=True)
        
        carat = st.slider(
            "Carat Weight (Mass):",
            min_value=0.20,
            max_value=5.00,
            value=float(init_carat),
            step=0.01,
            help="1 Carat = 200 mg. Carat dictates exponential value scaling."
        )

        col_c1, col_c2, col_c3 = st.columns(3)
        with col_c1:
            cuts = ["Fair", "Good", "Very Good", "Premium", "Ideal"]
            cut = st.selectbox("Cut Quality", cuts, index=cuts.index(init_cut))
        with col_c2:
            colors = ["D", "E", "F", "G", "H", "I", "J"]
            color = st.selectbox("Color Grade", colors, index=colors.index(init_color), help="D (Colorless) to J (Warm)")
        with col_c3:
            clarities = ["IF", "VVS1", "VVS2", "VS1", "VS2", "SI1", "SI2", "I1"]
            clarity = st.selectbox("Clarity Grade", clarities, index=clarities.index(init_clarity), help="IF (Flawless) to I1 (Included)")

        # Auto caliper calculation
        auto_calc = st.checkbox("Synchronize facet dimensions automatically", value=True,
                                help="Calculates standard round-brilliant mm dimensions from Carat and Cut automatically.")

        if auto_calc:
            est_diam = round(6.41 * (carat ** (1/3)), 2)
            est_depth_mm = round(est_diam * 0.615, 2)
            x_val, y_val, z_val = est_diam, est_diam, est_depth_mm
            depth_pct, table_pct = 61.5, 57.0
            st.markdown(f"<div style='font-size: 0.75rem; color: #94a3b8; margin-top: 4px;'>📐 Calipers auto-set: <strong>{est_diam} × {est_diam} × {est_depth_mm} mm</strong> • Depth: 61.5% • Table: 57.0%</div>", unsafe_allow_html=True)
        else:
            col_m1, col_m2, col_m3 = st.columns(3)
            with col_m1:
                x_val = st.number_input("Length X (mm)", 0.5, 12.0, float(init_x), 0.01)
            with col_m2:
                y_val = st.number_input("Width Y (mm)", 0.5, 12.0, float(init_y), 0.01)
            with col_m3:
                z_val = st.number_input("Depth Z (mm)", 0.5, 10.0, float(init_z), 0.01)
            col_m4, col_m5 = st.columns(2)
            with col_m4:
                depth_pct = st.number_input("Depth %", 43.0, 79.0, float(init_depth), 0.1)
            with col_m5:
                table_pct = st.number_input("Table %", 43.0, 95.0, float(init_table), 0.1)

    # Prediction and valuation
    with col_right:
        st.markdown('<div class="section-title"><span>📈</span> Fair Market Valuation</div>', unsafe_allow_html=True)

        feature_dict = {
            "carat": carat,
            "cut": cut,
            "color": color,
            "clarity": clarity,
            "depth": depth_pct,
            "table": table_pct,
            "x": x_val,
            "y": y_val,
            "z": z_val
        }
        feature_df = pd.DataFrame([feature_dict])

        if model is not None:
            raw_pred = model.predict(feature_df)[0]
            price_pred = max(150.0, float(raw_pred))
            
            # Confidence interval from 10-fold CV RMSE
            cv_rmse = 550.18
            lower_bound = max(100.0, price_pred - cv_rmse)
            upper_bound = price_pred + cv_rmse
            price_per_carat = price_pred / carat

            # Market tier classification
            if price_pred >= 10000:
                tier_html = '<span class="badge-tier badge-tier-luxury">👑 Investment Grade / High Luxury</span>'
            elif price_pred >= 3500:
                tier_html = '<span class="badge-tier badge-tier-fine">💎 Fine Jewelry Standard</span>'
            else:
                tier_html = '<span class="badge-tier badge-tier-commercial">🛍️ Commercial Retail Standard</span>'

            st.markdown(f"""<div class="valuation-card">
<div style="margin-bottom: 6px;">{tier_html}</div>
<div class="valuation-label">Estimated Fair Market Retail Value</div>
<div class="valuation-price">${price_pred:,.2f}</div>
<div class="valuation-range">
Confidence Range (10-Fold CV RMSE ±${cv_rmse:,.0f}): <strong style="color: #f8fafc;">${lower_bound:,.2f} to ${upper_bound:,.2f} USD</strong>
</div>
<div style="font-size: 0.78rem; color: #94a3b8; border-top: 1px solid rgba(148, 163, 184, 0.15); padding-top: 6px;">
Appraised Price Per Carat: <strong style="color: #38bdf8;">${price_per_carat:,.2f} / ct</strong>
</div>
</div>""", unsafe_allow_html=True)

            volume = x_val * y_val * z_val
            st.markdown(f"""<div class="kpi-row">
<div class="kpi-item">
<div class="kpi-item-title">Grading Spec</div>
<div class="kpi-item-value">{cut} • {color}</div>
</div>
<div class="kpi-item">
<div class="kpi-item-title">Clarity Tier</div>
<div class="kpi-item-value">{clarity}</div>
</div>
<div class="kpi-item">
<div class="kpi-item-title">Est. Volume</div>
<div class="kpi-item-value">{volume:.1f} mm³</div>
</div>
</div>""", unsafe_allow_html=True)

            # Certificate text
            cert_text = f"""GemVal Diamond Valuation Certificate
Issue Date: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Model: Histogram Gradient Boosting (10-Fold CV RMSE: $550.18)

Specifications:
  Carat: {carat:.2f} ct ({carat * 200:.1f} mg)
  Cut: {cut}
  Color: {color}
  Clarity: {clarity}

Measurements:
  Dimensions: {x_val:.2f} x {y_val:.2f} x {z_val:.2f} mm
  Depth: {depth_pct:.1f}% | Table: {table_pct:.1f}%
  Volume: {volume:.2f} mm³

Valuation:
  Estimated Value: ${price_pred:,.2f} USD
  Price Per Carat: ${price_per_carat:,.2f} USD/ct
  Confidence Range: ${lower_bound:,.2f} - ${upper_bound:,.2f} USD
"""
            st.markdown("<div style='margin-top: 10px;'>", unsafe_allow_html=True)
            st.download_button(
                label="📄 Export Valuation Certificate (.txt)",
                data=cert_text,
                file_name=f"GemVal_Appraisal_{carat}ct_{cut}_{color}.txt",
                mime="text/plain",
                use_container_width=True
            )
            st.markdown("</div>", unsafe_allow_html=True)

    # Sensitivity curve expander
    with st.expander("📈 View Carat Price Sensitivity Curve & Pipeline Vector", expanded=False):
        col_curve, col_vec = st.columns([1.5, 1])
        with col_curve:
            st.caption("How market value scales across carat weights for this cut, color, and clarity:")
            carat_pts = np.linspace(0.3, 2.5, 12)
            c_rows = []
            for c_pt in carat_pts:
                d_est = round(6.41 * (c_pt ** (1/3)), 2)
                c_rows.append({
                    "carat": c_pt, "cut": cut, "color": color, "clarity": clarity,
                    "depth": 61.5, "table": 57.0, "x": d_est, "y": d_est, "z": round(d_est * 0.615, 2)
                })
            curve_preds = model.predict(pd.DataFrame(c_rows))
            chart_df = pd.DataFrame({
                "Carat Weight": [round(c, 2) for c in carat_pts],
                "Market Price ($)": [round(max(0, p), 2) for p in curve_preds]
            }).set_index("Carat Weight")
            st.line_chart(chart_df, color="#38bdf8")

        with col_vec:
            st.caption("Raw Pipeline Input Vector:")
            st.dataframe(feature_df, use_container_width=True)

# Benchmark comparison
elif current_page == "benchmark":
    st.markdown('<a href="/" target="_self" class="nav-back-link">← Return to Valuation Terminal</a>', unsafe_allow_html=True)
    st.markdown('<div class="section-title"><span>📊</span> 10-Fold Cross-Validation Performance Comparison</div>', unsafe_allow_html=True)
    st.caption("Evaluation of 5 distinct algorithms on 53,920 records (strictly excluding Task 1 models):")

    benchmark_data = [
        {"Algorithm": "Extra Trees Regressor", "Architecture": "Randomized Tree Ensemble", "Mean RMSE ($)": 530.93, "Std Dev ($)": 20.76, "Error %": "13.50%", "Runtime": "176.6s", "Model Size": "326 MB"},
        {"Algorithm": "Hist Gradient Boosting", "Architecture": "Histogram-Binned Boosting", "Mean RMSE ($)": 550.18, "Std Dev ($)": 10.56, "Error %": "13.99%", "Runtime": "33.6s", "Model Size": "0.35 MB (Production)"},
        {"Algorithm": "Ridge Regression", "Architecture": "L2-Regularized Linear", "Mean RMSE ($)": 1137.13, "Std Dev ($)": 51.12, "Error %": "28.91%", "Runtime": "3.1s", "Model Size": "0.02 MB"},
        {"Algorithm": "AdaBoost Regressor", "Architecture": "Sequential Boosting", "Mean RMSE ($)": 1412.72, "Std Dev ($)": 31.17, "Error %": "35.92%", "Runtime": "87.3s", "Model Size": "0.85 MB"},
        {"Algorithm": "Linear SVR", "Architecture": "Support Vector Machine", "Mean RMSE ($)": 1466.87, "Std Dev ($)": 56.58, "Error %": "37.30%", "Runtime": "3.5s", "Model Size": "0.04 MB"}
    ]
    st.dataframe(pd.DataFrame(benchmark_data), use_container_width=True)

    st.markdown('<div class="section-title" style="margin-top: 32px; margin-bottom: 12px;"><span>📉</span> Visual Error Spread (Mean RMSE by Algorithm)</div>', unsafe_allow_html=True)

    chart_bar_df = pd.DataFrame({
        "Algorithm": [r["Algorithm"] for r in benchmark_data],
        "Mean RMSE ($)": [r["Mean RMSE ($)"] for r in benchmark_data]
    }).set_index("Algorithm")
    st.bar_chart(chart_bar_df, color="#818cf8")

    st.markdown("""
    <div style="margin-top: 15px; padding: 12px; background: rgba(30, 41, 59, 0.4); border-radius: 10px;">
        <span style="color: #38bdf8; font-weight: 700;">Key Engineering Decision:</span>
        <span style="color: #cbd5e1; font-size: 0.85rem;"> While Extra Trees reached $530 RMSE, its 326 MB file size causes slow cloud boot times. Hist Gradient Boosting provides within 3% accuracy at only 0.35 MB, making it the superior production choice.</span>
    </div>
    """, unsafe_allow_html=True)

# 4Cs Guide
elif current_page == "guide":
    st.markdown('<a href="/" target="_self" class="nav-back-link">← Return to Valuation Terminal</a>', unsafe_allow_html=True)
    st.markdown('<div class="section-title"><span>🎓</span> Diamond 4Cs Industry Pricing Dynamics</div>', unsafe_allow_html=True)
    g_col1, g_col2 = st.columns(2, gap="large")
    with g_col1:
        st.markdown("""
        **1. Carat Weight**
        * 1 Carat = 200 mg. Value scales exponentially as benchmark milestones (1.00 ct, 2.00 ct) are crossed due to natural scarcity.
        
        **2. Cut Quality**
        * Ideal > Premium > Very Good > Good > Fair.
        * Cut determines facet light return and optical brilliance.
        """)
    with g_col2:
        st.markdown("""
        **3. Color Grade**
        * D through F are completely colorless and command top premiums. G through I offer near-colorless value.
        
        **4. Clarity Grade**
        * Measures internal microscopic inclusions. VS1 and VS2 represent the commercial "eye-clean" sweet spot.
        """)

# Footer
st.markdown("""
<div style="text-align: center; color: #475569; font-size: 0.7rem; padding: 8px 0 2px 0; border-top: 1px solid rgba(148, 163, 184, 0.08);">
    GemVal Enterprise AI • High-Density Market Valuation System
</div>
""", unsafe_allow_html=True)
